import disnake.ui

from ..db_api import *
from ...core import *
from . import error_callbacks


class GetItemAmountModal(disnake.ui.Modal):
    def __init__(self, inter, item_id, func, label, title, max_amount: int = None):
        self.inter = inter
        self.item_id = item_id
        self.func = func
        self.lang = User.get_language(user_id=inter.author.id)
        self.max_amount = max_amount
        if self.max_amount is None:
            self.max_amount = Item.get_amount(item_id, inter.author.id)
        components = [
            disnake.ui.TextInput(
                label=label[self.lang] if type(label) == dict else label,
                placeholder=Locales.Global.you_have_amount[self.lang].format(
                    max_amount=self.max_amount),
                custom_id="amount",
                style=disnake.TextInputStyle.short,
                max_length=10,
                required=True
            )
        ]
        super().__init__(title=title[self.lang] if type(title) == dict else title, components=components)

    async def callback(self, inter: disnake.ModalInteraction):
        if not inter.text_values['amount'].isdigit():
            await error_callbacks.modal_input_is_not_number(inter)
        else:
            if int(inter.text_values['amount']) > self.max_amount:
                inter.text_values['amount'] = self.max_amount
            await self.func(inter, self.item_id, int(inter.text_values['amount']))
