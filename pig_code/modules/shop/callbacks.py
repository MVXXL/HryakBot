from ...utils import *
from . import embeds, components


async def shop(inter, message=None, init_category: str = None, init_page: int = 1):
    await BotUtils.pre_command_check(inter)
    lang = User.get_language(inter.author.id)
    shops = {'static_shop': Shop.get_static_shop,
             'daily_shop': Shop.get_daily_shop,
             'case_shop': Shop.get_case_shop,
             'coins_shop': Shop.get_coins_shop,
             'premium_skins_shop': Shop.get_premium_skins_shop,
             }
    items_by_cats = {}
    for shop_ in shops:
        items_by_cats[translate(Locales.Shop.titles[shop_], lang)] = shops[shop_]()
    embeds = await BotUtils.generate_items_list_embeds(inter, items_by_cats, lang, sort=False,
                                                       list_type='shop',
                                                       title=translate(Locales.Wardrobe.wardrobe_title, lang),
                                                       select_item_component_id='item_select;shop',
                                                       cat_as_title=True)
    for i in ['coins_shop', 'premium_skins_shop']:
        for embed in embeds[translate(Locales.Shop.titles[i], lang)]['embeds']:
            embed['embed'].description = translate(Locales.Shop.buy_hollars_description, lang)
    await BotUtils.pagination(inter if message is None else message, lang,
                              embeds=embeds,
                              return_if_starts_with=['back_to_inventory', 'wardrobe_category_choose'],
                              embed_thumbnail_file=await Func.get_image_path_from_link(utils_config.image_links['shop']), arrows=False, categories=True,
                              init_category=init_category, init_page=init_page)


async def shop_item_buy(inter, item_id):
    lang = User.get_language(inter.author.id)
    print(Shop.is_item_in_cooldown(inter.author.id, item_id))
    if Shop.is_item_in_cooldown(inter.author.id, item_id):
        await error_callbacks.default_error_callback(inter,
                                                     translate(Locales.ErrorCallbacks.shop_buy_cooldown_title, lang),
                                                     translate(Locales.ErrorCallbacks.shop_buy_cooldown_desc, lang,
                                                               {'item': Item.get_name(item_id, lang),
                                                                'timestamp': Shop.get_timestamp_of_cooldown_pass(
                                                                    inter.author.id, item_id)}),
                                                     edit_original_message=False, ephemeral=True,)
        return
    if Item.get_amount(Item.get_market_price_currency(item_id), inter.author.id) < Item.get_market_price(item_id):
        await error_callbacks.not_enough_money(inter)
        return
    User.add_item(inter.author.id, Item.get_market_price_currency(item_id), -Item.get_market_price(item_id))
    User.add_item(inter.author.id, Item.clean_id(item_id), Item.get_amount(item_id))
    User.append_buy_history(inter.author.id, Item.clean_id(item_id), amount=Item.get_amount(item_id))
    await send_callback(inter, edit_original_message=False, ephemeral=True,
                        embed=generate_embed(
                            title=translate(Locales.ShopItemBought.title, lang,
                                            {'item': Item.get_name(item_id, lang).lower()}) + f' x{Item.get_amount(item_id)}',
                            description=translate(Locales.ShopItemBought.desc, lang),
                            prefix=Func.generate_prefix('scd'),
                            inter=inter,
                        ))


async def shop_item_selected(inter, item_id, message: disnake.Message = None, category: str = None, page: int = 1):
    lang = User.get_language(inter.author.id)
    await send_callback(inter if message is None else message,
                        embed=await BotUtils.generate_item_selected_embed(inter, lang, item_id=item_id, _type='shop'),
                        components=components.shop_item_selected(item_id, lang, category=category, page=page))
