from ..core import *
from ..utils import *
from .. import modules


class Tasks(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.daily_shop_update.start()
        self.give_items.start()
        self.test.start()
        if not config.TEST:
            self.monitoring_data_update.start()
            self.create_logs_copy.start()

    @tasks.loop(seconds=10)
    async def test(self):
        print(1)
        utils_config.profiler.dump_stats(f'output_file{"" if not config.TEST else "_test"}.prof')
        utils_config.profiler.disable()
        utils_config.profiler.enable()

        # print(globals(), len(str(globals())))

    @tasks.loop(seconds=60)
    async def daily_shop_update(self):
        last_update_timestamp = Shop.get_update_timestamp()
        if config.TEST:
            Shop.add_shop_state()
        if last_update_timestamp is None:
            Shop.add_shop_state()
        elif last_update_timestamp < int(datetime.datetime.combine(datetime.date.today(), datetime.time(0, 0)).timestamp()):
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
            for user_id in Tech.get_all_users(include_where=f"JSON_EXTRACT(inventory, '$.{item_id}.amount') > 0", exclude_users=allowed_users):
                User.set_item_amount(user_id, item_id, 0)
                await asyncio.sleep(.1)


    @tasks.loop(seconds=3600)
    async def monitoring_data_update(self):
        # Tech.create_user_table()
        # Tech.create_shop_table()
        # Tech.create_promo_code_table()
        # Tech.create_guild_table()
        # Tech.create_families_table()
        # Tech.create_trades_table()
        # Tech.create_items_table()
        # print('tables created')
        # await Pig.fix_pig_structure_for_all_users()
        # print('pig structure fixed')
        # await Stats.fix_stats_structure_for_all_users()
        # print('stats structure fixed')
        # await Tech.fix_settings_structure_for_all_users()
        # print('settings structure fixed')
        # await Guild.fix_settings_structure_for_all_guilds()
        # print('guild structure fixed')
        # for guild in self.client.guilds:
        #     Guild.register_guild_if_not_exists(guild.id)
        #     await asyncio.sleep(0.1)
        # print('guilds registered')
        # with open('user_data.json', 'r') as f:
        #     data = json.load(f)
        #     for k, v in data.items():
        #         print(k, v)
        #         User.register_user_if_not_exists(k)
        #         User.add_item(k, 'coins', v['money'])
        #         User.set_new_settings(k, v['settings'])
        await self.client.wait_until_ready()
        servers = len(self.client.guilds)
        Func.send_data_to_sdc(self.client)
        Func.send_data_to_boticord(self.client)
        await Func.send_data_to_stats_channel(self.client, servers)

    @tasks.loop(seconds=2 * 3600)
    async def create_logs_copy(self):
        try:
            async with aiofiles.open(config.RESERVE_LOGS_FOLDER_PATH + f'/logs_copy_{Func.get_current_timestamp()}.json', 'w') as f:
                await f.write(open(config.LOGS_PATH, 'r').read())
            async with aiofiles.open(config.LOGS_PATH, 'w') as f:
                await f.write('')
        except Exception as e:
            print(e)


def setup(client):
    client.add_cog(Tasks(client))
