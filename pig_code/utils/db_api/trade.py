from .connection import Connection
from .tech import Tech
from .user import User
from ..functions import Func
from ...core import *
from ...core.config import trades_schema


class Trade:

    @staticmethod
    def exists(trade_id):
        result = Connection.make_request(
            f"SELECT EXISTS(SELECT 1 FROM {trades_schema} WHERE id = {trade_id})",
            commit=False,
            fetch=True
        )
        return bool(result)

    @staticmethod
    def update_data(trade_id, new_trade):
        new_trade = json.dumps(new_trade, ensure_ascii=False)
        Connection.make_request(
            f"UPDATE {trades_schema} SET data = %s WHERE id = {trade_id}", (new_trade,)
        )

    @staticmethod
    def get_data(trade_id):
        result = Connection.make_request(
            f"SELECT data FROM {trades_schema} WHERE id = {trade_id}",
            commit=False,
            fetch=True
        )
        return json.loads(result)

    @staticmethod
    def create(trade_id, user1_id, user2_id):
        data = json.dumps({str(user1_id): {'items': {}, 'agree': False}, str(user2_id): {'items': {}, 'agree': False}})
        Connection.make_request(
            f"INSERT INTO {trades_schema} (id, data) "
            f"VALUES (%s, %s)", params=(trade_id, data)
        )
        return json.loads(data)

    @staticmethod
    def add_item(trade_id, user_id, item_id, amount: int):
        data = Trade.get_data(trade_id)
        if item_id in data[str(user_id)]['items']:
            data[str(user_id)]['items'][item_id]['amount'] += amount
        else:
            data[str(user_id)]['items'][item_id] = {'amount': amount}
        Trade.update_data(trade_id, data)

    @staticmethod
    def clear_items(trade_id, user_id):
        data = Trade.get_data(trade_id)
        data[str(user_id)]['items'] = {}
        Trade.update_data(trade_id, data)

    @staticmethod
    def get_item_amount(trade_id, user_id, item_id):
        data = Trade.get_data(trade_id)
        if item_id not in data[str(user_id)]['items']:
            return 0
        else:
            return data[str(user_id)]['items'][item_id]['amount']

    @staticmethod
    def remove_item(trade_id, user_id, item_id, amount: int = None):
        data = Trade.get_data(str(trade_id))
        if item_id not in data[str(user_id)]:
            return
        else:
            if amount is not None:
                data[str(user_id)][item_id]['items']['amount'] -= amount
            else:
                data[str(user_id)].pop(item_id)
        Trade.update_data(trade_id, data)

    @staticmethod
    async def get_user(client, trade_id, index: int = 0, fetch: bool = True):
        data = Trade.get_data(str(trade_id))
        user_id = list(data)[index]
        if not fetch:
            return user_id
        return await User.get_user(client, user_id)

    @staticmethod
    def get_user_data(trade_id, user_id):
        data = Trade.get_data(str(trade_id))
        return data[str(user_id)]

    @staticmethod
    def set_agree(trade_id, user_id, agree: bool = True):
        data = Trade.get_data(str(trade_id))
        data[str(user_id)]['agree'] = agree
        Trade.update_data(trade_id, data)

    @staticmethod
    def is_agree(trade_id, user_id):
        data = Trade.get_data(str(trade_id))
        return data[str(user_id)]['agree']

    @staticmethod
    async def get_agree_number(client, trade_id):
        return sum([Trade.is_agree(trade_id, await Trade.get_user(client, trade_id, i, fetch=False)) for i in range(2)])
