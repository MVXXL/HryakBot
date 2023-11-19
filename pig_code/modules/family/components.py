from ...core import *
from ...utils import *


def accept_reject_user_to_family(lang, user_id, family_id) -> list:
    components = [
        disnake.ui.Button(
            style=disnake.ButtonStyle.green,
            label=Locales.Global.accept[lang],
            custom_id=f'family;join_requests;accept;{user_id};{family_id}',
        ),
        disnake.ui.Button(
            style=disnake.ButtonStyle.red,
            label=Locales.Global.reject[lang],
            custom_id=f'family;join_requests;reject;{user_id};{family_id}',
        )
    ]
    return components
