from discord.ext import tasks, commands
import discord
import discord.utils
import os.path
import json
import traceback
import asyncio


class Bot(commands.Bot):
    """The Windia FAQ bot base
    Inherits from discord.ext.commands.Bot"""

    def __init__(self, prefix):
        self.prefix = prefix
        self.queued_commands = list()

        super().__init__(prefix, help_command=None)

    async def on_ready(self):
        """Loads the commands and then prints a message to the console once the Bot has connected"""
        
        print(f'{self.user.name} connected.')

    async def on_error(self, event, *args, **kwargs):
        """Prints unhandled errors to console"""

        exception_message = traceback.format_exc().splitlines()[-1]
        user_message = args[0]

        if user_message:
            print(f'User {user_message.author.name} caused an unhandled exception\n' \
                  f'Event caused by event: {event}' \
                  f'Exception caused by message: {user_message.content}\n' \
                  f'Exception: {exception_message}')
        else:
            print(f'Unhandled exception caused by event: {event}' \
                  f'Exception: {exception_message}')

    async def on_command_error(self, ctx: commands.Context, exception: commands.CommandError):
        """Prints unhandled command errors to console"""

        if isinstance(exception, (commands.MissingPermissions, commands.UserInputError)):
            return

        error_message = f'Unhandled exception by: {ctx.author.name}\n' \
                        f'Message: {ctx.message.content}\n' \
                        f'Error Type: {type(exception).__name__}\n' \
                        f'Error: {exception}'

        print(error_message)


    async def on_message(self, message: discord.Message):
        """Command handling"""

        if message.author.bot:
            return

        if isinstance(message.channel, discord.DMChannel):
            await message.channel.send('Please use me in a public channel!')
            return


        if message.content.startswith(self.prefix):
            raw_command = message.content.lower()[1::].split(' ')
            command = raw_command[0]
            
            if self.get_command(command):
                task = asyncio.create_task(self.process_commands(message))
                self.queued_commands.append(task)

    @tasks.loop(seconds=1/10)
    async def dequeue_commands(self):
        """This loop serves as a queue for processing commands so they aren't all processed at once"""

        if len(self.unprocessed_commands) > 0:
            await self.unprocessed_commands.pop(0)

    @dequeue_commands.before_loop
    async def before_dequeue_commands(self):
        """Output to the console that Command Processing has started"""

        await self.bot.wait_until_ready()
        print('Command Processing started')
