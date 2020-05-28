import re
from typing import Tuple

import discord.utils
from discord.ext import commands

import windiautils


class Bot(commands.Bot):
    """The Windia FAQ Bot base
    Inherits from discord.ext.commands.Bot

    Members
    -------
    queued_commands
        A list of commands queued by the bot to process and output to the user
    
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

        self.config = windiautils.Config.getInstance()
        super().__init__(command_prefix, help_command=None)

    async def on_ready(self):
        """Alerts the user that the bot is initialized
        
        await on_ready()

        This is a coroutine. This is not called directly; it is fired whenever the
        bot is logged into Discord and is ready for use."""

        print(f'{self.user.name} connected.')

    async def on_message(self, message: discord.Message):
        """An event thrown when a user sends a message in the bot's guilds, used for command handling.

        await on_message(message: discord.Message)

        This is a coroutine. This is not called directly; it is fired whenever the 
        Bot receives a message. This is used for attempting to parse the message 
        for a command. If the message is sent by a bot, it is ignored. If the message 
        begins with the command prefix, it is then tested for membership in the bot's 
        stored commands. If it passes, then the message is processed by a bot as a
        command.
        
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
                await self.process_commands(message)

    async def log(self, event: str, *messages: Tuple[str, str]):
        logging_channel_id = await self.config.aiogetint('Logging', 'Channel')
        if channel := self.get_channel(logging_channel_id):
            embed = discord.Embed(title=event, description='', color=discord.Color.purple())

            for name, value in messages:
                embed.add_field(name=name, value=value)

            return await channel.send(embed=embed)
        else:
            print()
            print('----------------------------------')
            print(event)

            for name, value in messages:
                print(f'{name}: {value}')

            print('----------------------------------')

    async def send_embed(self, title: str, description: str, messageable: discord.abc.Messageable, author: discord.Member, fields: Tuple[Tuple[str, str]] = tuple()):
        embed = discord.Embed(title=title, description=description, color=discord.Color.purple())
        embed.set_author(name=f'{author}', icon_url=author.avatar_url)
        embed.set_footer(text='Send FAQ suggestions to your nearest staff member and everything else to thewallacems '
                              'on GitHub :)')

        # embed any first image url found in the description
        if match := re.match(r'(https[^\s]+\.(jpe?g|png))', description):
            embed.set_image(url=match.group(0))

        for name, value in fields:
            embed.add_field(name=name, value=value)

        return await messageable.send(embed=embed)
