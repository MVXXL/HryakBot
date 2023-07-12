from ..db_api import *
from ...core import *
from . import error_callbacks


class GetItemAmountModal(disnake.ui.Modal):
    def __init__(self, inter, item_id, func, label):
        self.inter = inter
        self.item_id = item_id
        self.func = func
        self.lang = User.get_language(user_id=inter.author.id)
        components = [
            disnake.ui.TextInput(
                label=label[self.lang],
                placeholder=Locales.Global.you_have_amount[self.lang].format(
                    max_amount=Inventory.get_item_amount(inter.author.id, item_id)),
                custom_id="amount",
                style=disnake.TextInputStyle.short,
                max_length=10,
                required=True
            ),
        ]
        super().__init__(title=Locales.InventoryItemCookModal.title[self.lang], components=components)

    async def callback(self, inter: disnake.ModalInteraction):
        if not inter.text_values['amount'].isdigit():
            await error_callbacks.modal_input_is_not_number(inter)
        else:
            if int(inter.text_values['amount']) > Inventory.get_item_amount(inter.author.id, self.item_id):
                inter.text_values['amount'] = Inventory.get_item_amount(inter.author.id, self.item_id)
            await self.func(inter, self.item_id, int(inter.text_values['amount']))
