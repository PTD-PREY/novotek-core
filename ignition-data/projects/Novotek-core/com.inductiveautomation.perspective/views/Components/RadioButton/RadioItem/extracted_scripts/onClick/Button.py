	payload = {
		"radio_group_name": self.view.params.radioGroupName,
	 	"label": self.view.params.label
	}

	system.perspective.sendMessage("SelectRadioGroupInstance", payload=payload)