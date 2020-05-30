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

        if await windiautils.create_command(command.lower(), description):
            return await ctx.send(f'{command} was added successfully.')
        else:
            return await ctx.send(f'{command} already exists.')


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

        if await windiautils.update_command(command.lower(), description):
            return await ctx.send(f'{command} was updated successfully.')
        else:
            return await ctx.send(f'{command} does not exist.')

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

        if (existing := await windiautils.get_command(command.lower())) and not windiautils.get_command(alias.lower()):
            await windiautils.create_command(alias.lower(), existing)
            return await ctx.send(f'The alias {alias} has been added to {command}.')

        else:
            if not existing:
                return await ctx.send(f'{command} is not a command.')
            else:
                return await ctx.send(f'{alias} is already a command.')

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

        if await windiautils.delete_command(command.lower()):
            return await ctx.send(f'{command} was removed.')
        else:
            return await ctx.send(f'{command} is not a command.')

    async def cog_before_invoke(self, ctx):
        """"""

        if not await windiautils.database_exists():
            await windiautils.create_database()

    async def cog_check(self, ctx: commands.Context):
        """Checks if the user attempting to invoke an admin command has the manage_message permission

        Checks if the author has manage messages permission, which is enough to invoke
        the CRUD commands for FAQ commands

        Parameters
        ----------
        ctx: discord.ext.commands.Context
            The context of the message sent by the user received by the bot
        """

        return ctx.channel.permissions_for(ctx.author).manage_messages

    @commands.Cog.listener('on_message')
    async def faq_check(self, message: discord.Message):
        """Check if the user is trying to invoke an faq_command

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

            if (output := await windiautils.get_command(command.lower())) and await windiautils.database_exists():
                if not guild:
                    # means the command was invoked in a DM channel
                    return await windiautils.send_embed(
                        title=command,
                        description=output,
                        messageable=author,
                        author=author
                    )

                bot_channel_id = await self.bot.config.aiogetint('Bot', 'Channel')
                if bot_channel := guild.get_channel(bot_channel_id):
                    if not any((channel.id == bot_channel.id, bot_channel.permissions_for(author).manage_messages)):
                        # the command was attempted to be invoked by a non-mod in some channel besides the bot channel
                        raise commands.CheckFailure(message='You do not have permission to invoke the FAQ command here.')

                return await windiautils.send_embed(
                    title=command,
                    description=output,
                    messageable=channel,
                    author=author
                )


def setup(bot):
    bot.add_cog(FAQ(bot))
