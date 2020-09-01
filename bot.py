# bot.py
import os
import random
import discord

from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix = '!')

# # # TO DO # # #
# Add error handling for wrong commands
# Add ban/muting capabilities
# Add language parsing


# --- Connecting to Server --- #
@bot.event
async def on_ready():
# -- Basic way to name Guild -- #
#	for guild in client.guilds:  
#		if guild.name == GUILD:
#			break

# -- Using find() to determine guild name -- #
#	guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)

# -- Using get() to determine guild name -- #
	guild = discord.utils.get(bot.guilds, name = GUILD)

	print(
	f'{bot.user} is connected to the following guild:\n'
	f'{guild.name}(id: {guild.id})'
	)
	
	members = '\n - '.join([member.name for member in guild.members])
	print(f'Guild Members: \n - {members}')
	

# --- New Members --- #
@bot.event
async def on_member_join(member):
	await member.create_dm()
	await member.dm_channel.send(
		f'Hi {member.name}, welcome to the UNR IEEE Student chapter discord!  Make sure to introduce yourself and have fun!'
	)

# --- Chat Filter --- #
#with open("bad-words.txt") as file:
#	bad_words = [bad_word.strip().lower() for bad_word in file.readlines()]
#@bot.event
#async def on_message(message):
#	message_content = message.content.strip().lower()
#	for bad_word in bad_words:
#		if any(bad_word in message for bad_word in bad_words):
#			await bot.send_message(message.channel, "{}, your message has been censored.".format(message.author.mention))
#			await bot.delete_message(message)

# --- Exception Handling --- #
@bot.event
async def on_error(event, *args, **kwargs):
	with open('err.log', 'a') as f:
		if event == 'on_message':
			f.write(f'Unhandled message: {args[0]}\n')
		else:
			raise

# #################### #
# --- Bot Commands --- #
# #################### #

# --- Role Assignment --- #
@bot.command(help = 'Use this to assign a role!')
async def addrole(ctx, major: str):
	member = ctx.message.author
	role = discord.utils.get(member.guild.roles, name = major)
		
	await member.add_roles(role, reason = 'Adding role to user', atomic = True)
	await ctx.send('Your role has been added!')
	
@addrole.error
async def info_error(ctx, error):
	if isinstance(error, commands.CommandError):
		await ctx.send('That is an invalid role, or missing a role.  Check your command and try again, make sure to type "!addrole <role>"!')


bot.run(TOKEN)