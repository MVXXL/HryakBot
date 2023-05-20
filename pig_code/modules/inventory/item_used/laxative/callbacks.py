import asyncio
import datetime
import random

from .....core import *
from .....utils import *
from . import embeds
from . import components


async def laxative_used(inter, lang):
    Pig.add_buff(inter.author.id, 'laxative', 1)
    await BotUtils.send_callback(inter, embed=embeds.laxative_used(inter, lang),
                                 ephemeral=True, edit_original_message=False)
