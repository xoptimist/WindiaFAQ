import difflib
import discord

from aioify import aioify


async def process_faq_command(self, command: str, messageable: discord.abc.Messageable, author: discord.Member):
    if command in self.faq_commands:
        return await self.bot.send_embed(command, self.faq_commands[command], messageable, author)
    elif command not in self.faq_commands:
        closest_commands = await self.get_closest_commands(command)
        if len(closest_commands) > 0:
            cmds = ', '.join([f'**{command}**' for command in closest_commands])
            return await messageable.send(f'Did you mean... {cmds}?')


async def get_closest_commands(self, cmd: str):
    if len(cmd) < 2:
        return []

    def __get_closest_commands():
        all_commands = list(self.faq_commands.keys()) + [command.name for command in list(self.bot.commands)]
        return [command for command in all_commands if
                cmd in command or difflib.SequenceMatcher(None, cmd, command).ratio() > min(0.8,
                                                                                            1.0 - 1 / len(cmd))]
    aiogcc = aioify(obj=__get_closest_commands, name='aiogcc')
    return await aiogcc()
