from discord.ext import tasks, commands
import botcore
import discord
import windiautils

class Help(commands.Cog):
    """A cog used for the Help command
        
    Members
    -------
    bot: botcore.Bot
        The Discord Bot that the Cog is loaded into
    
    Methods
    -------
    async def help_command(ctx: discord.ext.commands.Context)
        DMs the user invoking the command the list of commands
    """

    def __init__(self, bot: botcore.Bot):
        """The constructor for the Help cog
        
        Members
        -------
        bot: botcore.Bot
            The Discord Bot that the Cog is loaded into
        """

        self.bot: botcore.Bot = bot

    @commands.command(name='help', hidden=True)
    async def help_command(self, ctx: commands.Context):
        """DMs the user invoking the command the list of commands
        
        await help(ctx: discord.ext.commands.Context)
        
        This is a coroutine. This is not called directly; it is called whenever
        a user uses the `$help` command. This will collect a list of all Bot commands
        and FAQ commands and output a list of their names into the user's DM
        channel.
        
        Parameters
        ----------
        ctx: discord.ext.commands.Context
            The context of the command sent by the user
        """
        
        messages = list()

        help = '''```Here is our list of commands

        Utility Commands
        ----------------
        '''

        for command in self.bot.walk_commands():
            # Don't show users the hidden commands
            if command.hidden:
                continue

            # Check for a number below 2000 so the message doesn't go over 2000 characters
            if len(help) > 1900:
                messages.append(help)
                help = '\n'
                
            help += f'{command.name} - {command.description}\n'

        help += '''
        FAQ Commands
        ------------
        '''

        for command, _ in windiautils.load_commands():
            if len(help) > 1900:
                messages.append(help)
                help = '\n'
                
            help += f'{command}\n'

        help += '```'

        messages.append(help)

        for message in messages:
            try:
                await ctx.author.send(message)
                return await ctx.send('I have DMed you a list of commands.', delete_after=5.0)
            except discord.Forbidden:
                return await ctx.send('I could not DM you a list of commands since you are not accepting DMs from me.')

def setup(bot):
    """Adds the cog to the Discord Bot
    
    This is not called directly; it is called when the Bot
    called the load_extension function on a cog file path.
    """

    bot.add_cog(Help(bot))