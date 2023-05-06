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
        await BotUtils.send_callback(inter, embed=BotUtils.generate_embed(title=f'User ***{user}*** was blocked',
                                                                         color=utils_config.main_color,
                                                                         footer=f'ID: {user.id}',
                                                                         footer_url=Func.generate_footer_url('user_avatar', user)))

    @user.sub_command(guild_ids=config.ADMIN_GUILDS, description='Unblock user')
    async def unblock_user(self, inter, user: disnake.User = commands.Param(description='User or user\'s ID')):
        await BotUtils.pre_command_check(inter)
        User.register_user_if_not_exists(user.id)
        User.set_block(user.id, False)
        User.set_block_reason(user.id, '')
        await BotUtils.send_callback(inter, embed=BotUtils.generate_embed(title=f'User ***{user}*** was unblocked',
                                                                         color=utils_config.main_color,
                                                                         footer=f'ID: {user.id}',
                                                                         footer_url=Func.generate_footer_url('user_avatar', user)))

    @user.sub_command(guild_ids=config.ADMIN_GUILDS, description='Give premium to user')
    async def give_premium(self, inter, user: disnake.User = commands.Param(description='User or user\'s ID')):
        await BotUtils.pre_command_check(inter)
        User.register_user_if_not_exists(user.id)
        User.set_premium(user.id, True)
        await BotUtils.send_callback(inter, embed=BotUtils.generate_embed(title=f'User ***{user}*** got premium',
                                                                         color=utils_config.main_color,
                                                                         footer=f'ID: {user.id}',
                                                                         footer_url=Func.generate_footer_url('user_avatar', user)))

    @user.sub_command(guild_ids=config.ADMIN_GUILDS, description='Remove premium from user')
    async def remove_premium(self, inter, user: disnake.User = commands.Param(description='User or user\'s ID')):
        await BotUtils.pre_command_check(inter)
        User.register_user_if_not_exists(user.id)
        User.set_premium(user.id, False)
        await BotUtils.send_callback(inter, embed=BotUtils.generate_embed(title=f'User ***{user}*** lost premium',
                                                                         color=utils_config.main_color,
                                                                         footer=f'ID: {user.id}',
                                                                         footer_url=Func.generate_footer_url('user_avatar', user)))

    @user.sub_command(guild_ids=config.ADMIN_GUILDS, description='Remove premium from user')
    async def add_item(self, inter, user: disnake.User = commands.Param(description='User or user\'s ID'),
                        item: str = commands.Param(description='Item ID'),
                        amount: int = commands.Param(description='Amount of item', default=1)):
        await BotUtils.pre_command_check(inter)
        User.register_user_if_not_exists(user.id)
        if item not in items:
            await BotUtils.send_callback(inter, 'Item not exist')
        else:
            Inventory.add_item(user.id, item, amount)
            await BotUtils.send_callback(inter, embed=BotUtils.generate_embed(title=f'User ***{user}*** got {item} x{amount}',
                                                                             color=utils_config.main_color,
                                                                             footer=f'ID: {user.id}',
                                                                         footer_url=Func.generate_footer_url('user_avatar', user)))

    @dev.sub_command_group()
    async def server(self, inter):
        pass

    @server.sub_command(description='Leave from a server')
    async def leave(self, inter, server: disnake.Guild = commands.Param(description='Server\'s ID')):
        await BotUtils.pre_command_check(inter)
        await server.leave()
        await BotUtils.send_callback(inter, embed=BotUtils.generate_embed(title=f'I left from ***{server}***',
                                                                         color=utils_config.main_color,
                                                                         footer=f'ID: {server.id}',
                                                                         footer_url=Func.generate_footer_url('user_avatar', self.client.user)))


def setup(client):
    client.add_cog(AdminCommands(client))
