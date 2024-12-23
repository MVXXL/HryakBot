from ...core import *
from ...utils import *
from . import embeds
from . import components


async def help(inter):
    await Utils.pre_command_check(inter)
    lang = User.get_language(inter.user.id)
    await Utils.pagination(inter, lang, embeds={
        translate(Locales.Help.basic_help_title, lang): embeds.basic_help(inter, lang),
    }, categories=True, arrows=False)
