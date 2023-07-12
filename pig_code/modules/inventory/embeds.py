from ...core import *
from ...utils import *


def inventory_item_selected(inter, item_id, lang,
                            inventory_type='inventory') -> disnake.Embed:
    fields = [{'name': f"📋 ⟩ {Locales.Global.description[lang]}",
               'value': f"*{Inventory.get_item_description(item_id, lang)}*"}]
    footer = Func.generate_footer(inter, second_part=item_id)
    footer_url = Func.generate_footer_url('user_avatar', inter.author)
    prefix = Func.generate_prefix(Inventory.get_item_emoji(item_id))
    embed_color = utils_config.rarity_colors[Inventory.get_item_rarity(item_id)]
    description = ''
    thumbnail_url = None
    thumbnail_file = None
    if inventory_type == 'inventory' or (
            inventory_type == 'shop' and not Inventory.get_item_type(item_id).startswith('skin')):
        if inventory_type == 'inventory':
            description = f'{Locales.Global.amount[lang]}: **{Inventory.get_item_amount(inter.author.id, item_id)}**\n' \
                          f'{Locales.Global.type[lang]}: **{Inventory.get_item_type(item_id, lang)}**\n' \
                          f'{Locales.Global.rarity[lang]}: **{Inventory.get_item_rarity(item_id, lang)}**\n' \
                          f'{Locales.Global.cost_per_item[lang]}: **{Inventory.get_item_cost(item_id)}** 🪙'
        if Inventory.get_item_image_url(item_id) is not None:
            thumbnail_url = Inventory.get_item_image_url(item_id)
        elif Inventory.get_item_image_file(item_id) is not None:
            thumbnail_file = Inventory.get_item_image_file(item_id)
    elif inventory_type == 'wardrobe' or (
            inventory_type == 'shop' and Inventory.get_item_type(item_id).startswith('skin')):
        skin_type = Inventory.get_item_skin_type(item_id)
        preview_options = utils_config.default_pig['skins'].copy()
        preview_options[skin_type] = item_id
        if inventory_type == 'wardrobe':
            description = f'{Locales.Global.amount[lang]}: **{Inventory.get_item_amount(inter.author.id, item_id)}**\n' \
                          f'{Locales.Global.type[lang]}: **{Inventory.get_item_type(item_id, lang)}**\n' \
                          f'{Locales.Global.rarity[lang]}: **{Inventory.get_item_rarity(item_id, lang)}**'
        thumbnail_file = Func.build_pig(tuple(preview_options.items()),
                                        tuple(utils_config.default_pig['genetic'].items()))
    if inventory_type == 'shop':
        description = f'{Locales.Global.price[lang]}: **{Inventory.get_item_shop_price(item_id)}** 🪙\n' \
                      f'{Locales.Global.type[lang]}: **{Inventory.get_item_type(item_id, lang)}**\n' \
                      f'{Locales.Global.rarity[lang]}: **{Inventory.get_item_rarity(item_id, lang)}**'
    embed = generate_embed(
        title=Inventory.get_item_name(item_id, lang),
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


def wardrobe_item_wear(inter, item_id, lang) -> disnake.Embed:
    skin_type = Inventory.get_item_skin_type(item_id)
    preview_options = Pig.get_skin(inter.author.id, 'all')
    preview_options[skin_type] = Pig.get_skin(inter.author.id, skin_type)
    embed = generate_embed(
        title=Locales.WardrobeItemWear.title[lang].format(item=Inventory.get_item_name(item_id, lang)),
        description=random.choice(Locales.WardrobeItemWear.desc_list[lang]).format(
            item=Inventory.get_item_name(item_id, lang)),
        prefix=Func.generate_prefix('scd'),
        inter=inter,
        thumbnail_file=generate_user_pig(inter.author.id),
    )
    return embed


def wardrobe_item_remove(inter, item_id, lang) -> disnake.Embed:
    embed = generate_embed(
        title=Locales.WardrobeItemRemove.title[lang].format(item=Inventory.get_item_name(item_id, lang)),
        description=Locales.WardrobeItemRemove.desc[lang].format(item=Inventory.get_item_name(item_id, lang)),
        prefix=Func.generate_prefix('scd'),
        inter=inter,
        thumbnail_file=generate_user_pig(inter.author.id),
    )
    return embed
