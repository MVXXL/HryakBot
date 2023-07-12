from ...core import *
from ...utils import *
from . import embeds
from . import components


async def breed(inter, partner):
    await Botutils.pre_command_check(inter)
    Botutils.raise_if_language_not_supported(inter.author.id)
    User.register_user_if_not_exists(partner.id)
    Pig.create_pig_if_no_pig(partner.id)
    Botutils.check_pig_breed_cooldown(inter.author)
    Botutils.check_pig_breed_cooldown(partner)
    lang = User.get_language(inter.author.id)
    min_weight_to_breed = 50
    if partner == inter.author:
        await error_callbacks.default_error_callback(inter, Locales.ErrorCallbacks.cant_breed_with_yourself_title[lang],
                                                     Locales.ErrorCallbacks.cant_breed_with_yourself_desc[lang])
        return
    if partner.bot is True:
        await error_callbacks.default_error_callback(inter, Locales.ErrorCallbacks.bot_as_partner_breed_title[lang],
                                                     Locales.ErrorCallbacks.bot_as_partner_breed_desc[lang])
        return
    if Pig.get_weight(inter.author.id) < min_weight_to_breed:
        await error_callbacks.default_error_callback(inter, Locales.Breed.not_enough_weight_title[lang],
                                                     Locales.Breed.not_enough_weight_desc[lang].format(
                                                         pig=Pig.get_name(inter.author.id),
                                                         weight=min_weight_to_breed))
        return
    if Pig.get_weight(partner.id) < min_weight_to_breed:
        await error_callbacks.default_error_callback(inter, Locales.Breed.not_enough_weight_title[lang],
                                                     Locales.Breed.not_enough_weight_desc[lang].format(
                                                         pig=Pig.get_name(partner.id),
                                                         weight=min_weight_to_breed))
        return
    message = await send_callback(inter,
                                  embed=embeds.personal_breed_invite(inter, lang, partner),
                                  components=components.invite_components(lang))

    def check(interaction):
        if message is not None:
            right_message = message.id == interaction.message.id
            return right_message and partner.id == interaction.author.id

    try:
        interaction = await inter.client.wait_for('button_click', check=check, timeout=120)
    except asyncio.exceptions.TimeoutError:
        await send_callback(message, embed=embeds.breed_canceled(inter, lang, partner, 'no_response'))
        return
    if interaction.component.custom_id == 'in:accept':
        await interaction.response.defer(ephemeral=True)
        mini_pig_chances = {'fail': 50,
                            # 'pet_hryak_default': (Pig.get_weight(inter.author.id) + Pig.get_weight(partner.id)) / 1.5
                            }
        mini_pig = Func.random_choice_with_probability(mini_pig_chances)
        Pig.set_last_breed(inter.author.id, Func.get_current_timestamp())
        Pig.set_last_breed(partner.id, Func.get_current_timestamp())
        if mini_pig == 'fail':
            await send_callback(inter, embed=embeds.pig_breed_fail(inter, lang, partner))
        else:
            Pig.make_pregnant(partner.id, partner.id, mini_pig)
            await send_callback(inter, embed=embeds.pig_breed_ok(inter, lang, partner, mini_pig))
    elif interaction.component.custom_id == 'in:reject':
        await send_callback(interaction, embed=embeds.breed_canceled(inter, lang, partner, 'partner_reject'))


async def pregnancy(inter):
    await Botutils.pre_command_check(inter)
    lang = User.get_language(inter.author.id)
    if Pig.is_pregnant(inter.author.id):
        await send_callback(inter, embed=embeds.pregnancy(inter, lang))
    else:
        await error_callbacks.default_error_callback(inter, Locales.Pregnancy.not_pregnant_title[lang],
                                                     Locales.Pregnancy.not_pregnant_desc[lang], prefix='🐖')
