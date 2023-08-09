from .connection import Connection
from .tech import Tech
from .user import User
from ..functions import Func
from ...core import *
from ...core.config import trades_schema
from .inventory import Inventory


class Trades:

    @staticmethod
    def exists(trade_id):
        result = Connection.make_request(
            f"SELECT EXISTS(SELECT 1 FROM {trades_schema} WHERE id = {trade_id})",
            commit=False,
            fetch=True
        )
        return bool(result)

    @staticmethod
    def update_trade(trade_id, new_trade):
        new_trade = json.dumps(new_trade, ensure_ascii=False)
        Connection.make_request(
            f"UPDATE {trades_schema} SET data = %s WHERE id = {trade_id}", (new_trade,)
        )

    @staticmethod
    def get_trade_data(trade_id):
        print(trade_id)
        result = Connection.make_request(
            f"SELECT data FROM {trades_schema} WHERE id = {trade_id}",
            commit=False,
            fetch=True
        )
        return json.loads(result)

    @staticmethod
    def create_trade(trade_id, user1_id, user2_id):
        data = json.dumps({str(user1_id): {}, str(user2_id): {}})
        Connection.make_request(
            f"INSERT INTO {trades_schema} (id, data) "
            f"VALUES (%s, %s)", params=(trade_id, data)
        )
        return json.loads(data)

    @staticmethod
    def add_item_to_trade(trade_id, user_id, item_id, amount: int):
        data = Trades.get_trade_data(trade_id)
        if item_id in data[str(user_id)]:
            data[str(user_id)][item_id]['amount'] += amount
        else:
            data[str(user_id)][item_id] = {'amount': amount}
        Trades.update_trade(trade_id, data)

    @staticmethod
    def get_trade_item_amount(trade_id, user_id, item_id):
        data = Trades.get_trade_data(trade_id)
        if item_id not in data[str(user_id)]:
            return 0
        else:
            return data[str(user_id)][item_id]['amount']

    @staticmethod
    def remove_item_from_trade(trade_id, user_id, item_id, amount: int = None):
        data = Trades.get_trade_data(str(trade_id))
        if item_id not in data[str(user_id)]:
            return
        else:
            if amount is not None:
                data[str(user_id)][item_id]['amount'] -= amount
            else:
                data[str(user_id)].pop(item_id)
        Trades.update_trade(trade_id, data)

    @staticmethod
    async def get_user(client, trade_id, index: int = 0, fetch: bool = True):
        data = Trades.get_trade_data(str(trade_id))
        user_id = list(data)[index]
        if not fetch:
            return user_id
        return await User.get_user(client, user_id)

    @staticmethod
    def get_user_data(trade_id, index: int = 0):
        data = Trades.get_trade_data(str(trade_id))
        return data[list(data)[index]]
