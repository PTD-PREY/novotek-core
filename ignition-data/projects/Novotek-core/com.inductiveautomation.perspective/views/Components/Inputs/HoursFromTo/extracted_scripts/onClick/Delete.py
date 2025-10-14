	selected_id = self.view.params.id

	system.perspective.sendMessage("DeleteTimeEntry", payload={"selected_id": selected_id})