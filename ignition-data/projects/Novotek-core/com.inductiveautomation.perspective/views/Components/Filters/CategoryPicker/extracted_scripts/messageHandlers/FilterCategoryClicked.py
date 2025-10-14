	# implement your handler here
	if payload['label'] == "selectAll":
		for unselected in self.view.params.unselected:
			self.view.params.selected.append(unselected)
			self.view.params.unselected.remove(unselected)
	elif payload['label'] == "unselectAll":
		for selected in self.view.params.selected:
			self.view.params.unselected.append(selected)
			self.view.params.selected.remove(selected)
	else:
		if payload['selected']:
			self.view.params.unselected.append(payload['value'])
			self.view.params.selected.remove(payload['value'])
		else:
			self.view.params.selected.append(payload['value'])
			self.view.params.unselected.remove(payload['value'])
	system.perspective.print(self.view.params.selected)