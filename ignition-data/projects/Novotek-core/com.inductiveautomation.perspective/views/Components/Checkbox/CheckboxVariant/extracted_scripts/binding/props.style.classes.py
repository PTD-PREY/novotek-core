# {
#     "struct": {
#         "selected": "{view.params.selected}",
#         "size": "{view.params.size}",
#         "style": "{view.params.style}"
#     },
#     "waitOnAll": true
# }

	if value['selected'] :
		return "buttons/" + value['style'] + "_flat buttons/size/btn_txt_" + value['size']
	else:
		return "buttons/grey_flat buttons/size/btn_txt_" + value['size']