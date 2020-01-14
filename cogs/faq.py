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
        self.ext_commands: dict = windiautils.load_commands()

    @commands.command(name='add', hidden=True)
    @commands.has_permissions(manage_messages=True)
    async def add_command(self, ctx: commands.Context, command: str = None, *, description: str = None):
        """Updates an existing command"""
        
        if not command:
            await ctx.send('Please enter a command to add.')
        elif command in self.ext_commands:
            await ctx.send(f'{command} is already a registered command.')
        else:
            self.ext_commands[command] = description
            windiautils.save_commands(self.ext_commands)
            await ctx.send(f'{command} was added.')

    @commands.command(name='update', hidden=True)
    @commands.has_permissions(manage_messages=True)
    async def update_command(self, ctx: commands.Context, command: str = None, *, description: str = None):
        """Updates an existing command"""

        if not command:
            await ctx.send('Please enter a command to update.')
        elif not command in self.ext_commands:
            await ctx.send(f'{command} is not a registered command.')
        else:
            self.ext_commands[command] = description
            windiautils.save_commands(self.ext_commands)
            await ctx.send(f'{command} was updated.')

    @commands.command(name='remove', hidden=True)
    @commands.has_permissions(manage_messages=True)
    async def remove_command(self, ctx: commands.Context, *, command: str = None):
        """Removes an existing command"""

        if not command:
            await ctx.send('Please enter a command to remove.')
        elif not command in self.ext_commands:
            await ctx.send(f'{command} is not a registered command.')
        else:
            self.ext_commands.pop(command)
            windiautils.save_commands(self.ext_commands)
            await ctx.send(f'{command} was removed.')

    @commands.Cog.listener('on_message')
    async def faq_check(self, message):
        """Check if the user is trying to invoke an ext_command"""

        raw_command = message.content.lower()[1::].split(' ')
        command = raw_command[0]

        if command in self.ext_commands:
            await message.channel.send(self.ext_commands[command])

def setup(bot):
    bot.add_cog(FAQ(bot))