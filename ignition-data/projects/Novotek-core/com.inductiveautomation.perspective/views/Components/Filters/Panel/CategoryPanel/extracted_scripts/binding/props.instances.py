# {
#     "path": "view.params.selected"
# }

	selectedBind = []
	
	for selected in value:
		elem = {
		  "label": selected,
		  "selected": True
		}
		
		selectedBind.append(elem)
		
	return sorted(selectedBind)