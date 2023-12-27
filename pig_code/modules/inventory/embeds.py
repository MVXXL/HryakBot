from ...core import *
from ...utils import *


async def inventory_item_selected(inter, item_id, lang,
                            inventory_type='inventory') -> disnake.Embed:
    fields = [{'name': f"📋 ⟩ {Locales.Global.description[lang]}",
               'value': f"*{Item.get_description(item_id, lang)}*"}]
    footer = Func.generate_footer(inter, second_part=item_id)
    footer_url = Func.generate_footer_url('user_avatar', inter.author)
    prefix = Func.generate_prefix(Item.get_emoji(item_id))
    embed_color = utils_config.rarity_colors[Item.get_rarity(item_id)]
    description = ''
    thumbnail_url = None
    thumbnail_file = None
    if inventory_type == 'inventory' or (
            inventory_type == 'shop' and not Item.get_type(item_id).startswith('skin')):
        if inventory_type == 'inventory':
            description = f'{Locales.Global.amount[lang]}: **{Item.get_amount(item_id, inter.author.id)}**\n' \
                          f'{Locales.Global.type[lang]}: **{Item.get_type(item_id, lang)}**\n' \
                          f'{Locales.Global.rarity[lang]}: **{Item.get_rarity(item_id, lang)}**\n' \
                          f'{Locales.Global.cost_per_item[lang]}: **{Item.get_sell_price(item_id)}** 🪙'
        if await Item.get_image_file_path(item_id) is not None:
            thumbnail_file = await Item.get_image_file_path(item_id)
    elif inventory_type == 'wardrobe' or (
            inventory_type == 'shop' and Item.get_type(item_id).startswith('skin')):
        skin_type = Item.get_skin_type(item_id)
        preview_options = utils_config.default_pig['skins'].copy()
        preview_options[skin_type] = item_id
        if inventory_type == 'wardrobe':
            description = f'{Locales.Global.amount[lang]}: **{Item.get_amount(item_id, inter.author.id)}**\n' \
                          f'{Locales.Global.type[lang]}: **{Item.get_type(item_id, lang)}**\n' \
                          f'{Locales.Global.rarity[lang]}: **{Item.get_rarity(item_id, lang)}**'
        thumbnail_file = await BotUtils.build_pig(tuple(preview_options.items()),
                                        tuple(utils_config.default_pig['genetic'].items()))
    if inventory_type == 'shop':
        description = f'{Locales.Global.price[lang]}: **{Item.get_market_price(item_id)}** 🪙\n' \
                      f'{Locales.Global.type[lang]}: **{Item.get_type(item_id, lang)}**\n' \
                      f'{Locales.Global.rarity[lang]}: **{Item.get_rarity(item_id, lang)}**'
    embed = generate_embed(
        title=Item.get_name(item_id, lang),
        description=description,
        prefix=prefix,
        footer=footer,
        footer_url=footer_url,
        # timestamp=True,
        color=embed_color,
        thumbnail_url=thumbnail_url,
        thumbnail_file=thumbnail_file,
        fields=fields
    )
    return embed


async def wardrobe_item_wear(inter, item_id, lang) -> disnake.Embed:
    skin_type = Item.get_skin_type(item_id)
    preview_options = Pig.get_skin(inter.author.id, 'all')
    preview_options[skin_type] = Pig.get_skin(inter.author.id, skin_type)
    embed = generate_embed(
        title=Locales.WardrobeItemWear.title[lang].format(item=Item.get_name(item_id, lang)),
        description=random.choice(Locales.WardrobeItemWear.desc_list[lang]).format(
            item=Item.get_name(item_id, lang)),
        prefix=Func.generate_prefix('scd'),
        inter=inter,
        thumbnail_file=await BotUtils.generate_user_pig(inter.author.id),
    )
    return embed


async def wardrobe_item_remove(inter, item_id, lang) -> disnake.Embed:
    embed = generate_embed(
        title=Locales.WardrobeItemRemove.title[lang].format(item=Item.get_name(item_id, lang)),
        description=Locales.WardrobeItemRemove.desc[lang].format(item=Item.get_name(item_id, lang)),
        prefix=Func.generate_prefix('scd'),
        inter=inter,
        thumbnail_file=await BotUtils.generate_user_pig(inter.author.id),
    )
    return embed
