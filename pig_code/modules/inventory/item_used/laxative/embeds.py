import asyncio
import datetime
import random

from .....core import *
from .....utils import *


def laxative_used(inter, lang) -> disnake.Embed:
    embed = BotUtils.generate_embed(
        title=locales['item_used']['laxative_title'][lang],
        description=f"{locales['item_used']['laxative_desc'][lang].format(pig=Pig.get_name(inter.author.id), step=Pig.get_buff_value(inter.author.id, 'laxative'))}",
        prefix=Func.generate_prefix('💊'),
        footer=Func.generate_footer(inter, second_part='laxative_used'),
        footer_url=Func.generate_footer_url('user_avatar', inter.author),
    )
    return embed


