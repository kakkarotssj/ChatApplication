import time
import socket
import threading


HOST = "127.0.0.1"
PORT = 5000
connections = []


class ThreadObject(threading.Thread):
    def __init__(self, connection, user_name):
        threading.Thread.__init__(self)
        self.connection = connection
        self.user_name = user_name

    def run(self):
        while True:
            try:
                message = self.connection.recv(1024)
                for conn in connections:
                    conn.send(str(self.user_name) + " -> " + message)
            except:
                pass


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    print "\t\t\t\t\t\t ******CHAT SERVER STARTED******"
    s.listen(10)

    while True:
        new_connection, new_address = s.accept()

        print str(new_address[0]) + " connected to our server at " + str(time.ctime(time.time()))
        new_connection.send("Hello User, Please Enter your nickname")
        user_name = new_connection.recv(1024)
        new_connection.send("You are all set.")

        connections.append(new_connection)
        new_thread_object = ThreadObject(new_connection, user_name)
        new_thread_object.start()


if __name__ == "__main__":
    main()
