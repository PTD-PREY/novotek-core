	# implement your handler here
	from threading import Timer
	
	self.hideMessage(payload['uuid'])
	Timer(1.0, removeMessageTimer, [payload['uuid']], {'self': self}).start()
	
def removeMessageTimer(uuid, self):
	self.removeMessage(uuid)