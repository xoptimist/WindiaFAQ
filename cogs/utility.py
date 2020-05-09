from discord.ext import tasks, commands
from datetime import datetime
from sympy.solvers import solve
from sympy import Symbol
import discord
import discord.utils
import botcore
import math
import re

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

    @commands.command(name='id', description='Displays your Discord ID to link to Windia', usage=f'id [<user mention>]')
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
            online_count = int(activity.name.split(' ')[3])
            if online_count < 4: return await ctx.send(f'The server is currently **offline**.')
            else: return await ctx.send(f'The server is currently **online** with {online_count} players.')
        else:
            return await ctx.send('I am currently unable to get the online count, sorry!')
            

    # REMINDER: Check the flags repo
    @commands.command(name='magic', description='Shows how much magic needed to one shot a monster')
    async def magic_command(self, ctx, hp=None, spellatk=None, *, args=None):
        if not hp and not spellatk and not args:
            message = (
                f'Usage: {self.bot.command_prefix}{ctx.invoked_with} <hp> <spell attack> <args>\n'
                f'Args:\n'
                f'\t-a: Elemental Amplification\n'
                f'\t-l: Loveless Staff\n'
                f'\t-s: Elemental Staff\n'
                f'\t-e: Elemental Advantage\n'
                f'\t-d: Elemental Disadvantage\n\n'
                f'Example Usage: {self.bot.command_prefix}magic 43376970 570 -asle'
            )

            return await ctx.send(message)
        
        if not hp:
            return await ctx.send(f'Please enter an amount of HP.\nEX: {self.bot.command_prefix}magic 32000000 <spell attack> <args>')
        elif not spellatk:
            return await ctx.send(f'Please enter an amount of Spell Attack.\nEX: {self.bot.command_prefix}magic <hp> 570 <args>')
        else:
            try:
                hp = int(hp)
                spellatk = int(spellatk)
            except:
                return await ctx.send(f'HP and Spell Attack values must be an integer.')

        message = (
            f'```\n'
            f'Spell Attack: {spellatk}\n'
        )

        staff = 1.0
        elemental = 1.0
        mastery = 0.6

        if args:
            if re.search(r'-[^l]*(l|s)[^l]*', args):# loveless or elemental staff
                staff = 1.25
                message += f'Staff Multiplier: {staff}x\n'
            if re.search(r'-[^e]*e[^e]*', args):    # elemental advantage
                elemental = 1.5
                message += f'Elemental Advantage: {elemental}x\n'
            elif re.search(r'-[^d]*d[^d]*', args):  # elemental disadvantage
                elemental = 0.5
                message += f'Elemental Disadvantage: {elemental}x\n'
        
        x = Symbol('x')

        if args and re.search(r'-[^a]*a[^a]*', args):    # elemental amp
            message += f'BW Elemental Amp: 1.3x\n'
            message += f'FP/IL Elemental Amp: 1.4x\n\n'

            # F/P and I/L
            amp = 1.4
            solution = solve(((((((((x**2)/1000.0 + x *mastery *0.9)/30.0 + x/200.0)) *spellatk) *amp) *staff) *elemental)/hp - 1.0, x)
            fpil_magic = min([math.ceil(num) for num in solution if num >= 0.0])
            message += f'Magic for F/P or I/L: {fpil_magic}\n'

            # BW
            amp = 1.3
            solution = solve(((((((((x**2)/1000.0 + x *mastery *0.9)/30.0 + x/200.0)) *spellatk) *amp) *staff) *elemental)/hp - 1.0, x)
            bw_magic = min([math.ceil(num) for num in solution if num >= 0.0])
            message += f'Magic for BW: {bw_magic}```'
        else:
            solution = solve((((((((x**2)/1000.0 + x *mastery *0.9)/30.0 + x/200.0)) *spellatk) *staff) *elemental)/hp - 1.0, x)
            magic = min([math.ceil(num) for num in solution if num >= 0.0])
            message += f'\nMagic: {magic}```'

        return await ctx.send(message)

    @commands.command(name='time', description='Displays the server time')
    async def time_command(self, ctx):
        fmt_time = datetime.utcnow().strftime('%H:%M:%S, %d %b, %Y')
        return await ctx.send(f'The server\'s current time is {fmt_time} UTC-0.')

    def cog_check(self, ctx):
        if ctx.guild and (bot_channel := ctx.guild.get_channel(708715939486498937)):
            return ctx.channel.id == bot_channel.id or ctx.channel.permissions_for(ctx.author).manage_messages
        return True

def setup(bot):
    """Adds the cog to the Discord Bot
    
    This is not called directly; it is called when the Bot
    called the load_extension function on a cog file path.
    """

    bot.add_cog(Utility(bot))