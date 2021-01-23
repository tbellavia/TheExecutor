from ..runner.Runner import Runner
from ..config.Config import Config
from ..context.Context import Context


class InterpretedRunner(Runner):
	def __init__(self, content: str, config: Config, context: Context):
		super().__init__(content, config, context)

	def run(self) -> str:
		self._write_snippet()