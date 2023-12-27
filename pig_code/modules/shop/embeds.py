from ...core import *
from ...utils import *


# def shop_item_selected(inter, item_id, lang) -> disnake.Embed:
#     skin_type = Item.get_skin_type(item_id)
#     preview_options = utils_config.default_pig['skins'].copy()
#     preview_options[skin_type] = item_id
#     embed = generate_embed(
#         title=locales['wardrobe_item_selected']['title'][lang].format(item=Item.get_name(item_id, lang)),
#         description=locales['wardrobe_item_selected']['desc'][lang].format(
#             amount=Item.get_amount(inter.author.id, item_id),
#             type=Item.get_type(item_id, lang),
#         ),
#         prefix=Func.generate_prefix(Item.get_emoji(item_id)),
#         footer=Func.generate_footer(inter),
#         footer_url=Func.generate_footer_url('user_avatar', inter.author),
#         timestamp=True,
#         thumbnail_file=await BotUtils.build_pig(tuple(preview_options.items()),
#                                       tuple(utils_config.default_pig['genetic'].items())),
#         fields=[{'name': f"📋 ⟩ {Locales.Global.description[lang]}",
#                  'value': f"*{Item.get_description(item_id, lang)}*"}]
#     )
#     return embed


def shop_item_bought(inter, item_id, lang) -> disnake.Embed:
    embed = generate_embed(
        title=translate(Locales.ShopItemBought.title, lang, {'item': Item.get_name(item_id, lang)}),
        description=translate(Locales.ShopItemBought.desc, lang),
        prefix=Func.generate_prefix('scd'),
        inter=inter,
    )
    return embed


def item_buy_cooldown(inter, item_id, lang) -> disnake.Embed:
    embed = generate_embed(
        title=Locales.ErrorCallbacks.shop_buy_cooldown_title[lang],
        description=Locales.ErrorCallbacks.shop_buy_cooldown_desc[lang].format(
            item=Item.get_name(item_id, lang),
            timestamp=Shop.get_timestamp_of_cooldown_pass(inter.author.id, item_id)),
        prefix=Func.generate_prefix('scd'),
        inter=inter,
    )
    return embed

# def shop_item_selected(inter, item_id, lang) -> disnake.Embed:
#     fields = [{'name': f"📋 ⟩ {Locales.Global.description[lang]}",
#                'value': f"*{Item.get_description(item_id, lang)}*"}]
#     footer = Func.generate_footer(inter, second_part=item_id)
#     footer_url = Func.generate_footer_url('user_avatar', inter.author)
#     prefix = Func.generate_prefix(Item.get_emoji(item_id))
#     embed_color = utils_config.rarity_colors[Item.get_rarity(item_id)]
#     description = ''
#     thumbnail_url = None
#     thumbnail_file = None
#     if inventory_type == 'inventory' or (
#             inventory_type == 'shop' and not Item.get_type(item_id).startswith('skin')):
#         if inventory_type == 'inventory':
#             description = f'{Locales.Global.amount[lang]}: **{Item.get_amount(inter.author.id, item_id)}**\n' \
#                           f'{Locales.Global.type[lang]}: **{Item.get_type(item_id, lang)}**\n' \
#                           f'{Locales.Global.rarity[lang]}: **{Item.get_rarity(item_id, lang)}**\n' \
#                           f'{Locales.Global.cost_per_item[lang]}: **{Item.get_sell_price(item_id)}** 🪙'
#         if Inventory.get_item_image_url(item_id) is not None:
#             thumbnail_url = Inventory.get_item_image_url(item_id)
#         elif Inventory.get_item_image_file(item_id) is not None:
#             thumbnail_file = Inventory.get_item_image_file(item_id)
#     elif inventory_type == 'wardrobe' or (
#             inventory_type == 'shop' and Item.get_type(item_id).startswith('skin')):
#         skin_type = Item.get_skin_type(item_id)
#         preview_options = utils_config.default_pig['skins'].copy()
#         preview_options[skin_type] = item_id
#         if inventory_type == 'wardrobe':
#             description = f'{Locales.Global.amount[lang]}: **{Item.get_amount(inter.author.id, item_id)}**\n' \
#                           f'{Locales.Global.type[lang]}: **{Item.get_type(item_id, lang)}**\n' \
#                           f'{Locales.Global.rarity[lang]}: **{Item.get_rarity(item_id, lang)}**'
#         thumbnail_file = await BotUtils.build_pig(tuple(preview_options.items()),
#                                         tuple(utils_config.default_pig['genetic'].items()))
#     if inventory_type == 'shop':
#         description = f'{Locales.Global.price[lang]}: **{Item.get_market_price(item_id)}** 🪙\n' \
#                       f'{Locales.Global.type[lang]}: **{Item.get_type(item_id, lang)}**\n' \
#                       f'{Locales.Global.rarity[lang]}: **{Item.get_rarity(item_id, lang)}**'
#     embed = generate_embed(
#         title=Item.get_name(item_id, lang),
#         description=description,
#         prefix=prefix,
#         footer=footer,
#         footer_url=footer_url,
#         # timestamp=True,
#         color=embed_color,
#         thumbnail_url=thumbnail_url,
#         thumbnail_file=thumbnail_file,
#         fields=fields
#     )
#     return embed

# def inventory_item_sold(inter, item_id, amount, money_received, lang) -> disnake.Embed:
#     embed = generate_embed(
#         title=locales['inventory_item_sold']['title'][lang].format(item=Item.get_name(item_id, lang)),
#         description=f"- {locales['inventory_item_sold']['desc'][lang].format(item=Item.get_name(item_id, lang), amount=amount, money=money_received)}",
#         prefix=Func.generate_prefix('scd'),
#         footer=Func.generate_footer(inter, second_part='item_sold'),
#         footer_url=Func.generate_footer_url('user_avatar', inter.author),
#     )
#     return embed
