class Context:
	def __init__(self, extension, container, lang_type):
		self.extension = extension
		self.container = container
		self.lang_type = lang_type

	def __repr__(self):
		return f"<Context : .extension = {self.extension}, .lang_type = {self.lang_type}>"