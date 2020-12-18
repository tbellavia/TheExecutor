from ..config.Config import Config
from ..context.Contexts import Contexts
from ..sender.Sender import Sender


class Bot:
	def __init__(self, config: Config, contexts: Contexts):
		self.config = config
		self.contexts = contexts
		self.name = None

		assert not (config == None), "config must not be equal to None"
		assert not (contexts == None), "contexts must not be equal to None"

	def extract(self, content: str) -> str:
		"""
			Extract the content without backticks.
		"""
		pass

	def run(self, content: str) -> str:
		pass