from ..config.Config import Config
from ..context.Contexts import Contexts
from ..sender.Sender import Sender
from ..message.Message import Message
from ..runner.InterpretedRunner import InterpretedRunner
from ..runner.CompiledRunner import CompiledRunner
from ..types.Errors import *
from ..types.LangType import LangType
import discord


class Bot(discord.Client):
	def __init__(self, config: Config, contexts: Contexts, **kwargs: dict):
		super().__init__()
		self.config = config
		self.contexts = contexts
		self.name = kwargs.get("name")
		self.on_ready_header = kwargs.get("header")

		assert not (config is None), "config must not be equal to None"
		assert not (contexts is None), "contexts must not be equal to None"

		self.run(self.config.server.token)

	def exec(self, message: Message) -> str:
		extension = message.get_extension()
		context = self.contexts.get_context(extension)
		content = message.get_content()

		if context is None:
			return Errors.EXT_NOT_SUPPORTED.value
		else:
			if context.lang_type == LangType.INTERPRETED:
				runner = InterpretedRunner(content, self.config, context)
			elif context.lang_type == LangType.COMPILED:
				runner = CompiledRunner(content, self.config, context)
			else:
				return Errors.EXT_NOT_SUPPORTED.value

			return runner.run()

	async def on_message(self, discord_message):
		chan_id = str(discord_message.channel.id)

		message = Message(discord_message.content)
		if chan_id in self.config.server.channels:
			if message.is_valid_message():
				response = self.exec(message)
				await Sender.send(discord_message.channel, response)

	async def on_ready(self):
		if self.on_ready_header:
			print(self.on_ready_header)
		else:
			print("Bot is ready!")