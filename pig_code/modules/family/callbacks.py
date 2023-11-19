from ...core import *
from ...utils import *
from . import embeds
from . import components


async def create_family(inter, name, description, image_url, private, ask_to_join):
    await BotUtils.pre_command_check(inter)
    lang = User.get_language(inter.author.id)
    family_id = User.get_family(inter.author.id)
    if family_id is not None and Family.exists(family_id):
        await error_callbacks.default_error_callback(inter,
                                                     title=translate(Locales.Family.already_in_family_title, lang),
                                                     description=translate(Locales.Family.already_in_family_desc, lang),
                                                     prefix='👨‍👩‍🧒')
        return
    if Item.get_amount('coins', inter.author.id) < 500:
        await error_callbacks.not_enough_money(inter, 500, True, False)
        return
    Family.create(name, inter.author.id, description, image_url, private, ask_to_join)
    User.remove_item(inter.author.id, 'coins', 500)
    await send_callback(inter, embed=generate_embed(translate(Locales.CreateFamily.scd_title, lang),
                                                    translate(Locales.CreateFamily.scd_desc, lang, format_options={'family': name}),
                                                    prefix=Func.generate_prefix('👨‍👩‍🧒'),
                                                    inter=inter))


async def view_family(inter, family_id=None, edit_only: bool = False, lang=None, client=None):
    if not edit_only:
        await BotUtils.pre_command_check(inter)
    if lang is None:
        lang = User.get_language(inter.author.id)
    if not edit_only:
        if not Family.exists(family_id) and family_id is not None:
            await error_callbacks.default_error_callback(inter, Locales.Family.not_exist_title[lang],
                                                         Locales.Family.not_exist_desc[lang], prefix='🤔')
            return
        if family_id is None:
            family_id = User.get_family(inter.author.id)
            if family_id is None or not Family.exists(family_id):
                await error_callbacks.default_error_callback(inter, Locales.ViewFamily.no_family_title[lang],
                                                             Locales.ViewFamily.no_family_desc[lang], prefix='😢')
                return
    members = {family_id: Family.get_members(family_id)}
    family_description = Family.get_description(family_id)
    description = ''
    if family_description is not None and family_description:
        description += f'> {Family.get_description(family_id)}\n'
    await BotUtils.pagination(inter, lang,
                              embeds=await BotUtils.generate_items_list_embeds(inter, members, lang,
                                                                               description=description,
                                                                               fields_for_one_page=7,
                                                                               select_item_component_id='family;view_profile',
                                                                               title=Family.get_name(family_id),
                                                                               client=client,
                                                                               list_type='family_members', prefix=''),
                              embed_thumbnail_url=Family.get_image(family_id))


# async def public_families(inter):
#     await Botutils.pre_command_check(inter)
#     lang = User.get_language(inter.author.id)
#     print(Family.get_public_families())
#     families = Family.get_public_families()
#     print(Family.get_public_families())
#     family_description = Family.get_description(family_id)
#     description = ''
#     if family_description is not None and family_description:
#         description += f'> {Family.get_description(family_id)}\n'
#     await Botutils.pagination(inter, lang,
#                               embeds=await Botutils.generate_list_embeds(inter, members, lang,
#                                                                          description=description,
#                                                                          fields_for_one=7,
#                                                                          select_item_component_id='view_profile',
#                                                                          title=Family.get_name(family_id),
#                                                                          list_type='family_members', prefix=''))

async def delete_family(inter):
    await BotUtils.pre_command_check(inter)
    lang = User.get_language(inter.author.id)
    family_id = User.get_family(inter.author.id)
    if family_id is None or not Family.exists(family_id):
        await error_callbacks.default_error_callback(inter, Locales.Family.no_family_title[lang],
                                                     Locales.Family.no_family_desc[lang], prefix='😢')
        return
    if Family.get_member_role(family_id, inter.author.id) != 'owner':
        await error_callbacks.default_error_callback(inter,
                                                     title=Locales.DeleteFamily.not_owner_title[lang],
                                                     description=Locales.DeleteFamily.not_owner_desc[lang],
                                                     prefix='👑')
        return
    members = Family.get_members(family_id)
    for member in members:
        Family.remove_member(family_id, member)
    Family.delete(family_id)
    await send_callback(inter, embed=generate_embed(title=Locales.DeleteFamily.scd_title[lang],
                                                    prefix=Func.generate_prefix('💥'),
                                                    description=Locales.DeleteFamily.scd_desc[lang],
                                                    inter=inter))


async def change_family_settings(inter, name, description, image_url, private, ask_to_join):
    await BotUtils.pre_command_check(inter)
    lang = User.get_language(inter.author.id)
    family_id = User.get_family(inter.author.id)
    if family_id is None or not Family.exists(family_id):
        await error_callbacks.default_error_callback(inter,
                                                     title=Locales.ChangeFamilySettings.no_family_title[lang],
                                                     description=Locales.ChangeFamilySettings.no_family_desc[lang],
                                                     prefix='👨‍👩‍🧒')
        return
    if Family.get_member_role(family_id, inter.author.id) != 'owner':
        await error_callbacks.default_error_callback(inter,
                                                     title=Locales.ChangeFamilySettings.not_owner_title[lang],
                                                     description=Locales.ChangeFamilySettings.not_owner_desc[lang],
                                                     prefix='👑')
        return
    if name is not None:
        Family.set_name(family_id, name)
    if description is not None:
        Family.set_description(family_id, description)
    if image_url is not None:
        Family.set_image(family_id, image_url)
    if private is not None:
        Family.set_private(family_id, private)
    if ask_to_join is not None:
        Family.set_ask_to_join(family_id, ask_to_join)
    await send_callback(inter, embed=generate_embed(Locales.ChangeFamilySettings.scd_title[lang],
                                                    Locales.ChangeFamilySettings.scd_desc[lang].format(family=name),
                                                    prefix=Func.generate_prefix('⚙️'),
                                                    inter=inter))


async def invite_family(inter):
    await BotUtils.pre_command_check(inter)
    lang = User.get_language(inter.author.id)
    family_id = User.get_family(inter.author.id)
    if family_id is None or not Family.exists(family_id):
        await error_callbacks.default_error_callback(inter,
                                                     title=Locales.InviteFamily.no_family_title[lang],
                                                     description=Locales.InviteFamily.no_family_desc[lang],
                                                     prefix='👨‍👩‍🧒')
        return
    if Family.get_member_role(family_id, inter.author.id) not in ['owner']:
        await error_callbacks.default_error_callback(inter,
                                                     title=Locales.InviteFamily.not_owner_title[lang],
                                                     description=Locales.InviteFamily.not_owner_desc[lang],
                                                     prefix='👑')
        return
    await send_callback(inter, embed=generate_embed(title=Locales.InviteFamily.invite_code_title[lang],
                                                    prefix=Func.generate_prefix('🔗'),
                                                    description=Locales.InviteFamily.invite_code_desc[lang].format(
                                                        code=family_id),
                                                    inter=inter))


async def join_family(inter, family_id):
    await BotUtils.pre_command_check(inter)
    lang = User.get_language(inter.author.id)
    if not Family.exists(family_id):
        await error_callbacks.default_error_callback(inter, Locales.Family.not_exist_title[lang],
                                                     Locales.Family.not_exist_desc[lang], prefix='🤔')
        return
    user_family_id = User.get_family(inter.author.id)
    if Family.is_user_banned(family_id, inter.author.id):
        await error_callbacks.default_error_callback(inter,
                                                     title=Locales.Family.user_banned_title[lang],
                                                     description=Locales.Family.user_banned_desc[lang],
                                                     prefix='🤔')
        return
    if user_family_id is not None and Family.exists(user_family_id):
        await error_callbacks.default_error_callback(inter,
                                                     title=Locales.Family.already_in_family_title[lang],
                                                     description=Locales.Family.already_in_family_desc[lang],
                                                     prefix='👨‍👩‍🧒')
        return
    if not Family.is_ask_to_join(family_id):
        Family.add_member(family_id, inter.author.id)
        await send_callback(inter, embed=generate_embed(title=Locales.JoinFamily.scd_title[lang],
                                                        description=Locales.JoinFamily.scd_desc[lang].format(
                                                            family=Family.get_name(family_id)),
                                                        inter=inter, prefix=Func.generate_prefix('👨‍👩‍🧒')))
    else:
        owner = await User.get_user(inter.client, Family.get_owner(family_id))
        owner_lang = User.get_language(owner.id)
        dm_message = await send_callback(inter, send_to_dm=owner,
                                         embed=generate_embed(Locales.JoinFamily.dm_join_request_title[owner_lang],
                                                              Locales.JoinFamily.dm_join_request_desc[
                                                                  owner_lang].format(user=inter.author.display_name,
                                                                                     family=Family.get_name(family_id)),
                                                              inter=inter, prefix=Func.generate_prefix('🐽')),
                                         components=components.accept_reject_user_to_family(lang, inter.author.id,
                                                                                            family_id))
        Family.add_request(family_id, inter.author.id)
        await send_callback(inter, embed=generate_embed(Locales.JoinFamily.request_sent_title[lang],
                                                        Locales.JoinFamily.request_sent_desc[lang].format(
                                                            user=inter.author.display_name,
                                                            family=Family.get_name(family_id)),
                                                        inter=inter, prefix=Func.generate_prefix('🐽')))


async def leave_family(inter):
    await BotUtils.pre_command_check(inter)
    lang = User.get_language(inter.author.id)
    family_id = User.get_family(inter.author.id)
    if family_id is None or not Family.exists(family_id):
        await error_callbacks.default_error_callback(inter,
                                                     title=Locales.LeaveFamily.no_family_title[lang],
                                                     description=Locales.LeaveFamily.no_family_desc[lang],
                                                     prefix='👨‍👩‍🧒')
        return
    if Family.get_member_role(family_id, inter.author.id) == 'owner' and Family.exists(family_id):
        await error_callbacks.default_error_callback(inter,
                                                     title=Locales.LeaveFamily.owner_title[lang],
                                                     description=Locales.LeaveFamily.owner_desc[lang],
                                                     prefix='👑')
        return
    Family.remove_member(User.get_family(inter.author.id), inter.author.id)
    await send_callback(inter, embed=generate_embed(title=Locales.LeaveFamily.scd_title[lang],
                                                    description=Locales.LeaveFamily.scd_desc[lang].format(
                                                        family=Family.get_name(family_id)),
                                                    inter=inter, prefix=Func.generate_prefix('🥖')))


async def family_requests(inter, just_edit: bool = False, family_id=None, lang=None, client=None):
    if not just_edit:
        await BotUtils.pre_command_check(inter)
    if lang is None:
        lang = User.get_language(inter.author.id)
    if family_id is None:
        family_id = User.get_family(inter.author.id)
    if not just_edit:
        if family_id is None or not Family.exists(family_id):
            await error_callbacks.default_error_callback(inter,
                                                         title=Locales.Family.no_family_title[lang],
                                                         description=Locales.Family.no_family_desc[lang],
                                                         prefix='👨‍👩‍🧒')
            return
        if Family.get_member_role(family_id, inter.author.id) not in ['owner']:
            await error_callbacks.default_error_callback(inter,
                                                         title=Locales.FamilyRequests.not_owner_title[lang],
                                                         description=Locales.FamilyRequests.not_owner_desc[lang],
                                                         prefix='👑')
            return
    await BotUtils.pagination(inter, lang, embed_thumbnail_file=Func.get_image_path_from_link(utils_config.image_links['invite']),
                              embeds=await BotUtils.generate_items_list_embeds(inter,
                                                                               {family_id: list(
                                                                             Family.get_requests(family_id))},
                                                                               lang,
                                                                               empty_desc=Locales.FamilyRequests.empty[lang],
                                                                               select_item_component_id=f'family;join_requests;view_profile',
                                                                               title=f'',
                                                                               list_type='family_requests', prefix='',
                                                                               client=client))


async def family_profile(inter, user_id):
    lang = User.get_language(user_id)
    family_id = User.get_family(user_id)
    profile_components = None
    if Family.get_member_role(family_id, inter.author.id) in ['owner'] and Family.get_member_role(family_id,
                                                                                                  user_id) not in [
        'owner']:
        profile_components = [disnake.ui.Button(label=Locales.Global.kick[lang],
                                                style=disnake.ButtonStyle.red,
                                                custom_id=f'family;kick_user;{user_id};{family_id}'),
                              disnake.ui.Button(label=Locales.Global.ban[lang],
                                                style=disnake.ButtonStyle.red,
                                                custom_id=f'family;ban_user;{user_id};{family_id}')]
    await send_callback(inter,
                        embed=BotUtils.profile_embed(inter, lang, await User.get_user(inter.client, user_id), ['user', 'pig', 'family']),
                        components=profile_components,
                        edit_original_message=False, ephemeral=True)


async def family_member_kick(inter, user_id, family_id):
    lang = User.get_language(user_id)
    Family.remove_member(family_id, user_id)
    await send_callback(inter,
                        embed=generate_embed(Locales.FamilyMemberKick.scd_title[lang],
                                             Locales.FamilyMemberKick.scd_desc[lang].format(
                                                 user=await User.get_name(inter.client, user_id)),
                                             inter=inter, prefix=Func.generate_prefix('🦵'),
                                             thumbnail_file=BotUtils.generate_user_pig(user_id, eye_emotion='sad')),
                        edit_original_message=True, ephemeral=True)
    message = await inter.original_response()
    if message.reference is not None:
        await view_family(message.reference.cached_message, edit_only=True, family_id=family_id, lang=lang,
                          client=inter.client)


async def family_member_ban(inter, user_id, family_id):
    lang = User.get_language(user_id)
    Family.ban_member(family_id, user_id)
    await send_callback(inter,
                        embed=generate_embed(Locales.FamilyMemberBan.scd_title[lang],
                                             Locales.FamilyMemberBan.scd_desc[lang].format(
                                                 user=await User.get_name(inter.client, user_id)),
                                             inter=inter, prefix=Func.generate_prefix('🔨'),
                                             thumbnail_file=BotUtils.generate_user_pig(user_id, eye_emotion='angry')),
                        edit_original_message=True, ephemeral=True)
    message = await inter.original_response()
    if message.reference is not None:
        await view_family(message.reference.cached_message, edit_only=True, family_id=family_id, lang=lang,
                          client=inter.client)


async def accept_user_to_family(inter, user_id, family_id, ephemeral: bool = False):
    lang = User.get_language(inter.author.id)
    Family.add_member(family_id, user_id)
    Family.remove_request(family_id, user_id)
    await send_callback(inter, embed=generate_embed(Locales.Family.accept_user_title[lang],
                                                    Locales.Family.accept_user_desc[lang].format(
                                                        user=await User.get_name(inter.client, user_id)),
                                                    inter=inter, prefix=Func.generate_prefix('🐷'),
                                                    thumbnail_file=BotUtils.generate_user_pig(user_id)),
                        edit_original_message=True, ephemeral=ephemeral)
    message = await inter.original_response()
    if message.reference is not None:
        await family_requests(message.reference.cached_message, just_edit=True, family_id=family_id, lang=lang,
                              client=inter.client)


async def reject_user_to_family(inter, user_id, family_id, ephemeral: bool = True):
    lang = User.get_language(inter.author.id)
    Family.remove_request(family_id, user_id)
    await send_callback(inter, embed=generate_embed(Locales.Family.reject_user_title[lang],
                                                    Locales.Family.reject_user_desc[lang].format(
                                                        user=await User.get_name(inter.client, user_id)),
                                                    inter=inter, prefix=Func.generate_prefix('🐷'),
                                                    thumbnail_file=BotUtils.generate_user_pig(user_id)),
                        edit_original_message=True, ephemeral=ephemeral, )
    message = await inter.original_response()
    if message.reference is not None:
        await family_requests(message.reference.cached_message, just_edit=True, family_id=family_id, lang=lang,
                              client=inter.client)
