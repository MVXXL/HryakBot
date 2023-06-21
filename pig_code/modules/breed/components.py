import asyncio
import datetime
import random

from ...core import *
from ...utils import *


def invite_components(lang) -> list:
    components = [
        disnake.ui.Button(
            style=disnake.ButtonStyle.green,
            label=locales['words']['accept'][lang],
            custom_id=f'in:accept',
        ),
        disnake.ui.Button(
            style=disnake.ButtonStyle.red,
            label=locales['words']['reject'][lang],
            custom_id=f'in:reject',
        )
    ]
    return components
