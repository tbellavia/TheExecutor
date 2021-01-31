from ..runner.Runner import Runner
from ..config.Config import Config
from ..context.Context import Context
from ..docker.Docker import Docker
from ..types.Defines import RunnerDefs

class InterpretedRunner(Runner):
	def __init__(self, content: str, config: Config, context: Context):
		super().__init__(content, config, context)

	def run(self) -> str:
		self._build_filename()
		self._write_snippet()

		entrypoint = f"{self.context.entrypoint} {self.filename}"
		# print(entrypoint)
		#
		# As we can't pass a relative path for docker volume,
		# the context file must contain absolute path.
		# 
		volumes = {
			self.config.runner.snippets_path : RunnerDefs.WORKDIR.value,
			self.config.runner.resources_path : RunnerDefs.RESOURCES.value
		}
		workdir = RunnerDefs.WORKDIR.value

		docker = Docker(
			self.context.image,
			entrypoint=entrypoint,
			volumes=volumes,
			workdir=workdir
		)

		output = docker.run(timeout=self.config.runner.timeout)

		self._remove_snippet()
		return output