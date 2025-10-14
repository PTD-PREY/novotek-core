# {
#     "struct": {
#         "path": "{page.props.path}",
#         "width": "{page.props.dimensions.viewport.width}"
#     },
#     "waitOnAll": true
# }

	if value['width'] < 1000:
		system.perspective.closeDock('close_menu_desktop')
		system.perspective.openDock('close_menu_tablet')
	else:
		system.perspective.closeDock('close_menu_tablet')
		system.perspective.openDock('close_menu_desktop')