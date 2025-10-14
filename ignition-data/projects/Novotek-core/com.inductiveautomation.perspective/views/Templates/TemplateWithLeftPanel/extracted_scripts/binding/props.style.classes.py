# {
#     "struct": {
#         "path": "{page.props.path}",
#         "width": "{page.props.dimensions.viewport.width}"
#     },
#     "waitOnAll": true
# }

	if value['width'] < 1000:
		return "container/page_tablet"
	else:
		return "container/page_desktop"