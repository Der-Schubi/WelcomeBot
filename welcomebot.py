#!/usr/bin/python -u
# welcomebot.py
import os
import disnake
from dotenv import load_dotenv
from disnake.ext import commands

load_dotenv()
ENV_TOKEN = os.getenv('DISCORD_TOKEN')
ENV_GUILD = os.getenv('DISCORD_GUILD')
ENV_REACTION = os.getenv('DISCORD_REACTION')
ENV_COMMAND_ROLE = os.getenv('DISCORD_COMMAND_ROLE')
ENV_WELCOME_ROLE = os.getenv('DISCORD_WELCOME_ROLE')
ENV_LOG_CHANNEL = os.getenv('DISCORD_LOG_CHANNEL')
ENV_BLACKLIST = os.getenv('DISCORD_BLACKLIST')
ENV_STATUS = os.getenv('DISCORD_STATUS')

blacklist = ENV_BLACKLIST.split(',')

text_file = open('welcome_message.txt', 'r')
welcome_messages = text_file.read().split('[/]')
text_file.close()

text_file = open('help_message.txt', 'r')
help_messages = text_file.read()
text_file.close()

bot = commands.Bot(
  command_prefix='/',
  intents=disnake.Intents.all(),
  help_command=None,
  #sync_commands_debug=True,
)

def getName(member):
  if member.nick == None:
    return member.name
  else:
    return member.nick

@bot.event
async def on_ready():
  guild = disnake.utils.get(bot.guilds, name=ENV_GUILD)
  print(
    f'{bot.user} is connected to the following Guild:\n'
    f'{guild.name}(id: {guild.id})\n'
  )
  await bot.change_presence(activity=disnake.Game(name=ENV_STATUS))

@bot.event
async def on_member_update(before, after):
  guild = disnake.utils.get(bot.guilds, name=ENV_GUILD)
  channel = disnake.utils.get(guild.channels, name=ENV_LOG_CHANNEL)
  welcome_role = disnake.utils.get(guild.roles, name=ENV_WELCOME_ROLE)

  if welcome_role in after.roles and not welcome_role in before.roles:
    if str(after.id) in blacklist:
      await channel.send(f'I’m sorry Dave, I’m afraid I can’t do that…')
      print(f'User {getName(after)} is in Blacklist, cowardly refusing to send Message!')
    else:
      print(f'Role {welcome_role.name} was added to User {getName(after)}')
      print(f'Sending Welcome Message to {getName(after)}...')
      await after.create_dm()
      for message in welcome_messages:
        await after.dm_channel.send(message)
      await channel.send(f'Sent Welcome Message to {getName(after)}.')
    print(f'Removing Role from User...\n')
    await after.remove_roles(welcome_role)

async def is_user_qualified(inter: disnake.ApplicationCommandInteraction):
  guild = disnake.utils.get(bot.guilds, name=ENV_GUILD)
  command_role = disnake.utils.get(guild.roles, name=ENV_COMMAND_ROLE)
  return command_role in inter.author.roles

@bot.slash_command(name='welcome', description='Sends the Welcome Message to the specified User.')
@commands.check(is_user_qualified)
async def welcome(inter: disnake.ApplicationCommandInteraction, member: disnake.Member) -> None:
  if str(member.id) in blacklist:
    await inter.response.send_message(f'I’m sorry <@{inter.author.id}>, I’m afraid I can’t do that…')
    print(f'User {getName(member)} is in Blacklist, cowardly refusing to send Message!')
    return

  print(f'Sending Welcome Message to {getName(member)}...\n')
  await member.create_dm()
  for message in welcome_messages:
    await member.dm_channel.send(message)
  channel = disnake.utils.get(inter.guild.channels, name=ENV_LOG_CHANNEL)
  await channel.send(f'Sent Welcome Message to {getName(member)}.')
  await inter.response.send_message(ENV_REACTION)

@welcome.error
async def welcome_error(inter: disnake.ApplicationCommandInteraction, error):
  if isinstance(error, commands.BadArgument):
    await inter.response.send_message('I couldn\'t find that Member!')
  elif isinstance(error, commands.CommandError):
    await inter.response.send_message(f'You must have the Role {ENV_COMMAND_ROLE} to tell me what to do!')

@bot.slash_command(name='help', description='Help to Schubi\'s WelcomeBot.')
async def help(inter: disnake.ApplicationCommandInteraction) -> None:
  await inter.response.send_message(message)

bot.run(ENV_TOKEN)
