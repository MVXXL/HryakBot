from . import DisUtils
from .discord_utils import generate_embed
from .functions import Func, translate
from .components import Components
from ..core import *

class Embeds:
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
            description += translate(Locale.Profile.user_profile_desc, lang,
                                     format_options={'coins': Item.get_amount('coins', user.id),
                                                     'hollars': Item.get_amount('hollars', user.id),
                                                     'likes': rating_number,
                                                     'rating_status': rating_status}) + '\n\n'
        if 'pig' in info:
            description += translate(Locale.Profile.pig_profile_desc, lang,
                                     format_options={'pig_name': Pig.get_name(user.id),
                                                     'weight': Pig.get_weight(user.id),
                                                     'age': Pig.age(user.id, lang)}) + '\n\n'
        embed = generate_embed(
            title=translate(Locale.Profile.profile_title, lang, {'user': user.display_name}),
            description=description,
            prefix=Func.generate_prefix('🐽'),
            thumbnail_url=thumbnail_url,
            footer=Func.generate_footer(inter, second_part=f'{Stats.get_streak(user.id)} 🔥'),
            inter=inter,
        )
        return embed

    @staticmethod
    async def item_selected_embed(inter, lang, item_id, _type: str) -> discord.Embed:
        footer = Func.generate_footer(inter)
        footer_url = Func.generate_footer_url('user_avatar', inter.user)
        basic_info_desc = ''
        title = Item.get_name(item_id, lang)
        item_description = Item.get_description(item_id, lang)
        prefix = Func.generate_prefix(Item.get_emoji(item_id))
        embed_color = utils_config.rarity_colors[Item.get_rarity(item_id)]
        thumbnail_url = None
        if Item.get_type(item_id) == 'skin':
            preview_options = hryak.config.default_pig['skins'].copy()
            preview_options = Pig.set_skin_to_options(preview_options, item_id.split('.')[0])
            thumbnail_url = await hryak.GameFunc.build_pig(tuple(preview_options.items()))
        elif await Item.get_image_path(item_id, config.TEMP_FOLDER_PATH) is not None:
            thumbnail_url = await Item.get_image_path(item_id, config.TEMP_FOLDER_PATH)
        if _type in ['inventory', 'wardrobe']:
            basic_info_desc += f'{translate(Locale.Global.amount, lang)}: **{Item.get_amount(item_id, inter.user.id)}**\n'
            basic_info_desc += f'{translate(Locale.Global.type, lang)}: **{Item.get_skin_type(item_id, lang) if Item.get_type(item_id) == "skin" else Item.get_type(item_id, lang)}**\n'
            basic_info_desc += f'{translate(Locale.Global.rarity, lang)}: **{Item.get_rarity(item_id, lang)}**'
            if Item.is_salable(item_id):
                basic_info_desc += f'\n{translate(Locale.Global.cost_per_item, lang)}: **{Item.get_sell_price(item_id)} {Item.get_emoji(Item.get_sell_price_currency(item_id))}**'
        elif _type == 'shop':
            if Item.get_amount(item_id) > 1:
                basic_info_desc += f'{translate(Locale.Global.amount, lang)}: **{Item.get_amount(item_id)}**\n'
            basic_info_desc += f'{translate(Locale.Global.price, lang)}: **{Item.get_market_price(item_id)} {Item.get_emoji(Item.get_market_price_currency(item_id))}**\n'
            basic_info_desc += f'{translate(Locale.Global.type, lang)}: **{Item.get_skin_type(item_id, lang) if Item.get_type(item_id) == "skin" else Item.get_type(item_id, lang)}**\n'
            basic_info_desc += f'{translate(Locale.Global.rarity, lang)}: **{Item.get_rarity(item_id, lang)}**'
        embed = generate_embed(
            title=title,
            description=basic_info_desc,
            prefix=prefix,
            footer=footer,
            footer_url=footer_url,
            timestamp=True,
            color=embed_color,
            thumbnail_url=thumbnail_url,
            fields=[{'name': f"📋 ⟩ {translate(Locale.Global.description, lang)}",
                     'value': f"*{item_description}*"}]
        )
        return embed

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
            select_item_placeholder = translate(Locale.Inventory.select_item_placeholder, lang)
            footer_first_part = ''
            for item in v:
                item_label_without_prefix = 'Unknown'
                option_desc = None
                emoji = None
                field_value = '----'
                after_prefix = ''
                if list_type in ['inventory', 'wardrobe']:
                    if tradable_items_only and not Item.is_tradable(item):
                        continue
                    if Item.exists(item):
                        field_value = ''
                        if Item.get_amount(item, inter.user.id) == 0:
                            continue
                        if list_type == 'inventory':
                            field_value += f'{translate(Locale.Global.rarity, lang)}: {Item.get_rarity(item, lang)}\n'
                            if Item.is_salable(item):
                                field_value += f'{translate(Locale.Global.cost_per_item, lang)}: {Item.get_sell_price(item)} {Item.get_emoji(Item.get_sell_price_currency(item))}'
                            else:
                                field_value += f'{translate(Locale.Global.type, lang)}: {Item.get_type(item, lang)}'
                        elif list_type == 'wardrobe':
                            field_value += f'{translate(Locale.Global.type, lang)}: {Item.get_skin_type(item, lang)}\n' \
                                           f'{translate(Locale.Global.rarity, lang)}: {Item.get_rarity(item, lang)}'
                        field_value = f'```{field_value}```'
                        after_prefix = f" x{Item.get_amount(item, inter.user.id)}"
                        item_label_without_prefix = f'{Item.get_name(item, lang)}'
                        emoji = Item.get_emoji(item)
                        option_desc = Func.cut_text(Item.get_description(item, lang), 100)
                elif list_type == 'shop':
                    field_value = f'```{translate(Locale.Global.price, lang)}: {Item.get_market_price(item)} {Item.get_emoji(Item.get_market_price_currency(item))}\n' \
                                  f'{translate(Locale.Global.rarity, lang)}: {Item.get_rarity(item, lang)}```'
                    after_prefix = f" x{Item.get_amount(item)}" if Item.get_amount(item) > 1 else ""
                    item_label_without_prefix = f'{Item.get_name(item, lang)}'
                    emoji = Item.get_emoji(item)
                    option_desc = Func.cut_text(Item.get_description(item, lang), 100)
                    footer_first_part = f'{translate(Locale.Global.balance, lang)}: {Item.get_amount('coins', inter.user.id)} 🪙'
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
            page_embeds = Embeds.generate_embeds_list_from_fields(item_fields,
                                                                 description=description if item_fields else empty_desc,
                                                                 title=f'{Func.generate_prefix(prefix_emoji)}{title if not cat_as_title else cat}',
                                                                 fields_for_one=fields_for_one_page,
                                                                 footer=Func.generate_footer(inter,
                                                                                             first_part=footer_first_part),
                                                                 footer_url=Func.generate_footer_url('user_avatar',
                                                                                                     inter.user))
            page_components = Components.generate_select_components_for_pages(options, select_item_component_id,
                                                                         select_item_placeholder, category=cat,
                                                                         fields_for_one=fields_for_one_page)
            for i, embed in enumerate(page_embeds):
                complete_embeds[cat]['embeds'].append({'embed': embed, 'components': page_components[i]})
        return complete_embeds

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