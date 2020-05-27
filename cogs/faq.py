import discord
from discord.ext import commands

import botcore
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

    @commands.command(
        name='add',
        description='Adds a new FAQ command',
        usage='`FAQ command: string` `description: string`',
        hidden=True
    )
    async def add_command(self, ctx: commands.Context, command: str, *, description: str):
        """Attempts to add a new FAQ command
        
        await update_command(ctx: commands.context[, command: str = None, description: str = None])

        This is a coroutine. This is not called directly; it is called whenever
        the Bot receives the command `$add` from a user. This command attempts
        to add the given FAQ command with the given description.

        Parameters
        ----------
        ctx: discord.ext.commands.Context
            The context of the message sent by the user

        command: str = None
            The FAQ command to be added

        description: str = None
            The description for the given FAQ command
        """

        if command in self.faq_commands or self.bot.get_command(command):
            return await ctx.send(f'{command} is already a registered command.')

        self.faq_commands[command.lower()] = description
        windiautils.save_commands(self.faq_commands)
        return await ctx.send(f'{command} was added.')

    @commands.command(
        name='update',
        description='Updates a FAQ command',
        usage='`FAQ command: string` `new description: string`',
        hidden=True
    )
    async def update_command(self, ctx: commands.Context, command: str, *, description: str):
        """Attempts to update an existing FAQ command
        
        await update_command(ctx: commands.context[, command: str = None, description: str = None])

        This is a coroutine. This is not called directly; it is called whenever
        the Bot receives the command `$update` from a user. This command attempts
        to update the given FAQ command with the given description.

        Parameters
        ----------
        ctx: discord.ext.commands.Context
            The context of the message sent by the user

        command: str = None
            The FAQ command to be updated

        description: str = None
            The new description for the given FAQ command
        """

        if command not in self.faq_commands:
            return await ctx.send(f'{command} is not a registered command.')

        self.faq_commands[command.lower()] = description
        windiautils.save_commands(self.faq_commands)
        return await ctx.send(f'{command} was updated.')

    @commands.command(
        name='alias',
        description='Aliases a FAQ command',
        usage='`FAQ command: string` `alias: string`',
        hidden=True
    )
    async def alias_command(self, ctx: commands.Context, command: str, alias: str):
        """Attempts to alias an existing FAQ command
        
        await update_command(ctx: commands.context[, command: str = None, alias: str = None])

        This is a coroutine. This is not called directly; it is called whenever
        the Bot receives the command `$alias` from a user. This command attempts
        to alias the given FAQ command with the given alias.

        Parameters
        ----------
        ctx: discord.ext.commands.Context
            The context of the message sent by the user

        command: str = None
            The FAQ command to be updated

        alias: str = None
            The new alias for the given FAQ command
        """

        if command not in self.faq_commands:
            return await ctx.send(f'{command} is not a registered command.')
        elif alias in self.faq_commands:
            return await ctx.send(f'{alias} is already a registered command.')

        self.faq_commands[alias.lower()] = self.faq_commands[command]
        windiautils.save_commands(self.faq_commands)
        return await ctx.send(f'The alias {alias} has been added to {command}.')

    @commands.command(
        name='remove',
        description='Removes a FAQ command',
        usage='`FAQ command: string`',
        hidden=True
    )
    async def remove_command(self, ctx: commands.Context, command: str):
        """Attempts to remove an existing FAQ command
        
        await remove_command(ctx: commands.context[, command: str = None])

        This is a coroutine. This is not called directly; it is called whenever
        the Bot receives the command `$remove` from a user. This command attempts
        to remove the given FAQ command.

        Parameters
        ----------
        ctx: discord.ext.commands.Context
            The context of the message sent by the user

        command: str
            The FAQ command to be removed
        """

        if command not in self.faq_commands:
            return await ctx.send(f'{command} is not a registered command.')

        self.faq_commands.pop(command)
        windiautils.save_commands(self.faq_commands)
        return await ctx.send(f'{command} was removed.')

    def cog_check(self, ctx: commands.Context):
        """Checks if the user attempting to invoke an admin command has the manage_message permission
        
        self.cog_check(ctx: discord.ext.commands.Context)
        
        This is a coroutine. This is not called directly; it is called whenever
        a Cog command is sent by a user. This checks if the user sending any commands
        in this cog has the manage_messages permissions. If this fails, then
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
6        
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
            if self.bot.get_command(command):
                # this means it's a bot command, not a faq command
                return

            channel = message.channel
            guild = message.guild
            author = message.author

            if not guild:
                return await windiautils.process_faq_command(command, author, author)

            elif not (bot_channel := guild.get_channel(708715939486498937)):
                return await windiautils.process_faq_command(command, channel, author)

            if not any((channel.id == bot_channel.id, bot_channel.permissions_for(author).manage_messages)):
                # the command was attempted to be invoked by a non-mod in some channel besides the bot channel
                return await channel.send(f'Please use this command in the bot channel, {author.mention}.',
                                          delete_after=5.0)

            return await windiautils.process_faq_command(command, channel, author)


def setup(bot):
    """Adds the cog to the Discord Bot
    
    This is not called directly; it is called when the Bot
    called the load_extension function on a cog file path.
    """

    bot.add_cog(FAQ(bot))
