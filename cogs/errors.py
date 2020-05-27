from discord.ext import commands
from botcore import Bot
import sys
import traceback


class ErrorsCog(commands.Cog):
    __slots__ = ['bot']

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener('on_command_error')
    async def log_command_errors(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.UserInputError):
            return await ctx.send(
                f'**ERROR** {ctx.author.mention}, please follow the command\'s proper usage: '
                f'{self.bot.command_prefix}{ctx.invoked_with} {ctx.command.usage}'
            )
        elif isinstance(error, commands.CheckFailure):
            if isinstance(error, commands.BotMissingPermissions):
                return await ctx.send(
                    f'**ERROR** I lack permissions to use this command. I need `{error.missing_perms}`.'
                )
            elif isinstance(error, commands.BotMissingRole):
                return await ctx.send(
                    f'**ERROR** I lack the role to use this command. I need `{error.missing_role}`.'
                )
            elif isinstance(error, commands.BotMissingAnyRole):
                return await ctx.send(
                    f'**ERROR** I lack a role to use this command. I need one of any `{error.missing_roles}`.'
                )
            else:
                return await ctx.send(
                    f'**ERROR** {ctx.author.mention}, you lack permission to use this command.'
                )
        elif isinstance(error, commands.PrivateMessageOnly):
            return await ctx.send(
                f'**ERROR** {ctx.author.mention}, this command may only be used in DMs.'
            )
        elif isinstance(error, commands.NoPrivateMessage):
            return await ctx.send(
                f'**ERROR** {ctx.author.mention}, this command may not be used in DMs.'
            )
        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(
                f'**ERROR** {ctx.author.mention}, this command has been disabled.'
            )
        elif isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(
                f'**ERROR** {ctx.author.mention}, you are on cooldown for {error.retry_after} seconds.'
            )
        elif isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(
                f'**ERROR** {ctx.author.mention}, this command has been disabled.'
            )
        elif isinstance(error, commands.ConversionError):
            return await ctx.send(
                f'**ERROR** {ctx.author.mention}, {error.converter} failed!'
            )
        else:
            etype, value, tb = sys.exc_info()
            await self.bot.log(
                '**COMMAND ERROR**',
                ('An unknown or unhandled error has occurred', type(error).__name__),
                ('User Message', ctx.message.content),
                ('Error Message', "".join(traceback.format_exception(etype, value, tb)))
            )

            return await ctx.send(
                f'**ERROR** An unknown or unhandled error has occurred processing this command.'
            )

    @commands.Cog.listener('on_error')
    async def log_error(self, event_method: str, *args, **kwargs):
        etype, value, tb = sys.exc_info()
        await self.bot.log(
            '**ERROR**',
            (f'An unknown or unhandled error in {event_method} has occurred',
             f'Error Message: ```{"".join(traceback.format_exception(etype, value, tb))}```')
        )


def setup(bot: Bot):
    bot.add_cog(ErrorsCog(bot))
