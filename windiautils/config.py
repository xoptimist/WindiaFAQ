import asyncio
import os
import os.path
from typing import (
    NoReturn,
    Any,
    Union
)

import configobj

__all__ = ['Config']

CONFIG_FILE = 'windia.ini'
DEFAULT_CONFIG = {
    'Bot': {
        'Prefix': '$',
        'Secrets': {
            'Token': None
        },
        'Channel': 708715939486498937
    },
    'Logging': {
        'Channel': 714581563022770218
    }
}


def get_config() -> configobj.ConfigObj:
    if not os.path.exists(CONFIG_FILE):
        write_config()

    return configobj.ConfigObj(CONFIG_FILE)


def write_config() -> NoReturn:
    """Writes a default configuration file

    This is called when get_config does not find a configuration file
    Populates sections, keys, and values from DEFAULT_CONFIG
    """

    config = configobj.ConfigObj(DEFAULT_CONFIG)
    config.filename = CONFIG_FILE
    config.write()


class Config:
    """A singleton class for the project's config settings"""
    __slots__ = ['_config']

    __instance = None

    @staticmethod
    def getInstance():
        """Static access method for Config singleton
        
        Creates a new Config instance if one does not exist then returns
        the Config instance"""
        if not Config.__instance:
            Config()
        return Config.__instance

    def __init__(self):
        if Config.__instance:
            raise Exception('Cannot create multiple instances of a Singleton class')

        self._config = get_config()
        Config.__instance = self

    async def aioget(self, section: str, key: str, default: None = None) -> str:
        return await asyncio.get_event_loop().run_in_executor(None, self.get, section, key, default)

    async def aiogetint(self, section: str, key: str, default: None = None) -> int:
        return await asyncio.get_event_loop().run_in_executor(None, self.getint, section, key, default)

    async def aioset(self, section: str, key: str, value: Any) -> NoReturn:
        return await asyncio.get_event_loop().run_in_executor(None, self.getint, section, key, value)

    def get(self, section: str, key: str, default: None = None) -> Union[str, None]:
        """Returns the value inside the section's key in the configuration

        Gets the lowest section given in the parameter `section` and returns the value
        at the parameter `key`

        Parameters
        ----------
        section : str
            The section of the needed key as a filepath-like string
        key : str
            The key of the needed value in the configuration file
        default : Any
            A default value to return if no section or key is found

        Returns
        -------
        str
            The value in the configuration file at section[key]

        Raises
        ------
        KeyError
            Parameter `section` or parameter `key` not found in configuration file
        
        Examples
        --------
        config.ini
        > [Section]
        >     [Subsection]
        >         Key = value

        >>> config = Config.getInstance()
        >>> value = config.get('Section/Subsection', 'Key')
        """

        sections = section.split('/')
        _section = self._config
        for section in sections:
            try:
                _section = _section[section]
            except KeyError:
                return default
        try:
            return _section[key]
        except KeyError:
            return default

    def getint(self, section: str, key: str, default: None = None) -> Union[None, int]:
        return int(self.get(section, key, default))

    def set(self, section: str, key: str, value: Any) -> NoReturn:
        """Sets the value inside the section's key in the configuration

        Gets the lowest section given in the parameter `section` and sets the value
        at the key parameter `key` to parameter `value`

        Parameters
        ----------
        section : str
            The section of the needed key as a filepath-like string
        key : str
            The key of the needed value in the configuration file
        value : Any
            The value to set at the given key

        Returns
        -------
        NoReturn

        Raises
        ------
        KeyError
            Parameter `section` or parameter `key` not found in configuration file
        
        Examples
        --------
        config.ini
        > [Section]
        >     TR3YWAY = true
        >     [Subsection]
        >         Key = value

        >>> config = Config.getInstance()
        >>> config.set('Section', 'TR3YWAY', False)
        >>> config.set('Section/Subsection', 'Key', 'new value')
        """

        sections = section.split('/')
        _section = self._config

        for section in sections:
            try:
                _section = _section[section]
            except KeyError:
                raise KeyError(f'{section} does not exist in {self._config.filename}')
        try:
            _section[key] = value
            self._config.write()
        except KeyError:
            raise KeyError(f'{key} does not exist in {section}')
