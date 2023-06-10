import json
import random
import string

from ..core import *
from ..utils import *
from .. import modules


class AdminCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(guild_ids=config.ADMIN_GUILDS)
    @commands.is_owner()
    async def test(self, inter, sec: bool = False):
        await BotUtils.pre_command_check(inter)
        if sec:
            Connection.make_request(f"UPDATE {config.users_schema} SET events = '{'{}'}'")
        for user_id in Tech.get_all_users():
            print(user_id)
            # if User.get_language(user_id) == 'ru':
            if True:
                Events.add(user_id, title='Хочешь получить буст?',
                           # description='hello',
                           description='> Ты можешь получить буст в `5%` для веса хряка если находишься на сервере поддержки бота!\n\n'
                                       '> Также там каждый день выдаются `промокоды`!\n\n'
                                       '*Вот ссылка: https://discord.gg/btYvZZTeQx*',
                           expires_in=60 * 60 * 36, event_id='server_ad')

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
    async def unblock(self, inter, user: disnake.User = commands.Param(description='User or user\'s ID')):
        await BotUtils.pre_command_check(inter)
        User.register_user_if_not_exists(user.id)
        User.set_block(user.id, False)
        User.set_block_reason(user.id, '')
        await BotUtils.send_callback(inter, embed=BotUtils.generate_embed(title=f'User ***{user}*** was unblocked'))

    @user.sub_command(guild_ids=config.ADMIN_GUILDS, description='Block user from using promocodes')
    async def block_promocodes(self, inter, user: disnake.User = commands.Param(description='User or user\'s ID')):
        await BotUtils.pre_command_check(inter)
        User.register_user_if_not_exists(user.id)
        User.set_block_promocodes(user.id, True)
        await BotUtils.send_callback(inter, embed=BotUtils.generate_embed(
            title=f'User ***{user}*** was blocked from using promocodes'))

    @user.sub_command(guild_ids=config.ADMIN_GUILDS, description='Unblock user from using promocodes')
    async def unblock_promocodes(self, inter, user: disnake.User = commands.Param(description='User or user\'s ID')):
        await BotUtils.pre_command_check(inter)
        User.register_user_if_not_exists(user.id)
        User.set_block_promocodes(user.id, False)
        await BotUtils.send_callback(inter, embed=BotUtils.generate_embed(
            title=f'User ***{user}*** was unblocked from promos'))

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
        await BotUtils.send_callback(inter,
                                     embed=BotUtils.generate_embed(title=f'Balance of ***{user}*** now is {amount} 🪙'))

    @user.sub_command(guild_ids=config.ADMIN_GUILDS, description='Add money to user')
    async def reset_last_feed(self, inter,
                              user: disnake.User = commands.Param(description='User or user\'s ID', default=None)):
        await BotUtils.pre_command_check(inter)
        if user is None:
            user = inter.author
        Pig.set_last_feed(user.id, 0)
        await BotUtils.send_callback(inter, embed=BotUtils.generate_embed(title=f'You reset last feed for {user}'))

    @user.sub_command(guild_ids=config.ADMIN_GUILDS, description='Create user')
    async def create_user(self, inter,
                          user: disnake.User = commands.Param(description='User or user\'s ID', default=None)):
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

    @commands.slash_command(guild_ids=config.ADMIN_GUILDS)
    async def promo_code(self, inter):
        if inter.author.id not in [461480892188065792, 778291476073414656] + [inter.client.owner_id]:
            raise NotAllowedToUseCommand

    @promo_code.sub_command(description='Create promo code')
    async def create(self, inter, prise: str = commands.Param(description='Items that user will receive'),
                     max_uses: int = commands.Param(description='Max uses of promo code'),
                     promo_code_code: str = commands.Param(description='Promo code name', name='name',
                                                           default=None),
                     expires_in: int = commands.Param(description='Promocode will expire in seconds',
                                                      default=-1, large=True),
                     can_use: str = commands.Param(description='Who can use promo code',
                                                   default='everyone',
                                                   choices=['everyone', 'everyone_except_blocked'])):
        await BotUtils.pre_command_check(inter)
        # await server.leave()
        try:
            prise = json.loads(prise)
            if type(prise) == list:
                raise
        except:
            await BotUtils.send_callback(inter,
                                         embed=BotUtils.generate_embed(title=f'Bad json',
                                                                       color=utils_config.error_color))
            return
        for item in prise:
            if item not in items:
                await BotUtils.send_callback(inter,
                                             embed=BotUtils.generate_embed(title=f'Item "{item}" not exist',
                                                                           color=utils_config.error_color))
                return
        promo_code_code = PromoCode.create(max_uses, prise, expires_in=expires_in, can_use=can_use,
                                           code=promo_code_code)
        await BotUtils.send_callback(inter,
                                     embed=BotUtils.generate_embed(title=f'Promo code "{promo_code_code}" created'))

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
