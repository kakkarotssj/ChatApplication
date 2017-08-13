import threading
import socket
import time

HOST = "127.0.0.1"
PORT = 5000
connections = []
chat_threads = []


class ClientObject(threading.Thread):
    def __init__(self, conn, client_index, param_user_name):
        threading.Thread.__init__(self)
        self.connection = conn
        self.client_index = client_index
        self.user_name = param_user_name

    def run(self):
        while True:
            if self.client_index == 1:
                try:
                    message = chat_threads[1].connection.recv(1024)
                    if message == "quit":
                        chat_threads[1].connection.send(message)
                        chat_threads[0].connection.send("Other user has closed the connection.")
                    else:
                        if message != "":
                            chat_threads[0].connection.send(chat_threads[1].user_name + " -> " + message)
                except:
                    pass

            if self.client_index == 2:
                try:
                    message = chat_threads[0].connection.recv(1024)
                    if message == "quit":
                        chat_threads[0].connection.send(message)
                        chat_threads[1].connection.send("Other user has closed the connection.")
                    else:
                        if message != "":
                            chat_threads[1].connection.send(chat_threads[0].user_name + " -> " + message)
                except:
                    pass


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    print "\t\t\t\t\t\t *****CHAT SERVER STARTED******"
    s.listen(2)

    number_of_clients = 0
    while number_of_clients < 2:
        connection, address = s.accept()

        print str(address[0]) + " connected to our server at " + str(time.ctime(time.time()))
        connection.send("Hello User, Please Enter your nickname")
        user_name = connection.recv(1024)

        number_of_clients += 1
        connections.append(connection)
        chat_thread = ClientObject(connection, number_of_clients, user_name)
        chat_threads.append(chat_thread)

    for i in chat_threads:
        i.start()

if __name__ == "__main__":
    main()
