# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    bot.py                                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: bbellavi <bbellavi@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/11/16 06:16:50 by bbellavi          #+#    #+#              #
#    Updated: 2020/11/16 06:33:37 by bbellavi         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import discord

TOKEN = os.environ.get('DISCORD_TOKEN')
client = discord.Client()

@client.event
async def on_ready():
	print(f"{client.user} has connected to Discord!")

client.run(TOKEN)