import threading
import socket

SERVER = ("127.0.0.1", 5000)


class ReceiveMessages(threading.Thread):
    def __init__(self, s):
        threading.Thread.__init__(self)
        self.socket_connection = s

    def run(self):
        while True:
            try:
                message = self.socket_connection.recv(1024)
                print message
            except:
                pass


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect(SERVER)

    greeting_message = s.recv(1024)
    print greeting_message
    user_name = raw_input()
    s.send(user_name)

    receive_messages = ReceiveMessages(s)
    receive_messages.start()

    message = ""
    while message != "Quit":
        message = raw_input()
        s.send(message)


if __name__ == "__main__":
    main()
