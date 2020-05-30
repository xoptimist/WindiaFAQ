import os

from discord.ext import commands

import botcore


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

    @commands.command(
        name='reload',
        usage='`cog: str`',
        description='Reloads a cog',
        hidden=True
    )
    async def reload_cog(self, ctx: commands.Context, cog: str):
        cog = (cog if cog.startswith('cogs.') else f'cogs.{cog}').lower()

        try:
            self.bot.reload_extension(cog)
            return await ctx.send(f'{cog} reloaded successfully.')
        except commands.ExtensionNotLoaded:
            return await ctx.send(f'{cog} not loaded.')
        except commands.ExtensionAlreadyLoaded:
            return await ctx.send(f'{cog} is already loaded.')
        except commands.ExtensionNotFound:
            return await ctx.send(f'{cog} not found.')
        except commands.NoEntryPointError:
            return await ctx.send(f'{cog} has no setup function.')

    @commands.command(
        name='load',
        usage='`cog: str`',
        description='Loads a cog',
        hidden=True
    )
    async def load(self, ctx: commands.Context, cog: str):
        cog = (cog if cog.startswith('cogs.') else f'cogs.{cog}').lower()

        try:
            self.bot.load_extension(cog)
            return await ctx.send(f'{cog} loaded successfully.')
        except commands.ExtensionAlreadyLoaded:
            return await ctx.send(f'{cog} is already loaded.')
        except commands.ExtensionNotFound:
            return await ctx.send(f'{cog} not found.')
        except commands.NoEntryPointError:
            return await ctx.send(f'{cog} has no setup function.')

    @commands.command(
        name='unload',
        usage='`cog: str`',
        description='Unloads a cog',
        hidden=True
    )
    async def unload(self, ctx: commands.Context, cog: str):
        cog = (cog if cog.startswith('cogs.') else f'cogs.{cog}').lower()

        try:
            self.bot.unload_extension(cog)
            return await ctx.send(f'{cog} unloaded successfully.')
        except commands.ExtensionNotLoaded:
            return await ctx.send(f'{cog} not loaded.')

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

    @commands.command(name='pull', hidden=True)
    async def update_bot(self, ctx):
        """Updates the bot"""
        await ctx.send('Updating')
        os.system('git pull')


def setup(bot):
    """Adds the cog to the Discord Bot
    
    This is not called directly; it is called when the Bot
    called the load_extension function on a cog file path.
    """

    bot.add_cog(Admin(bot))
