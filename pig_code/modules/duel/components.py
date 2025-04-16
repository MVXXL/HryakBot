from ...core import *
from ...utils import *
from ...core import *


def invite_components(lang) -> list:
    components = [
        discord.ui.Button(
            style=discord.ButtonStyle.green,
            label=translate(Locale.Global.accept, lang),
            custom_id=f'in;accept',
        ),
        discord.ui.Button(
            style=discord.ButtonStyle.red,
            label=translate(Locale.Global.reject, lang),
            custom_id=f'in;reject',
        )
    ]
    return components
