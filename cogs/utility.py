from discord.ext import tasks, commands
import discord
import botcore

class Utility(commands.Cog):
    """A cog for various utilites to help out users
        
    Members
    -------
    bot: botcore.Bot
        The Discord Bot that the Cog is loaded into
    
    Methods
    -------
    async def get_id(ctx: discord.ext.commands.Context[, *, member: discord.Member = None])
        Tells a user their Discord ID
    """

    def __init__(self, bot: botcore.Bot):
        """The constructor for the Utility cog
        
        Members
        -------
        bot: botcore.Bot
            The Discord Bot that the Cog is loaded into
        """

        self.bot: botcore.Bot = bot

    @commands.command(name='id', description='Gets the user\'s Discord ID')
    async def get_id(self, ctx: commands.Context, member: discord.Member = None):
        """Tells a user their Discord ID
        
        await get_id(ctx: discord.ext.commands.Context[, *, member: discord.Member = None])
        
        This is a coroutine. This is not directly called; it is called whenever
        a user uses the `$id` command. If a member (usually a user mention) follows
        the command, it will post the mentioned user's Discord ID, else it will post
        the user invoking the command's Discord ID.
        """
        
        id = member.id if member else ctx.author.id
        mention = member.mention if member else ctx.author.mention

        await ctx.send(f'{mention}, your Discord ID is `{id}`\nType `@discord` in game and then enter this ID into the text box to link your in-game account to your Discord account.')

def setup(bot):
    """Adds the cog to the Discord Bot
    
    This is not called directly; it is called when the Bot
    called the load_extension function on a cog file path.
    """

    bot.add_cog(Utility(bot))