# {
#     "path": "view.params.label"
# }

	try:
		return globalVars.BRIDLES[value]["label"] # If this is a bridle, go get it's translation from globalVars
	except:
		return value