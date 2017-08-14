import sqlite3
import threading
import logging
import socket


class DatabaseManager(sqlite3.Connection):
    def __init__(self, db, local_tlock):
        self.conn = sqlite3.connect(database=db, check_same_thread=False)
        self.cur = self.conn.cursor()

        try:
            self.cur.execute(''' drop table users_registered ''')
            self.cur.execute(''' drop table users_online ''')
            self.cur.execute(''' drop table groups ''')
        except sqlite3.OperationalError:
            pass

        self.cur.execute(''' create table users_registered (user_name text, first_name text, last_name text,
         email_address text, gender text )''')
        self.cur.execute(''' create table users_online (user_name text) ''')
        self.cur.execute(''' create table groups (group_name text)''')
        self.conn.commit()

        self.t_lock = local_tlock

    def select_data(self, table_name, col):
        self.t_lock.acquire()
        try:
            self.cur.execute(''' select "%s" from "%s" ''' % (col, table_name))
            return self.cur.fetchall()
        finally:
            self.t_lock.release()

    def insert_data(self, table_name, *args):
        self.t_lock.acquire()
        try:
            if table_name in ["users_online", "groups"]:
                self.cur.execute(''' insert into "%s" values (?) ''' % table_name, args)

            if table_name == "users_registered":
                self.cur.execute(''' insert into "%s" values (?, ?, ?, ?, ?) ''' % table_name, args)

            self.conn.commit()
        finally:
            self.t_lock.release()

    def delete_data(self, table_name, arg):
        self.t_lock.acquire()
        try:
            self.cur.execute(''' delete from "%s" where user_name = (?) ''' % table_name, (arg,))
            self.conn.commit()
        finally:
            self.t_lock.release()

    def create_table(self, table_name, group_admin):
        self.t_lock.acquire()
        try:
            self.cur.execute(''' create table "%s" (user_name text) ''' % table_name)
            self.conn.commit()

            self.insert_data(table_name, group_admin)
        finally:
            self.t_lock.release()


class HandleConnection(threading.Thread):
    def __init__(self, local_conn, local_addr, local_db_manager, local_user_name_with_connections):
        threading.Thread.__init__(self)
        self.local_conn = local_conn
        self.local_addr = local_addr
        self.local_db_manager = local_db_manager
        self.local_unwc = local_user_name_with_connections

        # RECEIVE WHETHER USER WANTS TO LOGIN OR SIGNUP
        self.user_status = self.local_conn.recv(1024)

        if self.user_status == "Log In":
            logging.info("Client with IP address " + str(self.local_addr[0] + " wishes to LogIn at"))

            again = False
            while not again:
                count = 0
                # ASKS CONNECTED CLIENT FOR HIS/HER REGISTERED USER NAME
                self.user_name = self.local_conn.recv(1024)

                user_names_registered = self.local_db_manager.select_data("users_registered", "user_name")
                for u in user_names_registered:
                    if u[0].encode() == self.user_name:
                        count += 1

                if count == 0:
                    self.local_conn.send(str(self.user_name) + " doesn't exists. Retry.")
                    continue
                if count > 0:
                    self.local_conn.send("You have logged in successfully.")
                    self.local_db_manager.insert_data("users_online", self.user_name)
                    self.local_unwc[self.user_name] = self.local_conn
                    break

        if self.user_status == "Sign Up":
            logging.info("Client with IP address " + str(self.local_addr[0]) + " wishes to SignUp at")

            user_data = dict()
            user_data["first_name"] = self.local_conn.recv(1024)
            user_data["last_name"] = self.local_conn.recv(1024)
            user_data["email_address"] = self.local_conn.recv(1024)
            user_data["gender"] = self.local_conn.recv(1024)

            again = False
            while not again:
                count = 0
                self.user_name = self.local_conn.recv(1024)
                ''' ASKS FOR USER NAME AND VERIFY THAT THIS USER NAME DOES NOT EXISTS 
                                                                        OTHERWISE FORCE USER TO RE-ENTER USER NAME '''

                user_names_exists = self.local_db_manager.select_data("users_registered", "user_name")
                for u in user_names_exists:
                    if u[0].encode() == self.user_name:
                        count += 1

                if count > 0:
                    self.local_conn.send("User Name already exists. Please try with another.")
                    continue
                if count == 0:
                    self.local_conn.send("Congratulations. You are registered with User Name " + str(self.user_name) +
                                         ". Just use " + str(self.user_name) + "next time to login.")
                    self.local_db_manager.insert_data("users_online", self.user_name)
                    break

            user_data["user_name"] = self.user_name

            self.local_db_manager.insert_data("users_registered", user_data["user_name"], user_data["first_name"],
                                              user_data["last_name"], user_data["email_address"], user_data["gender"])
            self.local_db_manager.insert_data("users_online", self.user_name)
            self.local_unwc[self.user_name] = self.local_conn

        self.start()

    def run(self):
        while True:
            message = self.local_conn.recv(1024)

            if message == "quit":
                self.local_db_manager.delete_data("users_online", self.user_name)
                self.local_unwc[self.user_name].send("quit")
                del self.local_unwc[self.user_name]
                break

            elif message == "show users":
                online_users = self.local_db_manager.select_data("users_online", "user_name")
                for u in online_users:
                    self.local_conn.send(u[0].encode())
                self.local_conn.send("exit")

            elif message[:12] == "create group":
                group_name = message[len(message) - 13:]
                self.local_db_manager.insert_data("groups", group_name)
                self.local_db_manager.create_table(group_name, self.user_name)

                user_names_registered = self.local_db_manager.select_data("users_registered", "user_name")
                user_names_registered_string = []
                for u in user_names_registered:
                    user_names_registered_string.append(u[0].encode())

                group_member = self.local_conn.recv(1024)
                self.local_db_manager.insert_data(group_name, group_member)
                while group_member != "done":
                    group_member = self.local_conn.recv(1024)
                    if group_member in user_names_registered_string:
                        self.local_db_manager.insert_data(group_name, group_member)

            elif message == "show groups":
                all_groups = self.local_db_manager.select_data("groups", "group_name")
                for u in all_groups:
                    self.local_conn.send(u[0].encode())
                self.local_conn.send("exit")

            else:
                online_users = self.local_db_manager.select_data("users_online", "user_name")
                all_groups = self.local_db_manager.select_data("groups", "group_name")

                user_name_or_group_name, msg_to_user = message.split(":", 1)
                if user_name_or_group_name in online_users:
                    try:
                        self.local_unwc[user_name_or_group_name].send(msg_to_user)
                    except:
                        pass
                    self.local_unwc.send("done")

                elif user_name_or_group_name in all_groups:
                    for u in all_groups:
                        try:
                            self.local_unwc[u].send(message)
                        except:
                            pass
                    self.local_conn.send("done")

                else:
                    self.local_conn.send("There exists no such user. Try again.")


def main():
    logging.basicConfig(filename="server_logfile.log", filemode="w", level=logging.INFO,
                        format="%(message)s %(asctime)s")

    thread_lock = threading.Lock()
    db_manager = DatabaseManager("chat.db", thread_lock)
    logging.info("Database created with table names : 'users_registered', 'users_online', 'groups' at")

    host = "127.0.0.1"
    port = 5000
    server = (host, port)
    socket_object = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_object.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socket_object.bind(server)
    socket_object.listen(5)

    logging.info("SERVER started on Port No. " + str(port) + " at")

    user_name_with_connections = dict()

    while True:
        conn, addr = socket_object.accept()
        logging.info("User with IP address " + addr[0] + " connected to our SERVER at")
        new_client_thread = HandleConnection(conn, addr, db_manager, user_name_with_connections)


if __name__ == "__main__":
    main()
