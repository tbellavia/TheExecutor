# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    bot.py                                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: bbellavi <bbellavi@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/11/16 06:16:50 by bbellavi          #+#    #+#              #
#    Updated: 2020/11/19 01:21:37 by bbellavi         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import hashlib
import discord
import subprocess
import yaml


with open("config.yaml", "r") as f:
	config = yaml.load(f, Loader=yaml.FullLoader)

TOKEN			= config["bot"]["API_KEY"]
CWD				= os.getcwd()
POLL_DIR		= "poll"
EXEC_ROLES		= config["server"]["scope"]["roles"]
EXEC_CHANNELS 	= config["server"]["scope"]["channels"]
TIMEOUT			= int(config["exec"]["timeout"])

with open("context.yaml", "r") as f:
	CONTEXT = yaml.load(f, Loader=yaml.FullLoader)

class TheExecutor(discord.Client):
	async def on_ready(self):
		print(f"{self.user} has connected to Discord!")

	def _is_exec_channel(self, channel_id):
		return channel_id in EXEC_CHANNELS

	def _is_exec_role(self, rolename):
		return rolename in EXEC_ROLES

	def _is_valid_executor(self, roles, channel_id):
		is_exec = self._is_exec_channel(channel_id)
		is_role = any(self._is_exec_role(role) for role in roles)
		return is_exec and is_role

	def _get_command(self, filename, context):
		if context['interpreted']:
			return f"docker run -it --rm -v {CWD}/{POLL_DIR}:/tmp/{POLL_DIR} -w /tmp/{POLL_DIR} {context['image']} {context['interpreter']} {filename}"

	def _execute_interpreted(self):
		return None

	def _execute_compiled(self):
		return None

	def _execute(self, filename, context):
		command = self._get_command(filename, context)
		
		try:
			process = subprocess.run(command.split(), capture_output=True, timeout=TIMEOUT)
			if process.returncode != 0:
				result = "Error : " + process.stderr.decode() if process.stderr else process.stdout.decode()
			else:
				result = process.stdout.decode()
			
			if context['interpreter'] == "php":
				result = result[2:]
				
		except subprocess.TimeoutExpired:
			result = "Time limit exceeded"
		
		return result

	async def on_message(self, message):
		if not os.path.exists(POLL_DIR):
			os.mkdir(POLL_DIR)

		roles = [role.name for role in message.author.roles]
		channel_id = str(message.channel.id)
		content = message.content

		if self._is_valid_executor(roles, channel_id):

			if content.endswith("!run"):
				content = content[:-4]

				if content.startswith("```") and content.endswith("```"):
					extension = content[3:][:3].strip()

					if extension in CONTEXT.keys():
						content = content[5:-3].strip()
						msg_hash = hashlib.sha256(f"{content + str(message.id)}".encode()).hexdigest()
						filename = f"{msg_hash}.{extension}"
						fullname = f"{POLL_DIR}/{filename}"
						
						with open(fullname, 'w') as f:
							f.write(content)

						result = self._execute(filename, CONTEXT[extension])

						os.remove(fullname)

						await message.channel.send(f"```md\n{result}\n```")

TheExecutor().run(TOKEN)
