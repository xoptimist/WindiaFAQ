from botcore import Bot
from dotenv import load_dotenv
import os
import os.path
import traceback

load_dotenv()

cogs_path = './cogs'
cogs = [ f'cogs.{file[:-3]}' for file in os.listdir(cogs_path) if file.endswith('.py') ]
bot = Bot('~')

for cog in cogs:
    try:
        bot.load_extension(cog)
        print(cog, 'loaded')
    except:
        print(cog, 'could not be loaded')
        traceback.print_exc()

bot.run(os.getenv('TOKEN'), reconnect=True)