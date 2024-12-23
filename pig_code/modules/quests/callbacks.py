import discord.ui

from ...utils import *
from . import embeds, components


async def quests(inter, message=None, init_category: str = None, init_page: int = 1):
    await Utils.pre_command_check(inter)
    lang = User.get_language(inter.user.id)
    quests_ = {'daily_quests': Shop.get_consumables_shop,
               'weekly_quests': Shop.get_tools_shop
               }
    if init_category is None:
        description = f'{translate(Locales.Quests.main_page_desc, lang)}\n\n'
        for quest in quests_:
            description += f'> - {translate(Locales.Quests.titles[quest], lang)}\n'
        await send_callback(inter, embed=generate_embed(translate(Locales.Quests.main_page_title, lang),
                                                        description,
                                                        prefix=Func.generate_prefix('🛍️'),
                                                        thumbnail_url=await Func.get_image_path_from_link(
                                                            utils_config.image_links['quests']),
                                                        footer_url=Func.generate_footer_url(user=inter.user),
                                                        footer=Func.generate_footer(inter)),
                            components=[discord.ui.Select(custom_id='move_to;quests',
                                                          placeholder=translate(Locales.Global.choose_category, lang),
                                                          options=[discord.SelectOption(
                                                              label=translate(Locales.Quests.titles[quest], lang),
                                                              value=translate(Locales.Quests.titles[quest], lang)) for
                                                              quest in
                                                              quests_])])
        return
    items_by_cats = {}
    for shop_ in shops:
        if shops[shop_] is None:
            continue
        items_by_cats[f'{translate(Locales.Shop.titles[shop_], lang)}'] = shops[shop_]()
    embeds = await Utils.generate_items_list_embeds(inter, items_by_cats, lang, sort=False,
                                                    list_type='shop',
                                                    prefix_emoji='🛍️',
                                                    select_item_component_id='item_select;shop',
                                                    cat_as_title=True)
    # if User.get_age(inter.user.id) > 3600 * 24 * 7:
    #     for i in ['coins_shop', 'premium_skins_shop']:
    #         for embed in embeds[translate(Locales.Shop.titles[i], lang)]['embeds']:
    #             embed['embed'].description = translate(Locales.Shop.buy_hollars_description, lang)
    embeds[translate(Locales.Shop.titles['donation_shop'], lang)] = {
        'embeds': [{'embed': generate_embed(translate(Locales.Shop.donation_shop_title, lang),
                                            translate(Locales.Shop.donation_shop_desc, lang),
                                            prefix=Func.generate_prefix('🍩'),
                                            footer_url=Func.generate_footer_url(user=inter.user),
                                            color=utils_config.premium_color,
                                            footer=Func.generate_footer(inter)),
                    'components': []}]}
    await Utils.pagination(inter, lang, message=message,
                           embeds=embeds,
                           return_if_starts_with=['back_to_inventory', 'wardrobe_category_choose'],
                           embed_thumbnail_url=await Func.get_image_path_from_link(
                               utils_config.image_links['shop']), arrows=False, categories=True,
                           init_category=init_category, init_page=init_page)


async def shop_item_buy(inter, item_id):
    lang = User.get_language(inter.user.id)
    if Shop.is_item_in_cooldown(inter.user.id, item_id):
        await error_callbacks.default_error_callback(inter,
                                                     translate(Locales.ErrorCallbacks.shop_buy_cooldown_title, lang),
                                                     translate(Locales.ErrorCallbacks.shop_buy_cooldown_desc, lang,
                                                               {'item': Item.get_name(item_id, lang),
                                                                'timestamp': Shop.get_timestamp_of_cooldown_pass(
                                                                    inter.user.id, item_id)}),
                                                     edit_original_response=False, ephemeral=True, )
        return
    if Item.get_amount(Item.get_market_price_currency(item_id), inter.user.id) < Item.get_market_price(item_id):
        await error_callbacks.not_enough_money(inter)
        return
    User.remove_item(inter.user.id, Item.get_market_price_currency(item_id), Item.get_market_price(item_id))
    User.add_item(inter.user.id, Item.clean_id(item_id), Item.get_amount(item_id))
    History.append_shop_history(inter.user.id, Item.clean_id(item_id), amount=Item.get_amount(item_id))
    await send_callback(inter, edit_original_response=False, ephemeral=True,
                        embed=generate_embed(
                            title=translate(Locales.ShopItemBought.title, lang,
                                            {'item': Item.get_name(item_id,
                                                                   lang).lower()}) + f' x{Item.get_amount(item_id)}',
                            description=translate(Locales.ShopItemBought.desc, lang),
                            prefix=Func.generate_prefix('scd'),
                            inter=inter,
                        ))


async def shop_item_selected(inter, item_id, message: discord.Message = None, category: str = None, page: int = 1):
    lang = User.get_language(inter.user.id)
    await send_callback(inter if message is None else message,
                        embed=await Utils.generate_item_selected_embed(inter, lang, item_id=item_id, _type='shop'),
                        components=components.shop_item_selected(item_id, lang, category=category, page=page))
