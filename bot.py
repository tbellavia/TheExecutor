# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    bot.py                                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: bbellavi <bbellavi@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/11/16 06:16:50 by bbellavi          #+#    #+#              #
#    Updated: 2020/11/16 08:33:39 by bbellavi         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import hashlib
import discord
import subprocess

EXEC_CHANNEL = "777764433761271828"

TOKEN = os.environ.get('DISCORD_TOKEN')
CWD = os.getcwd()
POLL_DIR = "poll"
client = discord.Client()

class TheExecutor(discord.Client):
	async def on_ready(self):
		print(f"{self.user} has connected to Discord!")

	async def on_message(self, message):
		if not os.path.exists(POLL_DIR):
			os.mkdir(POLL_DIR)

		if str(message.channel.id) == EXEC_CHANNEL:
			if message.content.startswith("```py") and message.content.endswith("```"):
				content = message.content[5:-3]
				content = content.strip()
				
				msg_hash = hashlib.sha256(f"{message.content + str(message.id)}".encode()).hexdigest()
				filename = f"{msg_hash}.py"
				fullname = f"{POLL_DIR}/{filename}"
				
				with open(fullname, 'w') as f:
					f.write(content)
				
				COMMAND = f"docker run -it --rm -v {CWD}/{POLL_DIR}:/tmp/{POLL_DIR} -w /tmp/poll python:3 python {filename}"

				try:
					process = subprocess.run(COMMAND.split(), capture_output=True, timeout=10)
					if process.returncode != 0:
						result = "Error : " + process.stderr.decode() if process.stderr else process.stdout.decode()
					else:
						result = process.stdout.decode()
				except subprocess.TimeoutExpired:
					result = "Time limit exceeded"

				os.remove(fullname)

				await message.channel.send(f"```md\n{result}\n```")

TheExecutor().run(TOKEN)