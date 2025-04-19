from ...core import *
from ...utils import *
from . import embeds
from . import components


async def help(inter):
    await DisUtils.pre_command_check(inter)
    lang = await User.get_language(inter.user.id)
    await DisUtils.pagination(inter, lang, embeds={
        translate(Locales.Help.basic_help_title, lang): embeds.basic_help(inter, lang),
    }, categories=True, arrows=False)
