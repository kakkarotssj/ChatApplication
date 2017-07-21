import threading
import socket
import time

HOST = "127.0.0.1"
PORT = 5000
SERVER = (HOST, PORT)

clients_addresses = []
clients_connections = []

close_thread1 = False
close_thread2 = False


def accept_clients(s, thread_lock):
    while not close_thread1:
        thread_lock.acquire()
        try:
            client_connection, client_address = s.accept()
            clients_addresses.append(client_address)
            clients_connections.append(client_connection)
            print "New client with IP address " + str(client_address[0]) + " added at " + str(time.ctime(time.time()))
        except:
            pass
        finally:
            thread_lock.release()


def handle_messages():
    index = 0
    while not close_thread2:
        while index < len(clients_connections):
            try:
                message = clients_connections[index].recv(1024)
                if message != "" and message != "Quit":
                    print message
                    for connection in clients_connections:
                        connection.sendall(message)
            except:
                pass
            index += 1
            if index == len(clients_connections):
                index = 0


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(SERVER)
    s.listen(5)

    print "\t\t\t\t\t\t *****CHAT SERVER STARTED******"

    thread_lock = threading.Lock()
    thread1 = threading.Thread(target=accept_clients, args=(s, thread_lock))
    thread1.start()

    thread2 = threading.Thread(target=handle_messages, args=())
    thread2.start()

    thread1.join()
    thread2.join()
    s.close()


if __name__ == "__main__":
    main()
