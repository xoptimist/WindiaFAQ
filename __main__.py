"""This file serves as the entry point for WindiaFAQ

This file loads the environment variables from the .env file,
then loads the cogs used for the command modules for the WindiaFAQ
Discord Bot, then runs the WindiaFAQ Bot using the Token stored in 
the .env file.
"""

import os.path
import sys
import traceback

import discord.errors
from discord.ext import commands

from botcore import Bot
from windiautils import Config

config = Config.getInstance()
prefix = config.get('Bot', 'Prefix')
token = config.get('Bot/Secrets', 'Token')

if not token:
    print('No token set in the configuration file. Please set a token to use this bot.')
    sys.exit(0)

bot = Bot(prefix)
cogs_path = './cogs'
if os.path.exists(cogs_path):
    cogs = [f'cogs.{file[:-3]}' for file in os.listdir(cogs_path) if file.endswith('.py')]

    for cog in cogs:
        try:
            bot.load_extension(cog)
            print(f'{cog} loaded.')
        except commands.ExtensionAlreadyLoaded:
            print(f'{cog} is already loaded.')
        except commands.ExtensionNotFound:
            print(f'{cog} not found.')
        except commands.NoEntryPointError:
            print(f'{cog} has no setup function.')
        except Exception:
            print(f'An unhandled error was thrown while loading {cog}')
            traceback.print_exc()
            continue

try:
    bot.run(token, reconnect=True)
except discord.errors.LoginFailure:
    print('An improper token was passed. Please enter a valid token into the configuration file.')
    sys.exit(0)
except Exception:
    print('An unhandled error was thrown while logging into Discord.')
    traceback.print_exc()
    sys.exit(0)
