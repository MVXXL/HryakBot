from ....core import *
from ....utils import *


async def case_used(inter, gift_case, update):
    lang = User.get_language(inter.author.id)
    match gift_case:
        case 'common_case':
            item_types = ['skin']
            chances = {
                '2': 30,
                '3': 68,
                '4': 2,
                '5': .1
            }
        case 'rare_case':
            item_types = ['skin']
            chances = {
                '3': 25,
                '4': 73,
                '5': 2
            }
        case _:
            return
    User.remove_item(inter.author.id, gift_case)
    probable_items = {}
    for t in item_types:
        probable_items.update(Func.get_items_by_key(items, 'type', t))
    item_rarity = Func.random_choice_with_probability(chances)
    probable_items = Func.get_items_by_key(probable_items, 'rarity', item_rarity)
    probable_items = Inventory.get_items_obtainable_in_cases(probable_items)
    items_received = {Func.random_choice_with_probability({i: 1 for i in probable_items}): 1}
    for item, amount in items_received.items():
        User.add_item(inter.author.id, item, amount)
    await send_callback(inter, embed=generate_embed(
        title=Locales.ItemUsed.case_title[lang],
        description=f"{Locales.ItemUsed.case_desc[lang].format(items=BotUtils.get_items_in_str_list(items_received, lang))}",
        prefix=Func.generate_prefix('🎁'),
        color=utils_config.rarity_colors[str(BotUtils.get_rarest_item(items_received))],
        inter=inter,
    ), ephemeral=True, edit_original_message=False)
    await update()
