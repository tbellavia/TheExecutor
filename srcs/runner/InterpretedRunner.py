from ..runner.Runner import Runner
from ..config.Config import Config
from ..context.Context import Context


class InterpretedRunner(Runner):
	def __init__(self, _input: str, config: Config, context: Context):
		super().__init__(_input, config, context)
	
	def run(self) -> str:
		pass