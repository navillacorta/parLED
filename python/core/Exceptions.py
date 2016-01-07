class BadDevice(Exception):
	def __init__(self, *args):
		message = "Invalid Interface Object"
		super(BadDevice, self).__init__(message, *args) 
