# {
#     "struct": {
#         "selected": "{view.params.selected}",
#         "textColor": "{view.params.textColor}"
#     },
#     "waitOnAll": true
# }

	temp_class = "colors/border/{color} borders/borderBottom" if value["selected"] else "colors/border/grey200 borders/borderBottom"
	color = value["textColor"] if value["textColor"] else "primary500"
	return temp_class.format(color = color.replace("-",""))