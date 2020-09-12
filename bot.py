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
bot.remove_command('help')

# # # TO DO # # #
# Add error handling for wrong commands
# Add ban/muting capabilities
# Add language parsing
# Add !help support


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

	embed = discord.Embed(
		colour = discord.Colour.blue()
	)
	
	embed.set_author(name = 'Welcome to the UNR IEEE Student Chapter!')
	embed.add_field(name = 'Introductions', value = 'Make sure to introduce yourself, invite your friends, and help foster this growing community!', inline = False)
	embed.add_field(name = 'Questions/Help', value = 'If you have any questions feel free to DM an officer or ask in the chat!', inline = False)
	embed.add_field(name = 'Rules', value = 'As we are a club we are held to the UNR Student Code of Conduct so please keep that in mind during your visit.  For a more indepth look at the rules please see #rules in the server.', inline = False)
	embed.add_field(name = 'Bot Help', value = 'This process is automatic, for more commands type "!help" in any chat.  Any questions or concerns about the bot can be directed to @Tollaw#0124', inline = False)
	
	await member.create_dm()
	await member.dm_channel.send(embed = embed)

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

# --- New Help Command ---#
@bot.command(pass_context = True)
async def help(ctx):
	author = ctx.message.author
	
	embed = discord.Embed(
		colour = discord.Colour.blue()
	)
	
	embed.set_author(name = 'The UNR IEEE Student Chapter Help Menu')
	embed.add_field(name = 'General Help', value = 'Please message @Officer if you have any concerns', inline = False)
	embed.add_field(name = 'Bot Issues', value = 'If you need help with something with the bot, message @Tollaw#0124', inline = False)
	embed.add_field(name = '!addrole', value = 'Use this command to assign yourself a role, Alumni and Faculty will need mod verification.', inline = False)
	embed.add_field(name = '!details', value = 'This is my github if you are curious how my brain works: https://github.com/Tollaw/UNR-IEEE-Discord-Bot ', inline = False)
	
	
	
	await discord.User.send(author, embed = embed)


# --- Role Assignment --- #
@bot.command(help = 'Use this to assign a role!')
async def addrole(ctx, major: str):
	member = ctx.message.author
	role = discord.utils.get(member.guild.roles, name = major)
		
	await member.add_roles(role, reason = 'Adding role to user', atomic = True)
	#await ctx.send('Your role has been added!')
	
@addrole.error
async def info_error(ctx, error):
	if isinstance(error, commands.CommandError):
		await ctx.send('That is an invalid role, or missing a role.  Check your command and try again, make sure to type "!addrole <role>"!')


bot.run(TOKEN)