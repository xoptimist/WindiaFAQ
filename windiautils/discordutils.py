import discord
import re

from typing import (
    Tuple,
    Collection
)

__all__ = ['send_embed']


async def send_embed(
        title: str,
        description: str,
        messageable: discord.abc.Messageable,
        author: discord.Member,
        *,
        footer: str = 'Send FAQ suggestions to your nearest staff member and everything else to wallace05#0828 :)',
        fields: Collection[Tuple[str, str]] = tuple()
):
    embed = discord.Embed(title=title, description=description, color=discord.Color.purple())
    embed.set_author(name=f'{author}', icon_url=author.avatar_url)
    embed.set_footer(text=footer)

    # embed any first image url found in the description
    if match := re.match(r'(https[^\s]+\.(jpe?g|png))', description):
        embed.set_image(url=match.group(0))

    for name, value in fields:
        embed.add_field(name=name, value=value)

    return await messageable.send(embed=embed)
