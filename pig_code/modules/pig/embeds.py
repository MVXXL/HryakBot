from ...core import *
from ...utils import *


def pig_feed(inter, lang, weight_changed: float, pooped_poop: int) -> disnake.Embed:
    weight_changed_description = ''
    pooped_poop_description = random.choice(Locales.Feed.pig_pooped_desc_list[lang])
    if weight_changed >= 0:
        weight_changed_description = random.choice(Locales.Feed.feed_scd_desc_list[lang])
    elif weight_changed < 0:
        weight_changed_description = random.choice(Locales.Feed.feed_fail_desc_list[lang])
    embed = generate_embed(
        title=Locales.Feed.feed_scd_title[lang],
        description=f'- {weight_changed_description.format(pig=Pig.get_name(inter.author.id), mass=abs(weight_changed))}\n'
                    f'- {pooped_poop_description.format(pig=Pig.get_name(inter.author.id), poop=pooped_poop)}\n\n'
                    f"*{Locales.Feed.total_pig_weight[lang].format(weight=Pig.get_weight(inter.author.id))}*",
        prefix=Func.generate_prefix('🐷'),
        thumbnail_file=BotUtils.generate_user_pig(inter.author.id, eye_emotion='happy'),
        inter=inter,
    )
    return embed


def pig_meat(inter, lang, bacon_add: int, weight_lost: float) -> disnake.Embed:
    embed = generate_embed(
        title=Locales.Meat.meat_title[lang],
        description=f'- {random.choice(Locales.Meat.meat_desc_list[lang]).format(pig=Pig.get_name(inter.author.id), meat=bacon_add)}\n'
                    f'- {random.choice(Locales.Meat.weight_lost_desc_list[lang]).format(pig=Pig.get_name(inter.author.id), weight_lost=weight_lost)}\n\n'
                    f"*{Locales.Meat.total_pig_weight[lang].format(weight=Pig.get_weight(inter.author.id))}*",
        prefix=Func.generate_prefix('🐷'),
        thumbnail_file=BotUtils.generate_user_pig(inter.author.id),
        inter=inter,
    )
    return embed


def pig_rename(inter, lang) -> disnake.Embed:
    embed = generate_embed(
        title=Locales.Rename.scd_title[lang].format(pig=Pig.get_name(inter.author.id)),
        prefix=Func.generate_prefix('🐷'),
        inter=inter,
    )
    return embed
