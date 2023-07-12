from ..core import *
from ..utils import *
from .. import modules


class AdminCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(guild_ids=config.ADMIN_GUILDS)
    @commands.is_owner()
    async def test(self, inter, sec: bool = False):
        await Botutils.pre_command_check(inter)
        await send_callback(inter, embed=generate_embed('Hello'),
                            components=[
                                [disnake.ui.Button(label='Hello1'),
                                 disnake.ui.Button(label='Hello1'),
                                 disnake.ui.Button(label='Hello1'),
                                 disnake.ui.Button(label='Hello1'),
                                 disnake.ui.Button(label='Hello1')],
                                [disnake.ui.Button(label='Hello1'),
                                 disnake.ui.Button(label='Hello1'),
                                 disnake.ui.Button(label='Hello1'),
                                 disnake.ui.Button(label='Hello1'),
                                 disnake.ui.Button(label='Hello1')],
                                [disnake.ui.Button(label='Hello1'),
                                 disnake.ui.Button(label='Hello1'),
                                 disnake.ui.Button(label='Hello1'),
                                 disnake.ui.Button(label='Hello1'),
                                 disnake.ui.Button(label='Hello1')],
                                [disnake.ui.Button(label='Hello1'),
                                 disnake.ui.Button(label='Hello1'),
                                 disnake.ui.Button(label='Hello1'),
                                 disnake.ui.Button(label='Hello1'),
                                 disnake.ui.Button(label='Hello1')]]

                            )
    @commands.slash_command(guild_ids=config.ADMIN_GUILDS, description='Block user')
    async def block(self, inter, user: disnake.User = commands.Param(description='User or user\'s ID'),
                    reason: str = commands.Param(description='Reason', default=None)):
        await Botutils.pre_command_check(inter)
        User.register_user_if_not_exists(user.id)
        User.set_block(user.id, True)
        User.set_block_reason(user.id, reason)
        await send_callback(inter, embed=generate_embed(title=f'User ***{user}*** was blocked'))

    @commands.slash_command(guild_ids=config.ADMIN_GUILDS, description='Unblock user')
    async def unblock(self, inter, user: disnake.User = commands.Param(description='User or user\'s ID')):
        await Botutils.pre_command_check(inter)
        User.register_user_if_not_exists(user.id)
        User.set_block(user.id, False)
        User.set_block_reason(user.id, '')
        await send_callback(inter, embed=generate_embed(title=f'User ***{user}*** was unblocked'))

    @commands.slash_command(guild_ids=config.ADMIN_GUILDS, description='Block user from using promocodes')
    async def block_promocodes(self, inter, user: disnake.User = commands.Param(description='User or user\'s ID')):
        await Botutils.pre_command_check(inter)
        User.register_user_if_not_exists(user.id)
        User.set_block_promocodes(user.id, True)
        await send_callback(inter, embed=generate_embed(
            title=f'User ***{user}*** was blocked from using promocodes'))

    @commands.slash_command(guild_ids=config.ADMIN_GUILDS, description='Unblock user from using promocodes')
    async def unblock_promocodes(self, inter, user: disnake.User = commands.Param(description='User or user\'s ID')):
        await Botutils.pre_command_check(inter)
        User.register_user_if_not_exists(user.id)
        User.set_block_promocodes(user.id, False)
        await send_callback(inter, embed=generate_embed(
            title=f'User ***{user}*** was unblocked from promos'))

    @commands.slash_command(guild_ids=config.ADMIN_GUILDS, description='Give premium to user')
    async def give_premium(self, inter, user: disnake.User = commands.Param(description='User or user\'s ID')):
        await Botutils.pre_command_check(inter)
        User.register_user_if_not_exists(user.id)
        User.set_premium(user.id, True)
        await send_callback(inter, embed=generate_embed(title=f'User ***{user}*** got premium',
                                                        color=utils_config.main_color,
                                                        footer=f'ID: {user.id}',
                                                        footer_url=Func.generate_footer_url(
                                                            'user_avatar', user)))

    @commands.slash_command(guild_ids=config.ADMIN_GUILDS, description='Remove premium from user')
    async def remove_premium(self, inter, user: disnake.User = commands.Param(description='User or user\'s ID')):
        await Botutils.pre_command_check(inter)
        User.register_user_if_not_exists(user.id)
        User.set_premium(user.id, False)
        await send_callback(inter, embed=generate_embed(title=f'User ***{user}*** lost premium'))

    @commands.slash_command(guild_ids=config.ADMIN_GUILDS + config.PUBLIC_TEST_GUILDS, description='Add item by it\'s id')
    async def add_item(self, inter, user: disnake.User = commands.Param(description='User or user\'s ID'),
                       item: str = commands.Param(description='Item ID'),
                       amount: int = commands.Param(description='Amount of item', default=1)):
        await Botutils.pre_command_check(inter)
        User.register_user_if_not_exists(user.id)
        if item not in items:
            await send_callback(inter, 'Item not exist')
        else:
            User.add_item(user.id, item, amount)
            await send_callback(inter,
                                embed=generate_embed(title=f'User ***{user}*** got {item} x{amount}'))

    @commands.slash_command(guild_ids=config.ADMIN_GUILDS + config.PUBLIC_TEST_GUILDS, description='Add money to user')
    async def add_money(self, inter, user: disnake.User = commands.Param(description='User or user\'s ID'),
                        amount: int = commands.Param(description='Amount of money', default=1)):
        await Botutils.pre_command_check(inter)
        User.add_money(user.id, amount)
        await send_callback(inter, embed=generate_embed(title=f'User ***{user}*** got {amount} 🪙'))

    @commands.slash_command(guild_ids=config.ADMIN_GUILDS + config.PUBLIC_TEST_GUILDS, description='Add money to user')
    async def set_money(self, inter, user: disnake.User = commands.Param(description='User or user\'s ID'),
                        amount: int = commands.Param(description='Amount of money', default=1)):
        await Botutils.pre_command_check(inter)
        User.set_money(user.id, amount)
        await send_callback(inter,
                            embed=generate_embed(title=f'Balance of ***{user}*** now is {amount} 🪙'))

    @commands.slash_command(guild_ids=config.ADMIN_GUILDS + config.PUBLIC_TEST_GUILDS, description='Add weight to user')
    async def add_weight(self, inter, user: disnake.User = commands.Param(description='User or user\'s ID'),
                        amount: int = commands.Param(description='Amount of money', default=1)):
        await Botutils.pre_command_check(inter)
        Pig.add_weight(user.id, amount)
        await send_callback(inter, embed=generate_embed(title=f'User ***{user}*** got {amount} kg'))

    @commands.slash_command(guild_ids=config.ADMIN_GUILDS, description='Add money to user')
    async def reset_last_feed(self, inter,
                              user: disnake.User = commands.Param(description='User or user\'s ID', default=None)):
        await Botutils.pre_command_check(inter)
        if user is None:
            user = inter.author
        Pig.set_last_feed(user.id, 0)
        await send_callback(inter, embed=generate_embed(title=f'You reset last feed for {user}'))

    @commands.slash_command(guild_ids=config.ADMIN_GUILDS, description='Create user')
    async def create_user(self, inter,
                          user: disnake.User = commands.Param(description='User or user\'s ID', default=None)):
        await Botutils.pre_command_check(inter)
        User.register_user_if_not_exists(user.id)
        Pig.create_pig_if_no_pig(user.id)
        await send_callback(inter, embed=generate_embed(title=f'User created: {user}'))

    @commands.slash_command(guild_ids=config.ADMIN_GUILDS, description='Add all posible skins to user')
    async def add_all_skins(self, inter,
                            user: disnake.User = commands.Param(description='User or user\'s ID', default=None)):
        await Botutils.pre_command_check(inter)
        if user is None:
            user = inter.author
        User.register_user_if_not_exists(user.id)
        for item in Func.get_items_by_key(items, 'type', 'skin'):
            User.set_item_amount(user.id, item, 1)
        await send_callback(inter,
                            embed=generate_embed(title=f'User ***{user}*** got all skins'))

    @commands.slash_command(guild_ids=config.ADMIN_GUILDS + config.PUBLIC_TEST_GUILDS, description='Update shop')
    async def update_shop(self, inter):
        await Botutils.pre_command_check(inter)
        Shop.add_shop_state(Func.generate_shop_daily_items())
        await send_callback(inter, embed=generate_embed(title=f'Shop updated'))

    @commands.slash_command(guild_ids=config.ADMIN_GUILDS)
    async def _promocode(self, inter):
        if inter.author.id not in [461480892188065792, 778291476073414656] + [inter.client.owner_id]:
            raise NotAllowedToUseCommand

    @_promocode.sub_command(description='Create promo code')
    async def create(self, inter, prise: str = commands.Param(description='Items that user will receive'),
                     max_uses: int = commands.Param(description='Max uses of promo code'),
                     promo_code_code: str = commands.Param(description='Promo code name', name='name',
                                                           default=None),
                     expires_in: int = commands.Param(description='Promocode will expire in seconds',
                                                      default=-1, large=True),
                     can_use: str = commands.Param(description='Who can use promo code',
                                                   default='everyone',
                                                   choices=['everyone', 'everyone_except_blocked'])):
        await Botutils.pre_command_check(inter)
        # await server.leave()
        try:
            prise = json.loads(prise)
            if type(prise) == list:
                raise
        except:
            await send_callback(inter,
                                embed=generate_embed(title=f'Bad json',
                                                     color=utils_config.error_color))
            return
        for item in prise:
            if item not in items:
                await send_callback(inter,
                                    embed=generate_embed(title=f'Item "{item}" not exist',
                                                         color=utils_config.error_color))
                return
        promo_code_code = PromoCode.create(max_uses, prise, expires_in=expires_in, can_use=can_use,
                                           code=promo_code_code)
        await send_callback(inter,
                            embed=generate_embed(title=f'Promo code "{promo_code_code}" created'))

    @commands.slash_command()
    async def server(self, inter):
        pass

    @server.sub_command(description='Leave from a server')
    async def leave(self, inter, server: disnake.Guild = commands.Param(description='Server\'s ID')):
        await Botutils.pre_command_check(inter)
        await server.leave()
        await send_callback(inter, embed=generate_embed(title=f'I left from ***{server}***'))

    @server.sub_command(description='Bot servers')
    async def servers(self, inter):
        await Botutils.pre_command_check(inter)
        # for i in self.client.get_all_members():
        #     print(dir(i))
        await send_callback(inter, f'{len(self.client.guilds)} '
                                   f'{len(set([i for i in self.client.get_all_members() if not i.bot]))}')
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
        # page_embeds = generate_embeds_list_from_fields(item_fields, title='Servers')
        # page_components = BotUtils.generate_select_components_for_pages(options, 'guild_select', 'Choose server')
        # await BotUtils.pagination(inter, 'en', embeds=page_embeds, components=page_components if options else None,
        #                           hide_button=False)


def setup(client):
    client.add_cog(AdminCommands(client))
