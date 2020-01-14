from discord.ext import tasks, commands
import botcore
import windiautils

class Help(commands.Cog):
    """A cog used for the Help command to display all the commands"""

    def __init__(self, bot):
        self.bot: botcore.Bot = bot

    @commands.command(name='help', hidden=True)
    async def help_command(self, ctx: commands.Context):
        """DMs the user the list of commands and their descriptions."""
        
        user = self.bot.get_user(ctx.author.id)
        bot_commands = list(self.bot.commands) + list(windiautils.load_commands())
        messages = list()

        help = 'Here is our list of commands\n\n'

        for command in bot_commands:
            if isinstance(command, commands.Command) and command.hidden:
                continue

            if len(help) > 1900:
                message.append(help)
                help = '\n'

            help += f'`{command}`\n'

        messages.append(help)

        for message in messages:
            await user.send(message)

        await ctx.send('I have DMed you a list of commands.')

def setup(bot):
    bot.add_cog(Help(bot))