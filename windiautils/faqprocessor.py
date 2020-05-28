import difflib
import aiosqlite

import os.path

__all__ = ['create_database', 'database_exists', 'add_command', 'get_command', 'update_command', 'delete_command']


async def is_nearest_match(command, faq_command):
    return any((command in faq_command, faq_command in command,
                difflib.SequenceMatcher(None, command, faq_command).ratio() > min(0.8, 1.0 - 1 / len(command))))


async def get_nearest_match(connection: aiosqlite.Connection, command: str):
    nearest_matches = []

    if len(command) > 2:
        # produces too many matches with only 2 characters in a command so ignore this
        async with connection.execute(" SELECT * FROM commands; ") as cursor:
            async for row in cursor:
                if is_nearest_match(command, row['command']):
                    nearest_matches.append(row['command'])

    return nearest_matches

__commands_file = 'windia.db'


async def create_database():
    async with aiosqlite.connect(__commands_file) as db:
        await db.execute(" DROP TABLE IF EXISTS commands; ")
        await db.execute(" CREATE TABLE commands(command, description); ")
        await db.commit()


async def database_exists():
    return os.path.exists(__commands_file)


async def add_command(command: str, value: str):
    async with aiosqlite.connect(__commands_file) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(" SELECT * FROM commands WHERE command = ?; ", (command, )) as cursor:
            if await cursor.fetchone():
                return False
            else:
                await db.execute(" INSERT INTO commands (command, description) VALUES (?, ?); ", (command, value, ))
                await db.commit()
                return True


async def get_command(command: str):
    async with aiosqlite.connect(__commands_file) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(" SELECT * FROM commands WHERE command = ?; ", (command, )) as cursor:
            if row := await cursor.fetchone():
                return row['description']
            else:
                nearest_matches = await get_nearest_match(db, command)
                if nearest_matches:
                    return f'Did you mean... {",".join(nearest_matches)}?'
                else:
                    return None


async def update_command(command: str, value: str):
    async with aiosqlite.connect(__commands_file) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(" SELECT * FROM commands WHERE command = ?; ", (command, )) as cursor:
            if await cursor.fetchone():
                await db.execute(" UPDATE commands SET description = ? WHERE command = ?; ", (value, command, ))
                await db.commit()
                return True
            else:
                return False


async def delete_command(command: str):
    async with aiosqlite.connect(__commands_file) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(" SELECT * FROM commands WHERE command = ?; ", (command,)) as cursor:
            if await cursor.fetchone():
                await db.execute(" DELETE FROM commands WHERE command = ?; ", (command,))
                await db.commit()
                return True
            else:
                return False

