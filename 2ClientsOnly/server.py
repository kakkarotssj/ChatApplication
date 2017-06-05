import socket
import threading
import time

#GLOABAL CONSTANTS

HOST = "127.0.0.1"
PORT = 5000

#GLOBAL VARIABLES

close_thread1 = False
close_thread2 = False
close_thread3 = False
close_thread4 = False

conn1 = None
addr1 = None
conn2 = None
addr2 = None

nickname1 = None
nickname2 = None


def accept_connection1(s, thread_lock):
    global conn1
    global addr1
    global nickname1
    global close_thread1
    while not close_thread1:
        thread_lock.acquire()
        try:
            conn1, addr1 = s.accept()
            if addr1 is not None:
                connection_time = time.ctime(time.time())
                conn1.sendall("Enter your nickname ::: ")
                nickname1 = conn1.recv(1024)
                conn1.sendall("\t\t\t\t\t\t" + nickname1 + ", Welcome to CHAT ROOM")
                print str(nickname1) + " with IP address " + str(addr1[0]) + " added at " + \
                str(connection_time) + " on port number " + str(addr1[1])
                close_thread1 = True
        except:
            pass
        finally:
            thread_lock.release()


def accept_connection2(s, thread_lock):
    global conn2
    global addr2
    global nickname2
    global close_thread2
    while not close_thread2:
        thread_lock.acquire()
        try:
            conn2, addr2 = s.accept()
            if addr2 is not None:
                connection_time = time.ctime(time.time())
                conn2.sendall("Enter your nickname ::: ")
                nickname2 = conn2.recv(1024)
                conn2.sendall("\t\t\t\t\t\t" + nickname2 + ", Welcome to CHAT ROOM")
                print str(nickname2) + " with IP address " + str(addr2[0]) + " added at " + \
                str(connection_time) + " on port number " + str(addr2[1])
                close_thread2 = True
        except:
            pass
        finally:
            thread_lock.release()


def handle_messages1to2():
    global close_thread3
    while not close_thread3:
        try:
            message1 = conn1.recv(1024)
            if message1 != "":
                print str(nickname1) + " -> " + str(message1)
                conn2.sendall(str(nickname1) + " -> " + str(message1))
            if message1 == "Quit":
                conn1.sendall("Quit")
                close_thread3 = True
        except:
            pass


def handle_messages2to1():
    global close_thread4
    while not close_thread4:
        try:
            message2 = conn2.recv(1024)
            if message2 != "":
                print str(nickname2) + " -> " + str(message2)
                conn1.sendall(str(nickname2) + " -> " + str(message2))
            if message2 == "Quit":
                conn1.sendall("Quit")
                close_thread4 = True
        except:
            pass


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.listen(2)

    global close_thread1
    global close_thread2

    thread_lock = threading.Lock()
    thread1 = threading.Thread(target=accept_connection1, args=(s, thread_lock))
    thread1.start()
    thread2 = threading.Thread(target=accept_connection2, args=(s, thread_lock))
    thread2.start()

    print "\t\t\t\t\t\t ***** CHAT SERVER STARTED *****"

    thread1.join()
    thread2.join()

    thread3 = threading.Thread(target=handle_messages1to2)
    thread3.start()
    thread4 = threading.Thread(target=handle_messages2to1)
    thread4.start()

    thread3.join()
    thread4.join()

    s.close()


if __name__ == "__main__":
    main()

