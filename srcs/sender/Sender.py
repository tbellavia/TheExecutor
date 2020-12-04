from ..types.Errors import Errors
from discord import TextChannel
import discord
import math

class Sender:
	CHUNK_MAX_SIZE = 2000
	@staticmethod
	async def send(channel: TextChannel, message: str):
		channel.send(message)

	@staticmethod
	async def send_file(channel: TextChannel, filename: str):
		try:
			with open(filename, "r") as f:
				file = discord.File(f)
				await channel.send(file=file)
		except FileNotFoundError:
			await channel.send(Errors.FILE_NOT_FOUND)
		except UnicodeDecodeError:
			await channel.send(Errors.FILE_TOO_LARGE)

	@staticmethod
	async def send_long_message(channel: TextChannel, message: str):
		chunks_nb = math.ceil( len(message) / Sender.CHUNK_MAX_SIZE )

		for i in range(chunks_nb):
			chunk = message[ i * Sender.CHUNK_MAX_SIZE : ( i + 1 ) * Sender.CHUNK_MAX_SIZE ]
			await channel.send(chunk)