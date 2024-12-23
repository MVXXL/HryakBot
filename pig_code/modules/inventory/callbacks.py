from ...utils import *
from . import embeds
from . import components


async def wardrobe(inter, message=None, select_item_component_id: str = 'item_select;wardrobe',
                   pre_command_check=True, ephemeral=False, edit_original_response=True, edit_followup: bool = False,
                   tradable_items_only: bool = False,
                   init_category: str = None, init_page: int = 1):
    if pre_command_check:
        await Utils.pre_command_check(inter)
    lang = User.get_language(inter.user.id)
    _items = Tech.get_all_items((('inventory_type', 'wardrobe'),), user_id=inter.user.id)
    items_by_cats = {}
    embed_thumbnail_url = await Utils.generate_user_pig(inter.user.id)
    empty_desc = translate(Locales.Wardrobe.wardrobe_empty_desc, lang)
    item_types = set()
    for item in _items:
        item_types.add(Item.get_skin_type(item))
    item_types = sorted(item_types)
    for i, item_type in enumerate(['all'] + item_types):
        items_by_cats[
            translate(Locales.SkinTypes[item_type], lang) if item_type != 'all' else translate(Locales.Global.everything, lang)] = \
            Tech.get_all_items((('skin_config', 'type', item_type),)) if item_type != 'all' else _items
    await Utils.pagination(inter, lang, message=message,
                           embeds=await Utils.generate_items_list_embeds(inter, items_by_cats, lang, empty_desc,
                                                                         list_type='wardrobe',
                                                                         select_item_component_id=select_item_component_id,
                                                                         title=translate(
                                                                                   Locales.Wardrobe.wardrobe_title,
                                                                                   lang),
                                                                         tradable_items_only=tradable_items_only),
                           embed_thumbnail_url=embed_thumbnail_url, ephemeral=ephemeral,
                           edit_original_response=edit_original_response, edit_followup=edit_followup, init_category=init_category,
                           init_page=init_page)


async def inventory(inter, message=None, select_item_component_id: str = 'item_select;inventory',
                    pre_command_check=True, ephemeral=False, edit_original_response=True, edit_followup: bool = False,
                    tradable_items_only: bool = False,
                    init_category: str = None, init_page: int = 1):
    if pre_command_check:
        await Utils.pre_command_check(inter)
    lang = User.get_language(inter.user.id)
    _items = Tech.get_all_items((('inventory_type', 'inventory'),), user_id=inter.user.id)
    empty_desc = translate(Locales.Inventory.inventory_empty_desc, lang)
    items_by_cats = {translate(Locales.Inventory.inventory_title, lang): _items}
    await Utils.pagination(inter, lang, message=message,
                           embeds=await Utils.generate_items_list_embeds(inter, items_by_cats, lang, empty_desc,
                                                                         select_item_component_id=select_item_component_id,
                                                                         title=translate(
                                                                                   Locales.Inventory.inventory_title,
                                                                                   lang),
                                                                         tradable_items_only=tradable_items_only),
                           embed_thumbnail_url=await Func.get_image_path_from_link(
                                  utils_config.image_links['inventory']), ephemeral=ephemeral,
                           edit_original_response=edit_original_response, edit_followup=edit_followup, init_category=init_category,
                           init_page=init_page)


async def wardrobe_item_selected(inter, item_id, message: discord.Message = None, category: str = None, page: int = 1):
    lang = User.get_language(inter.user.id)
    await send_callback(inter if message is None else message,
                        embed=await Utils.generate_item_selected_embed(inter, lang, item_id=item_id,
                                                                       _type='wardrobe'),
                        components=components.inventory_item_selected(inter.user.id, item_id, lang, _type='wardrobe',
                                                                      category=category, page=page))


async def inventory_item_selected(inter, item_id, message: discord.Message = None, category: str = None, page: int = 1, edit_followup: bool = False):
    lang = User.get_language(inter.user.id)
    await send_callback(inter if message is None else message, edit_followup=edit_followup,
                        embed=await Utils.generate_item_selected_embed(inter, lang, item_id=item_id,
                                                                       _type='inventory'),
                        components=components.inventory_item_selected(inter.user.id, item_id, lang, _type='inventory',
                                                                      category=category, page=page))


async def wardrobe_item_wear(inter, item_id, message: discord.Message = None, category: str = None, page: int = 1):
    lang = User.get_language(inter.user.id)
    not_compatible_skins = Utils.get_not_compatible_skins(inter.user.id, item_id)
    if not_compatible_skins:
        await error_callbacks.not_compatible_skin(inter, item_id, not_compatible_skins, message)
        return
    choose_parts = False
    if Item.get_skin_type(item_id) in ['eyes', 'pupils']:
        choose_parts = True
    if Item.get_skin_type(item_id) in ['body'] and Item.get_amount('body_combiner', inter.user.id) > 0:
        choose_parts = True
    if choose_parts:
        custom_id = f'in;select_part;{random.randrange(100000)}'
        await send_callback(inter if message is None else message,
                            embed=await embeds.wardrobe_item_choose_layers_to_wear(inter, item_id, lang),
                            components=components.choose_parts_to_wear(item_id, lang, custom_id),
                            edit_original_response=False,
                            ephemeral=True
                            )

        def check(interaction):
            return interaction.data.get('custom_id') == custom_id

        interaction = await inter.client.wait_for('interaction', check=check)
        if 'all' not in interaction.data.get('values'):
            for i in interaction.data.get('values'):
                Pig.set_skin(inter.user.id, item_id, i)
        else:
            Pig.set_skin(inter.user.id, item_id)
    else:
        Pig.set_skin(inter.user.id, item_id)
    await send_callback(inter if message is None else message,
                        embed=await embeds.wardrobe_item_wear(inter, item_id, lang),
                        edit_original_response=True if choose_parts else False,
                        ephemeral=True
                        )
    await wardrobe_item_selected(inter, item_id, inter.message, category=category, page=page)


async def wardrobe_item_remove(inter, item_id, message: discord.Message = None, category: str = None, page: int = 1):
    lang = User.get_language(inter.user.id)
    Pig.remove_skin(inter.user.id, item_id)
    await send_callback(inter if message is None else message,
                        embed=await embeds.wardrobe_item_remove(inter, item_id, lang),
                        edit_original_response=False,
                        ephemeral=True
                        )
    await wardrobe_item_selected(inter, item_id, inter.message, category=category, page=page)
