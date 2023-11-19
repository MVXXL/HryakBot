from ...core import *
from ...utils import *


def fight_is_starting(inter, lang, user: disnake.User, time_to_start: int, chances) -> disnake.Embed:
    embed = generate_embed(
        title=Locales.Duel.fight_will_start_in[lang].format(time_to_start=time_to_start),
        description=f'# **{Pig.get_name(inter.author.id)}** *vs* **{Pig.get_name(user.id)}**',
        prefix=Func.generate_prefix('⚔️'),
        inter=inter,
        fields=[{'name': f'{Pig.get_name(inter.author.id)}',
                 'value': Locales.Duel.fight_starting_field_value[lang].format(
                     weight=Pig.get_weight(inter.author.id), chance=chances[0]),
                 'inline': True},
                {'name': f'{Pig.get_name(user.id)}',
                 'value': Locales.Duel.fight_starting_field_value[lang].format(weight=Pig.get_weight(user.id),
                                                                               chance=chances[1]),
                 'inline': True
                 },
                ],
    )
    return embed


def fight_is_going(inter, lang, user: disnake.User, gif) -> disnake.Embed:
    embed = generate_embed(
        title=Locales.Duel.fight_is_going_title[lang],
        description=f'# **{Pig.get_name(inter.author.id)}** *vs* **{Pig.get_name(user.id)}**',
        image_url=gif,
        prefix=Func.generate_prefix('⚔️'),
        inter=inter,
        # fields=[{'name': 'Maxim',
        #          'value': '```Weight: 200 kg\n'
        #                   'Win chance: 70 %```',
        #          'inline': True},
        #         {'name': 'Neiro',
        #          'value': '```Weight: 100 kg\n'
        #                   'Win chance: 30 %```',
        #          'inline': True
        #          },
        #         ]
    )
    return embed


def user_won(inter, lang, user: disnake.User, money_earned, gif) -> disnake.Embed:
    embed = generate_embed(
        title=Locales.Duel.fight_ended_title[lang],
        description=Locales.Duel.fight_ended_desc[lang].format(user=user.display_name, money_earned=money_earned),
        image_url=gif,
        prefix=Func.generate_prefix('🎉'),
        inter=inter
        # fields=[{'name': 'Maxim',
        #          'value': '```Weight: 200 kg\n'
        #                   'Win chance: 70 %```',
        #          'inline': True},
        #         {'name': 'Neiro',
        #          'value': '```Weight: 100 kg\n'
        #                   'Win chance: 30 %```',
        #          'inline': True
        #          },
        #         ]
    )
    return embed
