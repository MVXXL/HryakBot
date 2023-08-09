from ...core import *
from ...utils import *
from . import embeds
from . import components


async def help(inter):
    await BotUtils.pre_command_check(inter)
    lang = User.get_language(inter.author.id)
    await BotUtils.pagination(inter, lang, embeds={
        Locales.Help.basic_help_title[lang]: embeds.basic_help(inter, lang),
    }, categories=True, arrows=False)
