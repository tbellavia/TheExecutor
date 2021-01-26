from enum import Enum

class DockerOpts(Enum):
	ENV = "-e"
	VOLUME = "-v"
	DELETE = "--rm"
	WORKDIR = "-w"