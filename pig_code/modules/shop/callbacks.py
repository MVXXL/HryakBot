from ...utils import *
from . import embeds, components


async def shop(inter, message=None):
    await Botutils.pre_command_check(inter)
    lang = User.get_language(inter.author.id)
    shops = {'static_shop': Shop.get_last_static_shop,
             'daily_shop': Shop.get_last_daily_shop,
             'case_shop': Shop.get_last_case_shop
             }
    items_by_cats = {}
    for shop_ in shops:
        items_by_cats[Locales.Shop.titles[shop_][lang]] = shops[shop_]()
    await Botutils.pagination(inter if message is None else message, lang,
                              embeds=await Botutils.generate_list_embeds(inter, items_by_cats, lang, sort=False,
                                                                   not_include_if_amount_0=False,
                                                                   title=Locales.Wardrobe.wardrobe_title[lang],
                                                                   select_item_component_id='shop_item_select',
                                                                   cat_as_title=True,
                                                                   basic_info=[['price'], ['rarity'], ['type']]),
                              return_if_starts_with=['back_to_inventory', 'wardrobe_category_choose'],
                              embed_thumbnail_file='bin/images/shop_thumbnail.png', arrows=False, categories=True)


async def shop_item_buy(inter, item_id):
    lang = User.get_language(inter.author.id)
    if Shop.is_item_in_cooldown(inter.author.id, item_id):
        await send_callback(inter, edit_original_message=False, ephemeral=True,
                            embed=embeds.item_buy_cooldown(inter, item_id, lang))
        return
    if User.get_money(inter.author.id) < Inventory.get_item_shop_price(item_id):
        await error_callbacks.not_enough_money(inter)
        return
    User.add_money(inter.author.id, -Inventory.get_item_shop_price(item_id))
    User.add_item(inter.author.id, item_id)
    User.append_buy_history(inter.author.id, item_id)
    await send_callback(inter, edit_original_message=False, ephemeral=True,
                        embed=embeds.shop_item_bought(inter, item_id, lang))


async def shop_item_selected(inter, item_id, message: disnake.Message = None):
    lang = User.get_language(inter.author.id)
    await send_callback(inter if message is None else message,
                        embed=Botutils.generate_item_selected_embed(inter, lang, item_id=item_id,
                                                                    basic_info=['price', 'type', 'rarity']),
                        components=components.shop_item_selected(inter.author.id, item_id, lang)
                        )
