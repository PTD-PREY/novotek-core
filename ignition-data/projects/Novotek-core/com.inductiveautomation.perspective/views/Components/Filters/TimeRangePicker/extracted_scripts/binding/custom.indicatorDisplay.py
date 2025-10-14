# {
#     "struct": {
#         "from": "{view.params.from}",
#         "to": "{view.params.to}"
#     },
#     "waitOnAll": true
# }

	if not value['from'] and not value['to']:
		return False
	else:
		return True