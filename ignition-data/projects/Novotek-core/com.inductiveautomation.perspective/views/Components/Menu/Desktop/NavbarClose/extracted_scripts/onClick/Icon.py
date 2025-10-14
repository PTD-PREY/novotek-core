	current_theme = self.session.props.theme

	if current_theme == "novotek-light":
		self.session.props.theme = "novotek-dark"
	else:
		self.session.props.theme = "novotek-light"