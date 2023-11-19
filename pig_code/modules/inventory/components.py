from ...core.items.item_components.item_components import item_components
from ...utils import *


def inventory_item_selected(user_id, item_id, lang, _type, category: str = None, page: int = 1) -> list:
    components = []
    if item_id in item_components:
        for component_id, component in item_components[item_id].items():
            components.append(disnake.ui.Button(
                style=disnake.ButtonStyle.primary if 'color' not in component else component['color'],
                label=component['label'][lang],
                custom_id=f'{component_id};{item_id};{category};{page}',
            ))

    if _type == 'wardrobe':
        if Pig.get_skin(user_id, Item.get_skin_type(item_id)) != item_id:
            components.append(disnake.ui.Button(
                style=disnake.ButtonStyle.primary,
                label=Locales.Global.wear[lang],
                custom_id=f'wear_skin;{item_id};{category};{page}',
            ))
            components.append(disnake.ui.Button(
                style=disnake.ButtonStyle.primary,
                label=Locales.Global.preview[lang],
                custom_id=f'preview_skin;{item_id};{category};{page}',
            ))
        else:
            components.append(disnake.ui.Button(
                style=disnake.ButtonStyle.primary,
                label=Locales.Global.remove_cloth[lang],
                custom_id=f'remove_skin;{item_id};{category};{page}',
            ))
    components.append(disnake.ui.Button(
        style=disnake.ButtonStyle.grey,
        label='↩️',
        custom_id=f'back_to_inventory;{_type};{category};{page}',
    ))
    return components

# def skins_category_choose_components(user_id, lang) -> list:
#     components = []
#     generated_options = []
#
#     inventory = User.get_inventory(user_id)
#     inventory = Func.get_items_by_types(inventory, ['skin'])
#     types = set()
#     for item_id in inventory:
#         types.add(Item.get_type(item_id))
#     generated_options.append(disnake.SelectOption(
#         label=Locales.Global.all_skins[lang],
#         value='skin:all',
#         # emoji=option['emoji'],
#         # description=option['description']
#     ))
#     for t in types:
#         generated_options.append(disnake.SelectOption(
#             label=Locales.ItemTypes[t][lang],
#             value=t,
#             # emoji=option['emoji'],
#             # description=option['description']
#         ))
#     if generated_options:
#         components.append(disnake.ui.Select(options=generated_options, custom_id='wardrobe_category_choose',
#                                             placeholder=Locales.Global.choose_category[lang]))
#     return components
