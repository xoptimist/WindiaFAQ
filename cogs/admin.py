from discord.ext import tasks, commands
import botcore
import traceback
import sys

class Admin(commands.Cog):
    """A cog to do admin errands such as loading/unloading other cogs
        
    Members
    -------
    bot: botcore.Bot
        The Discord Bot that the Cog is loaded into
    
    Methods
    -------
    async def reload_cog(self, ctx: commands.Context, cog: str):
        Attempts to reload a cog

    async def reload_cog(self, ctx: commands.Context, cog: str):
        Attempts to reload a cog

    async def load_cog(self, ctx: commands.Context, cog: str):
        Attempts to load a cog

    async def unload_cog(self, ctx: commands.Context, cog: str):
        Attempts to unload a cog

    async def logout(self, ctx: commands.Context):
        Attempts to logout of discord

    def cog_check(self, ctx: commands.Context):
        Checks if the user attempting to invoke any admin commands is the owner of the bot
    """

    def __init__(self, bot: botcore.Bot):
        """The constructor for the Admin cog
        
        Members
        -------
        bot: botcore.Bot
            The Discord Bot that the Cog is loaded into
        """

        self.bot: botcore.Bot = bot

    @commands.command(name='reload', hidden=True)
    async def reload_cog(self, ctx: commands.Context, cog: str):
        """Attempts to reload a cog
        
        await reload(ctx: discord.ext.commands.Context,
                         cog: str)

        This is a coroutine. This is not called directly; it is called whenever
        a user attempts to use the command `$reload`. If the cog_check passes,
        this command will attempt to reload the given cog. 

        Parameters
        ----------
        ctx: discord.ext.commands.Context
            The context of the command sent by the user

        cog: str
            The name of the cog being reloaded. This is the name of the Python
            file that the user is attempting to reload. It can either be in the
            form cogs.{file_name} or just {file_name}.
        """

        cog = (cog if cog.startswith('cogs.') else f'cogs.{cog}').lower()

        try:
            self.bot.reload_extension(cog)
            await ctx.send(f'{cog} reloaded succesfully.')
        except commands.ExtensionNotLoaded:
            await ctx.send(f'{cog} not loaded.')
        except commands.ExtensionAlreadyLoaded:
            await ctx.send(f'{cog} is already loaded.')
        except commands.ExtensionNotFound:
            await ctx.send(f'{cog} not found.')
        except commands.NoEntryPointError:
            await ctx.send(f'{cog} has no setup function.')

    @commands.command(name='load', hidden=True)
    async def load_cog(self, ctx: commands.Context, cog: str):
        """Attempts to load a cog
        
        await load(ctx: discord.ext.commands.Context,
                         cog: str)

        This is a coroutine. This is not called directly; it is called whenever
        a user attempts to use the command `$load`. If the cog_check passes,
        this command will attempt to load the given cog. 

        Parameters
        ----------
        ctx: discord.ext.commands.Context
            The context of the command sent by the user

        cog: str
            The name of the cog being loaded. This is the name of the Python
            file that the user is attempting to load. It can either be in the
            form cogs.{file_name} or just {file_name}.
        """

        cog = (cog if cog.startswith('cogs.') else f'cogs.{cog}').lower()

        try:
            self.bot.load_extension(cog)
            await ctx.send(f'{cog} loaded successfully.')
        except commands.ExtensionAlreadyLoaded:
            await ctx.send(f'{cog} is already loaded.')
        except commands.ExtensionNotFound:
            await ctx.send(f'{cog} not found.')
        except commands.NoEntryPointError:
            await ctx.send(f'{cog} has no setup function.')

    @commands.command(name='unload', hidden=True)
    async def unload_cog(self, ctx: commands.Context, cog: str):
        """Attempts to unload a cog
        
        await unload_cog(ctx: discord.ext.commands.Context,
                         cog: str)

        This is a coroutine. This is not called directly; it is called whenever
        a user attempts to use the command `$unload`. If the cog_check passes,
        this command will attempt to unload the given cog. 

        Parameters
        ----------
        ctx: discord.ext.commands.Context
            The context of the command sent by the user

        cog: str
            The name of the cog being unloaded. This is the name of the Python
            file that the user is attempting to unload. It can either be in the
            form cogs.{file_name} or just {file_name}.
        """

        cog = (cog if cog.startswith('cogs.') else f'cogs.{cog}').lower()

        try:
            self.bot.unload_extension(cog)
            await ctx.send(f'{cog} unloaded successfully.')
        except commands.ExtensionNotLoaded:
            await ctx.send(f'{cog} not loaded.')

    @commands.command(name='logout', hidden=True)
    async def logout(self, ctx: commands.Context):
        """Attempts to logout of discord
        
        await logout(ctx: discord.ext.commands.Context)

        This is a coroutine. This is not called directly; it is called whenever
        a user attempts to use the `$logout` command. If this command passes the
        cog check, the bot will log out.

        Parameters
        ----------
        ctx: discord.ext.commands.Context
            The context in which the command was sent
        """

        await ctx.send('Goodbye!')
        await self.bot.logout()
        sys.exit(0)

    def cog_check(self, ctx: commands.Context):
        """Checks if the user attempting to invoke any admin commands is the owner of the bot
        
        cog_check(ctx: discord.ext.commands.Context)
        
        This event is not called directly; it is called whenever a user 
        attempts to invoke an admin command. If the user attempting to
        invoke the command is the owner of the bot, then the check passes
        and the command will be processed, else it will be ignored.
        
        Parameters
        ----------
        ctx: discord.ext.commands.Context
            The context of the command being sent
        """

        return self.bot.is_owner(ctx.author)

def setup(bot):
    """Adds the cog to the Discord Bot
    
    This is not called directly; it is called when the Bot
    called the load_extension function on a cog file path.
    """

    bot.add_cog(Admin(bot))