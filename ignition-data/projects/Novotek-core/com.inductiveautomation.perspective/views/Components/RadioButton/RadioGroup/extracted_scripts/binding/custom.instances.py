# {
#     "struct": {
#         "items": "{view.params.instances}",
#         "radioGroupName": "{view.params.radioGroupName}",
#         "selected": "{view.params.selected}"
#     },
#     "waitOnAll": true
# }

	bindValue = []
	index = 0
	
	for instance in value["items"]:
		item = {
			"label": instance["label"],
			"icon": instance["icon"],
			"position": "middle",
			"selected": False,
			"radioGroupName": value["radioGroupName"]
		}
		
		if instance["label"] == value["selected"]:
			item["selected"] = True
		
		if index == 0:
			item["position"] = "first"
		elif index == (len(value["items"])-1):
			item["position"] = "last"
	
		bindValue.append(item)
		index = index + 1
	
	return bindValue