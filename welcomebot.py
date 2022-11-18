#!/usr/bin/python
# welcomebot.py
import os
import discord
import re
from dotenv import load_dotenv
from discord.ext import commands

text_file = open("welcome_message.txt", "r")
welcome_messages = text_file.read().split("[/]")
text_file.close()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(intents=discord.Intents.all(), command_prefix='!')

@bot.event
async def on_ready():
  guild = discord.utils.get(bot.guilds, name=GUILD)
  print(
    f'{bot.user} is connected to the following guild:\n'
    f'{guild.name}(id: {guild.id})\n'
  )

@bot.event
async def on_member_update(before, after):
  guild = discord.utils.get(bot.guilds, name=GUILD)
  welcome_role = discord.utils.get(guild.roles, name="welcome")

  if welcome_role in after.roles and not welcome_role in before.roles:
    print(f'Role {welcome_role.name} was added to User {after.name}')
    print(f'Sending Welcome Message to {after.name}...')
    await after.create_dm()
    for message in welcome_messages:
      await after.dm_channel.send(message)
    print(f'Removing Role from User...\n')
    await after.remove_roles(welcome_role)


@bot.command(name='welcome')
async def welcome(ctx):
  if ctx.author == bot.user:
    return

  print('Command incoming:')
  print(f'Author Name: {ctx.author.name}')
  print(f'Author ID: {ctx.author.id}')
  print(f'Content: {ctx.message.content}')
  print(f'Clean_Content: {ctx.message.clean_content}')
  print(f'System_Content: {ctx.message.system_content}\n')

  if '<@' in ctx.message.system_content.lower():
    mentions = re.findall(r'\<.*?\>', ctx.message.system_content)
    for mention in mentions:
      print(f'Found Mention: {mention}')
      user_id = int(mention.replace("<", "").replace(">", "").replace("@", ""))
      member = bot.get_user(user_id)
      print(f'Sending Welcome Message to {member.name}...\n')
      await member.create_dm()
      for message in welcome_messages:
        await member.dm_channel.send(message)
    await ctx.message.add_reaction('<:O7_2:641014558982537236>')
    # To get the string for a custom emoji type \:emoji_name: in Discord and press enter

bot.run(TOKEN)
