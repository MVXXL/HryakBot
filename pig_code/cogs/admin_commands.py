import discord

from ..core import *
from ..utils import *
from .. import modules


class AdminCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @discord.app_commands.command(description='Check if the bot is ready')
    @discord.app_commands.guilds(*[*config.ADMIN_GUILDS, *config.TEST_GUILDS])
    @commands.is_owner()
    async def is_ready(self, inter):
        await Utils.pre_command_check(inter, owner_only=True)
        if self.client.is_ready():
            await send_callback(inter, f'*{self.client.user} is ready*')
        else:
            await send_callback(inter, f'*{self.client.user} is not ready*')

    @discord.app_commands.command(description='Sync the tree')
    @discord.app_commands.guilds(*[*config.ADMIN_GUILDS, *config.TEST_GUILDS])
    @commands.is_owner()
    async def sync_tree(self, inter):
        await Utils.pre_command_check(inter, owner_only=True)
        await self.client.tree.sync()
        for guild_id in config.ADMIN_GUILDS + config.TEST_GUILDS + config.PUBLIC_TEST_GUILDS:
            try:
                await self.client.tree.sync(guild=discord.Object(guild_id))
            except:
                pass
        await send_callback(inter, f'*Tree is synced*')

    @discord.app_commands.command(description='test')
    @discord.app_commands.guilds(*[*config.ADMIN_GUILDS, *config.TEST_GUILDS])
    @commands.is_owner()
    async def test(self, inter):
        await Utils.pre_command_check(inter, owner_only=True)
        o = Func.generate_aaio_url(100, f'test{random.randrange(1000)}', 'RUB', lang='ru')
        await send_callback(inter, f'{o}')

    @discord.app_commands.command(description='Block user from using the bot')
    @discord.app_commands.guilds(*[*config.ADMIN_GUILDS, *config.TEST_GUILDS])
    @commands.is_owner()
    async def block(self, inter, user: discord.User, reason: str = None):
        await Utils.pre_command_check(inter, owner_only=True)
        User.register_user_if_not_exists(user.id)
        User.set_block(user.id, True)
        User.set_block_reason(user.id, reason)
        await send_callback(inter, f'*User **{user}** has been blocked*')

    @discord.app_commands.command(description='Unblock user from using the bot')
    @discord.app_commands.guilds(*[*config.ADMIN_GUILDS, *config.TEST_GUILDS])
    @commands.is_owner()
    async def unblock(self, inter, user: discord.User):
        await Utils.pre_command_check(inter, owner_only=True)
        User.register_user_if_not_exists(user.id)
        User.set_block(user.id, False)
        User.set_block_reason(user.id, '')
        await send_callback(inter, f'*User **{user}** has been unblocked*')

    @discord.app_commands.command(description='Add item to user\'s inventory')
    @discord.app_commands.guilds(*[*config.ADMIN_GUILDS, *config.TEST_GUILDS, *config.PUBLIC_TEST_GUILDS])
    async def add_item(self, inter, user: discord.User, item_id: str, amount: int = 1):
        await Utils.pre_command_check(inter, owner_only=True)
        User.register_user_if_not_exists(user.id)
        if not Item.exists(item_id):
            await send_callback(inter, "*Item doesn't exist*")
        else:
            User.add_item(user.id, item_id, amount)
            await send_callback(inter, f'*User **{user}** received **{item_id} x{amount}***')

    @add_item.autocomplete('item_id')
    async def autocomplete_item_id(self, interaction, current: str):
        return [discord.app_commands.Choice(name=i, value=i) for i in
                difflib.get_close_matches(current, Tech.get_all_items(), n=25, cutoff=0.1)]

    @discord.app_commands.command(description='Add weight to user')
    @discord.app_commands.guilds(*[*config.ADMIN_GUILDS, *config.TEST_GUILDS, *config.PUBLIC_TEST_GUILDS])
    async def add_weight(self, inter, user: discord.User, amount: int = 1):
        await Utils.pre_command_check(inter, owner_only=True)
        Pig.add_weight(user.id, amount)
        await send_callback(inter, f'*User **{user}** received **{amount} kg***')

    @commands.slash_command(guild_ids=config.ADMIN_GUILDS,
                            description='Set order status')
    async def set_order_status(self, inter, order_id: str = commands.Param(description='Order ID'),
                               status=commands.Param(
                                   choices=['success', 'in_process', 'expired'])
                               ):
        await Utils.pre_command_check(inter)
        Order.set_status(order_id, status)
        await send_callback(inter, f'*Order **{order_id}** status has been set to **{status}***')

    @discord.app_commands.command(description='Add all available skins to user')
    @discord.app_commands.guilds(*[*config.ADMIN_GUILDS, *config.TEST_GUILDS])
    async def add_all_skins(self, inter,
                            user: discord.User):
        await Utils.pre_command_check(inter, owner_only=True)
        if user is None:
            user = inter.user
        User.register_user_if_not_exists(user.id)
        for item in Tech.get_all_items((('type', 'skin'),)):
            User.set_item_amount(user.id, item, 1)
        await send_callback(inter, f'*User **{user}** received all available skins*')

    @discord.app_commands.command(description='Update shop')
    @discord.app_commands.guilds(*[*config.ADMIN_GUILDS, *config.TEST_GUILDS, *config.PUBLIC_TEST_GUILDS])
    async def update_shop(self, inter):
        await Utils.pre_command_check(inter, owner_only=True)
        Shop.add_shop_state()
        await send_callback(inter, f'*Shop updated*')

    @discord.app_commands.command(description='Create a promo code')
    @discord.app_commands.describe(
        prise='Items that user will receive | Has to be json | Ex: {"coins": 10, "rare_case": 2}')
    @discord.app_commands.describe(lifespan='For how long the promocode will be usable (in minutes)')
    @discord.app_commands.guilds(*[*config.ADMIN_GUILDS, *config.TEST_GUILDS, *config.PUBLIC_TEST_GUILDS])
    async def create_promocode(self, inter, prise: str,
                               max_uses: int = 999999,
                               name: str = None,
                               lifespan: int = -1):
        await Utils.pre_command_check(inter, allowed_users=config.PROMOCODERS)
        try:
            prise = json.loads(prise)
            if type(prise) == list:
                raise
        except:
            await send_callback(inter,
                                embed=generate_embed(title=f'*Bad json*',
                                                     color=utils_config.error_color))
            return
        for item in prise:
            if not Item.exists(item):
                await send_callback(inter,
                                    embed=generate_embed(title=f'*Item **"{item}"** doesn\'t exist*',
                                                         color=utils_config.error_color))
                return
        if PromoCode.exists(name):
            PromoCode.delete(name)
        promo_code_code = PromoCode.create(max_uses, prise, lifespan=lifespan * 60,
                                           code=name)
        await send_callback(inter,
                            embed=generate_embed(title=f'*Promo code `{promo_code_code}` created*'))

    @discord.app_commands.command(description='Leave from a server')
    @discord.app_commands.guilds(*[*config.ADMIN_GUILDS, *config.TEST_GUILDS])
    async def leave(self, inter, server: str):
        await Utils.pre_command_check(inter, owner_only=True)
        await self.client.get_guild(int(server)).leave()
        await send_callback(inter, f'*I left from *{server}***')

    @discord.app_commands.command(description='Returns a list of guilds')
    @discord.app_commands.guilds(*[*config.ADMIN_GUILDS, *config.TEST_GUILDS])
    async def guilds(self, inter):
        await Utils.pre_command_check(inter, owner_only=True)
        d = {}
        for guild in self.client.guilds:
            d[guild] = len(set([i for i in guild.members if not i.bot]))
        d = dict(sorted(d.items(), key=lambda x: x[1], reverse=True))
        embeds = []
        total_member_count = 0
        for guild in self.client.guilds:
            total_member_count += guild.member_count
        title = f'🌐・{len(self.client.guilds)} | {len(set([i for i in self.client.get_all_members() if not i.bot]))}/{len(self.client.users)}'
        embed = generate_embed(title, '')
        for n, i in enumerate(d):
            embed.description += f"> {n+1}. {d[i]} | {i} [{i.id}]\n"
            if len(embed.description) >= 4000:
                embeds.append(embed)
                embed = generate_embed(title, '')
        embeds.append(embed)
        await Utils.pagination(inter, 'en', embeds=embeds)


async def setup(client):
    await client.add_cog(AdminCommands(client))
