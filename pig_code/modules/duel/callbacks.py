from ...utils import *
from . import embeds
from . import components
from ...utils.discord_utils import send_callback, generate_embed
from ...core import *


async def duel(inter, opponent, bet):
    await DisUtils.pre_command_check(inter)
    lang = User.get_language(inter.user.id)
    User.register_user_if_not_exists(opponent.id)
    if opponent == inter.user:
        await error_callbacks.default_error_callback(inter, translate(
            Locale.ErrorCallbacks.cant_play_with_yourself_duel_title, lang),
                                                     translate(Locale.ErrorCallbacks.cant_play_with_yourself_duel_desc,
                                                               lang))
        return
    if opponent.bot is True:
        await error_callbacks.default_error_callback(inter,
                                                     translate(Locale.ErrorCallbacks.bot_as_opponent_duel_title, lang),
                                                     translate(Locale.ErrorCallbacks.bot_as_opponent_duel_desc, lang))
        return
    message = await send_callback(inter,
                                  embed=generate_embed(
                                      title=translate(Locale.Duel.invite_title, lang),
                                      description=translate(Locale.Duel.personal_invite_desc, lang).format(
                                          opponent=opponent.display_name,
                                          user=inter.user.display_name, bet=bet),
                                      prefix=Func.generate_prefix('⚔️'),
                                      inter=inter,
                                  ),
                                  components=components.invite_components(lang))
    await DisUtils.send_notification(opponent, inter,
                                     translate(Locale.Duel.invite_title, User.get_language(opponent.id)),
                                     translate(Locale.Duel.personal_invite_dm_desc, User.get_language(opponent.id),
                                               format_options={'user': inter.user.display_name, 'bet': bet}),
                                     prefix_emoji='⚔️',
                                     url_label=translate(Locale.Global.message, User.get_language(opponent.id)),
                                     url=message.jump_url if message is not None else None, send_to_dm=True,
                                     create_command_notification=False,
                                     guild=inter.guild)

    def check(interaction):
        if message is not None and interaction.message is not None:
            right_message = message.id == interaction.message.id
            return right_message and opponent.id == interaction.user.id

    try:
        interaction = await inter.client.wait_for('interaction', check=check, timeout=120)
    except asyncio.exceptions.TimeoutError:
        await error_callbacks.default_error_callback(inter, translate(Locale.Duel.duel_canceled_title, lang),
                                                     translate(Locale.Duel.no_response_desc, lang,
                                                               format_options={'user': opponent.display_name}))
        return
    if interaction.data.get('custom_id') == 'in;accept':
        await interaction.response.defer(ephemeral=True)
        response = hryak.requests.duel_requests.duel(inter.user.id, opponent.id, bet)
        if response.get('status') == '400;no_money':
            broke_user = await User.get_user(inter.client, response.get('user_id'))
            await error_callbacks.default_error_callback(inter, translate(Locale.Duel.duel_canceled_title, lang),
                                                         translate(Locale.Duel.no_money_for_bet_desc, lang,
                                                                   format_options={'user': broke_user.display_name}))
            return
        for i in range(10):
            await send_callback(interaction, embed=embeds.fight_is_starting(inter, lang, inter.user.id, opponent.id, 10 - i,
                                                                            list(response.get('chances').values())))
            await asyncio.sleep(1)
        await send_callback(interaction, embed=embeds.fight_is_going(inter, lang, inter.user.id, opponent.id,
                                                                     random.choice(hryak.config.fight_gifs)))
        await asyncio.sleep(11)
        await send_callback(interaction, embed=embeds.user_won(inter, lang, response.get('winner_id'), response.get('money_earned'),
                                                               random.choice(hryak.config.win_gifs)))
    elif interaction.data.get('custom_id') == 'in;reject':
        await error_callbacks.default_error_callback(inter, translate(Locale.Duel.duel_canceled_title, lang),
                                                     translate(Locale.Duel.opponent_reject_desc, lang,
                                                               format_options={'user': opponent.display_name}))
