# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    bot.py                                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: bbellavi <bbellavi@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/11/16 06:16:50 by bbellavi          #+#    #+#              #
#    Updated: 2020/11/17 12:23:00 by bbellavi         ###   ########.fr        #
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

CONTEXT			= {
	"py" : {
		"image"			: "python:3",
		"interpreter"	: "python"
	},
	"sh" : {
		"image"			: "bash",
		"interpreter"	: "bash",
	},
	"js" : {
		"image"			: "node",
		"interpreter"	: "node"
	},
	"php" : {
		"image"			: "php:7.4-cli",
		"interpreter"	: "php"
	}
}

class TheExecutor(discord.Client):
	async def on_ready(self):
		print(f"{self.user} has connected to Discord!")

	def get_command(self, filename, context):
		return f"docker run -it --rm -v " \
				f"{CWD}/{POLL_DIR}:/tmp/{POLL_DIR} " \
				f"-w /tmp/{POLL_DIR} " \
				f"{context['image']} " \
				f"{context['interpreter']} {filename}"

	def execute(self, filename, context):
		command = self.get_command(filename, context)
		
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

	def is_exec_channel(self, channel_id):
		return channel_id in EXEC_CHANNELS

	def is_exec_role(self, rolename):
		return rolename in EXEC_ROLES

	async def on_message(self, message):
		if not os.path.exists(POLL_DIR):
			os.mkdir(POLL_DIR)

		user_roles = [role.name for role in message.author.roles]


		if self.is_exec_channel(str(message.channel.id)) and any(self.is_exec_role(role) for role in user_roles):
			content = message.content

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

						result = self.execute(filename, CONTEXT[extension])

						os.remove(fullname)

						await message.channel.send(f"```md\n{result}\n```")

TheExecutor().run(TOKEN)
