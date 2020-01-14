from discord.ext import tasks, commands
import discord
import botcore

class Utility(commands.Cog):
    """A cog for various utilites to help out users"""

    def __init__(self, bot):
        self.bot: botcore.Bot = bot

    @commands.command(name='id', description='Gets the user\'s Discord ID')
    async def get_id(self, ctx: commands.Context, *, member: discord.Member = None):
        """Gets the user's Discord ID"""
        
        id = member.id if member else ctx.user.id
        mention = member.mention if member else ctx.user.mention

        await ctx.send(f'{mention}, your Discord ID is `{id}`\nType `@discord` in game and then enter this ID into the text box to link your in-game account to your Discord account.')

def setup(bot):
    bot.add_cog(Utility(bot))