from discord.ext import tasks, commands
import asyncio
import botcore
import discord
import difflib
import json
import os.path
import windiautils

class FAQ(commands.Cog):
    """A cog used for the Windia FAQ and managing the Windia FAQ
        
    Members
    -------
    bot: botcore.Bot
        The Discord Bot that the Cog is loaded into

    faq_commands: dict
        A dictionary of frequently asked questions and their descriptions
    
    Methods
    -------
    async def add_command(ctx: discord.ext.commands.Context[, command: str = None, *, description: str = None])
        Attempts to add a new FAQ command

    async def update_command(ctx: discord.ext.commands.Context[, command: str = None, *, description: str = None])
        Attempts to update an existing FAQ command

    async def remove_command(ctx: discord.ext.commands.Context[, command: str = None])
        Attempts to remove an existing FAQ command

    def cog_check(ctx: commands.Context)
        Checks if the user attempting to invoke an admin command has the manage_message permission

    async def faq_check(self, message: discord.Message)
        Check if the user is trying to invoke an faq_command
    """

    def __init__(self, bot: botcore.Bot):
        """The constructor for the FAQ cog
        
        Members
        -------
        bot: botcore.Bot
            The Discord Bot that the Cog is loaded into

        faq_commands: dict
            A dictionary of frequently asked questions and their descriptions
        """

        self.bot: botcore.Bot = bot
        self.faq_commands: dict = windiautils.load_commands()

    @commands.command(name='add', hidden=True)
    async def add_command(self, ctx: commands.Context, command: str = None, *, description: str = None):
        """Attempts to add a new FAQ command
        
        await update_command(ctx: commands.context[, command: str = None, description: str = None])

        This is a coroutine. This is not called directly; it is called whenever
        the Bot receives the command `$add` from a user. This command attempts
        to add the given FAQ command with the given description.

        Parameters
        ----------
        ctx: discord.ext.commands.Context
            The context of the message sent by the user

        [command: str = None]
            The FAQ command to be added

        [description: str = None]
            The description for the given FAQ command
        """

        if not command:
            await ctx.send('Please enter a command to add.')
        elif not description:
            await ctx.send('Please enter a description for the command.')
        elif command in self.faq_commands:
            await ctx.send(f'{command} is already a registered command.')
        else:
            self.faq_commands[command.lower()] = description
            windiautils.save_commands(self.faq_commands)
            await ctx.send(f'{command} was added.')

    @commands.command(name='update', hidden=True)
    async def update_command(self, ctx: commands.Context, command: str = None, *, description: str = None):
        """Attempts to update an existing FAQ command
        
        await update_command(ctx: commands.context[, command: str = None, description: str = None])

        This is a coroutine. This is not called directly; it is called whenever
        the Bot receives the command `$update` from a user. This command attempts
        to update the given FAQ command with the given description.

        Parameters
        ----------
        ctx: discord.ext.commands.Context
            The context of the message sent by the user

        [command: str = None]
            The FAQ command to be updated

        [description: str = None]
            The new description for the given FAQ command
        """

        if not command:
            await ctx.send('Please enter a command to update.')
        elif not command in self.faq_commands:
            await ctx.send(f'{command} is not a registered command.')
        elif not description:
            await ctx.send('Please enter a description for the command.')
        else:
            self.faq_commands[command.lower()] = description
            windiautils.save_commands(self.faq_commands)
            await ctx.send(f'{command} was updated.')

    @commands.command(name='remove', hidden=True)
    async def remove_command(self, ctx: commands.Context, command: str = None):
        """Attempts to remove an existing FAQ command
        
        await remove_command(ctx: commands.context[, command: str = None])

        This is a coroutine. This is not called directly; it is called whenever
        the Bot receives the command `$remove` from a user. This command attempts
        to remove the given FAQ command.

        Parameters
        ----------
        ctx: discord.ext.commands.Context
            The context of the message sent by the user

        [command: str = None]
            The FAQ command to be removed
        """

        if not command:
            await ctx.send('Please enter a command to remove.')
        elif not command in self.faq_commands:
            await ctx.send(f'{command} is not a registered command.')
        else:
            self.faq_commands.pop(command)
            windiautils.save_commands(self.faq_commands)
            await ctx.send(f'{command} was removed.')

    def cog_check(self, ctx: commands.Context):
        """Checks if the user attempting to invoke an admin command has the manage_message permission
        
        cog_check(ctx: discord.ext.commands.Context)
        
        This is a coroutine. This is not called directly; it is called whenever
        a Cog command is sent by a user. This checks if the user sending the
        command has the manage_messages permissions. If this fails, then
        the command is not processed.

        Parameters
        ----------
        ctx: discord.ext.commands.Context
            The context of the message sent by the user received by the bot
        """

        return ctx.channel.permissions_for(ctx.author).manage_messages

    @commands.Cog.listener('on_message')
    async def faq_check(self, message: discord.Message):
        """Check if the user is trying to invoke an faq_command
        
        await faq_check(message: discord.Message)

        This is a coroutine. This is not called directly. This event is
        a listener for the Bot's on_message event and is called whenever
        the on_message event is called. This event checks if the
        user is attempting to call any command listed in the faq_commands
        dictionary and sends the FAQ description of that command to the
        context channel.

        FAQ commands are not handled like normal commands; rather they are
        just manually parsed through the message's content by checking
        if the message starts with the bot's command prefix and followed
        by a FAQ command name.

        Parameters
        ----------
        message: discord.Message
            The message object sent by the user to parse for a FAQ command
        """

        if message.content.startswith(self.bot.command_prefix):
            raw_command = message.content.lower()[1::].split(' ')
            command = raw_command[0]

            if command in self.faq_commands:
                await message.channel.send(self.faq_commands[command])
            elif command not in self.faq_commands and not self.bot.get_command(command):
                closest_commands = await self.get_closest_commands(command)
                if len(closest_commands) > 0:
                    description = '\n'.join([ f'**{command}**' for command in closest_commands ])
                    embed = discord.Embed(
                        title='Did you mean...',
                        description=description,
                        colour=discord.Color.purple())

                    await message.channel.send(embed=embed)

    async def get_closest_commands(self, cmd: str):
        all_commands = list(self.faq_commands.keys()) + [ command.name for command in list(self.bot.commands) ]
        closest_commands = []

        async def iter_commands():
            for command in all_commands:
                if difflib.SequenceMatcher(None, cmd, command).ratio() >= 0.8:
                    closest_commands.append(command)
        
        future = asyncio.ensure_future(iter_commands())
        await asyncio.wait([future], return_when=asyncio.ALL_COMPLETED)

        return closest_commands

def setup(bot):
    """Adds the cog to the Discord Bot
    
    This is not called directly; it is called when the Bot
    called the load_extension function on a cog file path.
    """

    bot.add_cog(FAQ(bot))