# {
#     "struct": {
#         "isFrom": "{view.params.isFrom}",
#         "isTo": "{view.params.isTo}"
#     },
#     "waitOnAll": true
# }

	is_from = value["isFrom"]
	is_to = value["isTo"]

	if not is_from and not is_to:
		return "On :"
	if is_to:
		return "To :"
	if is_from:
		return "From :"
