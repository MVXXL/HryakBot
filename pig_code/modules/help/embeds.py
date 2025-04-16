from ...utils import *
from ...utils.discord_utils import generate_embed
from ...core import *



def basic_help(inter, lang) -> discord.Embed:
    embed = generate_embed(
        title=translate(Locales.Help.basic_help_title, lang),
        description=translate(Locales.Help.basic_help_desc, lang),
        prefix=Func.generate_prefix('🥓'),
        inter=inter,
    )
    return embed
