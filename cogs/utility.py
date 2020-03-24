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

    @commands.command(name='id', description='Displays your Discord ID to link to Windia')
    async def id_command(self, ctx: commands.Context, member: discord.Member = None):
        """Tells a user their Discord ID
        
        await id_command(ctx: discord.ext.commands.Context[, *, member: discord.Member = None])
        
        This is a coroutine. This is not directly called; it is called whenever
        a user uses the `$id` command. If a member (usually a user mention) follows
        the command, it will post the mentioned user's Discord ID, else it will post
        the user invoking the command's Discord ID.
        """

        member = member or ctx.author
        
        id = member.id
        mention = member.mention

        return await ctx.send(f'{mention}, your Discord ID is `{id}`\nType `@discord` in game and then enter this ID into the text box to link your in-game account to your Discord account.')

    @commands.command(name='online', description='Displays the online count')
    async def online_command(self, ctx: commands.Context):
        """Displays the online count for Windia
        
        await online_command(ctx: discord.ext.commands.Context)
        
        This is a coroutine. This is not directly called; it is called whenever
        a user uses the `$online` command. This function displays the Windia
        online count by obtaining it from Windia Bot's status.
        """

        if isinstance(ctx.guild, discord.DMChannel):
            return await ctx.send('This command may only be used in the Windia Discord.')

        if (windia_bot := ctx.guild.get_member(614221348780113920)):
            activity = windia_bot.activity
            online_count = int(activity.description.split(' ')[3])
            if online_count < 4: return await ctx.send(f'The server is currently **offline**.')
            else: return await ctx.send(f'The server is currently **online** with {online_count} players.')
        else:
            return await ctx.send('I am currently unable to get the online count, sorry!')


def setup(bot):
    """Adds the cog to the Discord Bot
    
    This is not called directly; it is called when the Bot
    called the load_extension function on a cog file path.
    """

    bot.add_cog(Utility(bot))