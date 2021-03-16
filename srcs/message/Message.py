from ..types.Defines import *


class Message:
	def __init__(self, message: str):
		self.message = message
		self.content = None
		self.extension = None
		self.command = None

	def is_valid_message(self):
		return self.message.startswith(BACKTICKS) and self.message.endswith(RUN_CMD)

	def get_content(self) -> str:
		if self.is_valid_message():
			newline = self.message.find(NEWLINE)
			content = self.message[ newline + 1: ]
			content = content.replace( f"{BACKTICKS}{RUN_CMD}", "" )
			self.content = content
			return self.content
		self.content = None
		return self.content

	def get_extension(self) -> str:
		if self.is_valid_message:
			newline = self.message.find(NEWLINE)
			self.extension = self.message[ len(BACKTICKS) : newline ]
			return self.extension
		return None
