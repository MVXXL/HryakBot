from ...utils import *


async def pig_breed_ok(inter, lang, became_pregnant, mini_pig) -> disnake.Embed:
    embed = generate_embed(
        title='OK',
        description=f'{became_pregnant.display_name}, {Item.get_name(mini_pig, lang)}',
        prefix=Func.generate_prefix('🐷'),
        thumbnail_file=await BotUtils.generate_user_pig(inter.author.id),
        inter=inter,
    )
    return embed


async def pig_breed_fail(inter, lang, partner) -> disnake.Embed:
    # print(123132, Pig.get_time_of_next_breed(inter.author.id), Func.get_current_timestamp())
    embed = generate_embed(
        title=Locales.Breed.fail_title[lang],
        description=Locales.Breed.fail_desc[lang].format(pig=Pig.get_name(inter.author.id),
                                                         partner=Pig.get_name(partner.id),
                                                         retry=Pig.get_time_of_next_breed(inter.author.id)),
        prefix=Func.generate_prefix('🔞'),
        thumbnail_file=await BotUtils.generate_user_pig(inter.author.id, eye_emotion='sad'),
        inter=inter,
    )
    return embed


def personal_breed_invite(inter, lang, user: disnake.User) -> disnake.Embed:
    embed = generate_embed(
        title=Locales.Breed.invite_title[lang],
        description=Locales.Breed.personal_invite_desc[lang].format(partner=user.display_name,
                                                                    user=inter.author.display_name),
        prefix=Func.generate_prefix('🔞'),
        inter=inter
    )
    return embed


def breed_canceled(inter, lang, user: disnake.User, reason: str) -> disnake.Embed:
    description = ''
    if reason == 'partner_reject':
        description = Locales.Breed.partner_reject_desc[lang].format(user=user.display_name)
    elif reason == 'no_response':
        description = Locales.Breed.no_response_desc[lang].format(user=user.display_name)
    embed = generate_embed(
        title=Locales.Breed.breed_canceled_title[lang],
        description=description,
        prefix=Func.generate_prefix('🔞'),
        inter=inter
    )
    return embed


def pregnancy(inter, lang) -> disnake.Embed:
    embed = generate_embed(
        title='Pregnancy status',
        description=f'Вы беременны ребёнком: **{Pig.pregnant_with(inter.author.id)}**\n'
                    f'Отец: {Pig.get_name(Pig.pregnant_by(inter.author.id))} ({inter.author.display_name})',
        prefix=Func.generate_prefix('🤰'),
        inter=inter
    )
    return embed
