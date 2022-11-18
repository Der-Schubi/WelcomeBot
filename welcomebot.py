#!/usr/bin/python
# welcomebot.py
import os
import discord
import re
from dotenv import load_dotenv

text_file = open("welcome_message.txt", "r")
welcome_messages = text_file.read().split("[/]")
text_file.close()

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

@client.event
async def on_member_update(before, after):
  guild = discord.utils.get(client.guilds, name=GUILD)
  welcome_role = discord.utils.get(guild.roles, name="welcome")

  if welcome_role in after.roles and not welcome_role in before.roles:
    print(f'Role {welcome_role.name} was added to User {after.name}')
    print(f'Sending Welcome Message to {after.name}...')
    await after.create_dm()
    for message in welcome_messages:
      await after.dm_channel.send(message)
    print(f'Removing Role from User...\n')
    await after.remove_roles(welcome_role)

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
        for message in welcome_messages:
          await after.dm_channel.send(message)

client.run(TOKEN)
