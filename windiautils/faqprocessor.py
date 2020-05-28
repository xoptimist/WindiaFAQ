import difflib
import asyncio

from windiautils import load_commands

from typing import (
    Union,
    List
)

faq_commands = load_commands()


async def process_faq_command(command: str) -> Union[None, str]:
    """Processes the given command for FAQ output

    Checks if the command `command` is an exact match with one in `faq_commands`,
    if not attempts to return any close matches

    Parameters
    ----------
    command: str
        The FAQ command invoked for question

    Returns
    -------
    None
        If no close matches to command `command` are found in `faq_commands`

    str
        The description of the FAQ command if it is found, or a string containing
        close matches of the FAQ commands
    """

    if command in faq_commands:
        return faq_commands[command]
    elif command not in faq_commands:
        closest_commands = await get_closest_commands(command)
        if len(closest_commands) > 0:
            cmds = ', '.join([f'**{command}**' for command in closest_commands])
            return f'Did you mean... {cmds}?'
        else:
            return None


async def get_closest_commands(cmd: str) -> List[str]:
    if len(cmd) < 2:
        return []

    def __get_closest_commands():
        return [command for command in faq_commands if
                cmd in command or difflib.SequenceMatcher(None, cmd, command).ratio() > min(0.8,
                                                                                            1.0 - 1 / len(cmd))]

    return await asyncio.get_event_loop().run_in_executor(None, __get_closest_commands)
