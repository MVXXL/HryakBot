from ...utils import *
from . import embeds
from . import components


async def wardrobe(inter, message=None):
    await Botutils.pre_command_check(inter)
    lang = User.get_language(inter.author.id)
    _items = Func.get_items_by_types(User.get_inventory(inter.author.id), include_only=['skin'])
    items_by_cats = {}
    embed_thumbnail_file = generate_user_pig(inter.author.id)
    print(embed_thumbnail_file)
    empty_desc = Locales.Wardrobe.wardrobe_empty_desc[lang]
    item_types = set()
    for item in _items:
        item_types.add(Inventory.get_item_type(item))
    item_types = sorted(item_types)
    for i, item_type in enumerate(['all'] + item_types):
        items_by_cats[Locales.ItemTypes[item_type][lang] if item_type != 'all' else Locales.Global.everything[lang]] = \
            Func.get_items_by_key(_items, 'type', include_only=item_type) if item_type != 'all' else _items
    await Botutils.pagination(inter if message is None else message, lang,
                              embeds=await  Botutils.generate_list_embeds(inter, items_by_cats, lang, empty_desc,
                                                                   show_amount_in_field_value=True,
                                                                   title=Locales.Wardrobe.wardrobe_title[lang],
                                                                   basic_info=[['type'], ['rarity']]),
                              embed_thumbnail_file=embed_thumbnail_file)


async def inventory(inter, message=None):
    await Botutils.pre_command_check(inter)
    lang = User.get_language(inter.author.id)
    _items = Func.get_items_by_types(User.get_inventory(inter.author.id), not_include=['skin'])
    embed_thumbnail_file = 'bin/images/inventory_thumbnail.png'
    empty_desc = Locales.Inventory.inventory_empty_desc[lang]
    items_by_cats = {Locales.Inventory.inventory_title[lang]: _items}
    await Botutils.pagination(inter if message is None else message, lang,
                              embeds=await  Botutils.generate_list_embeds(inter, items_by_cats, lang, empty_desc,
                                                                   show_amount_in_field_value=True,
                                                                   title=Locales.Inventory.inventory_title[lang],
                                                                   basic_info=[['rarity'], ['cost', 'type']]),
                              embed_thumbnail_file=embed_thumbnail_file)


async def inventory_item_selected(inter, item_id, message: disnake.Message = None):
    lang = User.get_language(inter.author.id)
    await send_callback(inter if message is None else message,
                        embed=Botutils.generate_item_selected_embed(inter, lang, item_id=item_id,
                                                                    basic_info=['amount', 'type', 'rarity', 'cost']),
                        components=components.inventory_item_selected(inter.author.id, item_id, lang))


async def wardrobe_item_wear(inter, item_id, message: disnake.Message = None):
    lang = User.get_language(inter.author.id)
    Pig.set_skin(inter.author.id, item_id)
    await send_callback(inter if message is None else message,
                        embed=embeds.wardrobe_item_wear(inter, item_id, lang),
                        edit_original_message=False,
                        ephemeral=True
                        )
    await inventory_item_selected(inter, item_id, inter.message)


async def wardrobe_item_remove(inter, item_id, message: disnake.Message = None):
    lang = User.get_language(inter.author.id)
    Pig.remove_skin(inter.author.id, Inventory.get_item_skin_type(item_id))
    await send_callback(inter if message is None else message,
                        embed=embeds.wardrobe_item_remove(inter, item_id, lang),
                        edit_original_message=False,
                        ephemeral=True
                        )
    await inventory_item_selected(inter, item_id, inter.message)
