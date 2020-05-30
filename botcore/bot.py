from typing import Tuple

import discord.utils
from discord.ext import commands

import windiautils


class Bot(commands.Bot):
    __slots__ = ['config']

    def __init__(self, command_prefix: str):
        self.config = windiautils.Config.getInstance()
        super().__init__(command_prefix, help_command=None)

    async def on_ready(self):
        """Alerts the user that the bot is initialized
        
        await on_ready()

        This is a coroutine. This is not called directly; it is fired whenever the
        bot is logged into Discord and is ready for use."""

        print(f'{self.user.name} connected.')

        activity = discord.Activity(name='WindiaMS <3', type=discord.ActivityType.watching)
        await self.change_presence(activity=activity)

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
            return await windiautils.send_embed(
                title=event,
                description='',
                messageable=channel,
                author=self.user,
                fields=messages
            )
        else:
            print()
            print('----------------------------------')
            print(event)

            for name, value in messages:
                print(f'{name}: {value}')

            print('----------------------------------')
