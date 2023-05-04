import asyncio
import datetime
import random

from .....core import *
from .....utils import *


def pay(lang):
    component = disnake.ui.Button(
        label=locales['words']['pay'][lang],
        custom_id='pay:5',
        emoji='🪙',
        style=disnake.ButtonStyle.primary
    )
    return component


def run_away(lang):
    component = disnake.ui.Button(
        label=locales['words']['run_away'][lang],
        custom_id='run_away',
        emoji='🏃‍♂️',
        # style=disnake.ButtonStyle.primary
    )
    return component
