class Client2Server(dict):
	def __init__(self):
		self.renew_protocol()

	def renew_protocol(self):
		self["is_login"] = False
		self["login_credentials"] = {
			"username" = None,
			"password" = None
		}

		self["is_signup"] = False
		self["signup_values"] = {
			"username" = None,
			"first_name" = None,
			"last_name" = None,
			"email" = None,
			"password" = None
		}

		self["is_message"] = False
		self["message"] = {
			"sender" = None,
			"content" = None,
			"receiver" = None
		}

		self["is_dbquery"] = False
		self["dbquery"] = {
			"query" = False,
		}

	def setup_login(self, login_credentials):
		self["is_login"] = True
		self["login_credentials"]["username"] = login_credentials["username"]
		self["login_credentials"]["password"] = login_credentials["password"]

	def setup_signup(self, signup_values):
		self["is_signup"] = True
		self["signup_values"]["username"] = signup_values["username"]
		self["signup_values"]["first_name"] = signup_values["first_name"]
		self["signup_values"]["last_name"] = signup_values["last_name"]
		self["signup_values"]["email"] = signup_values["email"]
		self["signup_values"]["password"] = signup_values["password"]

	def setup_message(self, message):
		self["is_message"] = True
		self["message"]["sender"] = message["sender"]
		self["message"]["content"] = message["content"]
		self["message"]["receiver"] = message["receiver"]

	def setup_dbquery(self, query):
		if query in ["show_online_users"]:
			self["is_dbquery"] = True
			self["dbquery"]["query"] = query
			return "success"
		else:
			return "No matching query"


class Server2Client(dict):
	def __init__(self):
		self["receiver_username"] = None

		self["is_error"] = False
		self["error"] = None

		self["is_message"] = False,
		self["message"] = None

		self["is_dbquery"] = False
		self["dbquery_result"] = {
			"online_users" = None
		}

	def setup_receiver_username(self, receiver_username):
		self["receiver_username"] = "receiver_username"

	def setup_error(self, error):
		self["is_error"] = True
		self["error"] = error

	def setup_message(self, message):
		self["is_message"] = True
		self["message"] = message

	def setup_dbquery_results(self, online_users):
		self["is_dbquery"] = True
		self["dbquery_results"]["online_users"] = online_users
