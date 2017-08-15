import threading
import random
import logging
import socket
import sys


class ReceiveMessages(threading.Thread):
    def __init__(self, local_socket_object):
        threading.Thread.__init__(self)
        self.local_socket_object = local_socket_object

        self.start()

    def run(self):
        while True:
            try:
                msg = self.local_socket_object.recv(1024)
                if msg != "quit":
                    print msg
                else:
                    break
            except:
                pass


def get_group_name():
    groups = {1: "gangsta", 2: "GOTFans", 3: "gokuFans", 4: "vegetaFans", 5: "saitamaFans"}

    return groups[random.randint(1, 5)]


def main():
    logging.basicConfig(filename="client_logfile.log", filemode="w", level=logging.INFO,
                        format="%(message)s %(asctime)s")

    server = ("127.0.0.1", 5000)
    socket_object = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_object.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        socket_object.connect(server)
    except StandardError:
        logging.critical("Client side failed to connect. Try again.")
        sys.exit()

    logging.info("This is just a test. at")
    print "\t\t\t\t\t *****Instructions*****"
    print "Choose 1 to LogIn or 2 to SignUp"
    print "LogIn Instructions... Enter registered User Name to LogIn"
    print "SignUp Instructions... You'll need First and Last name, email-address, gender and a unique User Name"

    # COLLECT WHETHER CLIENT WISHES TO LOGIN OR SIGNUP
    again = False
    while not again:
        user_status = input("Enter 1 to LogIn or 2 to SignUp")

        if user_status == 1:
            logging.info("User wishes to Log In at")
            socket_object.send("Log In")
            break

        elif user_status == 2:
            logging.info("User wishes to Sign Up at")
            socket_object.send("Sign Up")
            break

        else:
            print "Please Enter a valid input to proceed"
            logging.info("Client didn't make a valid input")

    # IF USER WISHES TO LOGIN
    if user_status == 1:
        logging.info("Client connected is now trying to Login at")
        user_name = raw_input("Enter your registered user name")
        socket_object.send(user_name)

        # NOW WAIT FOR LOGIN STATUS
        login_status = socket_object.recv(1024)

        while not again:
            if login_status[-14:-1] == "successfully":
                print login_status + " You may proceed."
                break
            else:
                print "Entered user name doesn't exists. Please retry with another one."
                user_name = raw_input("Enter correct registered user name")
                socket_object.send(user_name)
                login_status = socket_object.recv(1024)

    # IF USER WISHES TO SIGN UP
    if user_status == 2:
        logging.info("Client connected is now trying to Sign Up at")
        print "Fill up the requirements."

        first_name = raw_input("Enter your First Name : ")
        while not again:
            if first_name != "":
                socket_object.send(first_name)
                break
            else:
                first_name = raw_input("Please enter valid non-empty string.")

        last_name = raw_input("Enter your Last Name : ")
        while not again:
            if last_name != "":
                socket_object.send(last_name)
                break
            else:
                last_name = raw_input("Please enter valid non-empty string.")

        email_address = raw_input("Enter your Email Address : ")
        while not again:
            if email_address != "":
                socket_object.send(email_address)
                break
            else:
                email_address = raw_input("Please enter valid non-empty string.")

        gender = raw_input("Gender Please. M or F")
        while not again:
            if gender != ""and (gender in ["M", "m", "F", "f"]):
                socket_object.send(gender)
                break
            else:
                gender = raw_input("Please enter valid character.")

        print "Great. You are just one step away."
        user_name = raw_input("Choose your User Name wisely. It has to be unique. User Name : ")
        socket_object.send(user_name)
        while not again:
            check_status = socket_object.recv(1024)
            # CHECKING IF USER NAME IS AVAILABLE

            if check_status[-6:-1] == "login":
                print check_status
                break
            else:
                user_name = raw_input("This User Name already exists. Try with another. User Name : ")
                socket_object.send(user_name)

        print "Now that you have successfully logged in. You can chat with other users and do lot of awesome things."

        receive_messages = ReceiveMessages(socket_object)

        print "An action is 'quit' or 'show users' or 'create group *', 'show groups'," \
              " 'group_name/user_name:your_message'"
        print "Enter 'show users' to get a list of all online users."
        print "Create Group Instructions : "
        print "Enter 'create group' to create a new group followed by its group name. eg : create group '%s'" \
              % get_group_name()
        print "Enter user names one by one to add them into this group. Enter 'done' to finalize group_members."
        print "Advice: Enter 'show users' before creating group to see who can be added to this group."
        print "You can enter 'show groups' to see already created groups."
        print "To chat with a user or in a group..."
        print "You can type user_name followed by a colon and then action to that user. eg. 'kakkarotssj:hello'. "
        print "Warning. If mentioned user name doesn't exists then, you need to enter action again."
        print "Finally, enter 'quit' to leave chat room."
        print "\n You are ready to go now. Enjoy (y)"

        action = raw_input("Enter action : ")
        while not again:
            if action == "quit":
                socket_object.send(action)
                break

            else:
                if action == "show users":
                    socket_object.send(action)
                    users_online = []
                    while not again:
                        user_online = socket_object.recv(1024)
                        if user_online == "exit":
                            break
                        else:
                            users_online.append(user_online)
                    for i in users_online:
                        print i + ", ",

                elif action[:12] == "create group":
                    while not again:
                        if action[:12] == "create gorup" and action[13:] != "":
                            socket_object.send(action)
                            print "You need at least one more member other than you to create group."

                            member = raw_input("Enter user name of new member : ")
                            if member != "":
                                socket_object.send(member)

                            while member != "done":
                                member = raw_input("Enter user name of new member : ")
                                if member != "":
                                    socket_object.send(member)
                                else:
                                    print "Please enter a valid non-empty string."
                            break
                        else:
                            print "Enter a valid non-empty string for group name."
                            action = raw_input("Enter action to create group again.")

                elif action == "show groups":
                    socket_object.send(action)
                    all_groups = []
                    while not again:
                        group_name = socket_object.recv(1024)
                        if group_name == "exit":
                            break
                        else:
                            all_groups.append(group_name)
                    for i in all_groups:
                        print i + ", ",

                else:
                    user_name, msg = action.split(":", 1)
                    if len(user_name) != 0 and len(msg) != 0:
                        socket_object.send(action)

                    sent_status = socket_object.recv(1024)
                    if sent_status == "done":
                        pass
                    else:
                        print sent_status

                action = raw_input("Enter action : ")


if __name__ == "__main__":
    main()
