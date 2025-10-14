
	import uuid
	from threading import Timer
	
	if payload['messageType'] and payload['message']:
		payload['uuid'] = str(uuid.uuid1())
		payload['new'] = 1
		
		self.view.custom.toasts.append(payload)
		self.refreshBinding("props.instances")
		if payload['messageType'] != "error":
			Timer(3.0, hideMessageTimer, [payload['uuid']], {'self': self}).start()
			
def hideMessageTimer(uuid, self):
	from threading import Timer
	self.hideMessage(uuid)
	Timer(1.0, removeMessageTimer, [uuid], {'self': self}).start()
	
def removeMessageTimer(uuid, self):
	self.removeMessage(uuid)