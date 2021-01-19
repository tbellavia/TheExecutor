from ..types.LangType import LangType
from ..docker.Docker import  Docker
from .Context import Context
import yaml
import json


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
			container = Docker(value['image'], value['interpreter'])
			lang_type = LangType.INTERPRETED if value['interpreted'] else LangType.COMPILED
			self.contexts[key] = Context(key, container, lang_type)
	
	def get_context(self, extension: str) -> Context:
		return (self.contexts.get(extension))