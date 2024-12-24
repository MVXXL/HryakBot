import discord.app_commands

from ...core import *
from ..functions import Func, translate
from .main import send_callback, generate_embed
from . import error_callbacks
from ..db_api import *

if not config.GITHUB_PUBLIC_VERSION:
    from .hidden import *


class Utils:

    @staticmethod
    async def pre_command_check(inter, ephemeral=False, defer=True, language_check: bool = True,
                                owner_only: bool = False, allowed_users: list = None):
        User.register_user_if_not_exists(inter.user.id)
        if defer:
            try:
                await inter.response.defer(ephemeral=ephemeral)
            except:
                pass
        if inter.is_guild_integration() and inter.guild is not None and not inter.guild.chunked:
            try:
                await asyncio.wait_for(inter.guild.chunk(), timeout=5)
            except asyncio.TimeoutError:
                print("> Chunking took too long and was stopped")
        if inter.guild is not None:
            Guild.register_guild_if_not_exists(inter.guild.id)
        if not Stats.get_language_changed(inter.user.id) and language_check:
            lang = str(inter.locale)
            if lang in ['ru', 'uk']:
                lang = 'ru'
            else:
                lang = 'en'
            User.set_language(inter.user.id, lang)
            Stats.set_language_changed(inter.user.id, True)
            Pig.rename(inter.user.id, Func.generate_random_pig_name(User.get_language(inter.user.id)))
        if User.is_blocked(inter.user.id):
            raise UserInBlackList(inter.user)
        if owner_only and not await inter.client.is_owner(inter.user):
            raise NotBotOwner(inter.user)
        if allowed_users is not None and inter.user.id not in allowed_users:
            raise NotBotOwner(inter.user)
        for event_id, event_data in Events.get_events(inter.user.id).copy().items():
            Events.remove(inter.user.id, event_id)
            wait_for_btn = .7
            if event_data['expires_in'] is None or event_data['expires_in'] + event_data[
                'created'] > Func.get_current_timestamp():
                await Utils.event_callback(inter, event_data, wait_for_btn)

    @staticmethod
    async def event_callback(inter, event, wait_for_btn: float = .7):
        lang = User.get_language(inter.user.id)
        title = event['title'] if type(event['title']) != dict else translate(event['title'], lang)
        description = event['description'] if type(event['description']) != dict else translate(event['description'],
                                                                                                lang)
        embed = generate_embed(title=title,
                               description=description,
                               timestamp=event['created'],
                               inter=inter)
        components = [
            discord.ui.Button(
                custom_id='in;ok',
                style=discord.ButtonStyle.green,
                # emoji='✅',
                label=translate(Locales.Global.got_it_btn, lang),
                disabled=True
            )]
        message = await send_callback(inter, embed=embed, components=components)
        await asyncio.sleep(wait_for_btn)
        components[0].disabled = False
        message = await send_callback(message, embed=embed, components=components)
        while True:
            def check(interaction):
                if message is not None and interaction.message is not None and type(
                        interaction) == discord.interactions.Interaction:
                    right_message = message.id == interaction.message.id
                    return right_message
            interaction = await inter.client.wait_for('interaction',
                                                      check=check)
            if not Utils.check_if_right_user(interaction):
                continue
            if interaction.data.get('custom_id') == 'in;ok':
                await interaction.response.defer()
                break
            break

    @staticmethod
    async def confirm_message(inter, lang, description: str = '', image_url=None, ctx_message=False,
                              ephemeral: bool = False):
        message = await send_callback(inter, embed=generate_embed(
            title=translate(Locales.Global.are_you_sure, lang),
            description=description,
            prefix=Func.generate_prefix('❓'),
            image_url=image_url,
            inter=inter,
        ), ctx_message=ctx_message,
                                      ephemeral=ephemeral,
                                      components=[
                                          discord.ui.Button(
                                              label=translate(Locales.Global.yes, lang),
                                              custom_id='in;yes',
                                              # emoji='✅',
                                              style=discord.ButtonStyle.green
                                          ),
                                          discord.ui.Button(
                                              label=translate(Locales.Global.no, lang),
                                              custom_id='in;no',
                                              # emoji='❌',
                                              style=discord.ButtonStyle.red
                                          )
                                      ])

        def check(interaction):
            if message is not None and interaction.message is not None:
                right_message = message.id == interaction.message.id
                return right_message and Utils.check_if_right_user(interaction)

        interaction = await inter.client.wait_for('interaction', check=check)
        try:
            await interaction.response.defer(ephemeral=True)
        except discord.errors.HTTPException:
            return
        if interaction.data.get('custom_id') == 'in;yes':
            return True
        elif interaction.data.get('custom_id') == 'in;no':
            return False

    @staticmethod
    def generate_embeds_list_from_fields(fields: list, title: str = '', description: str = '',
                                         color=utils_config.main_color, fields_for_one: int = 25,
                                         thumbnail_url: str = None, footer: str = None,
                                         footer_url: str = None, timestamp: bool = True):
        fields_for_one -= 1
        embeds = []
        create_embed = lambda: generate_embed(title=title, color=color, description=description,
                                              thumbnail_url=thumbnail_url, footer=footer, footer_url=footer_url,
                                              timestamp=timestamp)
        embed = create_embed()
        for i, field in enumerate(fields, 1):
            embed.add_field(name=field['name'], value=field['value'], inline=field['inline'])
            if i % (fields_for_one + 1) == 0:
                embeds.append(embed)
                embed = create_embed()
        if len(fields) == 0 or i % (fields_for_one + 1) != 0:
            embeds.append(embed)
        return embeds

    @staticmethod
    def generate_select_components_for_pages(options: list, custom_id, placeholder, fields_for_one: int = 25,
                                             category=None):
        fields_for_one -= 1
        components = []
        generated_options = []

        if not options:
            return [components]

        def append_components(page: int = 1):
            components.append([
                discord.ui.Select(options=generated_options, custom_id=f'{custom_id};{category};{page}',
                                  placeholder=placeholder)])

        c = 1
        for i, option in enumerate(options, 1):
            generated_options.append(discord.SelectOption(
                label=option['label'],
                value=option['value'],
                emoji=option['emoji'],
                description=option['description']
            ))
            if i % (fields_for_one + 1) == 0:
                append_components(c)
                generated_options = []
                c += 1
        if generated_options:
            append_components(c)
        else:
            components.append([])
        return components

    @staticmethod
    def get_items_in_str_list(items_to_convert: dict, lang, add_prefixes: bool = True):
        list_res = []
        for item_id in items_to_convert:
            if type(items_to_convert[item_id]) == dict:
                if items_to_convert[item_id]["amount"] > 0:
                    list_res.append(
                        f'{Func.generate_prefix(Item.get_emoji(item_id)) if add_prefixes else ""}{Item.get_name(item_id, lang)} x{items_to_convert[item_id]["amount"]}')
            else:
                if items_to_convert[item_id] > 0:
                    list_res.append(
                        f'{Func.generate_prefix(Item.get_emoji(item_id)) if add_prefixes else ""}{Item.get_name(item_id, lang)} x{items_to_convert[item_id]}')
        return '\n'.join(list_res)

    @staticmethod
    async def generate_items_list_embeds(inter, _items, lang, empty_desc='Empty', title=None,
                                         prefix_emoji: str = '📦', description='', fields_for_one_page: int = 7,
                                         list_type: str = 'inventory', tradable_items_only: bool = False,
                                         select_item_component_id: str = 'item_select;inventory', sort=True,
                                         cat_as_title=False, client=None):
        complete_embeds = {}
        if sort:
            sorted_items = {}
            for cat in _items:
                if list_type == 'inventory':
                    sorted_items[cat] = sorted(_items[cat], key=lambda x: Item.get_type(x))
                elif list_type == 'wardrobe':
                    sorted_items[cat] = sorted(_items[cat], key=lambda x: Item.get_skin_type(x))
            if sorted_items:
                _items = sorted_items.copy()
            # elif list_type == 'shop':
            #     for cat in _items:
            #         sorted_items[cat] = sorted(_items[cat], key=lambda x: Item.get_market_price(x))
            #     _items = sorted_items.copy()
        if client is None:
            client = inter.client
        for cat, v in _items.items():
            item_fields = []
            options = []
            complete_embeds[cat] = {'embeds': []}
            select_item_placeholder = translate(Locales.Inventory.select_item_placeholder, lang)
            footer_first_part = ''
            for item in v:
                item_label_without_prefix = 'Unknown'
                option_desc = None
                emoji = None
                field_value = '----'
                if list_type in ['inventory', 'wardrobe']:
                    if tradable_items_only and not Item.is_tradable(item):
                        continue
                    if Item.exists(item):
                        field_value = ''
                        if Item.get_amount(item, inter.user.id) == 0:
                            continue
                        if list_type == 'inventory':
                            field_value += f'{translate(Locales.Global.rarity, lang)}: {Item.get_rarity(item, lang)}\n'
                            if Item.is_salable(item):
                                field_value += f'{translate(Locales.Global.cost_per_item, lang)}: {Item.get_sell_price(item)} {Item.get_emoji(Item.get_sell_price_currency(item))}'
                            else:
                                field_value += f'{translate(Locales.Global.type, lang)}: {Item.get_type(item, lang)}'
                        elif list_type == 'wardrobe':
                            field_value += f'{translate(Locales.Global.type, lang)}: {Item.get_skin_type(item, lang)}\n' \
                                           f'{translate(Locales.Global.rarity, lang)}: {Item.get_rarity(item, lang)}'
                        field_value = f'```{field_value}```'
                        after_prefix = f" x{Item.get_amount(item, inter.user.id)}"
                        item_label_without_prefix = f'{Item.get_name(item, lang)}'
                        emoji = Item.get_emoji(item)
                        option_desc = Func.cut_text(Item.get_description(item, lang), 100)
                elif list_type == 'shop':
                    field_value = f'```{translate(Locales.Global.price, lang)}: {Item.get_market_price(item)} {Item.get_emoji(Item.get_market_price_currency(item))}\n' \
                                  f'{translate(Locales.Global.rarity, lang)}: {Item.get_rarity(item, lang)}```'
                    after_prefix = f" x{Item.get_amount(item)}" if Item.get_amount(item) > 1 else ""
                    item_label_without_prefix = f'{Item.get_name(item, lang)}'
                    emoji = Item.get_emoji(item)
                    option_desc = Func.cut_text(Item.get_description(item, lang), 100)
                    footer_first_part = f'{translate(Locales.Global.balance, lang)}: {Item.get_amount('coins', inter.user.id)} 🪙'
                item_fields.append(
                    {
                        'name': f'{Func.generate_prefix(emoji, backticks=False)}{item_label_without_prefix}',
                        'value': field_value,
                        'inline': False,
                        'after_prefix': after_prefix})
                options.append(
                    {'label': item_label_without_prefix,
                     'value': f'{item}',
                     'emoji': emoji,
                     'description': option_desc
                     }
                )
            item_fields = Func.field_inline_alternation(item_fields)
            for field in item_fields:
                if field['inline'] is True:
                    field['name'] = Func.cut_text(field['name'], 15)
                field['name'] = f'{field['name']}{field['after_prefix']}'
            page_embeds = Utils.generate_embeds_list_from_fields(item_fields,
                                                                 description=description if item_fields else empty_desc,
                                                                 title=f'{Func.generate_prefix(prefix_emoji)}{title if not cat_as_title else cat}',
                                                                 fields_for_one=fields_for_one_page,
                                                                 footer=Func.generate_footer(inter,
                                                                                             first_part=footer_first_part),
                                                                 footer_url=Func.generate_footer_url('user_avatar',
                                                                                                     inter.user))
            page_components = Utils.generate_select_components_for_pages(options, select_item_component_id,
                                                                         select_item_placeholder, category=cat,
                                                                         fields_for_one=fields_for_one_page)
            for i, embed in enumerate(page_embeds):
                complete_embeds[cat]['embeds'].append({'embed': embed, 'components': page_components[i]})
        return complete_embeds

    @staticmethod
    async def generate_item_selected_embed(inter, lang, item_id, _type: str) -> discord.Embed:
        footer = Func.generate_footer(inter)
        footer_url = Func.generate_footer_url('user_avatar', inter.user)
        basic_info_desc = ''
        title = Item.get_name(item_id, lang)
        item_description = Item.get_description(item_id, lang)
        prefix = Func.generate_prefix(Item.get_emoji(item_id))
        embed_color = utils_config.rarity_colors[Item.get_rarity(item_id)]
        thumbnail_url = None
        if Item.get_type(item_id) == 'skin':
            # skin_type = Item.get_skin_type(item_id)
            preview_options = utils_config.default_pig['skins'].copy()
            preview_options = Pig.set_skin_to_options(preview_options, item_id.split('.')[0])
            thumbnail_url = await Utils.build_pig(tuple(preview_options.items()))
        elif await Item.get_image_path(item_id) is not None:
            thumbnail_url = await Item.get_image_path(item_id)
        if _type in ['inventory', 'wardrobe']:
            basic_info_desc += f'{translate(Locales.Global.amount, lang)}: **{Item.get_amount(item_id, inter.user.id)}**\n'
            basic_info_desc += f'{translate(Locales.Global.type, lang)}: **{Item.get_skin_type(item_id, lang) if Item.get_type(item_id) == "skin" else Item.get_type(item_id, lang)}**\n'
            basic_info_desc += f'{translate(Locales.Global.rarity, lang)}: **{Item.get_rarity(item_id, lang)}**'
            if Item.is_salable(item_id):
                basic_info_desc += f'\n{translate(Locales.Global.cost_per_item, lang)}: **{Item.get_sell_price(item_id)} {Item.get_emoji(Item.get_sell_price_currency(item_id))}**'
        elif _type == 'shop':
            if Item.get_amount(item_id) > 1:
                basic_info_desc += f'{translate(Locales.Global.amount, lang)}: **{Item.get_amount(item_id)}**\n'
            basic_info_desc += f'{translate(Locales.Global.price, lang)}: **{Item.get_market_price(item_id)} {Item.get_emoji(Item.get_market_price_currency(item_id))}**\n'
            basic_info_desc += f'{translate(Locales.Global.type, lang)}: **{Item.get_skin_type(item_id, lang) if Item.get_type(item_id) == "skin" else Item.get_type(item_id, lang)}**\n'
            basic_info_desc += f'{translate(Locales.Global.rarity, lang)}: **{Item.get_rarity(item_id, lang)}**'
        embed = generate_embed(
            title=title,
            description=basic_info_desc,
            prefix=prefix,
            footer=footer,
            footer_url=footer_url,
            timestamp=True,
            color=embed_color,
            thumbnail_url=thumbnail_url,
            fields=[{'name': f"📋 ⟩ {translate(Locales.Global.description, lang)}",
                     'value': f"*{item_description}*"}]
        )
        return embed

    @staticmethod
    async def send_promocodes_guild_message(guild: discord.Guild):
        members_count = len([i for i in guild.members if not i.bot])
        promocodes = []
        if members_count >= 30:
            promocodes.append(PromoCode.create(5, {'coins': 30}))
        elif members_count >= 100:
            promocodes.append(PromoCode.create(3, {'rare_case': 2}))
            promocodes.append(PromoCode.create(5, {'coins': 100}))
            promocodes.append(PromoCode.create(members_count // 5, {'coins': 30}))
        elif members_count > 500:
            promocodes.append(PromoCode.create(1, {'gold_body': 1}))
            promocodes.append(PromoCode.create(5, {'rare_case': 2}))
            promocodes.append(PromoCode.create(5, {'common_case': 3}))
            promocodes.append(PromoCode.create(members_count // 50, {'coins': 100}))
            promocodes.append(PromoCode.create(members_count // 10, {'coins': 50}))
        elif members_count > 1000:
            promocodes.append(PromoCode.create(1, {'gold_body': 1}))
            promocodes.append(PromoCode.create(1, {'gold_pupils': 1}))
            promocodes.append(PromoCode.create(5, {'rare_case': 2}))
            promocodes.append(PromoCode.create(5, {'common_case': 3}))
            promocodes.append(PromoCode.create(members_count // 50, {'coins': 100}))
            promocodes.append(PromoCode.create(members_count // 10, {'coins': 50}))
            promocodes.append(PromoCode.create(3, {'hollars': 20}))
        promocodes_text = ''
        for promocode in promocodes:
            promocodes_text += f'- {promocode}\n' \
                               f' > Содержимое: **{Utils.get_items_in_str_list(PromoCode.get_prise(promocode), "ru", add_prefixes=False)}**\n' \
                               f' > Макс. использований: **{PromoCode.max_uses(promocode)}**\n'
        await Utils.send_notification(guild.owner, title='Привет', prefix_emoji='🍖',
                                      description=f'*Вижу у вас неплохой сервер. В честь этого мы дарим вам промокоды для розыгрыша между участниками. Думаю это поможет поднять актив на сервере*\n\n'
                                                  f'**Вот промокоды:**\n'
                                                  f'{promocodes_text}')

    @staticmethod
    async def pagination(inter,
                         lang: str,
                         embeds,
                         message: discord.Message = None,
                         timeout: int = 180,
                         embed_thumbnail_url: str = None,
                         ctx_message: bool = False,
                         everyone_can_click: bool = False,
                         return_if_starts_with: list = None,
                         arrows: bool = True,
                         categories: bool = False,
                         ephemeral=False,
                         edit_original_response=True,
                         edit_followup: bool = False,
                         init_category=None,
                         init_page=1):
        if return_if_starts_with is None:
            return_if_starts_with = ['back_to_inventory', 'item_select']
        complete_embeds = {}
        current_page = init_page
        current_cat = None

        def set_thumbnail_if_not_none():
            if embed_thumbnail_url is not None:
                get_current_embed()['embed'].set_thumbnail(url=embed_thumbnail_url)

        def is_categorised_pages():
            try:
                return type(embeds) == dict and type(list(embeds.values())[0]) == dict and \
                    'embeds' in list(embeds.values())[0] and 'embed' in list(embeds.values())[0]['embeds'][0]
            except:
                return False

        def get_current_embed():
            if not is_categorised_pages():
                return embeds[list(embeds)[current_page - 1]]
            else:
                return embeds[current_cat]['embeds'][current_page - 1]

        def category_components():
            options = [discord.SelectOption(label=j, value=str(i), emoji='➡️' if current_cat == i else None) for i, j in
                       enumerate(embeds)]
            if is_categorised_pages():
                options = [discord.SelectOption(label=i, value=str(i), emoji='➡️' if current_cat == i else None) for i
                           in embeds]
            return discord.ui.Select(custom_id='in;choose_category',
                                     placeholder=translate(Locales.Global.choose_category, lang),
                                     options=options,
                                     row=3)

        def arrows_components():
            return [discord.ui.Button(
                style=discord.ButtonStyle.primary,
                emoji='◀',
                custom_id='in;previous',
                row=4
            ),
                discord.ui.Button(
                    style=discord.ButtonStyle.primary,
                    emoji='▶',
                    custom_id='in;next',
                    row=4
                )
            ]

        if is_categorised_pages():
            current_cat = list(embeds)[0]
            if init_category is not None and init_category in embeds:
                current_cat = init_category
            if len(embeds) > 1:
                for cat in embeds.copy():
                    for embed in embeds[cat]['embeds']:
                        embed['components'].append(category_components())
                        if len(embeds[cat]['embeds']) > 1:
                            embed['components'] += arrows_components()
                for i in embeds:
                    if len(embeds[i]['embeds']) > 1:
                        for j, embed in enumerate(embeds[i]['embeds']):
                            embed['embed'].set_footer(
                                text=f'📚 {translate(Locales.Global.page, lang)}: {j + 1}')
            elif len(embeds[list(embeds)[0]]['embeds']) > 1:
                for i, embed in enumerate(embeds[list(embeds)[0]]['embeds']):
                    embed['components'] += arrows_components()
                    embed['embed'].set_footer(text=f'📚 {translate(Locales.Global.page, lang)}: {i + 1}')


        else:
            for i, embed in enumerate(embeds):
                if type(embed) == discord.Embed:
                    complete_embeds[str(i)] = {'embed': embed,
                                               'components': []}
                elif type(embed) == str:
                    if type(embeds[embed]) == discord.Embed:
                        complete_embeds[embed] = {'embed': embeds[embed],
                                                  'components': []}
                    elif type(embeds[embed]) == dict:
                        complete_embeds[embed] = embeds[embed]
                elif type(embed) == dict:
                    complete_embeds[str(i)] = embed
            for i, embed in enumerate(complete_embeds.values()):
                if 'components' not in embed:
                    embed['components'] = []
                if len(embeds) > 1:
                    if categories:
                        embed['components'].append(category_components())
                    if arrows:
                        embed['components'] += arrows_components()
            embeds = complete_embeds.copy()
            for i, element in enumerate(embeds.values()):
                if arrows and len(embeds) > 1:
                    element['embed'].set_footer(
                        text=f'📚 {translate(Locales.Global.page, lang)}: {i + 1}',
                        icon_url=Func.generate_footer_url('user_avatar', inter.user))
        if is_categorised_pages():
            if len(embeds[current_cat]['embeds']) < current_page:
                current_page = 1
        else:
            if len(embeds) < current_page:
                current_page = 1
        set_thumbnail_if_not_none()
        message = await send_callback(inter if message is None else message, embed=get_current_embed()['embed'],
                                      components=get_current_embed()['components'],
                                      ctx_message=ctx_message, ephemeral=ephemeral,
                                      edit_original_response=edit_original_response, edit_followup=edit_followup)
        if message is None:
            try:
                message = await inter.original_response()
            except:
                pass

        def check(interaction):
            if message is not None and interaction.message is not None and type(
                    interaction) == discord.interactions.Interaction:
                right_message = message.id == interaction.message.id
                return right_message

        while True:
            try:
                interaction = await inter.client.wait_for('interaction',
                                                          check=check,
                                                          timeout=timeout)
                if not everyone_can_click and inter.user.id != interaction.user.id:
                    try:
                        await send_callback(interaction,
                                            embed=generate_embed(
                                                prefix=Func.generate_prefix('❌'),
                                                color=utils_config.error_color,
                                                title=Locales.Pagination.wrong_user_title[
                                                    User.get_language(interaction.user.id)],
                                                description=Locales.Pagination.wrong_user_desc[
                                                    User.get_language(interaction.user.id)],
                                                inter=inter),
                                            edit_original_response=False,
                                            ephemeral=True)
                    except:
                        pass
                    continue
            except asyncio.exceptions.TimeoutError as e:
                try:
                    set_thumbnail_if_not_none()
                    await message.edit(components=[Utils.generate_hide_button()])
                except:
                    pass
                return
            if type(interaction) != discord.interactions.Interaction:
                continue
            if interaction.data.get('custom_id') in ['in;next', 'in;previous', 'hide', 'in;choose_category']:
                try:
                    if not ephemeral:
                        await interaction.response.defer(ephemeral=True)
                except discord.errors.HTTPException:
                    return
            if interaction.data.get('custom_id') == 'in;next':
                embeds_num = len(embeds)
                if is_categorised_pages():
                    embeds_num = len(embeds[current_cat]['embeds'])
                current_page = Func.get_changed_page_number(embeds_num, current_page, 1)
            elif interaction.data.get('custom_id') == 'in;previous':
                embeds_num = len(embeds)
                if is_categorised_pages():
                    embeds_num = len(embeds[current_cat]['embeds'])
                current_page = Func.get_changed_page_number(embeds_num, current_page, -1)
            elif interaction.data.get('custom_id') == 'in;choose_category':
                if not is_categorised_pages():
                    current_page = int(interaction.data.get('values')[0]) + 1
                else:
                    current_cat = interaction.data.get('values')[0]
                    current_page = 1
            elif interaction.data.get('custom_id') == 'hide':
                return
            elif Func.startswith_list(interaction.data.get('custom_id'), return_if_starts_with):
                return
            else:
                continue
            embed = get_current_embed()['embed']
            components = get_current_embed()['components']
            for i in range(len(components)):
                try:
                    if components[i].custom_id == 'in;choose_category':
                        components[i] = category_components()
                except TypeError as e:
                    continue
            set_thumbnail_if_not_none()
            await send_callback(interaction if not ctx_message else message,
                                embed=embed,
                                components=components
                                )

    @staticmethod
    def generate_hide_button():
        hide_button = discord.ui.Button(
            style=discord.ButtonStyle.red,
            emoji='⛔',
            custom_id='hide',
        )
        return hide_button

    @staticmethod
    def get_not_compatible_skins(user_id, item_id):
        """Returns skins worn by the user that are not compatible with item_id"""
        pig = Pig.get(user_id)
        not_compatible_skins = []
        for _skin in pig['skins']:
            _skin = pig['skins'][_skin]
            if _skin is None:
                continue
            if Item.get_not_compatible_skins(item_id) is not None and (
                    item_id in Item.get_not_compatible_skins(_skin) or Item.get_skin_type(
                item_id) in Item.get_not_compatible_skins(_skin)):
                not_compatible_skins.append(_skin)
            elif Item.get_not_compatible_skins(item_id) is not None and (
                    Item.get_skin_type(_skin) in Item.get_not_compatible_skins(
                item_id) or _skin in Item.get_not_compatible_skins(item_id)):
                not_compatible_skins.append(_skin)
        return not_compatible_skins

    @staticmethod
    async def send_notification(user: discord.User, inter=None, title: str = None, description: str = None,
                                prefix_emoji: str = None, url_label: str = None, url: str = None,
                                send_to_dm: bool = True,
                                create_command_notification: bool = False, notification_id: str = None,
                                guild=None):
        """
        :type user: object
            User who will receive notification
        :param title:
            Title of notification
        :param description:
            Description of notification
        :param prefix_emoji:
            The prefix before title
        :param url_label:
            The button label containing url
        :param url:
            The URL that will be placed in the button below the message
        :param send_to_dm:
            If true it will try to send notification to user's dm
        :param create_command_notification:
            If true it will show notification next time when user will use the bot command
            (will not work if sending notification to dm was successful)
        :param notification_id:
            Needed for create_command_notification. If not specified, a random ID will be generated.
        :param guild:
            The notification will not be sent if both users are not in the specified guild
        """
        lang = User.get_language(user.id)
        embed = generate_embed(
            title=title,
            description=description,
            prefix=Func.generate_prefix(prefix_emoji),
            footer_url=Func.generate_footer_url('user_avatar', user),
            footer=Func.generate_footer(user=user)
        )
        components = []
        if url is not None:
            components.append(
                discord.ui.Button(style=discord.ButtonStyle.url,
                                  label=translate(url_label, lang),
                                  url=url)
            )
        dm_message = None
        if send_to_dm:
            if guild is None or (
                    guild.get_member(inter.user.id) is not None and guild.get_member(user.id) is not None):
                dm_message = await send_callback(None, embed=embed, components=components, send_to_dm=user)
        if create_command_notification:
            if dm_message is None:
                Events.add(user.id, title=title,
                           description=description, expires_in=100 * 3600,
                           event_id=notification_id)
        return

    @staticmethod
    def users_have_mutual_guilds(user1, user2) -> bool:
        """Will return true if user1 and user2 have any mutual guilds"""
        return bool(set(user1.mutual_guilds).intersection(set(user2.mutual_guilds)))

    @staticmethod
    def check_if_right_user(interaction, except_users: list = None):
        if except_users is None:
            except_users = []
        if interaction.user.id in except_users:
            return True
        return interaction.message.interaction.user.id == interaction.user.id

    @staticmethod
    async def generate_user_pig(user_id, eye_emotion: str = None, preview_items: dict = None):
        user_skin = Pig.get_skin(user_id, 'all')
        for k, v in user_skin.items():
            if Item.get_amount(v, user_id) <= 0:
                user_skin[k] = None
        if preview_items is not None:
            for item_id in preview_items.values():
                user_skin = Pig.set_skin_to_options(user_skin, item_id)
        final_pig = await Utils.build_pig(tuple(user_skin.items()),
                                          tuple(Pig.get_genetic(user_id, 'all').items()),
                                          eye_emotion=eye_emotion)
        return final_pig

    @staticmethod
    @aiocache.cached(ttl=86400)
    async def build_pig(skins: tuple, genetic: tuple = None, eye_emotion: str = None, remove_transparency: bool = True):
        """The actual code is hidden due to security reasons"""
        if config.GITHUB_PUBLIC_VERSION:
            return await Func.get_image_path_from_link(utils_config.image_links['image_is_blocked'])
        else:
            return await Hidden.build_pig(skins, genetic, eye_emotion, remove_transparency)

    @staticmethod
    def get_duel_winning_chances(user1, user2):
        """The actual code is hidden due to security reasons"""
        if config.GITHUB_PUBLIC_VERSION:
            return {user1: 50, user2: 50}
        else:
            return Hidden.get_duel_winning_chances(user1, user2)

    @staticmethod
    def get_trade_total_tax(trade_id):
        total_tax = {}
        for user_id in Trade.get_users(trade_id):
            for item_id in Trade.get_items(trade_id, user_id):
                item_tax = Utils.calculate_item_tax(item_id, user_id)
                if item_tax[1] not in total_tax:
                    total_tax[item_tax[1]] = 0
                total_tax[item_tax[1]] += Trade.get_item_amount(trade_id, user_id, item_id) * item_tax[0]
        return {k: math.ceil(v) for k, v in total_tax.items() if v > 0}

    @staticmethod
    def get_user_wealth(user_id):
        wealth = {}
        for item_id in User.get_inventory(user_id):
            if Item.get_wealth_impact(item_id) is not None and Item.get_market_price(item_id) is not None:
                if Item.get_market_price_currency(item_id) not in wealth:
                    wealth[Item.get_market_price_currency(item_id)] = 0
                wealth[Item.get_market_price_currency(item_id)] += Item.get_amount(item_id,
                                                                                   user_id) * Item.get_market_price(
                    item_id) * Item.get_wealth_impact(item_id)
        return wealth

    @staticmethod
    def get_user_tax_percent(user_id, currency: str):
        """The actual code is hidden due to security reasons"""
        if config.GITHUB_PUBLIC_VERSION:
            return 5
        else:
            return Hidden.get_user_tax_percent(user_id, currency, Utils.get_user_wealth(user_id))

    @staticmethod
    def calculate_item_tax(item_id, user_id):
        tax = Item._get_tax(item_id)
        if tax is None:
            return [0, "coins"]
        elif isinstance(tax, list):
            return tax
        elif tax == 'auto':
            return [round(Item.get_market_price(item_id) * (
                        Utils.get_user_tax_percent(user_id, Item.get_market_price_currency(item_id)) / 100), 3),
                    Item.get_market_price_currency(item_id)]
        elif tax.endswith('%'):
            return [round(Item.get_market_price(item_id) * (float(tax[:-1]) / 100), 3),
                    Item.get_market_price_currency(item_id)]


    @staticmethod
    def get_transfer_amount_with_tax(amount, tax):
        amount_with_tax = math.ceil(amount + amount * (tax / 100))
        return amount_with_tax

    @staticmethod
    async def calculate_buff_multipliers(client, user_id, use_buffs: bool = False):
        res = utils_config.base_buff_multipliers.copy()
        pig_buffs = await Utils.get_all_pig_buffs(client, user_id)
        pig_buffs_raw = {i: [] for i in res.copy()}
        for buff in pig_buffs:
            if use_buffs and buff in ['laxative', 'compound_feed']:
                Pig.remove_buff(user_id, buff)
            for multiplier_name, multiplier in pig_buffs[buff].items():
                pig_buffs_raw[multiplier_name].append(multiplier)
        pig_buffs_raw = {k: sorted(v, key=lambda x: x.startswith('x')) for k, v in pig_buffs_raw.items()}
        for multiplier_name in pig_buffs_raw:
            for multiplier in pig_buffs_raw[multiplier_name]:
                digit_multiplier = float(multiplier[1:])
                match multiplier[0]:
                    case 'x':
                        res[multiplier_name] *= digit_multiplier
                    case '+':
                        res[multiplier_name] += digit_multiplier
                    case '-':
                        res[multiplier_name] -= digit_multiplier
        res = {k: round(v, 2) for k, v in res.items()}
        return res

    @staticmethod
    async def get_all_pig_buffs(client, user_id):
        buffs = {}
        for buff in Pig.get_buffs(user_id):
            if Pig.get_buff_amount(user_id, buff) > 0 or not Pig.buff_expired(user_id, buff):
                buffs[buff] = Item.get_buffs(buff)
            for i in config.BOT_GUILDS:
                bot_guild = client.get_guild(i)
                if bot_guild is not None:
                    if bot_guild.get_member(user_id) is not None:
                        buffs['support_server'] = {'weight': 'x1.05'}
        buffs['pig_weight'] = {}
        pchip_function = PchipInterpolator(np.array([0, 50, 100, 500, 5000, 20000, 1000000]),
                                           np.array([0, .5, 1, 5, 15, 20, 30]))
        buffs['pig_weight']['pooping'] = f'+{round(float(pchip_function(Pig.get_weight(user_id))), 2)}'
        pchip_function = PchipInterpolator(np.array([0, 20, 50, 1000, 10000, 1000000]),
                                           np.array([0, 0, 1, 1.5, 2, 10]))
        buffs['pig_weight']['vomit_chance'] = f'x{round(float(pchip_function(Pig.get_weight(user_id))), 2)}'
        return buffs

    @staticmethod
    def calculate_missed_streak_days(user_id):
        return (Func.get_current_timestamp() - History.get_last_streak_timestamp(user_id)) // utils_config.streak_timeout

    @staticmethod
    def filter_users(client, users, is_on_server: int):
        result = []
        guild = client.get_guild(is_on_server)
        for user_id in users:
            if is_on_server:
                if guild.get_member(int(user_id)) is not None:
                    result.append(user_id)
        return result

    @staticmethod
    async def profile_embed(inter, lang, user: discord.User = None, info: list = None,
                            thumbnail_url=None) -> discord.Embed:
        if user is None:
            user = inter.user
        description = ''
        if 'user' in info:
            rating_status = ''
            rating_number = User.get_rating_total_number(user.id)
            if rating_number > 0:
                rating_status = '💚'
            elif rating_number < 0:
                rating_status = '⚠️'
            description += translate(Locales.Profile.user_profile_desc, lang,
                                     format_options={'coins': Item.get_amount('coins', user.id),
                                                     'hollars': Item.get_amount('hollars', user.id),
                                                     'likes': rating_number,
                                                     'rating_status': rating_status}) + '\n\n'
        if 'pig' in info:
            description += translate(Locales.Profile.pig_profile_desc, lang,
                                     format_options={'pig_name': Pig.get_name(user.id),
                                                     'weight': Pig.get_weight(user.id),
                                                     'age': Pig.age(user.id, lang)}) + '\n\n'
        embed = generate_embed(
            title=translate(Locales.Profile.profile_title, lang, {'user': user.display_name}),
            description=description,
            prefix=Func.generate_prefix('🐽'),
            thumbnail_url=thumbnail_url,
            footer=Func.generate_footer(inter, second_part=f'{Stats.get_streak(user.id)} 🔥'),
            inter=inter,
        )
        return embed

    @staticmethod
    def bool_command_choice():
        choices = [
            discord.app_commands.Choice(name=locale_str('true'), value='true'),
            discord.app_commands.Choice(name=locale_str('false'), value='false')
        ]
        return choices
