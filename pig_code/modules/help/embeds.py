from ...core import *
from ...utils import *


def basic_help(inter, lang) -> disnake.Embed:
    embed = generate_embed(
        title=Locales.Help.basic_help_title[lang],
        description=Locales.Help.basic_help_desc[lang],
        prefix=Func.generate_prefix('🥓'),
        inter=inter,
    )
    return embed

# def basic_help(inter, lang) -> disnake.Embed:
#     embed = generate_embed(
#         title=locales['help']['basic_help_title'][lang],
#         description=locales['help']['basic_help_desc'][lang],
#         prefix=Func.generate_prefix('🥓'),
#         # thumbnail_file=await BotUtils.generate_user_pig(inter.author.id),
#         footer=Func.generate_footer(inter, user=inter.author),
#         footer_url=Func.generate_footer_url('user_avatar', inter.author),
#     )
#     return embed
