import socket
import threading

SERVER = ("127.0.0.1", 5000)

close_thread = False


def receive_messages(s, thread_lock):
    global close_thread
    while not close_thread:
        try:
            message = s.recv(1024)
            thread_lock.acquire()
            if message != "Quit":
                print message
            else:
                close_thread = True
            thread_lock.release()
        except:
            pass


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(SERVER)

    thread_lock = threading.Lock()
    thread1 = threading.Thread(target=receive_messages, args=(s, thread_lock))
    thread1.start()

    stop_sending_message = False
    while not stop_sending_message:
        message = raw_input()
        s.sendall(message)
        if message == "Quit":
            stop_sending_message = True

    thread1.join()
    s.close()


if __name__ == "__main__":
    main()
