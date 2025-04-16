from ..core import *
from ..utils import *
from .. import modules


class Tasks(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.daily_shop_update.start()
        self.process_streaks.start()
        self.process_orders.start()
        if not config.TEST:
            self.monitoring_data_update.start()

    @tasks.loop(seconds=60)
    async def register_guilds(self):
        await self.client.wait_until_ready()
        Guild.register([guild.id for guild in self.client.guilds])

    @tasks.loop(seconds=60)
    async def process_streaks(self):
        await self.client.wait_until_ready()
        users = Tech.get_all_users(where=f"JSON_EXTRACT(stats, '$.streak') > 0")
        print(users)
        for user_id in users:
            if hryak.GameFunc.calculate_missed_streak_days(user_id) > 1:
                Stats.set_streak(user_id, 0)
            await asyncio.sleep(1)

    @tasks.loop(seconds=60)
    async def daily_shop_update(self):
        last_update_timestamp = Shop.get_update_timestamp()
        if config.TEST:
            Shop.add_shop_state()
        if last_update_timestamp is None:
            Shop.add_shop_state()
        elif last_update_timestamp < int(
                datetime.datetime.combine(datetime.date.today(), datetime.time(0, 0)).timestamp()):
            Shop.add_shop_state()

    @tasks.loop(seconds=300)
    async def give_items(self):
        await self.client.wait_until_ready()
        for item_id in Tech.get_all_items(exceptions=(('requirements', None),)):
            allowed_users = Item.get_all_allowed_users_by_requirements(self.client, item_id)
            for user_id in allowed_users:
                User.register_user_if_not_exists(user_id)
                User.set_item_amount(user_id, item_id, 1)
                await asyncio.sleep(.1)
            for user_id in Tech.get_all_users(where=f"JSON_EXTRACT(inventory, '$.{item_id}.amount') > 0",
                                              exclude_users=allowed_users):
                User.set_item_amount(user_id, item_id, 0)
                await asyncio.sleep(.1)

    @tasks.loop(seconds=5)
    async def process_orders(self):
        for order_id in Order.get_all_orders():
            user_id = Order.get_user(order_id)
            lang = User.get_language(user_id)
            if Order.get_status(order_id) in ['success', 'hold']:
                await DisUtils.send_notification(await User.get_user(self.client, user_id),
                                                 title=translate(Locale.PremiumShop.item_give_notification_title, lang),
                                                 description=translate(Locale.PremiumShop.item_give_notification_desc,
                                                                       lang, {'items': DisUtils.get_items_in_str_list(
                                                      Order.get_items(order_id),
                                                      User.get_language(user_id))}),
                                                 prefix_emoji='💎')
                for item_id, amount in Order.get_items(order_id).items():
                    User.add_item(user_id, item_id, amount)
                Stats.add_successful_orders(user_id, 1)
                Stats.add_dollars_donated(user_id, round(
                    Order.get_amount(order_id) / utils_config.currency_to_usd[Order.get_currency(order_id)], 2))
                Order.delete(order_id)
            await asyncio.sleep(.3)

    @tasks.loop(seconds=3600)
    async def monitoring_data_update(self):
        await self.client.wait_until_ready()
        servers = len(self.client.guilds)
        Func.send_data_to_sdc(self.client)
        Func.send_data_to_boticord(self.client)
        await Func.send_data_to_stats_channel(self.client, servers)


async def setup(client):
    await client.add_cog(Tasks(client))
