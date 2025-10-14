# {
#     "path": "../Dropdown.props.value"
# }

	if self.getSibling("Dropdown").props.value in ["", [], None]:
		return self.view.params.icons.left.value
	else:
		return "novotek_icons/close-line"