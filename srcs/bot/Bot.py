from ..config.Config import Config
from ..context.Contexts import Contexts
from ..sender.Sender import Sender
from ..message.Message import Message
import discord


class Bot(discord.Client):
	def __init__(self, config: Config, contexts: Contexts, **kwargs: dict):
		super().__init__()
		self.config = config
		self.contexts = contexts
		self.name = kwargs.get("name")
		self.on_ready_header = kwargs.get("header")

		assert not (config == None), "config must not be equal to None"
		assert not (contexts == None), "contexts must not be equal to None"

		self.run(self.config.server.token)

	def exec(self, content: str) -> str:
		pass

	async def on_message(self, message):
		chan_id = str(message.channel.id)

		message = Message(message.content)
		if chan_id in self.config.server.channels:
			if message.is_valid_message():
				content = message.get_content()
				self.exec(content)

	async def on_ready(self):
		if self.on_ready_header:
			print(self.on_ready_header)
		else:
			print("Bot is ready!")