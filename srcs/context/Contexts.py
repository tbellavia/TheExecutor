from ..types.LangType import LangType
from .Context import Context
import yaml


class Contexts:
	def __init__(self, filename=None):
		self.contexts = {}

		if filename is not None:
			self.load(filename)

	def __repr__(self):
		return f"<Contexts : {self.contexts}"

	def load(self, filename: str):
		with open(filename, 'r') as f:
			data = yaml.load(f, Loader=yaml.FullLoader)

		for key, value in data.items():
			image = value['image']
			entrypoint = value['entrypoint']
			lang_type = LangType.INTERPRETED if value['interpreted'] else LangType.COMPILED
			self.contexts[key] = Context(key, image, entrypoint, lang_type)
	
	def get_context(self, extension: str) -> Context:
		return (self.contexts.get(extension))