#!/usr/bin/python
# welcomebot.py
import os
import discord
import re
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
  guild = discord.utils.get(client.guilds, name=GUILD)
  print(
    f'{client.user} is connected to the following guild:\n'
    f'{guild.name}(id: {guild.id})'
  )

  members = '\n - '.join([member.name for member in guild.members])
  print(f'Guild Members:\n - {members}\n')

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.lower().startswith('/welcome '):

    print('Message incoming:')
    print(f'Author Name: {message.author.name}')
    print(f'Author ID: {message.author.id}')
    print(f'Content: {message.content}')
    print(f'Clean_Content: {message.clean_content}')
    print(f'System_Content: {message.system_content}\n')

    if '<@' in message.system_content.lower():
      mentions = re.findall(r'\<.*?\>', message.system_content)
      for mention in mentions:
        print(f'Found Mention: {mention}')
        user_id = int(mention.replace("<", "").replace(">", "").replace("@", ""))
        member = client.get_user(user_id)
        print(f'Sending Welcome Message to {member.name}...\n')
        await member.create_dm()
        await member.dm_channel.send(
          f'Hi {member.name}!'
        )

  #if 'testing' in message.content.lower():
  #    response = 'Huhu!'
  #    await message.channel.send(response)


client.run(TOKEN)
