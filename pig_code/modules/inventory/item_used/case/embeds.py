import asyncio
import datetime
import random

from .....core import *
from .....utils import *


def case_used(inter, lang, items_received) -> disnake.Embed:
    embed = BotUtils.generate_embed(
        title=locales['item_used']['case_title'][lang],
        description=f"{locales['item_used']['case_desc'][lang].format(items=BotUtils.get_items_in_str_list(items_received, lang))}",
        prefix=Func.generate_prefix('🎁'),
        timestamp=True,
        color=utils_config.rarity_colors[str(BotUtils.get_rarest_item(items_received))],
        footer=Func.generate_footer(inter),
        footer_url=Func.generate_footer_url('user_avatar', inter.author),
    )
    return embed
