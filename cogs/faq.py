from discord.ext import tasks, commands
import botcore
import windiautils
import json
import os.path
import traceback

class FAQ(commands.Cog):
    """A cog used for the FAQ and managing the FAQ"""

    def __init__(self, bot):
        self.bot: botcore.Bot = bot
        self.faq_commands: dict = windiautils.load_commands()

    @commands.command(name='add', hidden=True)
    async def add_command(self, ctx: commands.Context, command: str = None, *, description: str = None):
        """Updates an existing command"""
        
        if not command:
            await ctx.send('Please enter a command to add.')
        elif command in self.faq_commands:
            await ctx.send(f'{command} is already a registered command.')
        else:
            self.faq_commands[command] = description
            windiautils.save_commands(self.faq_commands)
            await ctx.send(f'{command} was added.')

    @commands.command(name='update', hidden=True)
    async def update_command(self, ctx: commands.Context, command: str = None, *, description: str = None):
        """Updates an existing command"""

        if not command:
            await ctx.send('Please enter a command to update.')
        elif not command in self.faq_commands:
            await ctx.send(f'{command} is not a registered command.')
        else:
            self.faq_commands[command] = description
            windiautils.save_commands(self.faq_commands)
            await ctx.send(f'{command} was updated.')

    @commands.command(name='remove', hidden=True)
    async def remove_command(self, ctx: commands.Context, *, command: str = None):
        """Removes an existing command"""

        if not command:
            await ctx.send('Please enter a command to remove.')
        elif not command in self.faq_commands:
            await ctx.send(f'{command} is not a registered command.')
        else:
            self.faq_commands.pop(command)
            windiautils.save_commands(self.faq_commands)
            await ctx.send(f'{command} was removed.')

    def cog_check(self, ctx: commands.Context):
        """Any commands in this cog are FAQ administrative commands, so only special users should use them"""

        return ctx.channel.permissions_for(ctx.author).manage_messages

    @commands.Cog.listener('on_message')
    async def faq_check(self, message):
        """Check if the user is trying to invoke an faq_command"""

        raw_command = message.content.lower()[1::].split(' ')
        command = raw_command[0]

        if command in self.faq_commands:
            await message.channel.send(self.faq_commands[command])

def setup(bot):
    bot.add_cog(FAQ(bot))