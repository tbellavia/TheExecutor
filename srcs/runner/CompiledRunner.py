from ..config.Config import Config
from ..context.Context import Context
from ..types.Defines import RunnerDefs
from ..docker.Docker import Docker
from .Runner import Runner


class CompiledRunner(Runner):
	def __init__(self, content: str, config: Config, context: Context):
		super().__init__(content, config, context)

	def run(self) -> str:
		self._build_filename()
		self._write_snippet()

		# Command to be executed into the docker container
		entrypoint = f"{self.context.entrypoint} {self.filename}"

		volumes = {
			self.config.runner.snippets_path : RunnerDefs.WORKDIR.value,
			self.config.runner.resources_path : RunnerDefs.RESOURCES.value
		}

		workdir = RunnerDefs.WORKDIR.value

		docker = Docker(
			self.context.image,
			entrypoin=entrypoint,
			volumes=volumes,
			workdir=workdir,
		)

		output = docker.run(timeout=self.config.runner.timeout)

		# self._remove_snippet()
		return output