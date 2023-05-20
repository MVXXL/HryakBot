import asyncio
import datetime
import random

import disnake

from ...core import *
from ...utils import *


def basic_help(inter, lang) -> disnake.Embed:
    embed = BotUtils.generate_embed(
        title=locales['help']['basic_help_title'][lang],
        description=locales['help']['basic_help_desc'][lang],
        prefix=Func.generate_prefix('🥓'),
        # thumbnail_file=BotUtils.generate_user_pig(inter.author.id),
        footer=Func.generate_footer(inter, user=inter.author),
        footer_url=Func.generate_footer_url('user_avatar', inter.author),
    )
    return embed

