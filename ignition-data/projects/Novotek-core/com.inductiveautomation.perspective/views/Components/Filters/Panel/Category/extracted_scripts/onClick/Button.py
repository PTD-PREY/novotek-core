	payloadSend = {
		'selected': self.view.params.selected,
		'label': self.view.params.label,
		'value': self.view.params.label
	}
	
	system.perspective.sendMessage("FilterCategoryClicked", payload=payloadSend)