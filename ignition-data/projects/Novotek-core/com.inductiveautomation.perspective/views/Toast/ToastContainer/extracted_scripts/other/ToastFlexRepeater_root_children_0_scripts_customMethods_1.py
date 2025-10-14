	# implement your method here
	size = len(self.props.instances)
	if uuid:
		instances = []
		otherNotHide = False
		for x in range(size):
			if self.props.instances[x]['uuid'] != uuid:
				if self.props.instances[x]['messageType'] != "":
					instances.append(self.props.instances[x])
				if self.props.instances[x]['messageType'] in ["info", "success", "warning"]:
					otherNotHide = True
		
		if otherNotHide == False:
			self.view.custom.toasts = instances