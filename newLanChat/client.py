import socket

from standards import SERVER_ADDRESS
from receiver import Receiver
from input_manager import InputManager
from protocols import Client2Server
from sender import Sender


class Client:
	def __init__(self):
		self.socket_object = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket_object.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)

		self._connect()

		self.input_service = InputManager()
		self.sender_service = Sender()
		self.protocol = Client2Server()
		self.receiver_service = Receiver()

		self.username = None
		self.is_authenticated = False
		self._authenticate()

	def _connect(self):
		self.socket_object.connect(SERVER_ADDRESS)

	def _authenticate(self):
		is_login = input_service.take_input()
		if is_login:
			login_credentials = {}

			self.username = input_service.take_input()
			login_credentials["username"] = self.username

			password = input_service.take_input()
			login_credentials["password"] = password

			self.protocol.setup_login(login_credentials)
		else:
			signup_values = {}

			self.username = input_service.take_input()
			signup_values["username"] = self.username

			first_name = input_service.take_input()
			signup_values["first_name"] = first_name

			last_name = input_service.take_input()
			signup_values["last_name"] = last_name

			email = input_service.take_input()
			signup_values["email"] = email

			password = input_service.take_input()
			signup_values["password"] = password

			self.protocol.setup_signup(signup_values)

		while not self.is_authenticated: 
			self.sender_service.send(protocol)
			error = self.receiver_service.get_msg()

			if not error["is_error"]:
				self.is_authenticated = True
			else:
				print error["error"]

	def start(self):
		operation = self.input_service.take_input()
		if operation[:5] == "query":
			status = self.protocol.setup_dbquery(operation[6:])
			print status
		else:
			message["sender"] = self.username
			message["content"], message["receiver"] = operation.split(':', 1)

			status = self.protocol.setup_message(message)
			print status

client = Client()
client.start()