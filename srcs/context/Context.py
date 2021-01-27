class Context:
	def __init__(self, extension, image, entrypoint, lang_type):
		self.extension = extension
		self.image = image
		self.entrypoint = entrypoint
		self.lang_type = lang_type

	def __repr__(self):
		return f"<Context : .extension = {self.extension}, .lang_type = {self.lang_type}>"