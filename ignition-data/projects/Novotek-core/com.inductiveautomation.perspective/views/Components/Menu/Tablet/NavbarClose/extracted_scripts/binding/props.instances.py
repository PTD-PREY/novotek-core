# {
#     "expression": "runScript(\"navigation.navbar()\")"
# }

	open = value
	
	for group in value:
		for item in group['instances']:
			item['iconOnly'] = True
	return open