class Authenticator:
	def __init__(self, user, pswd):
		self.user = user
		self.pswd = pswd

	def initialAuthData(self):
		cm = {'user': self.user, 'token': self.pswd}
		return cm

class ClientFactory:
	def __init__(self, user, pswd):
		self.user = user
		self.pswd = pswd

	def newAuthenticator(self):
		return Authenticator(self.user, self.pswd)
