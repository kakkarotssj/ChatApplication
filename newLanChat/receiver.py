from standards import BUFFER_SIZE
from socket import socket


class Receiver(threading.Thread):
	def __init__(self, socket_object):
		threading.Thread.__init__(self)
		self.socket_object = socket_object
		self.msg = None

	def run(self):
		while True:
			try:
				self.msg = self.socket_object.recv(BUFFER_SIZE)
				print self.msg
			except socket.error:
				pass

	def get_msg(self):
		return self.msg
