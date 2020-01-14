from discord.ext import tasks, commands

import asyncio
import discord
import discord.utils
import json
import os.path
import traceback


class Bot(commands.Bot):
    """The Windia FAQ Bot base
    Inherits from discord.ext.commands.Bot
    
    Methods
    -------
    async def on_ready()
        Alerts the user that the bot is initialized
        
    async def on_error(event: str, *args, **kwargs)
        Prints unhandled errors to console

    async def on_command_error(ctx: discord.ext.commands.Context,
                               exception: discord.ext.commands.CommandError)
        Prints unhandled command errors to console

    async def on_message(message: discord.Message)
        An event thrown when a user sends a message in the bot's guilds, used for command handling

    async def dequeue_commands()
        A loop to process commands from the bot's guild members

    async def before_dequeue_commands()
        An event fired once before the dequeue command loop starts
    """

    def __init__(self, command_prefix: str):
        """The constructor for the Bot class

        Bot(command_prefix: str)

        Members
        -------
        queued_commands
            A list of commands queued by the bot to process and output to the user
        """

        self.queued_commands = list()
        super().__init__(command_prefix, help_command=None)

    async def on_ready(self):
        """Alerts the user that the bot is initialized
        
        await on_ready()

        This is a coroutine. This is not called directly; it is fired whenever the
        bot is logged into Discord and is ready for use."""
        
        print(f'{self.user.name} connected.')

    async def on_error(self, event: str, *args, **kwargs):
        """Prints unhandled errors to console
        
        await on_error(event: str, *args, **kwargs)

        This is a coroutine. This is not called directly; it is fired whenever the
        bot catches an exception that is unhandled. This event prints an error
        message to the console.

        TODO: Add logging to a Discord channel.

        Parameters
        ----------

        event: str
            The event method's name that caused the exception.
        """


        print(args)
        print([*kwargs])

        error_message = args[0]

        print(f'Unhandled exception caused by event: {event}' \
              f'Exception: {message}')

    async def on_command_error(self, ctx: commands.Context, exception: commands.CommandError):
        """Prints unhandled command errors to console.
        
        await on_command_error(ctx: discord.ext.commands.Context,
                               exception: discord.ext.commands.CommandError)

        This is a coroutine. This is not called directly; it is fired whenever the
        bot catches an exception in a command that is unhandled. This event prints
        an error message to the console.
        
        TODO: Add logging to a Discord channel.
        
        Parameters
        ----------

        ctx: discord.ext.commands.Context
            The context of the message that threw the exception

        exception: discord.ext.commands.CommandError
            The exception that was thrown
        """

        error_message = f'Unhandled exception by: {ctx.author.name}\n' \
                        f'Message: {ctx.message.content}\n' \
                        f'Error Type: {type(exception).__name__}\n' \
                        f'Error: {exception}'

        print(error_message)

    async def on_message(self, message: discord.Message):
        """An event thrown when a user sends a message in the bot's guilds, used for command handling.

        await on_message(message: discord.Message)

        This is a coroutine. This is not called directly; it is fired whenever the 
        Bot receives a message. This is used for attempting to parse the message 
        for a command. If the message is sent by a bot, it is ignored. If the message 
        begins with the command prefix, it is then tested for membership in the bot's 
        stored commands. If it passes, then the message is queued to be processed 
        by the bot as a command, otherwise it is ignored.
        
        Parameters
        ----------
        message: discord.Message
            The message object received by the Bot to attempt to process as a command
        """

        if message.author.bot:
            return

        if message.content.startswith(self.command_prefix):
            raw_command = message.content.lower()[1::].split(' ')
            command = raw_command[0]
            
            if self.get_command(command):
                task = asyncio.create_task(self.process_commands(message))
                self.queued_commands.append(task)

    @tasks.loop(seconds=1/10)
    async def dequeue_commands(self):
        """A loop to process commands from the bot's guild members

        await dequeue_commands()

        This is a coroutine. This event is not called directly; rather the
        loop is initialized by calling dequeue_commands.start(). This loop
        serves to dequeue and process all commands that the bot has stored 
        from the users of its guilds. This is a First-In-First-Out process.
        """

        if len(self.unprocessed_commands) > 0:
            await self.unprocessed_commands.pop(0)

    @dequeue_commands.before_loop
    async def before_dequeue_commands(self):
        """An event fired once before the dequeue commands loop starts

        await before_dequeue_commands()
        
        This is a coroutine. This event is not called directly; it is fired before 
        the dequeue_commands loop starts. This is used to do any extraneous setup 
        before the bot initializes command processing.
        """

        await self.bot.wait_until_ready()
        print('Command Processing started')
