"""This file serves as the entry point for WindiaFAQ

This file loads the environment variables from the .env file,
then loads the cogs used for the command modules for the WindiaFAQ
Discord Bot, then runs the WindiaFAQ Bot using the Token stored in 
the .env file.
"""

from botcore import Bot
from dotenv import load_dotenv
from discord.ext import commands
import discord.errors
import os
import os.path
import sys
import traceback

if not os.path.exists('./.env'):
    print('No .env file could be found!')
    print('Please create a .env file, place it in the main directory, and format it like this:')
    print('\tTOKEN = \'<INSERT TOKEN HERE>\'')
    print('\tPREFIX = \'<INSERT PREFIX HERE>\'')
    sys.exit(0)

load_dotenv()

prefix = os.getenv('PREFIX', None)
token = os.getenv('TOKEN', None)

if not prefix or prefix == '':
    print('No prefix set in the .env file. Please set a prefix to use this bot.')
    print('EX: PREFIX = \'PREFIX\'')
    sys.exit(0)

if not token or token == '':
    print('No token set in the .env file. Please set a token to use this bot.')
    print('EX: TOKEN = \'TOKEN\'')
    sys.exit(0)

cogs_path = './cogs'
if os.path.exists(cogs_path):
    cogs = [ f'cogs.{file[:-3]}' for file in os.listdir(cogs_path) if file.endswith('.py') ]

bot = Bot(prefix)

for cog in cogs:
    try:
        bot.load_extension(cog)
        print(f'{cog} loaded')
    except commands.ExtensionAlreadyLoaded:
        print(f'{cog} is already loaded.')
    except commands.ExtensionNotFound:
        print(f'{cog} not found.')
    except commands.NoEntryPointError:
        print(f'{cog} has no setup function.')
    except:
        print(f'An unhandled error was thrown while loading {cog}')
        traceback.print_exc()
        continue

try:
    bot.run(token, reconnect=True)
except discord.errors.LoginFailure:
    print('An improper token was passed. Please enter a valid token into the .env file.')
    sys.exit(0)
except:
    print('An unhandled error was thrown while logging into Discord.')
    traceback.print_exc()
    sys.exit(0)