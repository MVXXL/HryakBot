from ...utils import *
from ...utils.discord_utils import generate_embed
from ...core import *


async def inventory_item_selected(inter, item_id, lang,
                                  inventory_type='inventory') -> discord.Embed:
    fields = [{'name': f"📋 ⟩ {translate(Locale.Global.description, lang)}",
               'value': f"*{Item.get_description(item_id, lang)}*"}]
    footer = Func.generate_footer(inter, second_part=item_id)
    footer_url = Func.generate_footer_url('user_avatar', inter.user)
    prefix = Func.generate_prefix(Item.get_emoji(item_id))
    embed_color = utils_config.rarity_colors[Item.get_rarity(item_id)]
    description = ''
    thumbnail_url = None
    thumbnail_url = None
    if inventory_type == 'inventory' or (
            inventory_type == 'shop' and not Item.get_type(item_id).startswith('skin')):
        if inventory_type == 'inventory':
            description = f'{translate(Locale.Global.amount, lang)}: **{Item.get_amount(item_id, inter.user.id)}**\n' \
                          f'{translate(Locale.Global.type, lang)}: **{Item.get_type(item_id, lang)}**\n' \
                          f'{translate(Locale.Global.rarity, lang)}: **{Item.get_rarity(item_id, lang)}**\n' \
                          f'{translate(Locale.Global.cost_per_item, lang)}: **{Item.get_sell_price(item_id)}** 🪙'
        if await Item.get_image_path(item_id, config.TEMP_FOLDER_PATH) is not None:
            thumbnail_url = await Item.get_image_path(item_id, config.TEMP_FOLDER_PATH)
    elif inventory_type == 'wardrobe' or (
            inventory_type == 'shop' and Item.get_type(item_id).startswith('skin')):
        skin_type = Item.get_skin_type(item_id)
        preview_options = hryak.config.default_pig['skins'].copy()
        preview_options[skin_type] = item_id
        if inventory_type == 'wardrobe':
            description = f'{translate(Locale.Global.amount, lang)}: **{Item.get_amount(item_id, inter.user.id)}**\n' \
                          f'{translate(Locale.Global.type, lang)}: **{Item.get_type(item_id, lang)}**\n' \
                          f'{translate(Locale.Global.rarity, lang)}: **{Item.get_rarity(item_id, lang)}**'
        thumbnail_url = await hryak.GameFunc.build_pig(tuple(preview_options.items()),
                                              tuple(hryak.config.default_pig['genetic'].items()))
    if inventory_type == 'shop':
        description = f'{translate(Locale.Global.price, lang)}: **{Item.get_market_price(item_id)}** 🪙\n' \
                      f'{translate(Locale.Global.type, lang)}: **{Item.get_type(item_id, lang)}**\n' \
                      f'{translate(Locale.Global.rarity, lang)}: **{Item.get_rarity(item_id, lang)}**'
    embed = generate_embed(
        title=Item.get_name(item_id, lang),
        description=description,
        prefix=prefix,
        footer=footer,
        footer_url=footer_url,
        # timestamp=True,
        color=embed_color,
        thumbnail_url=thumbnail_url,
        fields=fields
    )
    return embed


async def wardrobe_item_choose_layers_to_wear(inter, item_id, lang) -> discord.Embed:
    skin_type = Item.get_skin_type(item_id)
    preview_options = Pig.get_skin(inter.user.id, 'all')
    preview_options[skin_type] = Pig.get_skin(inter.user.id, skin_type)
    embed = generate_embed(
        title=translate(Locale.WardrobeItemChooseLayerToWear.title, lang),
        description=translate(Locale.WardrobeItemChooseLayerToWear.desc, lang),
        prefix=Func.generate_prefix('🟣'),
        inter=inter,
        # thumbnail_url=await BotDisUtils.generate_user_pig(inter.user.id),
    )
    return embed


async def wardrobe_item_wear(inter, item_id, lang) -> discord.Embed:
    skin_type = Item.get_skin_type(item_id)
    preview_options = Pig.get_skin(inter.user.id, 'all')
    preview_options[skin_type] = Pig.get_skin(inter.user.id, skin_type)
    embed = generate_embed(
        title=translate(Locale.WardrobeItemWear.title, lang, {'item': Item.get_name(item_id, lang)}),
        description=translate(Locale.WardrobeItemWear.desc_list, lang, {'item': Item.get_name(item_id, lang)}),
        prefix=Func.generate_prefix('scd'),
        inter=inter,
        thumbnail_url=await DisUtils.generate_user_pig(inter.user.id),
    )
    return embed


async def wardrobe_item_remove(inter, item_id, lang) -> discord.Embed:
    embed = generate_embed(
        title=translate(Locale.WardrobeItemRemove.title, lang, {'item': Item.get_name(item_id, lang)}),
        description=translate(Locale.WardrobeItemRemove.desc, lang, {'item': Item.get_name(item_id, lang)}),
        prefix=Func.generate_prefix('scd'),
        inter=inter,
        thumbnail_url=await DisUtils.generate_user_pig(inter.user.id),
    )
    return embed
