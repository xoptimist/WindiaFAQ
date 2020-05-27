"""This file is for saving and loading FAQ commands for the Windia FAQ

Methods
-------
def load_commands() -> dict
    Attempts to load commands stored in commands.json, else loads a dictionary of default commands

def save_commands(commands: dict)
    Saves the commands to the commands file

__load_default_commands() -> dict
    Returns a dictionary of default commands
"""

import json
import os.path

__commands_file = 'commands.json'


def load_commands() -> dict:
    """Attempts to load commands stored in commands.json, else loads a dictionary of default commands
    
    Checks if the commands file exists; if it does, then the commands are loaded
    from the commands file, else it is loaded from the default commands.

    Returns
    -------
    A dictionary of FAQ commands
    """

    if not os.path.exists(__commands_file):
        return __load_default_commands()
    else:
        with open(__commands_file, 'r') as file:
            return json.load(file)


def save_commands(commands: dict):
    """Saves the commands to the commands file
    
    save_commands(commands: dict)

    Opens the __commands_file in write-mode, then dumps the commands dictionary into the file.

    Parameters
    ----------
    commands: dict
        The commands being stored into the commands file

    Raises
    ------
    TypeError
        If the commands passed is not of type dict
    """

    if not isinstance(commands, dict):
        raise TypeError

    with open(__commands_file, 'w') as file:
        json.dump(commands, file, indent=4)


def __load_default_commands() -> dict:
    """A dictionary of default commands
    
    __load_default_commands() -> dict
    
    A dictionary of some default commands used. This is used when no commands file
    is found when loading commands, so these commands are then saved into the 
    commands file.

    Returns
    -------
    A dictionary of default commands
    """

    default_commands = {
        'rates': 'Levels 1-9: 1x\n' \
                 'Levels 10-29: 20x\n' \
                 'Levels 30-49: 35x\n' \
                 'Levels 50-69: 50x\n' \
                 'Levels 70-99: 75x\n' \
                 'Levels 100-149: 90x\n' \
                 'Levels 150-250: 100x\n' \
                 'Quest EXP: 3x\n' \
                 'Meso: 6 * Monster Level ~ 9 * Monster Level\n' \
                 'Drop: Custom (use `@wd <item>` in game)',

        'unspecified': 'Open `windia.ini` in your Windia folder and adjust your resolution to one your monitor supports.',

        'dll': 'If you get an error saying a .dll file is missing, download and run this: https://aka.ms/vs/16/release/vc_redist.x86.exe.',

        'donate': 'To donate, go to https://shavit.selly.store/category/8635a6fe. Once you donate, check your junk/spam in the e-mail you typed into selly. It may take up to five minutes.',

        'download': 'To download, download the patcher at https://windia.me/download. Place this in an empty folder. Before you run it, add the folder to your antivirus and Windows Defender\'s exclusions. Then run the patcher.',

        'patch': 'To patch, run the patcher inside of your Windia folder.',

        'flames': 'Flames are items that provide extra stats to your gear. Stats gained upon leveling up are not affected by flame stats. Overalls get 2x the flame stats of other gears.\n' \
                  'Maximum eternal flame stats:  ((item_level + 1) / 20) * 10\n' \
                  'Maximum powerful flame stats: ((item_level + 1) / 20) * 7',

        'cog': 'Cog, or Chaos Scroll of Goodness, functions as a Chaos Scroll but gives +2 ~ +8 stats. You can convert 100 Chaos Scrolls into 1 Cog through the pink bushes in the Free Market, or find them through drops: `@wd chaos scroll of goodness`.',

        'webclient': 'If you get `Error: An exception occurred during a WebClient request.` when patching, open Task Manager and end the windia.dll process or restart your PC.',

        'antivirus': 'If you get `Windia.dll was not found` or `0x0F` when launching Windia, please add the game\'s folder to your antivirus and/or Windows Defender\'s exclusions then re-run the patcher.',

        'gfx': 'If you are experiencing frequent crashing while training or bossing, type `@settings` in game and turn off some of the options to mitigate the crashing and open System Options in game and turn graphics to low.',

        'damageskins': 'To turn off damage skins, open `windia.ini` and set `use_damage_skin` to 0.\n' \
                       'To change your damage skin, open `windia.ini` and set `damage_skin` to a valid damage skin ID. These can be found typing `@damageskins` in game.',

        'vote': 'To vote, either type `@vote` in game or log into the Windia site and click the Vote button at the top. You can vote 3x per day per account. This can be achieved by voting on different connections (data, Wi-Fi, VPN), different devices, different browsers, etc.',

        '3rdjob': '<https://forum.windia.me/index.php?threads/windia-custom-question-cheat-sheet-and-3rd-4th-job-advancement.154/>',

        'changepass': 'To change your password, you must link your account in-game by typing `@discord` and inputting your Discord ID into the text box. Then DM @Windia Bot#6611 on Discord `!resetpassword`.',

        'changepic': 'To change your PIC, you must link your account in-game by typing `@discord` and inputting your Discord ID into the text box. Then DM @Windia Bot#6611 on Discord `!resetpic`.',

        '250quests': 'Completing 250 quests on one character provides a 100 Weapon Attack and 150 Magic Attack buff to your entire account. This must be 250 quests on a single character.',

        'deletechar': 'To delete a character, log out of your account completely for 3 minutes, then you can delete your character.',

        'legion': 'For every 10 levels achieved on a unique class, you will obtain 1% All Stats for every character. Unique classes include all 2nd Job characters, Noblesse, Beginner, Legend, and Ironman. Ironman provides double legion bonuses for your account.',

        'ironman': 'To create an Ironman character, you must have 1,000 Legion. Create a Beginner and you will be prompted to make an Ironman. Ironman cannot trade, drop trade, or party with other players.',

        'viprole': 'To get your VIP role in Discord after purchasing VIP, type `@discord` in-game and input your Discord ID into the text box.',

        'sylph': 'To obtain a Sylph Ring, talk to the Mysterious Light on the left of the Free Market. This ring can only be traded between your own characters on your account which can also be done by talking to the Mysterious Light to the left of the Free Market.',
    }

    save_commands(default_commands)
    return default_commands
