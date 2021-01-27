from .DockerOpts import DockerOpts
from ..types.Errors import Errors
import subprocess

CMD_INITIALIZER = ["docker"]

class Docker:
	def __init__(self, image, entrypoint=None, **kwargs):
		self.image = image
		self.entrypoint = entrypoint
		self.volumes = kwargs.get('volumes')
		self.env = kwargs.get('env')
		self.command = CMD_INITIALIZER
		self.workdir = kwargs.get('workdir')
		self.remove = kwargs.get('remove', True)

	def _cmd_build(self, option):

		# Docker command usage is :
		#		docker [OPTIONS] COMMAND
		# So we firstly need to define docker option
		# Then we define the command to be runned by docker API.
		
		self.command.append(option)

		if self.remove is not None:
			assert(isinstance(self.remove, bool))
			if self.remove == True:
				self.command.append(DockerOpts.DELETE.value)

		if self.env is not None:
			# 
			# Here we are defining our environments as a dict
			# who's composed of key value pairs just as docker.
			# 
			assert(isinstance(self.env, dict))

			for key, val in self.env.items():
				self.command.append(DockerOpts.ENV.value)
				self.command.append(f"{key}={val}")

		if self.volumes is not None:
			# 
			# Here we are defining our volumes as a dict
			# who's composed of key value pairs just as docker.
			#
			assert(isinstance(self.volumes, dict))

			for key, val in self.volumes.items():
				self.command.append(DockerOpts.VOLUME.value)
				self.command.append(f"{key}:{val}")

		if self.workdir is not None:
			#
			# Here we are defining working directory
			# of the container.
			#
			assert(isinstance(self.workdir, str))

			self.command.append(DockerOpts.WORKDIR.value)
			self.command.append(self.workdir)

		assert(isinstance(self.image, str))
		self.command.append(self.image)

		if self.entrypoint is not None:
			# 
			#	Entrypoint is the entrypoint command.
			# 
			assert(isinstance(self.entrypoint, str))

			for command in self.entrypoint.split():
				self.command.append(command)

		return self.command

	def run(self, timeout=10) -> str:
		command = self._cmd_build("run")
		
		try:
			process = subprocess.run(command, capture_output=True, timeout=timeout)

			if process.returncode != 0:
				if process.stderr:
					error = process.stderr.decode()
				else:
					error = process.stdout.decode()

				output = f"Error : {error}"
			else:
				output = process.stdout.decode()

		except subprocess.TimeoutExpired:
			output = Errors.TIMEOUT_EXPIRED.value
		
		self.command = CMD_INITIALIZER
		return output
