from discord import TextChannel

class Sender:
    @staticmethod
    def send(channel: TextChannel, message: str):
        channel.send(message)