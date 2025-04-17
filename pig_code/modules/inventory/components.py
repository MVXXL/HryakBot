import discord.ui

from ...core.items.item_components.item_components import item_components
from ...utils import *
from ...core import *


def inventory_item_selected(user_id, item_id, lang, _type, category: str = None, page: int = 1) -> list:
    components = []
    if item_id in item_components:
        for component_id, component in item_components[item_id].items():
            components.append(discord.ui.Button(
                style=discord.ButtonStyle.primary if 'color' not in component else component['color'],
                label=translate(component['label'], lang),
                custom_id=f'{component_id};{item_id};{category};{page}',
            ))

    if _type == 'wardrobe':
        wear = False
        if Item.get_skin_type(item_id) in ['eyes', 'pupils', 'body']:
            for layer in Item.get_skin_layers(item_id):
                if Pig.get_skin(user_id, layer) == item_id:
                    wear = True
                    break
        elif Pig.get_skin(user_id, Item.get_skin_type(item_id)) == item_id:
            wear = True
        if not wear:
            components.append(discord.ui.Button(
                style=discord.ButtonStyle.primary,
                label=translate(Locales.Global.wear, lang),
                custom_id=f'wear_skin;{item_id};{category};{page}',
            ))
            components.append(discord.ui.Button(
                style=discord.ButtonStyle.primary,
                label=translate(Locales.Global.preview, lang),
                custom_id=f'preview_skin;{item_id};{category};{page}',
            ))
        else:
            components.append(discord.ui.Button(
                style=discord.ButtonStyle.primary,
                label=translate(Locales.Global.remove_cloth, lang),
                custom_id=f'remove_skin;{item_id};{category};{page}',
            ))
    components.append(discord.ui.Button(
        style=discord.ButtonStyle.grey,
        label='↩️',
        custom_id=f'back_to_inventory;{_type};{category};{page}',
    ))
    return components


def choose_parts_to_wear(item_id, lang, custom_id) -> list:
    components = []
    options = []
    options.append(
        discord.SelectOption(label=translate(Locales.WardrobeItemChooseLayerToWear.wear_all_option, lang), value='all'))
    for i in Item.get_skin_layers(item_id):
        options.append(discord.SelectOption(label=translate(hryak.locale.Locale.SkinLayers[i], lang), value=i))
    components.append(
        discord.ui.Select(custom_id=custom_id,
                          placeholder='Выберите части',
                          options=options,
                          max_values=len(options))
    )
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
#     generated_options.append(discord.SelectOption(
#         label=Locales.Global.all_skins[lang],
#         value='skin:all',
#         # emoji=option['emoji'],
#         # description=option['description']
#     ))
#     for t in types:
#         generated_options.append(discord.SelectOption(
#             label=Locales.ItemTypes[t][lang],
#             value=t,
#             # emoji=option['emoji'],
#             # description=option['description']
#         ))
#     if generated_options:
#         components.append(discord.ui.Select(options=generated_options, custom_id='wardrobe_category_choose',
#                                             placeholder=Locales.Global.choose_category[lang]))
#     return components
