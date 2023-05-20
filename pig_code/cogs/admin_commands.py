import random

from ..core import *
from ..utils import *
from .. import modules


class AdminCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(guild_ids=config.ADMIN_GUILDS)
    @commands.is_owner()
    async def dev(self, inter):
        pass

    @dev.sub_command_group()
    async def user(self, inter):
        pass

    @user.sub_command(guild_ids=config.ADMIN_GUILDS, description='Block user')
    async def block(self, inter, user: disnake.User = commands.Param(description='User or user\'s ID'),
                    reason: str = commands.Param(description='Reason', default=None)):
        await BotUtils.pre_command_check(inter)
        User.register_user_if_not_exists(user.id)
        User.set_block(user.id, True)
        User.set_block_reason(user.id, reason)
        await BotUtils.send_callback(inter, embed=BotUtils.generate_embed(title=f'User ***{user}*** was blocked'))

    @user.sub_command(guild_ids=config.ADMIN_GUILDS, description='Unblock user')
    async def unblock_user(self, inter, user: disnake.User = commands.Param(description='User or user\'s ID')):
        await BotUtils.pre_command_check(inter)
        User.register_user_if_not_exists(user.id)
        User.set_block(user.id, False)
        User.set_block_reason(user.id, '')
        await BotUtils.send_callback(inter, embed=BotUtils.generate_embed(title=f'User ***{user}*** was unblocked'))

    @user.sub_command(guild_ids=config.ADMIN_GUILDS, description='Give premium to user')
    async def give_premium(self, inter, user: disnake.User = commands.Param(description='User or user\'s ID')):
        await BotUtils.pre_command_check(inter)
        User.register_user_if_not_exists(user.id)
        User.set_premium(user.id, True)
        await BotUtils.send_callback(inter, embed=BotUtils.generate_embed(title=f'User ***{user}*** got premium',
                                                                          color=utils_config.main_color,
                                                                          footer=f'ID: {user.id}',
                                                                          footer_url=Func.generate_footer_url(
                                                                              'user_avatar', user)))

    @user.sub_command(guild_ids=config.ADMIN_GUILDS, description='Remove premium from user')
    async def remove_premium(self, inter, user: disnake.User = commands.Param(description='User or user\'s ID')):
        await BotUtils.pre_command_check(inter)
        User.register_user_if_not_exists(user.id)
        User.set_premium(user.id, False)
        await BotUtils.send_callback(inter, embed=BotUtils.generate_embed(title=f'User ***{user}*** lost premium'))

    @user.sub_command(guild_ids=config.ADMIN_GUILDS, description='Add item by it\'s id')
    async def add_item(self, inter, user: disnake.User = commands.Param(description='User or user\'s ID'),
                       item: str = commands.Param(description='Item ID'),
                       amount: int = commands.Param(description='Amount of item', default=1)):
        await BotUtils.pre_command_check(inter)
        User.register_user_if_not_exists(user.id)
        if item not in items:
            await BotUtils.send_callback(inter, 'Item not exist')
        else:
            Inventory.add_item(user.id, item, amount)
            await BotUtils.send_callback(inter,
                                         embed=BotUtils.generate_embed(title=f'User ***{user}*** got {item} x{amount}'))

    @user.sub_command(guild_ids=config.ADMIN_GUILDS, description='Add money to user')
    async def add_money(self, inter, user: disnake.User = commands.Param(description='User or user\'s ID'),
                       amount: int = commands.Param(description='Amount of money', default=1)):
        await BotUtils.pre_command_check(inter)
        User.add_money(user.id, amount)
        await BotUtils.send_callback(inter, embed=BotUtils.generate_embed(title=f'User ***{user}*** got {amount} 🪙'))

    @user.sub_command(guild_ids=config.ADMIN_GUILDS, description='Add money to user')
    async def set_money(self, inter, user: disnake.User = commands.Param(description='User or user\'s ID'),
                       amount: int = commands.Param(description='Amount of money', default=1)):
        await BotUtils.pre_command_check(inter)
        User.set_money(user.id, amount)
        await BotUtils.send_callback(inter, embed=BotUtils.generate_embed(title=f'Balance of ***{user}*** now is {amount} 🪙'))

    @user.sub_command(guild_ids=config.ADMIN_GUILDS, description='Add money to user')
    async def reset_last_feed(self, inter, user: disnake.User = commands.Param(description='User or user\'s ID', default=None)):
        await BotUtils.pre_command_check(inter)
        if user is None:
            user = inter.author
        Pig.set_last_feed(user.id, 0)
        await BotUtils.send_callback(inter, embed=BotUtils.generate_embed(title=f'You reset last feed for {user}'))

    @user.sub_command(guild_ids=config.ADMIN_GUILDS, description='Create user')
    async def create_user(self, inter, user: disnake.User = commands.Param(description='User or user\'s ID', default=None)):
        await BotUtils.pre_command_check(inter)
        User.register_user_if_not_exists(user.id)
        Pig.create_pig_if_no_pig(user.id)
        await BotUtils.send_callback(inter, embed=BotUtils.generate_embed(title=f'User created: {user}'))

    @user.sub_command(guild_ids=config.ADMIN_GUILDS, description='Add all posible skins to user')
    async def add_all_skins(self, inter,
                            user: disnake.User = commands.Param(description='User or user\'s ID', default=None)):
        await BotUtils.pre_command_check(inter)
        if user is None:
            user = inter.author
        User.register_user_if_not_exists(user.id)
        for item in Func.get_items_by_key(items, 'type', 'skin'):
            Inventory.set_item_amount(user.id, item, 1)
        await BotUtils.send_callback(inter,
                                     embed=BotUtils.generate_embed(title=f'User ***{user}*** got all skins'))

    @dev.sub_command(guild_ids=config.ADMIN_GUILDS, description='Update shop')
    async def update_shop(self, inter):
        await BotUtils.pre_command_check(inter)
        Shop.add_shop_state(Func.generate_shop_daily_items())
        await BotUtils.send_callback(inter, embed=BotUtils.generate_embed(title=f'Shop updated'))

    @dev.sub_command_group()
    async def server(self, inter):
        pass

    @server.sub_command(description='Leave from a server')
    async def leave(self, inter, server: disnake.Guild = commands.Param(description='Server\'s ID')):
        await BotUtils.pre_command_check(inter)
        await server.leave()
        await BotUtils.send_callback(inter, embed=BotUtils.generate_embed(title=f'I left from ***{server}***'))

    @server.sub_command(description='Bot servers')
    async def servers(self, inter):
        await BotUtils.pre_command_check(inter)
        await BotUtils.send_callback(inter, f'{len(self.client.guilds)}')
        # options = []
        # item_fields = []
        # for guild in self.client.guilds:
        #     item_fields.append(
        #         {
        #             'name': f'{guild}',
        #             'value': f'```Members: {len(guild.members)}\n'
        #                      f'{guild.id}```',
        #             'inline': True})
        #     options.append(
        #         {'label': f'{guild}',
        #          'value': guild.id,
        #          'description': f'Members: {len(guild.members)}',
        #          'emoji': None,
        #          }
        #     )
        # page_embeds = BotUtils.generate_embeds_list_from_fields(item_fields, title='Servers')
        # page_components = BotUtils.generate_select_components_for_pages(options, 'guild_select', 'Choose server')
        # await BotUtils.pagination(inter, 'en', embeds=page_embeds, components=page_components if options else None,
        #                           hide_button=False)


def setup(client):
    client.add_cog(AdminCommands(client))
