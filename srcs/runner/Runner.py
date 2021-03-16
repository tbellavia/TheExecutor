from ..docker.Docker import Docker
from ..config.Config import Config
from ..context.Context import Context
from abc import ABC, abstractmethod
from hashlib import sha256
import time
import os


class Runner(ABC):
	def __init__(self, content: str, config: Config, context: Context):
		self.content = content
		self.config = config
		self.context = context
		self.docker = None
		self.hash = None
		self.filename = None
		self.fullpath = None

	def _hash(self):
		# Create hash
		timestamp = str(time.time()).encode()
		hasher = sha256()
		hasher.update(timestamp)
		hasher.update(self.content.encode())

		self.hash = hasher.hexdigest()
		return self.hash

	def _build_filename(self):
		# Build filename
		self._hash()
		self.filename = f"{self.hash}.{self.context.extension}"
		return self.filename

	def _build_fullpath(self):
		# Build fullpath -> /{fullpath}/{filename}
		self._build_filename()
		self.fullpath = os.path.join(
			self.config.runner.snippets_path,
			self.filename
		)
		return self.fullpath

	def _write_snippet(self):
		self._build_fullpath()

		with open(self.fullpath, "w") as f:
			f.write(self.content)

	def _remove_snippet(self):
		os.remove(self.fullpath)

	@abstractmethod
	def run(self) -> str:
		pass
