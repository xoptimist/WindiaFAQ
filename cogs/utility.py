import re
from datetime import datetime

import discord
import discord.utils
from discord.ext import commands

import botcore
import windiautils


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

    @commands.command(
        name='id',
        description='Displays your Discord ID to link to Windia',
        usage=f'`optional user mention: ping`'
    )
    async def id_command(self, ctx: commands.Context, member: discord.Member = None):
        """Tells a user their Discord ID
        
        await id_command(ctx: discord.ext.commands.Context[, *, member: discord.Member = None])
        
        This is a coroutine. This is not directly called; it is called whenever
        a user uses the `$id` command. If a member (usually a user mention) follows
        the command, it will post the mentioned user's Discord ID, else it will post
        the user invoking the command's Discord ID.
        """

        member = member or ctx.author
        messageable = ctx.channel or ctx.author

        return await windiautils.send_embed(
            title=f'{member.display_name}\'s Discord ID: {member.id}',
            description=f'Type `@discord` in game and then enter this ID into the text box '
                        f'to link your in-game account to your Discord account.',
            messageable=messageable,
            author=ctx.author
        )

    @commands.command(
        name='online',
        description='Displays the online count',
        usage=''
    )
    async def online_command(self, ctx: commands.Context):
        """Displays the online count for Windia
        
        await online_command(ctx: discord.ext.commands.Context)
        
        This is a coroutine. This is not directly called; it is called whenever
        a user uses the `$online` command. This function displays the Windia
        online count by obtaining it from Windia Bot's status.
        """

        if isinstance(ctx.guild, discord.DMChannel):
            return await ctx.send('This command may only be used in the Windia Discord.')

        message = 'I am currently unable to get the online count, sorry!'

        if windia_bot := ctx.guild.get_member(614221348780113920):
            activity = windia_bot.activity
            online_count = int(activity.name.split(' ')[3])
            if online_count < 4:
                message = f'The server is currently **offline**.'
            else:
                message = f'The server is currently **online** with {online_count} players.'

        return await windiautils.send_embed(
            title=message,
            description='',
            messageable=ctx.channel,
            author=ctx.author
        )

    # REMINDER: Check the flags repo
    @commands.command(
        name='magic',
        description='Shows how much magic needed to one shot a monster',
        usage='`monster hp: integer` `spell attack: integer` `args: -[alsed]`'
    )
    async def magic_command(self, ctx, hp: int = None, spellatk: int = None, *, args = None):
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

            return await windiautils.send_embed(
                title='Magic Usage',
                description=message,
                messageable=ctx.channel or ctx.author,
                author=ctx.author
            )

        modifiers_msg = f'Spell Attack: {spellatk}\n'
        modifier = 1.0 * spellatk

        if args:
            if re.search(r'-[^ls]*[ls][^ls]*', args):  # loveless or elemental staff
                modifier *= 1.25
                modifiers_msg += f'Staff Multiplier: 1.25x\n'
            if re.search(r'-[^e]*e[^e]*', args):  # elemental advantage
                modifier *= 1.50
                modifiers_msg += f'Elemental Advantage: 1.50x\n'
            elif re.search(r'-[^d]*d[^d]*', args):  # elemental disadvantage
                modifier *= 0.50
                modifiers_msg += f'Elemental Disadvantage: 0.50x\n'

        magic_msg = ''

        if args and re.search(r'-[^a]*a[^a]*', args):  # elemental amp
            modifiers_msg += f'BW Elemental Amp: 1.30x\n'
            modifiers_msg += f'FP/IL Elemental Amp: 1.40x\n\n'

            # F/P and I/L
            fpil_magic = windiautils.calc_magic(monster_hp=hp, modifier=modifier*1.4)
            magic_msg += f'Magic for F/P or I/L: {fpil_magic}\n'

            # BW
            bw_magic = windiautils.calc_magic(monster_hp=hp, modifier=modifier*1.3)
            magic_msg += f'Magic for BW: {bw_magic}'
        else:
            magic = windiautils.calc_magic(monster_hp=hp, modifier=modifier)
            magic_msg += f'\nMagic: {magic}'

        return await windiautils.send_embed(
            title='Magic Calculator',
            description=f'The Magic required to one-hit a monster with {hp} HP',
            messageable=ctx.channel or ctx.author,
            author=ctx.author,
            fields=(('Modifiers', modifiers_msg),
                    ('Magic Required', magic_msg))
        )

    @commands.command(
        name='time',
        description='Displays the server time',
        usage=''
    )
    async def time_command(self, ctx):
        fmt_time = datetime.utcnow().strftime('%H:%M:%S, %d %b, %Y')
        return await windiautils.send_embed(
            title=f'The server\'s current time is {fmt_time} UTC-0.',
            description='',
            messageable=ctx.channel or ctx.author,
            author=ctx.author
        )

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
