# {
#     "path": "view.params.unselected"
# }

	unselectedBind = []
	
	for unselected in value:
		elem = {
		  "label": unselected,
		  "selected": False
		}
		
		unselectedBind.append(elem)
		
	return sorted(unselectedBind)