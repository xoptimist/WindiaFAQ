from discord.ext import tasks, commands
import botcore

class Admin(commands.Cog):
    """A cog to do admin errands such as loading/unloading other cogs"""

    def __init__(self, bot):
        self.bot: botcore.Bot = bot

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def reload_cog(self, ctx: commands.Context, cog: str):
        """Attempts to reload a cog"""

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
    @commands.is_owner()
    async def load_cog(self, ctx: commands.Context, cog: str):
        """Attempts to load a cog"""

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
    @commands.is_owner()
    async def unload_cog(self, ctx: commands.Context, cog: str):
        """Attempts to unload a cog"""

        cog = (cog if cog.startswith('cogs.') else f'cogs.{cog}').lower()

        try:
            self.bot.unload_extension(cog)
            await ctx.send(f'{cog} unloaded successfully.')
        except commands.ExtensionNotLoaded:
            await ctx.send(f'{cog} not loaded.')

def setup(bot):
    bot.add_cog(Admin(bot))