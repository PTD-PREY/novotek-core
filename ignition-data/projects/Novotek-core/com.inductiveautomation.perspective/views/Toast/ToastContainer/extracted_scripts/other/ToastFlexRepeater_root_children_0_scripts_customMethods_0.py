	# implement your method here
	size = len(self.props.instances)
	if uuid:
		instances = []
		for x in range(size):
			instance = 	{
							'uuid': self.props.instances[x]['uuid'], 
							'messageType':self.props.instances[x]['messageType'],
							'message':self.props.instances[x]['message'],
							'new': 0
						}

			if self.props.instances[x]['uuid'] == uuid:
				#hide
				instance['messageType']=''
				
			instances.append(instance)
		self.view.custom.toasts = instances
