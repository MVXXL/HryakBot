from disnake import OptionChoice

from ...core import *
from .main import send_callback, generate_embed
from . import error_callbacks
from ..functions import Func
from ..db_api import *


class BotUtils:

    @staticmethod
    async def pre_command_check(inter, ephemeral=False, defer=True, language_check: bool = True):
        if defer:
            try:
                await inter.response.defer(ephemeral=ephemeral)
            except:
                pass
        User.register_user_if_not_exists(inter.author.id)
        Pig.create_pig_if_no_pig(inter.author.id)
        if User.is_blocked(inter.author.id):
            raise UserInBlackList(inter.author)
        commands_used = Stats.get_total_commands_used(inter.author.id)
        if not Stats.get_language_changed(inter.author.id) and language_check:
            await BotUtils.choose_language_callback(inter, 'en')
            Stats.set_language_changed(inter.author.id, True)
        elif commands_used == 17:
            await BotUtils.rate_bot_callback(inter)
        else:
            for event_id, event_data in Events.get_events(inter.author.id).copy().items():
                Events.remove(inter.author.id, event_id)
                wait_for_btn = .7
                if event_data['expires_in'] is None or event_data['expires_in'] + event_data[
                    'created'] > Func.get_current_timestamp():
                    await BotUtils.event_callback(inter, event_data, wait_for_btn)

    @staticmethod
    async def choose_language_callback(inter, lang):
        message = await send_callback(inter,
                                      embed=generate_embed(
                                          title=Locales.ChooseLanguage.title[lang],
                                          description=Locales.ChooseLanguage.desc[lang],
                                          prefix=Func.generate_prefix('🏴‍☠️'),
                                          inter=inter),
                                      components=disnake.ui.Select(custom_id='select_lang',
                                                                   placeholder=
                                                                   Locales.ChooseLanguage.placeholder[lang],
                                                                   options=[disnake.SelectOption(
                                                                       label=bot_locale.full_names[i], value=i)
                                                                       for i in
                                                                       bot_locale.valid_discord_locales]))

        def check(interaction):
            try:
                return message.id == interaction.message.id
            except:
                return False

        while True:
            interaction = await inter.client.wait_for('interaction',
                                                      check=check
                                                      )
            if not BotUtils.check_if_right_user(interaction):
                continue
            if interaction.component.custom_id == 'select_lang':
                User.set_language(inter.author.id, interaction.values[0])
                break

    @staticmethod
    async def event_callback(inter, event, wait_for_btn: float = .7):
        lang = User.get_language(inter.author.id)
        title = event['title'] if type(event['title']) != dict else event['title'][lang]
        description = event['description'] if type(event['description']) != dict else event['description'][lang]
        embed = generate_embed(title=title,
                               description=description,
                               timestamp=event['created'],
                               inter=inter)
        components = [
            disnake.ui.Button(
                custom_id='ok',
                style=disnake.ButtonStyle.green,
                # emoji='✅',
                label=Locales.Global.got_it_btn[lang],
            )]
        message = await send_callback(inter, embed=embed)
        await asyncio.sleep(wait_for_btn)
        message = await send_callback(message, embed=embed, components=components)
        while True:
            interaction = await inter.client.wait_for('button_click',
                                                      check=lambda interaction: message.id == interaction.message.id)
            if not BotUtils.check_if_right_user(interaction):
                continue
            if interaction.component.custom_id == 'ok':
                await interaction.response.defer()
                break
            break

    @staticmethod
    async def rate_bot_callback(inter):
        lang = User.get_language(inter.author.id)
        message = await send_callback(inter,
                                      embed=generate_embed(
                                          title=Locales.RateBot.title[lang],
                                          description=Locales.RateBot.desc[lang],
                                          prefix=Func.generate_prefix('🏴‍☠️'),
                                          inter=inter),
                                      components=[
                                          disnake.ui.Button(style=disnake.ButtonStyle.link,
                                                            url='https://bots.server-discord.com/1102273144733049003',
                                                            label=Locales.RateBot.support_btn[lang],
                                                            ),
                                          disnake.ui.Button(
                                              custom_id='rate_later',
                                              style=disnake.ButtonStyle.grey,
                                              # url='https://bots.server-discord.com/1102273144733049003',
                                              label=Locales.RateBot.later_btn[lang],
                                          )
                                      ])
        while True:
            interaction = await inter.client.wait_for('button_click',
                                                      check=lambda interaction: message.id == interaction.message.id)
            if not BotUtils.check_if_right_user(interaction):
                continue
            if interaction.component.custom_id == 'rate_later':
                await interaction.response.defer()
                break
            break

    @staticmethod
    def check_pig_feed_cooldown(user: disnake.User):
        if Pig.get_last_feed(user.id) is not None:
            if Func.get_current_timestamp() < Pig.get_time_of_next_feed(user.id):
                raise PigFeedCooldown

    @staticmethod
    def check_pig_meat_cooldown(user: disnake.User):
        if Pig.get_last_meat(user.id) is not None:
            if Func.get_current_timestamp() < Pig.get_time_of_next_meat(user.id):
                raise PigMeatCooldown

    @staticmethod
    def check_pig_breed_cooldown(user: disnake.User):
        if Pig.get_last_breed(user.id) is not None:
            if Func.get_current_timestamp() < Pig.get_time_of_next_breed(user.id):
                raise PigBreedCooldown(user)

    # @staticmethod
    # def get_pig_feed_cooldown(user: disnake.User):
    #     if Pig.get_last_feed(user.id) is not None:
    #         if Func.get_current_timestamp() < Pig.get_time_of_next_feed(user.id):
    #             raise PigFeedCooldown

    @staticmethod
    async def confirm_message(inter, lang, description: str = ''):
        message = await send_callback(inter, embed=generate_embed(
            title=Locales.Global.are_you_sure[lang],
            description=description,
            prefix=Func.generate_prefix('❓'),
            inter=inter
        ), components=[
            disnake.ui.Button(
                label=Locales.Global.yes[lang],
                custom_id='yes',
                # emoji='✅',
                style=disnake.ButtonStyle.green
            ),
            disnake.ui.Button(
                label=Locales.Global.no[lang],
                custom_id='no',
                # emoji='❌',
                style=disnake.ButtonStyle.red
            )
        ])

        def check(interaction):
            if message is not None:
                right_message = message.id == interaction.message.id
                return right_message and BotUtils.check_if_right_user(interaction)

        interaction = await inter.client.wait_for('button_click', check=check)
        try:
            await interaction.response.defer(ephemeral=True)
        except disnake.errors.HTTPException:
            return
        if interaction.component.custom_id == 'yes':
            return True
        elif interaction.component.custom_id == 'no':
            return False

    @staticmethod
    def generate_embeds_list_from_fields(fields: list, title: str = '', description: str = '',
                                         color=utils_config.main_color, fields_for_one: int = 25,
                                         thumbnail_url: str = None):
        fields_for_one -= 1
        embeds = []
        create_embed = lambda: generate_embed(title=title, color=color, description=description,
                                              thumbnail_url=thumbnail_url)
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
    def generate_select_components_for_pages(options: list, custom_id, placeholder, fields_for_one: int = 25):
        fields_for_one -= 1
        components = []
        generated_options = []

        if not options:
            return [components]

        def append_components():
            components.append([
                disnake.ui.Select(options=generated_options, custom_id=custom_id, placeholder=placeholder)])

        for i, option in enumerate(options, 1):
            generated_options.append(disnake.SelectOption(
                label=option['label'],
                value=option['value'],
                emoji=option['emoji'],
                description=option['description']
            ))
            if i % (fields_for_one + 1) == 0:
                append_components()
                generated_options = []
        if generated_options:
            append_components()
        else:
            components.append([])
        return components

    @staticmethod
    def get_items_in_str_list(items_to_convert: dict, lang):
        list_res = []
        for item_id in items_to_convert:
            if type(items_to_convert[item_id]) == dict:
                list_res.append(f'{Func.generate_prefix(Inventory.get_item_emoji(item_id))}{Inventory.get_item_name(item_id, lang)} x{items_to_convert[item_id]["amount"]}')
            else:
                list_res.append(
                    f'{Func.generate_prefix(Inventory.get_item_emoji(item_id))}{Inventory.get_item_name(item_id, lang)} x{items_to_convert[item_id]}')
        return '\n'.join(list_res)

    @staticmethod
    def get_rarest_item(items_):
        rarest = 1
        for item_id in items_:
            rarity = Inventory.get_item_rarity(item_id)
            if int(rarity) > rarest:
                rarest = int(rarity)
        return rarest

    @staticmethod
    async def generate_list_embeds(inter, _items, lang, empty_desc='Empty', basic_info=None, title=None,
                                   prefix: str = '📦', description='', fields_for_one: int = 7, list_type: str = None,
                                   select_item_component_id: str = 'inventory_item_select', sort=True,
                                   thumbnail_url: str = None,
                                   cat_as_title=False, show_amount_in_field_value=False, not_include_if_amount_0=True,
                                   client=None):
        if basic_info is None:
            basic_info = []
        complete_embeds = {}
        new_items = {}
        try:
            if list(list(_items.values())[0])[0] in items:
                if sort:
                    for cat in _items:
                        new_items[cat] = dict(sorted(_items[cat].items(), key=lambda x: items[x[0]]['type']))
                    _items = new_items.copy()
        except:
            pass
        if client is None:
            client = inter.client
        for cat, v in _items.items():
            item_fields = []
            options = []
            complete_embeds[cat] = {'embeds': []}
            select_item_placeholder = Locales.Inventory.select_item_placeholder[lang]
            for item in v:
                item_label_without_prefix = item
                option_desc = None
                emoji = None
                field_value = '----'
                if list(list(_items.values())[0])[0] in items:
                    field_value = ''
                    if not_include_if_amount_0 and Inventory.get_item_amount(inter.author.id, item) <= 0:
                        continue
                    for i, element in enumerate(basic_info):
                        if 'amount' in element:
                            field_value += f'{Locales.Global.amount[lang]}: {Inventory.get_item_amount(inter.author.id, item)}\n'
                            continue
                        if 'price' in element:
                            field_value += f'{Locales.Global.price[lang]}: {Inventory.get_item_shop_price(item)} 🪙\n'
                            continue
                        if 'cost' in element:
                            cost = Inventory.get_item_cost(item)
                            if cost is not None:
                                field_value += f'{Locales.Global.cost_per_item[lang]}: {cost} 🪙\n'
                                continue
                        if 'type' in element:
                            field_value += f'{Locales.Global.type[lang]}: {Inventory.get_item_type(item, lang)}\n'
                            continue
                        if 'rarity' in element:
                            field_value += f'{Locales.Global.rarity[lang]}: {Inventory.get_item_rarity(item, lang)}\n'
                    field_value = f'```{field_value}```'
                    after_prefix = f" x{Inventory.get_item_amount(inter.author.id, item)}" if show_amount_in_field_value else ''
                    item_label_without_prefix = f'{Func.cut_text(Inventory.get_item_name(item, lang), 15)}{after_prefix}'
                    emoji = Inventory.get_item_emoji(item)
                    option_desc = Func.cut_text(Inventory.get_item_description(item, lang), 100)
                elif list_type == 'family_members':
                    member = await User.get_user(client, item)
                    item_label_without_prefix = f'{member.display_name}'
                    emoji = '👤'
                    select_item_placeholder = Locales.ViewFamily.select_member_placeholder[lang]
                    thumbnail_url = Family.get_image(cat)
                    if not thumbnail_url.startswith('http://') or not thumbnail_url.startswith('https://'):
                        thumbnail_url = None
                    role = Family.get_member_role(cat, member.id)
                    if role is not None:
                        option_desc = Locales.FamilyRoles[role][lang]
                        emoji = Locales.FamilyRolesEmojis[role]
                    field_value = f'```{Locales.Global.role[lang]}: {Locales.FamilyRoles[role][lang]}\n' \
                                  f'{Locales.Global.weight[lang]}: {Pig.get_weight(member.id)} {Locales.Global.kilograms_short[lang]}```'
                elif list_type == 'family_requests':
                    member = await User.get_user(client, item)
                    item_label_without_prefix = f'{member.display_name}'
                    select_item_placeholder = Locales.FamilyRequests.select_member_placeholder[lang]
                    field_value = f'*{Locales.Global.sent[lang]}: <t:{Family.get_request_timestamp(cat, member.id)}:R>*'
                item_fields.append(
                    {
                        'name': f'{Func.generate_prefix(emoji, backticks=True)}{item_label_without_prefix}',
                        'value': field_value,
                        'inline': False})
                options.append(
                    {'label': item_label_without_prefix,
                     'value': f'{item}',
                     'emoji': emoji,
                     'description': option_desc
                     }
                )
            if list_type not in ['family_requests']:
                item_fields = Func.field_inline_alternation(item_fields)
            page_embeds = BotUtils.generate_embeds_list_from_fields(item_fields,
                                                                    description=description if item_fields else empty_desc,
                                                                    title=f'{Func.generate_prefix(prefix)}{title if not cat_as_title else cat}',
                                                                    fields_for_one=fields_for_one,
                                                                    thumbnail_url=thumbnail_url)
            page_components = BotUtils.generate_select_components_for_pages(options, select_item_component_id,
                                                                            select_item_placeholder,
                                                                            fields_for_one=fields_for_one)
            for i, embed in enumerate(page_embeds):
                complete_embeds[cat]['embeds'].append({'embed': embed, 'components': page_components[i]})
        return complete_embeds

    @staticmethod
    def generate_item_selected_embed(inter, lang, title=None, item_description='', thumbnail_file=None,
                                     prefix: str = '📕', embed_color: str = utils_config.main_color,
                                     item_id=None, basic_info=None) -> disnake.Embed:
        if basic_info is None:
            basic_info = []
        footer = Func.generate_footer(inter, second_part=item_id if item_id is not None else '')
        footer_url = Func.generate_footer_url('user_avatar', inter.author)
        basic_info_desc = ''
        if item_id in items:
            title = Inventory.get_item_name(item_id, lang)
            item_description = Inventory.get_item_description(item_id, lang)
            prefix = Func.generate_prefix(Inventory.get_item_emoji(item_id))
            embed_color = utils_config.rarity_colors[Inventory.get_item_rarity(item_id)]
            if Inventory.is_skin(item_id):
                skin_type = Inventory.get_item_skin_type(item_id)
                preview_options = utils_config.default_pig['skins'].copy()
                preview_options[skin_type] = item_id
                thumbnail_file = BotUtils.build_pig(tuple(preview_options.items()),
                                                    tuple(utils_config.default_pig['genetic'].items()))
            elif Inventory.get_item_image_file(item_id) is not None:
                thumbnail_file = Inventory.get_item_image_file(item_id)
        for i, element in enumerate(basic_info):
            match element:
                case 'amount':
                    basic_info_desc += f'{Locales.Global.amount[lang]}: **{Inventory.get_item_amount(inter.author.id, item_id)}**\n'
                case 'price':
                    basic_info_desc += f'{Locales.Global.price[lang]}: **{Inventory.get_item_shop_price(item_id)}** 🪙\n'
                case 'type':
                    basic_info_desc += f'{Locales.Global.type[lang]}: **{Inventory.get_item_type(item_id, lang)}**\n'
                case 'rarity':
                    basic_info_desc += f'{Locales.Global.rarity[lang]}: **{Inventory.get_item_rarity(item_id, lang)}**\n'
                case 'cost':
                    cost = Inventory.get_item_cost(item_id)
                    if cost is not None:
                        basic_info_desc += f'{Locales.Global.cost_per_item[lang]}: **{cost}** 🪙\n'
        embed = generate_embed(
            title=title,
            description=basic_info_desc,
            prefix=prefix,
            footer=footer,
            footer_url=footer_url,
            timestamp=False,
            color=embed_color,
            thumbnail_file=thumbnail_file,
            fields=[{'name': f"📋 ⟩ {Locales.Global.description[lang]}",
                     'value': f"*{item_description}*"}]
        )
        return embed

    @staticmethod
    async def pagination(inter,
                         lang: str,
                         embeds,
                         timeout: int = 180,
                         embed_thumbnail_file: str = None,
                         ctx_message: bool = False,
                         everyone_can_click: bool = False,
                         return_if_starts_with: list = None,
                         arrows: bool = True,
                         categories: bool = False,
                         ephemeral=False,
                         edit_original_message=True):
        if return_if_starts_with is None:
            return_if_starts_with = ['back_to_inventory', 'inventory_item_select', 'shop_item_select']
        complete_embeds = {}
        current_page = 1
        current_cat = None

        def set_thumbnail_file_if_not_none():
            if embed_thumbnail_file is not None:
                get_current_embed()['embed'].set_thumbnail(
                    file=disnake.File(fp=embed_thumbnail_file))

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
            options = [disnake.SelectOption(label=j, value=str(i)) for i, j in enumerate(embeds)]
            if is_categorised_pages():
                options = [disnake.SelectOption(label=i, value=str(i)) for i in embeds]
            return [disnake.ui.StringSelect(custom_id='choose_category',
                                            placeholder=Locales.Global.choose_category[lang],
                                            options=options
                                            )]

        def arrows_components():
            return [disnake.ui.Button(
                style=disnake.ButtonStyle.primary,
                emoji='◀',
                custom_id='previous',
            ),
                disnake.ui.Button(
                    style=disnake.ButtonStyle.primary,
                    emoji='▶',
                    custom_id='next',
                )
            ]

        if is_categorised_pages():
            current_cat = list(embeds)[0]
            if len(embeds) > 1:
                for cat in embeds.copy():
                    for embed in embeds[cat]['embeds']:
                        embed['components'].append(category_components())
                        if len(embeds[cat]['embeds']) > 1:
                            embed['components'].append(arrows_components())
                for i in embeds:
                    if len(embeds[i]['embeds']) > 1:
                        for j, embed in enumerate(embeds[i]['embeds']):
                            embed['embed'].set_footer(
                                text=f'📚 {Locales.Global.page[lang]}: {j + 1}')
            elif len(embeds[list(embeds)[0]]['embeds']) > 1:
                for i, embed in enumerate(embeds[list(embeds)[0]]['embeds']):
                    embed['components'].append(arrows_components())
                    embed['embed'].set_footer(text=f'📚 {Locales.Global.page[lang]}: {i + 1}')


        else:
            for i, embed in enumerate(embeds):
                if type(embed) == disnake.Embed:
                    complete_embeds[str(i)] = {'embed': embed,
                                               'components': []}
                elif type(embed) == str:
                    if type(embeds[embed]) == disnake.Embed:
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
                        embed['components'].append(arrows_components())
            embeds = complete_embeds.copy()
            for i, element in enumerate(embeds.values()):
                if arrows and len(embeds) > 1:
                    element['embed'].set_footer(
                        text=f'📚 {Locales.Global.page[lang]}: {i + 1}',
                        icon_url=Func.generate_footer_url('user_avatar', inter.author))
        set_thumbnail_file_if_not_none()
        message = await send_callback(inter, embed=get_current_embed()['embed'],
                                      components=get_current_embed()['components'],
                                      ctx_message=ctx_message, ephemeral=ephemeral,
                                      edit_original_message=edit_original_message)
        if message is None:
            try:
                message = await inter.original_message()
            except:
                pass
        def check(interaction):
            if message is not None and type(interaction) == disnake.MessageInteraction:
                right_message = message.id == interaction.message.id
                return right_message

        while True:

            try:
                interaction = await inter.client.wait_for('interaction',
                                                          check=check,
                                                          timeout=timeout)
                if not everyone_can_click and not inter.author.id == interaction.author.id:
                    await send_callback(interaction,
                                        embed=generate_embed(
                                            prefix=Func.generate_prefix('❌'),
                                            color=utils_config.error_color,
                                            title=Locales.Pagination.wrong_user_title[lang],
                                            description=Locales.Pagination.wrong_user_desc[lang],
                                            inter=inter),
                                        edit_original_message=False,
                                        ephemeral=True)
                    continue
            except asyncio.exceptions.TimeoutError as e:
                try:
                    set_thumbnail_file_if_not_none()
                    await message.edit(components=[BotUtils.generate_hide_button()])
                except:
                    pass
                return
            except AttributeError:
                return
            if type(interaction) != disnake.interactions.message.MessageInteraction:
                continue
            if interaction.component.custom_id in ['next', 'previous', 'hide', 'choose_category']:
                try:
                    if not ephemeral:
                        await interaction.response.defer(ephemeral=True)
                except disnake.errors.HTTPException:
                    return
            if interaction.component.custom_id == 'next':
                embeds_num = len(embeds)
                if is_categorised_pages():
                    embeds_num = len(embeds[current_cat]['embeds'])
                current_page = Func.get_changed_page_number(embeds_num, current_page, 1)
            elif interaction.component.custom_id == 'previous':
                embeds_num = len(embeds)
                if is_categorised_pages():
                    embeds_num = len(embeds[current_cat]['embeds'])
                current_page = Func.get_changed_page_number(embeds_num, current_page, -1)
            elif interaction.component.custom_id == 'choose_category':
                if not is_categorised_pages():
                    current_page = int(interaction.values[0]) + 1
                else:
                    current_cat = interaction.values[0]
                    current_page = 1
            elif interaction.component.custom_id == 'hide':
                return
            elif Func.startswith_list(interaction.component.custom_id, return_if_starts_with):
                return
            else:
                continue
            embed = get_current_embed()['embed']
            components = get_current_embed()['components']
            set_thumbnail_file_if_not_none()
            await send_callback(interaction if not ctx_message else message,
                                embed=embed,
                                components=components)

    @staticmethod
    def generate_hide_button():
        hide_button = disnake.ui.Button(
            style=disnake.ButtonStyle.red,
            emoji='⛔',
            custom_id='hide',
        )
        return hide_button

    @staticmethod
    def check_if_right_user(interaction, except_users: list = None):
        if except_users is None:
            except_users = []
        if interaction.author.id in except_users:
            return True
        return interaction.message.interaction.user.id == interaction.author.id

    @staticmethod
    def get_commission(user1, user2, min: int = 5, max: int = 50):
        pigs_weight_dif = Pig.get_weight(user1.id) - Pig.get_weight(user2.id)
        commission = round(pigs_weight_dif * .35)
        if commission < min:
            commission = min
        if commission > max:
            commission = max
        return commission

    @staticmethod
    def get_amount_with_commission(amount, commission):
        amount_with_commission = round(amount + amount * (commission / 100))
        return amount_with_commission

    @staticmethod
    def generate_user_pig(user_id, eye_emotion: str = None):
        return BotUtils.build_pig(tuple(Pig.get_skin(user_id, 'all').items()),
                                  tuple(Pig.get_genetic(user_id, 'all').items()),
                                  eye_emotion=eye_emotion, user_id=user_id)

    @staticmethod
    @cached(TTLCache(maxsize=1000, ttl=60))
    def build_pig(skins: tuple, genetic: tuple = None, output_filename: str = None, output_path: str = None,
                  eye_emotion: str = None, user_id=None):
        skins = dict(skins)
        if genetic is None:
            genetic = utils_config.default_pig['genetic']
        else:
            genetic = dict(genetic)
        skin_types = ['body', 'tattoo', 'makeup', 'eyes', 'pupils',
                      'glasses', 'nose', '_nose', 'piercing_nose',
                      'face',
                      'piercing_ear', 'suit', 'hat', 'legs', 'tie']
        for i in skin_types:
            if i not in skins and i not in 'nose':
                skins[i] = None
        if 'eye_emotion' not in skins:
            skins['eye_emotion'] = None
        eye_emotion = skins['eye_emotion'] if eye_emotion is None else eye_emotion
        not_draw = []
        not_draw_raw = {}
        print(skins)
        for item in skins.values():
            if item is not None and item in items and 'not_draw' in items[item]:
                not_draw_raw[items[item]['type'].split(':')[1]] = items[item]['not_draw']
        for i, key in enumerate(skin_types):
            if key in skins and user_id is not None and Inventory.get_item_amount(user_id, skins[key]) == 0 and skins[
                key] is not None:
                skins[key] = None
                if key in not_draw_raw:
                    not_draw_raw.pop(key)
        print(not_draw_raw)
        for k, v in not_draw_raw.copy().items():
            for i in v:
                if i not in skin_types and i not in items:
                    continue
                skin_type = i
                if i in items:
                    skin_type = Inventory.get_item_skin_type(i)
                if skin_type in not_draw_raw and skin_types.index(skin_type) < skin_types.index(k):
                    not_draw_raw.pop(skin_type)
        for v in not_draw_raw.values():
            not_draw += v
        if skins['hat'] is not None:
            not_draw += ['piercing_ear']
        if 'paint' in not_draw:
            skins['body'] = None
        if output_filename is None:
            output_filename = random.randrange(10000000)
        skins_path = 'bin/pig_skins'
        for i, key in enumerate(skin_types):
            if key in not_draw or (key in skins and skins[key] in items and skins[key] in not_draw):
                continue
            folder_of_skin = key
            if key == 'nose':
                folder_of_skin = 'nose'
                key = 'body'
            part = skins[key]
            if skins[key] is None and key in genetic:
                part = genetic[key]
            elif skins[key] is None and key not in genetic:
                continue
            part_path = f'{skins_path}/{folder_of_skin}/{part}.png'
            if i == 0:
                built_pig_img = Image.open(part_path)
            else:
                img_to_paste = Image.open(part_path)
                if key == 'eyes':
                    if eye_emotion in utils_config.emotions_erase_cords:
                        draw = ImageDraw.Draw(img_to_paste)
                        for cords in utils_config.emotions_erase_cords[eye_emotion]:
                            if len(cords) == 3:
                                x1 = cords[0] - cords[2]
                                y1 = cords[1] - cords[2]
                                x2 = cords[0] + cords[2]
                                y2 = cords[1] + cords[2]
                                draw.ellipse([(x1, y1), (x2, y2)], fill=img_to_paste.getpixel((0, 0)))
                            else:
                                draw.polygon(cords, fill=img_to_paste.getpixel((0, 0)))
                built_pig_img = Image.alpha_composite(built_pig_img, img_to_paste)
        if output_path is None:
            output_path = f'bin/pigs/{output_filename}.png'
        built_pig_img.save(output_path)
        return output_path

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
    def profile_embed(inter, lang, user: disnake.User = None, info: list = None) -> disnake.Embed:
        if user is None:
            user = inter.author
        description = ''
        if 'user' in info:
            description += Locales.Profile.user_profile_desc[lang].format(balance=User.get_money(user.id),
                                                                          likes=len(User.get_likes(user.id))) + '\n\n'
        if 'pig' in info:
            description += Locales.Profile.pig_profile_desc[lang].format(pig_name=Pig.get_name(user.id),
                                                                         weight=Pig.get_weight(user.id),
                                                                         age=Pig.age(user.id, lang)) + '\n\n'
        if 'family' in info:
            family_id = User.get_family(user.id)
            description += Locales.Profile.family_profile_desc[lang].format(role=Family.get_member_role(
                family_id, user.id, lang))
        embed = generate_embed(
            title=Locales.Profile.profile_title[lang].format(user=user.display_name),
            description=description,
            prefix=Func.generate_prefix('🐽'),
            thumbnail_file=BotUtils.generate_user_pig(user.id),
            inter=inter,
            # fields=[{'name': Locales.Profile.pig_field_title[lang],
            #          'value': Locales.Profile.pig_field_value[lang].format(
            #              pig_name=Pig.get_name(user.id),
            #              weight=Pig.get_weight(user.id))}]
        )
        return embed

    @staticmethod
    def raise_if_language_not_supported(user_id, lang: str = 'en'):
        if User.get_language(user_id) == lang:
            raise LanguageNotSupported

    @staticmethod
    def bool_command_choice():
        choices = [
            # alternatively:
            # OptionChoice(Localized("Cat", key="OPTION_CAT"), "Cat")
            OptionChoice(Localized('True', data=Locales.Global.true_yes_command), 'True'),
            OptionChoice(Localized('False', data=Locales.Global.false_no_command), 'False')
        ]
        return choices

    # class SellItemModal(disnake.ui.Modal):
    #     def __init__(self, inter, item_id):
    #         self.inter = inter
    #         self.item_id = item_id
    #         lang = User.get_language(user_id=inter.author.id)
    #         components = [
    #             disnake.ui.TextInput(
    #                 label=Locales.InventoryItemSellModal.label[lang],
    #                 placeholder=Locales.InventoryItemSellModal.placeholder[lang].format(
    #                     max_amount=Inventory.get_item_amount(inter.author.id, item_id)),
    #                 custom_id="amount",
    #                 style=disnake.TextInputStyle.short,
    #                 max_length=10,
    #                 required=True
    #             ),
    #         ]
    #         super().__init__(title=Locales.InventoryItemSellModal.title[lang], components=components)
    #
    #     async def callback(self, inter: disnake.ModalInteraction):
    #         if not inter.text_values['amount'].isdigit():
    #             await errors.callbacks.modal_input_is_not_number(inter)
    #         else:
    #             await inventory_item_sold(inter, self.item_id, int(inter.text_values['amount']))
    #
    # class CookItemModal(disnake.ui.Modal):
    #     def __init__(self, inter, item_id):
    #         self.inter = inter
    #         self.item_id = item_id
    #         lang = User.get_language(user_id=inter.author.id)
    #         components = [
    #             disnake.ui.TextInput(
    #                 label=Locales.InventoryItemCookModal.label[lang],
    #                 placeholder=Locales.InventoryItemCookModal.placeholder[lang].format(
    #                     max_amount=Inventory.get_item_amount(inter.author.id, item_id)),
    #                 custom_id="amount",
    #                 style=disnake.TextInputStyle.short,
    #                 max_length=10,
    #                 required=True
    #             ),
    #         ]
    #         super().__init__(title=Locales.InventoryItemCookModal.title[lang], components=components)
    #
    #     async def callback(self, inter: disnake.ModalInteraction):
    #         if not inter.text_values['amount'].isdigit():
    #             await errors.callbacks.modal_input_is_not_number(inter)
    #         else:
    #             await inventory_item_cooked(inter, self.item_id, int(inter.text_values['amount']))

    # @staticmethod
    # def raise_error_if_no_item(user_id, item_id):
    #     if Inventory.get_item_amount(interaction.author.id, item_id) == 0:
    #         await modules.errors.callbacks.no_item(interaction)
    #     else:
    #         await modules.inventory.callbacks.inventory_item_used(interaction, item_id)

    # @staticmethod
    # def make_color(color: str) -> int:
    #     if not color:
    #         color = 0
    #     else:
    #         try:
    #             color = int(color.replace('#', '').replace('0x', ''), 16)
    #         except:
    #             color = 0
    #     return color

    # @staticmethod
    # def send_start_message(client, webhook_url):
    #     if type(client) == commands.bot.InteractionBot:
    #         username = client.user.name
    #         avatar_url = client.user.avatar.url
    #         # user = client.user
    #     else:
    #         username = 'Unknown'
    #         avatar_url = ''
    #         # user = username
    #     webhook = discord_webhook.DiscordWebhook(url=webhook_url,
    #                                              content=config.start_text,
    #                                              username=username,
    #                                              avatar_url=avatar_url)
    #     webhook.execute()
    #

    # @staticmethod
    # async def pre_command(inter, servers_data, black_list, ephemeral=True, defer=True, only_lang=False):
    #     if not only_lang:
    #         if defer:
    #             await inter.response.defer(ephemeral=ephemeral)
    #         if str(inter.author.id) in black_list['users'] and inter.author.id != inter.bot.owner_id:
    #             raise UserInBlackList
    #         if str(inter.guild.id) in black_list['guilds'] and inter.author.id != inter.bot.owner_id:
    #             raise GuildInBlackList
    #     lang = servers_data[str(inter.guild.id)]['lang']
    #     return lang
    #
    # # @staticmethod
    # # async def get_webhook_link(client, channel_id, self_url=True):
    # #     channel = client.get_channel(channel_id)
    # #     if channel is not None:
    # #         for webhook in await channel.webhooks():
    # #             if not self_url and requests.get(webhook.url).status_code == 200:
    # #                 return webhook.url
    # #             elif str(client.user.id) == str(webhook.user.id):
    # #                 return webhook.url
    # #         else:
    # #             webhook = await channel.create_webhook(name=client.user.name,
    # #                                                    avatar=await client.user.avatar.read())
    # #             return webhook.url
    #
    # @staticmethod
    # def get_command_name_and_options(ctx):
    #     try:
    #         sub_commands_types = ['OptionType.sub_command', 'OptionType.sub_command_group',
    #                               'ApplicationCommandType.chat_input']
    #         if ctx.data.options and str(ctx.data.options[0].type) == sub_commands_types[1]:
    #             if ctx.data.options[0].options and str(ctx.data.options[0].options[0].type) == sub_commands_types[0]:
    #                 command_text = f'{ctx.data.name} {ctx.data.options[0].name} {ctx.data.options[0].options[0].name}'
    #                 options = ctx.data.options[0].options[0].options
    #             else:
    #                 command_text = f'{ctx.data.name} {ctx.data.options[0].name}'
    #                 options = ctx.data.options[0].options
    #         elif ctx.data.options and str(ctx.data.options[0].type) == sub_commands_types[0]:
    #             command_text = f'{ctx.data.name} {ctx.data.options[0].name}'
    #             options = ctx.data.options[0].options
    #         else:
    #             command_text = f'{ctx.data.name}'
    #             options = ctx.data.options
    #     except:
    #         command_text, options = ctx.data.name, ctx.data.options
    #     return command_text, options
    #
    # @staticmethod
    # def generate_ephemeral_arg(default_value='true'):
    #     return commands.Param(
    #                   name=Localized(data=locales['ephemeral_var']['name']),
    #                   description=Localized(
    #                       data=locales['ephemeral_var']['description']),
    #                   choices=['✅ True', '❌ False'], default=default_value)
    #
    # @staticmethod
    # def str_to_bool(target):
    #     return True if target.lower() in ['✅ true', 'true', '✅', 'yes', 'да', 'так'] else False
    #
    # @staticmethod
    # def translate_permissions(perms, lang):
    #     missing_perms = []
    #     for perm in perms:
    #         if perm in locales['permissions']:
    #             missing_perms.append(locales['permissions'][perm][lang])
    #         else:
    #             missing_perms.append(perm.replace('_', ' ').capitalize())
    #     return missing_perms
    #
    # @staticmethod
    # def change_page(total_pages, cur_page, differ):
    #     if differ > 0:
    #         if cur_page + differ > total_pages:
    #             cur_page = 1
    #         else:
    #             cur_page += differ
    #     elif differ < 0:
    #         if cur_page + differ < 1:
    #             cur_page = total_pages
    #         else:
    #             cur_page += differ
    #     return cur_page
    #
    # @staticmethod
    # def gen_footer(inter, frst_part='user', sec_part='com_name'):
    #     separator = ' ・ '
    #     if sec_part == 'com_name':
    #         sec_part, options = Func.get_command_name_and_options(inter)
    #         sec_part = f'/{sec_part}'
    #     if frst_part == 'user':
    #         frst_part = inter.author
    #     if not frst_part or not sec_part:
    #         separator = ''
    #     footer = f'{frst_part}{separator}{sec_part}'
    #     return footer
    #
    # @staticmethod
    # def cut_name(name, length, dots=True):
    #     if len(name) > length + 3:
    #         if dots:
    #             name = name[:length - 3] + '...'
    #         else:
    #             name = name[:length]
    #     return name
    #
    # # @staticmethod
    # # def cooldown(inter, rate, per, pro_rate=None, pro_per=None, bucket_type=commands.BucketType.user):
    # #     now = datetime.datetime.now()
    # #     command_name, options = Func.get_command_name_and_options(inter)
    # #     user = data.cooldowns.get((inter.author.id, command_name))
    # #     pro_rate = pro_rate or rate
    # #     pro_per = pro_per or per
    # #     rate = pro_rate if inter.author.id in data.premium_list else rate
    # #     per = pro_per if inter.author.id in data.premium_list else per
    # #     if user and 'time' in user:
    # #         if (now - user['time']).total_seconds() < per:
    # #             if user['rate'] >= rate - 1:
    # #                 dif = per - (now.timestamp() - user['time'].timestamp())
    # #                 raise commands.errors.CommandOnCooldown(rate, dif, bucket_type)
    # #             else:
    # #                 user['rate'] += 1
    # #     else:
    # #         data.cooldowns[(inter.author.id, command_name)] = {
    # #             'rate': 1,
    # #             'time': now
    # #         }
    #
    # @staticmethod
    # def cooldown(inter, rate, per, pro_rate=None, pro_per=None, bucket_type=commands.BucketType.user):
    #     now = datetime.datetime.now()
    #     command_name, options = Func.get_command_name_and_options(inter)
    #     if command_name not in data.cooldowns:
    #         data.cooldowns[command_name] = {}
    #     if inter.author.id not in data.cooldowns[command_name]:
    #         data.cooldowns[command_name][inter.author.id] = {}
    #     if 'rate' not in data.cooldowns[command_name][inter.author.id]:
    #         data.cooldowns[command_name][inter.author.id]['rate'] = 1
    #     user = data.cooldowns[command_name].get(inter.author.id)
    #     pro_rate = rate if pro_rate is None else pro_rate
    #     pro_per = per if pro_per is None else pro_per
    #     rate = pro_rate if str(inter.author.id) in data.premium_list['users'] else rate
    #     per = pro_per if str(inter.author.id) in data.premium_list['users'] else per
    #     if inter.author.id == inter.client.owner.id:
    #         per = 0
    #     change_time = True
    #     if 'time' in user:
    #         if prev_time := user['time']:
    #             if (now - prev_time).total_seconds() < per:
    #                 if data.cooldowns[command_name][inter.author.id]['rate'] >= rate - 1:
    #                     dif = per - (now.timestamp() - prev_time.timestamp())
    #                     raise commands.errors.CommandOnCooldown(rate, dif, bucket_type)
    #                 else:
    #                     change_time = False
    #     data.cooldowns[command_name][inter.author.id]['rate'] += 1
    #     if change_time:
    #         data.cooldowns[command_name][inter.author.id]['rate'] = 0
    #         data.cooldowns[command_name][inter.author.id]['time'] = now
    #
    # @staticmethod
    # def get_prefix(guild, prefix='scd', sep='・'):
    #     if prefix is None:
    #         return ''
    #     emojis = Func.get_emojis(guild)
    #     prefix_emoji = prefix
    #     if prefix == 'scd':
    #         prefix_emoji = emojis["check_mark"]
    #     elif prefix == 'error':
    #         prefix_emoji = emojis["x"]
    #     elif prefix == 'warn':
    #         prefix_emoji = emojis["warn"]
    #     prefix = f'{prefix_emoji}{sep}'
    #     return prefix

    #
    # @staticmethod
    # async def send_command_use_webhook(client, inter):
    #     color = config.main_color
    #     if inter.author.id != client.owner_id:
    #         color = config.default_avatars[int(inter.author.default_avatar.key)]['hex']
    #     options_text = ''
    #     raw_options_text = ''
    #     command_text, options = Func.get_command_name_and_options(inter)
    #     discohook_embed = discord_webhook.DiscordEmbed(title='Command used',
    #                                                    description=f'**User:** {inter.author}\n'
    #                                                                f'**Guild:** `{inter.guild}`\n'
    #                                                                f'**Channel:** `{inter.channel}`\n'
    #                                                                f'**Command:** `{command_text}`\n',
    #                                                    color=color)
    #     for i, option in enumerate(options):
    #         value = option.value
    #         if type(value) == disnake.Member or type(value) == disnake.User:
    #             value = value.id
    #         options_text += f'{option.name}: `{Func.cut_name(value, 20)}`\n'
    #         raw_options_text += f'{option.name}: {Func.cut_name(value, 500)} '
    #     if options_text:
    #         discohook_embed.add_embed_field(name='Options',
    #                                         value=f'{options_text}')
    #     discohook_embed.add_embed_field(name='Raw command',
    #                                     value=f'```/{command_text} {raw_options_text}```',
    #                                     inline=False)
    #     if inter.data.target is not None:
    #         discohook_embed.add_embed_field(name='Target',
    #                                         value=f'{inter.data.target}')
    #     discohook_embed.set_footer(
    #         text=f'Guild ID: {inter.guild.id}\nChannel ID: {inter.channel.id}\nUser ID: {inter.author.id}')
    #     await Func.send_webhook_embed(config.command_use_webhook, discohook_embed, str(inter.client.user), inter.client.user.avatar.url)
    #
    #
    # @staticmethod
    # def numerate_list_to_text(elements_list: list) -> str:
    #     text = ''
    #     for i, j in enumerate(elements_list):
    #         text += f'**{i + 1}.** {j.capitalize()}\n'
    #     return text
    #
    #
    # @staticmethod
    # async def send_webhook_embed(url: str, embed, username=None, avatar_url=None):
    #     webhook = discord_webhook.DiscordWebhook(url=url, username=username, avatar_url=avatar_url)
    #     webhook.add_embed(embed)
    #     while True:
    #         webhook_ex = webhook.execute()
    #         if webhook_ex.status_code == 200:
    #             break
    #         else:
    #             await asyncio.sleep(webhook_ex.json()['retry_after'] / 1000 + .2)
    #
    #
    # @staticmethod
    # def get_emojis(guild):
    #     emojis = config.emojis
    #     if not guild.default_role.permissions.use_external_emojis:
    #         emojis = config.unicode_emojis
    #     return emojis
    #
    #
    # @staticmethod
    # async def send_guild_join_log_message(client, guild):
    #     emojis = Func.get_emojis(guild)
    #     embed = discord_webhook.DiscordEmbed(title='Bot Joined The Guild',
    #                                          description=f'',
    #                                          color=config.main_color)
    #     if guild.icon is not None:
    #         embed.set_thumbnail(url=guild.icon.url)
    #     embed.add_embed_field(name='Name', value=str(guild))
    #     embed.add_embed_field(name='Owner',
    #                           value=f'{guild.owner.mention}')
    #     embed.add_embed_field(name='Created',
    #                           value=f'<t:{round(guild.created_at.timestamp())}:D>\n'
    #                                 f'<t:{round(guild.created_at.timestamp())}:R>')
    #     embed.add_embed_field(
    #         name=f'Members',
    #         value=f'{emojis["members"]} Total: **{guild.member_count}**\n'
    #               f'{emojis["member"]} Users: **{len([m for m in guild.members if not m.bot])}**\n'
    #               f'{emojis["bot"]} Bots: **{len([m for m in guild.members if m.bot])}**'
    #     )
    #     embed.set_footer(text=f'Guild ID: {guild.id} | Owner ID: {guild.owner_id}')
    #     await Func.send_webhook_embed(config.guild_join_webhook, embed,
    #                                   username=str(client.user), avatar_url=client.user.avatar.url)
