from enum import Enum

BACKTICKS = "```"
NEWLINE = "\n"
RUN_CMD = "!run"

class RunnerDefs(Enum):
	WORKDIR = "/runner"
	RESOURCES = "/resources"