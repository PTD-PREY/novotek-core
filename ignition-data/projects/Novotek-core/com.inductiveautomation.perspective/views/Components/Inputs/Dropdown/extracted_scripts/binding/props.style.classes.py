# {
#     "path": "../Dropdown.props.value"
# }

	if self.getSibling("Dropdown").props.value in ["", [], None]:
		return "colors/text/grey400"
	else:
		return "buttons/error_blank"