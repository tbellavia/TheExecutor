from enum import Enum


class Errors(Enum):
	FILE_NOT_FOUND = "File not found"
	FILE_TOO_LARGE = "File too large"
	EXT_NOT_SUPPORTED = "Language is not supported."