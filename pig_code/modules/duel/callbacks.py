from ...core import *
from ...utils import *
from . import embeds
from . import components


async def duel(inter, opponent, bet):
    await BotUtils.pre_command_check(inter)
    lang = User.get_language(inter.author.id)
    User.register_user_if_not_exists(opponent.id)
    if opponent == inter.author:
        await error_callbacks.default_error_callback(inter, translate(
            Locales.ErrorCallbacks.cant_play_with_yourself_duel_title, lang),
                                                     translate(Locales.ErrorCallbacks.cant_play_with_yourself_duel_desc,
                                                               lang))
        return
    if opponent.bot is True:
        await error_callbacks.default_error_callback(inter,
                                                     translate(Locales.ErrorCallbacks.bot_as_opponent_duel_title, lang),
                                                     translate(Locales.ErrorCallbacks.bot_as_opponent_duel_desc, lang))
        return
    message = await send_callback(inter,
                                  embed=generate_embed(
                                      title=translate(Locales.Duel.invite_title, lang),
                                      description=translate(Locales.Duel.personal_invite_desc, lang).format(
                                          opponent=opponent.display_name,
                                          user=inter.author.display_name, bet=bet),
                                      prefix=Func.generate_prefix('⚔️'),
                                      inter=inter,
                                  ),
                                  components=components.invite_components(lang))
    await BotUtils.send_notification(inter, opponent,
                                     translate(Locales.Duel.invite_title, User.get_language(opponent.id)),
                                     translate(Locales.Duel.personal_invite_dm_desc, User.get_language(opponent.id),
                                               format_options={'user': inter.author.display_name, 'bet': bet}),
                                     prefix='⚔️',
                                     url_label=translate(Locales.Global.message, User.get_language(opponent.id)),
                                     url=message.jump_url if message is not None else None, send_to_dm=True, create_command_notification=False,
                                     guild=inter.guild)

    def check(interaction):
        if message is not None:
            right_message = message.id == interaction.message.id
            return right_message and opponent.id == interaction.author.id

    try:
        interaction = await inter.client.wait_for('button_click', check=check, timeout=120)
    except asyncio.exceptions.TimeoutError:
        await error_callbacks.default_error_callback(inter, translate(Locales.Duel.duel_canceled_title, lang),
                                                     translate(Locales.Duel.no_response_desc, lang,
                                                               format_options={'user': opponent.display_name}))
        return
    if interaction.component.custom_id == 'in;accept':
        await interaction.response.defer(ephemeral=True)
        if Item.get_amount('coins', inter.author.id) < bet:
            await error_callbacks.default_error_callback(inter, translate(Locales.Duel.duel_canceled_title, lang),
                                                         translate(Locales.Duel.no_money_for_bet_desc, lang,
                                                                   format_options={'user': inter.author.display_name}))
            return
        if Item.get_amount('coins', opponent.id) < bet:
            await error_callbacks.default_error_callback(inter, translate(Locales.Duel.duel_canceled_title, lang),
                                                         translate(Locales.Duel.no_money_for_bet_desc, lang,
                                                                   format_options={'user': opponent.display_name}))
            return
        chances = {}
        for member in [inter.author, opponent]:
            chances[member] = 100
            chances[member] += Pig.get_weight(member.id) / 2
            if Pig.get_time_to_next_feed(member.id) == -1:
                chances[member] += 20
        chances = Func.calculate_probabilities(chances, 1)
        winner = Func.random_choice_with_probability(chances)
        chances_copy = chances.copy()
        chances_copy.pop(winner)
        loser = list(chances_copy)[0]
        money_earned = int(round(bet * 1.9))
        User.remove_item(winner.id, 'coins', bet)
        User.remove_item(loser.id, 'coins', bet)
        User.add_item(winner.id, 'coins', money_earned)
        for i in range(7):
            await send_callback(interaction, embed=embeds.fight_is_starting(inter, lang, opponent, 7 - i,
                                                                            list(chances.values())))
            await asyncio.sleep(1)
        await send_callback(interaction, embed=embeds.fight_is_going(inter, lang, opponent,
                                                                     random.choice(utils_config.fight_gifs)))
        await asyncio.sleep(11)
        await send_callback(interaction, embed=embeds.user_won(inter, lang, winner, money_earned,
                                                               random.choice(utils_config.win_gifs)))
    elif interaction.component.custom_id == 'in;reject':
        await error_callbacks.default_error_callback(inter, translate(Locales.Duel.duel_canceled_title, lang),
                                                     translate(Locales.Duel.opponent_reject_desc, lang,
                                                               format_options={'user': opponent.display_name}))
