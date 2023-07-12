from ...core import *
from .main import *
from ..functions import Func
from ..db_api import *


def default_error_embed(inter, title, description, prefix: str = '❌', timestamp: bool = True,
                        color: str = utils_config.error_color) -> disnake.Embed:
    embed = generate_embed(
        title=title,
        description=description,
        prefix=Func.generate_prefix(prefix),
        inter=inter,
        color=color
    )
    return embed


async def default_error_callback(inter, title, description, prefix: str = '❌', timestamp: bool = True,
                                 color: str = utils_config.error_color):
    await send_callback(inter, embed=default_error_embed(inter, title, description, prefix, timestamp, color))


async def error(error, inter):
    lang = User.get_language(inter.author.id)
    text_error = str(type(error)).split('.')[-1].split('\'')[0]
    if type(error) == PigFeedCooldown:
        await send_callback(inter, embed=default_error_embed(inter,
                                                             title=Locales.ErrorCallbacks.pig_feed_cooldown_title[lang],
                                                             description=Locales.ErrorCallbacks.pig_feed_cooldown_desc[
                                                                 lang].format(
                                                                 pig=Pig.get_name(inter.author.id),
                                                                 timestamp=Pig.get_time_of_next_feed(
                                                                     inter.author.id)),
                                                             color=utils_config.main_color,
                                                             prefix='🍖'))
    elif type(error) == PigMeatCooldown:
        await send_callback(inter, embed=default_error_embed(inter,
                                                             title=Locales.ErrorCallbacks.pig_meat_cooldown_title[lang],
                                                             description=Locales.ErrorCallbacks.pig_meat_cooldown_desc[
                                                                 lang].format(
                                                                 pig=Pig.get_name(inter.author.id),
                                                                 timestamp=Pig.get_time_of_next_meat(
                                                                     inter.author.id)),
                                                             color=utils_config.main_color,
                                                             prefix='🥓'))
    elif type(error) == PigBreedCooldown:
        user = error.user
        if user is None:
            user = inter.author
        await send_callback(inter, embed=default_error_embed(inter,
                                                             title=Locales.ErrorCallbacks.pig_breed_cooldown_title[
                                                                 lang],
                                                             description=Locales.ErrorCallbacks.pig_breed_cooldown_desc[
                                                                 lang].format(
                                                                 pig=Pig.get_name(user.id),
                                                                 timestamp=Pig.get_time_of_next_breed(
                                                                     user.id)),
                                                             color=utils_config.main_color,
                                                             prefix='🔞'))
    elif type(error) == PaginationWrongUser:
        await send_callback(inter, embed=default_error_embed(inter,
                                                             Locales.Pagination.wrong_user_title[lang],
                                                             Locales.Pagination.wrong_user_desc[
                                                                 lang]),
                            edit_original_message=False,
                            ephemeral=True)
    elif type(error) == NotUserComponentClicked:
        await send_callback(inter, embed=default_error_embed(inter,
                                                             Locales.Pagination.wrong_user_title[lang],
                                                             Locales.Pagination.wrong_user_desc[lang]),
                            edit_original_message=False,
                            ephemeral=True)
    elif type(error) == NoMoney:
        await send_callback(inter, embed=default_error_embed(inter,
                                                             Locales.ErrorCallbacks.not_enough_money_title[lang],
                                                             Locales.ErrorCallbacks.not_enough_money_desc[lang]))
    elif type(error) == PlayWithYourselfDuel:
        await cant_play_with_yourself_duel(inter)
    elif type(error) == BotAsOpponentDuel:
        await bot_as_opponent_duel(inter)
    elif type(error) == BreedWithYourself:
        await cant_breed_with_yourself(inter)
    elif type(error) == BotAsPartnerBreed:
        await bot_as_partner_breed(inter)
    elif type(error) == LanguageNotSupported:
        await send_callback(inter, embed=default_error_embed(inter,
                                                             Locales.ErrorCallbacks.language_not_supported_title[
                                                                 lang],
                                                             Locales.ErrorCallbacks.language_not_supported_desc[
                                                                 lang]))
    elif type(error) == NotAllowedToUseCommand:
        await send_callback(inter, embed=default_error_embed(inter,
                                                             Locales.ErrorCallbacks.not_allowed_to_use_command_title[
                                                                 lang],
                                                             Locales.ErrorCallbacks.not_allowed_to_use_command_desc[
                                                                 lang]))
    elif type(error) == commands.errors.NotOwner:
        await send_callback(inter, embed=default_error_embed(inter,
                                                             Locales.ErrorCallbacks.not_allowed_to_use_command_title[
                                                                 lang],
                                                             Locales.ErrorCallbacks.not_owner_desc[lang]))
    elif type(error) == commands.errors.NSFWChannelRequired:
        await send_callback(inter, embed=default_error_embed(inter,
                                                             Locales.ErrorCallbacks.nsfw_required_title[
                                                                 lang],
                                                             Locales.ErrorCallbacks.nsfw_required_desc[lang]))
    elif type(error) == NoItemInInventory:
        desc = Locales.ErrorCallbacks.no_item_desc[lang]
        if error is not None:
            desc = error.desc[lang]
        await send_callback(inter, ephemeral=error.ephemeral,
                            edit_original_message=error.edit_original_message,
                            embed=default_error_embed(inter,
                                                      Locales.ErrorCallbacks.no_item_title[lang].format(
                                                          item=Inventory.get_item_name(error.item,
                                                                                       lang).lower()),
                                                      desc,
                                                      timestamp=True,
                                                      color=utils_config.main_color,
                                                      prefix=Inventory.get_item_emoji(error.item)))
    elif type(error) == commands.errors.BotMissingPermissions:
        perms = Func.translate_permissions(error.missing_permissions, lang)
        await send_callback(inter,
                            embed=default_error_embed(inter, Locales.ErrorCallbacks.bot_missing_perms_title[lang],
                                                      f'```{Func.numerate_list_as_text(perms, False)}```',
                                                      prefix='👧'),
                            edit_original_message=False,
                            ephemeral=True)
    elif type(error) == commands.errors.MissingPermissions:
        perms = Func.translate_permissions(error.missing_permissions, lang)
        await send_callback(inter,
                            embed=default_error_embed(inter, Locales.ErrorCallbacks.bot_missing_perms_title[lang],
                                                      f'```{Func.numerate_list_as_text(perms, False)}```',
                                                      prefix='👧'),
                            edit_original_message=False,
                            ephemeral=True)
    elif type(error) == commands.errors.CommandOnCooldown:
        await send_callback(inter, embed=default_error_embed(inter,
                                                             Locales.ErrorCallbacks.cooldown_title[lang],
                                                             Locales.ErrorCallbacks.cooldown_desc[lang].format(
                                                                 timestamp=round(
                                                                     Func.get_current_timestamp() + error.retry_after)),
                                                             prefix='⚠️',
                                                             color=utils_config.warn_color),
                            ephemeral=True, edit_original_message=False)
    elif type(error) == UserInBlackList:
        description = Locales.ErrorCallbacks.user_in_black_list_desc[lang]
        block_reason = User.get_block_reason(inter.author.id)
        if block_reason not in ['', None, 'None']:
            description += f"\n\n```{Locales.Global.reason[lang]}: {block_reason}```"
        await send_callback(inter, embed=default_error_embed(inter,
                                                             Locales.ErrorCallbacks.user_in_black_list_title[lang],
                                                             description,
                                                             prefix='📃'))
    else:
        await send_callback(inter, embed=generate_embed(
            title=f"{Locales.ErrorCallbacks.unknown_error_title[lang]}",
            color=utils_config.error_color,
            description=Locales.ErrorCallbacks.unknown_error_desc[lang],
            footer=Func.generate_footer(inter, second_part='Unknown error'),
            footer_url=Func.generate_footer_url('user_avatar', inter.author), prefix=Func.generate_prefix('💀')))
        error_by = ''
        if inter is not None:
            try:
                error_by += f'**Guild:** `{inter.guild.name}`|`[{inter.guild.id}]`\n'
            except:
                pass
            error_by += f'**User:** {inter.user}|`[{inter.user.id}]`\n'
        description = f'{error_by}' \
                      f'```{error}```'
        discohook_embed = discord_webhook.DiscordEmbed(title='Debugger',
                                                       description=description,
                                                       color=utils_config.error_color)
        try:
            raise error
        except Exception as e:
            await send_webhook_embed(config.DEBUGGER_WEBHOOK, discohook_embed, username=str(inter.client.user),
                                     avatar_url=inter.client.user.avatar.url,
                                     content='<@&1106677021691613205>',
                                     file_content=traceback.format_exc())
        raise error


async def cant_play_with_yourself_duel(inter):
    lang = User.get_language(inter.author.id)
    await send_callback(inter, embed=generate_embed(
        title=Locales.ErrorCallbacks.cant_play_with_yourself_duel_title[lang],
        description=Locales.ErrorCallbacks.cant_play_with_yourself_duel_desc[lang],
        prefix=Func.generate_prefix('❌'),
        inter=inter,
        color=utils_config.error_color
    ))


async def bot_as_opponent_duel(inter):
    lang = User.get_language(inter.author.id)
    await send_callback(inter, embed=generate_embed(
        title=Locales.ErrorCallbacks.bot_as_opponent_duel_title[lang],
        description=Locales.ErrorCallbacks.bot_as_opponent_duel_desc[lang],
        prefix=Func.generate_prefix('❌'),
        inter=inter,
        color=utils_config.error_color
    ))


async def cant_breed_with_yourself(inter):
    lang = User.get_language(inter.author.id)
    await send_callback(inter,
                        embed=default_error_embed(inter,
                                                  Locales.ErrorCallbacks.cant_breed_with_yourself_title[lang],
                                                  Locales.ErrorCallbacks.cant_breed_with_yourself_desc[lang]))


async def bot_as_partner_breed(inter):
    lang = User.get_language(inter.author.id)
    await send_callback(inter, embed=generate_embed(
        title=Locales.ErrorCallbacks.bot_as_partner_breed_title[lang],
        description=Locales.ErrorCallbacks.bot_as_partner_breed_desc[lang],
        prefix=Func.generate_prefix('❌'),
        inter=inter,
        color=utils_config.error_color
    ))


# async def cant_play_with_yourself_duel(inter):
#     lang = User.get_language(inter.author.id)
#     await send_callback(inter, embed=embeds.cant_play_with_yourself_duel(inter, lang))


async def not_enough_money(inter, minimum_money=None, ephemeral: bool = True, edit_original_message: bool = False):
    lang = User.get_language(inter.author.id)
    desc = Locales.ErrorCallbacks.not_enough_money_desc[lang]
    if minimum_money is not None:
        desc += f'\n\n*{Locales.Global.need[lang]}: **{minimum_money}** 🪙*'
    await send_callback(inter, embed=generate_embed(
        title=Locales.ErrorCallbacks.not_enough_money_title[lang],
        description=desc,
        prefix=Func.generate_prefix('💸'),
        inter=inter,
        color=utils_config.error_color
    ), ephemeral=ephemeral, edit_original_message=edit_original_message)


async def no_item(inter):
    lang = User.get_language(inter.author.id)
    await send_callback(inter, embed=generate_embed(
        title=Locales.ErrorCallbacks.no_item_title[lang],
        description=f"{Locales.ErrorCallbacks.no_item_desc[lang]}",
        prefix=Func.generate_prefix('❌'),
        inter=inter,
        color=utils_config.error_color
    ), ephemeral=True,
                        edit_original_message=False)


async def wrong_component_clicked(inter):
    lang = User.get_language(inter.author.id)
    await send_callback(inter, embed=generate_embed(
        title=Locales.ErrorCallbacks.wrong_component_clicked_title[lang],
        description=f"{Locales.ErrorCallbacks.wrong_component_clicked_desc[lang]}",
        prefix=Func.generate_prefix('error'),
        inter=inter,
        color=utils_config.error_color
    ),
                        edit_original_message=False, ephemeral=True)


async def modal_input_is_not_number(inter):
    lang = User.get_language(inter.author.id)
    await send_callback(inter, embed=generate_embed(
        title=Locales.ErrorCallbacks.modal_input_is_not_number_title[lang],
        description=f"{Locales.ErrorCallbacks.modal_input_is_not_number_desc[lang]}",
        prefix=Func.generate_prefix('error'),
        inter=inter,
        color=utils_config.error_color
    ), edit_original_message=False, ephemeral=True)
