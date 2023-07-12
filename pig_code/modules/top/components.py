import asyncio
import datetime
import random

from ...core import *
from ...utils import *


async def choose_user(inter, lang, users) -> disnake.Embed:
    # users = User.get_users_sorted_by('pig', 'weight', number=10)
    options = []
    for user_id in users:
        options.append(disnake.SelectOption(
            label=await User.get_name(inter.client, user_id),
            value=user_id,
            # description=option['description']
        ))
    return disnake.ui.Select(options=options, custom_id='view_profile', placeholder=Locales.Top.placeholder[lang])
