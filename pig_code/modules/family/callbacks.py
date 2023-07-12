from ...core import *
from ...utils import *
from . import embeds
from . import components


async def create_family(inter, name, description, image_url, private, ask_to_join):
    await Botutils.pre_command_check(inter)
    lang = User.get_language(inter.author.id)
    family_id = User.get_family(inter.author.id)
    if family_id is not None and Family.exists(family_id):
        await error_callbacks.default_error_callback(inter,
                                                     title=Locales.Family.already_in_family_title[lang],
                                                     description=Locales.Family.already_in_family_desc[lang],
                                                     prefix='👨‍👩‍🧒')
        return
    if User.get_money(inter.author.id) < 500:
        await error_callbacks.not_enough_money(inter, 500, False, True)
        return
    Family.create(name, inter.author.id, description, image_url, private, ask_to_join)
    User.add_money(inter.author.id, -500)
    await send_callback(inter, embed=generate_embed(Locales.CreateFamily.scd_title[lang],
                                                    Locales.CreateFamily.scd_desc[lang].format(family=name),
                                                    prefix=Func.generate_prefix('👨‍👩‍🧒'),
                                                    inter=inter))


async def view_family(inter, family_id = None):
    await Botutils.pre_command_check(inter)
    lang = User.get_language(inter.author.id)
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
    await Botutils.pagination(inter, lang,
                              embeds=await Botutils.generate_list_embeds(inter, members, lang,
                                                                         select_item_component_id='view_profile',
                                                                         title=Family.get_name(family_id),
                                                                         list_type='family_members', prefix=''))

async def delete_family(inter):
    await Botutils.pre_command_check(inter)
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
    await send_callback(inter, embed=generate_embed(title=Locales.DeleteFamily.scd_title[lang], prefix=Func.generate_prefix('💥'),
                                                    description=Locales.DeleteFamily.scd_desc[lang],
                                                    inter=inter))


async def invite_family(inter):
    await Botutils.pre_command_check(inter)
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
    await send_callback(inter, embed=generate_embed(title=Locales.InviteFamily.invite_code_title[lang], prefix=Func.generate_prefix('🔗'),
                                                    description=Locales.InviteFamily.invite_code_desc[lang].format(
                                                        code=family_id),
                                                    inter=inter))


async def join_family(inter, family_id):
    await Botutils.pre_command_check(inter)
    lang = User.get_language(inter.author.id)
    if not Family.exists(family_id):
        await error_callbacks.default_error_callback(inter, Locales.Family.not_exist_title[lang],
                                                     Locales.Family.not_exist_desc[lang], prefix='🤔')
        return
    user_family_id = User.get_family(inter.author.id)
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
    await Botutils.pre_command_check(inter)
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


async def family_requests(inter, just_edit: bool = False, family_id = None, lang=None):
    if not just_edit:
        await Botutils.pre_command_check(inter)
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
    await Botutils.pagination(inter, lang, embed_thumbnail_file='bin/images/invite.png',
                              embeds=await Botutils.generate_list_embeds(inter,
                                                                         {family_id: list(
                                                                             Family.get_requests(family_id))},
                                                                         lang,
                                                                         empty_desc=Locales.FamilyRequests.empty[lang],
                                                                         select_item_component_id=f'view_profile_family_requests',
                                                                         title=f'',
                                                                         list_type='family_requests', prefix=''))


async def accept_user_to_family(inter, user_id, family_id, ephemeral: bool = False):
    lang = User.get_language(user_id)
    Family.add_member(family_id, user_id)
    Family.remove_request(family_id, user_id)
    await send_callback(inter, embed=generate_embed(Locales.Family.accept_user_title[lang],
                                                    Locales.Family.accept_user_desc[lang].format(user=await User.get_name(inter.client, user_id)),
                                                    inter=inter, prefix=Func.generate_prefix('🐷'),
                                                    thumbnail_file=Botutils.generate_user_pig(user_id)),
                        edit_original_message=True, ephemeral=ephemeral)
    message = await inter.original_response()
    if message.reference is not None:
        await family_requests(message.reference.cached_message, just_edit=True, family_id=family_id, lang=lang)


async def reject_user_to_family(inter, user_id, family_id, ephemeral: bool = True):
    lang = User.get_language(user_id)
    Family.remove_request(family_id, user_id)
    await send_callback(inter, embed=generate_embed(Locales.Family.reject_user_title[lang],
                                                    Locales.Family.reject_user_desc[lang].format(user=await User.get_name(inter.client, user_id)),
                                                    inter=inter, prefix=Func.generate_prefix('🐷'),
                                                    thumbnail_file=Botutils.generate_user_pig(user_id)),
                        edit_original_message=True, ephemeral=ephemeral,)
    message = await inter.original_response()
    if message.reference is not None:
        await family_requests(message.reference.cached_message, just_edit=True, family_id=family_id, lang=lang)
