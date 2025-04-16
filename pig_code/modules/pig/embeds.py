from ...utils import *
from ...utils.discord_utils import generate_embed
from ...core import *



async def feed(inter, lang, weight_changed: float, pooped_amount: int, vomit: bool) -> discord.Embed:
    pooped_poop_description = translate(Locale.Feed.pig_pooped_desc_list, lang)
    eye_emotion = 'happy'
    if not vomit:
        weight_changed_description = translate(Locale.Feed.feed_scd_desc_list, lang)
    else:
        weight_changed_description = translate(Locale.Feed.feed_fail_desc_list, lang)
        eye_emotion = 'sad'
    description = f'- {translate(weight_changed_description, lang, {"pig": Pig.get_name(inter.user.id), "mass": abs(weight_changed)})}'
    if not vomit:
        description += f'\n- {translate(pooped_poop_description, lang, {"pig": Pig.get_name(inter.user.id), "poop": pooped_amount})}'
    description += f"\n\n*{translate(Locale.Feed.total_pig_weight, lang, {'weight': Pig.get_weight(inter.user.id)})}*"
    embed = generate_embed(
        title=translate(Locale.Feed.feed_scd_title, lang),
        description=description,
        prefix=Func.generate_prefix('🐷'),
        thumbnail_url=await DisUtils.generate_user_pig(inter.user.id, eye_emotion=eye_emotion),
        inter=inter,
        footer=Func.generate_footer(inter, second_part=f'{Stats.get_streak(inter.user.id)} 🔥')
    )
    return embed


async def butcher(inter, lang, lard_add: int, weight_lost: float) -> discord.Embed:
    embed = generate_embed(
        title=translate(Locale.Butcher.butcher_title, lang),
        description=f'- {translate(Locale.Butcher.butcher_desc_list, lang, {"pig": Pig.get_name(inter.user.id), "meat": lard_add})}\n'
                    f'- {translate(Locale.Butcher.weight_lost_desc_list, lang, {"pig": Pig.get_name(inter.user.id), "weight_lost": weight_lost})}\n\n'
                    f'*{translate(Locale.Butcher.total_pig_weight, lang, {"weight": Pig.get_weight(inter.user.id)})}*',
        prefix=Func.generate_prefix('🐷'),
        thumbnail_url=await DisUtils.generate_user_pig(inter.user.id),
        inter=inter,
    )
    return embed


def rename(inter, lang) -> discord.Embed:
    embed = generate_embed(
        title=translate(Locale.Rename.scd_title, lang),
        description=translate(Locale.Rename.scd_desc, lang, {'pig': Pig.get_name(inter.user.id)}),
        prefix=Func.generate_prefix('🐷'),
        inter=inter,
    )
    return embed
