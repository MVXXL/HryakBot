from ...utils import *
from ...utils.discord_utils import generate_embed
from ...core import *



def fight_is_starting(inter, lang, user_id: int, opponent_id: int, time_to_start: int, chances) -> discord.Embed:
    embed = generate_embed(
        title=translate(Locale.Duel.fight_is_starting_title, lang, {'time_to_start': time_to_start}),
        description=translate(Locale.Duel.fight_is_starting_desc, lang,
                              {'pig1': Pig.get_name(user_id), 'pig2': Pig.get_name(opponent_id)}),
        prefix=Func.generate_prefix('⚔️'),
        inter=inter,
        fields=[{'name': f'{Pig.get_name(user_id)}',
                 'value': translate(Locale.Duel.fight_starting_field_value, lang,
                                    {'weight': Pig.get_weight(user_id), 'chance': chances[0]}),
                 'inline': True},
                {'name': f'{Pig.get_name(opponent_id)}',
                 'value': translate(Locale.Duel.fight_starting_field_value, lang, {'weight': Pig.get_weight(opponent_id),
                                                                                    'chance': chances[1]}),
                 'inline': True
                 },
                ],
    )
    return embed


def fight_is_going(inter, lang, user_id: int, opponent_id: int, gif) -> discord.Embed:
    embed = generate_embed(
        title=translate(Locale.Duel.fight_is_going_title, lang),
        description=translate(Locale.Duel.fight_is_going_desc, lang,
                              {'pig1': Pig.get_name(user_id), 'pig2': Pig.get_name(opponent_id)}),
        image_url=gif,
        prefix=Func.generate_prefix('⚔️'),
        inter=inter,
    )
    return embed


def user_won(inter, lang, user_id: int, money_earned: int, gif_url: str) -> discord.Embed:
    embed = generate_embed(
        title=translate(Locale.Duel.fight_ended_title, lang),
        description=translate(Locale.Duel.fight_ended_desc, lang,
                              {'pig': Pig.get_name(user_id), 'user': f'<@&{user_id}>', 'money_earned': money_earned}),
        thumbnail_url=gif_url,
        prefix=Func.generate_prefix('🎉'),
        inter=inter
    )
    return embed
