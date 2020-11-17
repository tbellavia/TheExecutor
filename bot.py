# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    bot.py                                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: bbellavi <bbellavi@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/11/16 06:16:50 by bbellavi          #+#    #+#              #
#    Updated: 2020/11/17 11:06:36 by bbellavi         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import hashlib
import discord
import subprocess

TOKEN			= os.environ.get('DISCORD_TOKEN')
CWD				= os.getcwd()
POLL_DIR		= "poll"
EXEC_ROLE		= "L'exécuteur"
EXEC_CHANNELS 	= [
	"396825382009044996",
	"434394879829868565",
	"635116762555482112",
	"397040921671368704",
	"397040940415713293",
	"497371961119342602",
	"497373788414148609",
	"658360594319147008"
]

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

client = discord.Client()

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
		COMMAND = self.get_command(filename, context)
		
		try:
			process = subprocess.run(COMMAND.split(), capture_output=True, timeout=10)
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

		user_roles = [role.name for role in message.author.roles]


		if str(message.channel.id) in EXEC_CHANNELS and EXEC_ROLE in user_roles:
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

if TOKEN is not None:
	TheExecutor().run(TOKEN)
else:
	print("You must export your API to use bot.py")
	print("\n\techo \"export DISCORD_TOKEN=YOUR_API_KEY\" >> ~/.zshrc")
	print()
