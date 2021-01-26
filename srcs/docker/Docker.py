from .DockerOpts import DockerOpts

class Docker:
	def __init__(self, image, entrypoint=None, **kwargs):
		self.image = image
		self.entrypoint = entrypoint
		self.volumes = kwargs.get('volumes')
		self.env = kwargs.get('env')
		self.command = ["docker"]
		self.workspace = kwargs.get('workspace')
		self.remove = kwargs.get('remove')

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

		assert(isinstance(self.image, str))
		self.command.append(self.image)

		if self.entrypoint is not None:
			# 
			#	Entrypoint is the entrypoint command.
			# 
			assert(isinstance(self.entrypoint, str))
			self.command.append(self.entrypoint)

		return " ".join(self.command)

	def run(self):
		cmd = self._cmd_build("run")
