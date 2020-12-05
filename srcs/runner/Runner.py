from ..docker.Docker import Docker
from ..config.Config import Config
from ..context.Context import Context
from abc import ABC, abstractmethod


class Runner(ABC):
	def __init__(self, _input: str, config: Config, context: Context):
		self.input = _input
		self.config = config
		self.context = context
		self.docker = None
		self.hash = None

	@abstractmethod
	def run(self) -> str:
		pass