from ...core import *
from ...utils import *


def invite_components(lang) -> list:
    components = [
        discord.ui.Button(
            style=discord.ButtonStyle.green,
            label=translate(Locales.Global.accept, lang),
            custom_id=f'in;accept',
        ),
        discord.ui.Button(
            style=discord.ButtonStyle.red,
            label=translate(Locales.Global.reject, lang),
            custom_id=f'in;reject',
        )
    ]
    return components


