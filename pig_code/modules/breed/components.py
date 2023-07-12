from ...core import *
from ...utils import *


def invite_components(lang) -> list:
    components = [
        disnake.ui.Button(
            style=disnake.ButtonStyle.green,
            label=Locales.Global.accept[lang],
            custom_id=f'in:accept',
        ),
        disnake.ui.Button(
            style=disnake.ButtonStyle.red,
            label=Locales.Global.reject[lang],
            custom_id=f'in:reject',
        )
    ]
    return components
