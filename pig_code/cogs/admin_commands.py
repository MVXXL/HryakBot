import disnake
import requests

from ..core import *
from ..utils import *
from .. import modules


class AdminCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def autocomplete_items(inter: disnake.ApplicationCommandInteraction, user_input: str):
        return difflib.get_close_matches(user_input, Tech.get_all_items(), n=25, cutoff=0.1)

    @commands.slash_command(guild_ids=config.ADMIN_GUILDS)
    @commands.is_owner()
    async def test(self, inter):
        await inter.response.defer()
        r = await Func.async_speed_test(BotUtils.generate_user_pig, user_id=inter.author.id)
        await send_callback(inter, r)

    @commands.slash_command(guild_ids=config.ADMIN_GUILDS)
    @commands.is_owner()
    async def test2(self, inter):
        await inter.response.defer()
        components = [[disnake.ui.Button(label='-') for _ in range(5)] for _ in range(5)]
        await send_callback(inter, components=components)

    @commands.slash_command(guild_ids=config.ADMIN_GUILDS)
    @commands.is_owner()
    async def create_item(self, inter, item_id, _type, emoji,
                          skin_type=None,
                          image_file_1_url=None,
                          image_file_1_file: disnake.Attachment=None,
                          image_file_2_url=None,
                          image_file_2_file: disnake.Attachment=None,
                          cooked_item_id=None,
                          market_price: int = None,
                          market_price_currency: str = None,
                          salable: bool=False,
                          sell_price: int = None,
                          sell_price_currency: str = None,
                          tradable: bool=True,
                          rarity=commands.Param(choices=['1', '2', '3', '4', '5', '6']),
                          shop_category=commands.Param(choices=['always', 'daily', 'cases', 'premium_skins'], default=None),
                          inventory_type=commands.Param(choices=['inventory', 'wardrobe'])):
        await BotUtils.pre_command_check(inter)
        await send_callback(inter, '---------------------------\n'*5)
        data = {
            'id': item_id,
            'type': _type,
            'emoji': emoji,
            'cooked_item_id': cooked_item_id,
            'market_price': market_price,
            'market_price_currency': market_price_currency,
            'salable': salable,
            'sell_price': sell_price,
            'sell_price_currency': sell_price_currency,
            'tradable': tradable,
            'rarity': rarity,
            'shop_category': shop_category,
            'inventory_type': inventory_type,
            'skin_type': skin_type
        }
        if image_file_1_url is not None:
            data['image_file'] = requests.get(image_file_1_url).content
        if image_file_1_file is not None:
            data['image_file'] = await image_file_1_file.read()
        if image_file_2_url is not None:
            data['image_file_2'] = requests.get(image_file_2_url).content
        if image_file_2_file is not None:
            data['image_file_2'] = await image_file_2_file.read()
        for k, v in {'name': '{"en": "Cool item", "ru": "Крутой предмет"}',
                  'description': '{"en": "Its so cool", "ru": "Это очень крутой предмет"}',
                  # 'not_draw_skins': '["mouth", "blue_hat"]',
                  # 'not_compatible_skins': '["mouth", "blue_hat"]',
                  'requirements': '[[{"role": 1111, "guild": 1234}, '
                                       '{"role": 2222, "guild": 1234}], [{"guild": 4321}]]',
                  'case_drops': '[[{"items": ["coins"], "amount": [1, 5], "chance": 85}, {"items": ["hollars"], "amount": [1, 3], "chance": 15}], [{"items": ["red_hat"], "amount": [1, 1], "chance": 15}]]]',
                  'shop_cooldown': '{"2": 79200}'}.items():
            m = await send_callback(inter, f'> {k}\n> \n> Example: {v}', ctx_message=True)
            while True:
                message = await self.client.wait_for('message')
                print(message.reference)
                if message.author.id == inter.author.id and message.channel.id == inter.channel.id and\
                        len(message.mentions) > 0 and self.client.user.id == message.mentions[0].id and message.reference.message_id == m.id:
                    if message.content == '-':
                        break
                    try:
                        data[k] = Func.str_to_dict(message.content)
                    except:
                        continue
                    break
        Item.create(data)
        await send_callback(inter, f'Added: {item_id}', ctx_message=True)

    @commands.slash_command(guild_ids=config.ADMIN_GUILDS)
    @commands.is_owner()
    async def auto_add_to_cases(self, inter, item_id: str):
        rarity = Item.get_rarity(item_id)
        drops = Item.get_case_drops('common_case')
        try:
            drops[2][
                {"2": 0,
                 "3": 1,
                 "4": 2,
                 "5": 3}[rarity]
            ]['items'].append(item_id)
            Item.edit('common_case', {'case_drops': json.dumps(drops)})
        except IndexError:
            pass
        drops = Item.get_case_drops('rare_case')
        try:
            drops[2][
                {"3": 0,
                 "4": 1,
                 "5": 2}[rarity]
            ]['items'].append(item_id)
            Item.edit('rare_case', {'case_drops': json.dumps(drops)})
        except IndexError:
            pass
        await send_callback(inter, f'Yep', ctx_message=True)


    @commands.slash_command(guild_ids=config.ADMIN_GUILDS)
    @commands.is_owner()
    async def edit_item(self, inter, item_id=commands.Param(autocomp=autocomplete_items), col=commands.Param()):
        await BotUtils.pre_command_check(inter)
        await send_callback(inter, '---------------------------\n'*5)
        m = await send_callback(inter, embed=generate_embed(description=f'Old data: ```{Item.get_data(item_id, col)}```'), ctx_message=True)
        data = {}
        while True:
            message = await self.client.wait_for('message')
            print(message)
            print(message.author.id == inter.author.id, message.channel.id == inter.channel.id,len(message.mentions) > 0,
                  self.client.user.id == message.mentions[0].id, message.reference.message_id == m.id)
            if message.author.id == inter.author.id and message.channel.id == inter.channel.id and \
                    len(message.mentions) > 0 and self.client.user.id == message.mentions[0].id and message.reference.message_id == m.id:
                if message.content == '-':
                    break
                # try:
                if type(Func.str_to_dict(message.content)) in [dict, list]:
                    data[col] = Func.str_to_dict(message.content)
                elif type(Func.str_to_dict(message.content)) == int:
                    data[col] = int(message.content)
                else:
                    data[col] = message.content
                # except Exception as e:
                #     print(e)
                #     continue
                break
        print(data)
        Item.edit(item_id, data)
        await m.reply('👍')

    @commands.slash_command(guild_ids=config.ADMIN_GUILDS, description='Block user')
    async def block(self, inter, user: disnake.User = commands.Param(description='User or user\'s ID'),
                    reason: str = commands.Param(description='Reason', default=None)):
        await BotUtils.pre_command_check(inter)
        User.register_user_if_not_exists(user.id)
        User.set_block(user.id, True)
        User.set_block_reason(user.id, reason)
        await send_callback(inter, embed=generate_embed(title=f'User ***{user}*** was blocked'))

    @commands.slash_command(guild_ids=config.ADMIN_GUILDS, description='Unblock user')
    async def unblock(self, inter, user: disnake.User = commands.Param(description='User or user\'s ID')):
        await BotUtils.pre_command_check(inter)
        User.register_user_if_not_exists(user.id)
        User.set_block(user.id, False)
        User.set_block_reason(user.id, '')
        await send_callback(inter, embed=generate_embed(title=f'User ***{user}*** was unblocked'))

    @commands.slash_command(guild_ids=config.ADMIN_GUILDS + config.PUBLIC_TEST_GUILDS,
                            description='Add item by it\'s id')
    async def add_item(self, inter, user: disnake.User = commands.Param(description='User or user\'s ID'),
                       item: str = commands.Param(description='Item ID', autocomp=autocomplete_items),
                       amount: int = commands.Param(description='Amount of item', default=1)):
        await BotUtils.pre_command_check(inter)
        User.register_user_if_not_exists(user.id)
        if not Item.exists(item):
            await send_callback(inter, 'Item not exist')
        else:
            User.add_item(user.id, item, amount)
            await send_callback(inter,
                                embed=generate_embed(title=f'User ***{user}*** got {item} x{amount}'))

    @commands.slash_command(guild_ids=config.ADMIN_GUILDS + config.PUBLIC_TEST_GUILDS,
                            description='Remove item by it\'s id')
    async def remove_item(self, inter, user: disnake.User = commands.Param(description='User or user\'s ID'),
                          item: str = commands.Param(description='Item ID', autocomp=autocomplete_items),
                          amount: int = commands.Param(description='Amount of item', default=1)):
        await BotUtils.pre_command_check(inter)
        User.register_user_if_not_exists(user.id)
        if not Item.exists(item):
            await send_callback(inter, 'Item not exist')
        else:
            User.add_item(user.id, item, -amount)
            await send_callback(inter,
                                embed=generate_embed(title=f'User ***{user}*** lost {item} x{amount}'))

    @commands.slash_command(guild_ids=config.ADMIN_GUILDS + config.PUBLIC_TEST_GUILDS, description='Add money to user')
    async def add_money(self, inter, user: disnake.User = commands.Param(description='User or user\'s ID'),
                        amount: int = commands.Param(description='Amount of money', default=1)):
        await BotUtils.pre_command_check(inter)
        User.add_item(user.id, 'coins', amount)
        await send_callback(inter, embed=generate_embed(title=f'User ***{user}*** got {amount} 🪙'))

    # @commands.slash_command(guild_ids=config.ADMIN_GUILDS + config.PUBLIC_TEST_GUILDS, description='Add money to user')
    # async def set_money(self, inter, user: disnake.User = commands.Param(description='User or user\'s ID'),
    #                     amount: int = commands.Param(description='Amount of money', default=1)):
    #     await BotUtils.pre_command_check(inter)
    #     User.set_money(user.id, amount)
    #     await send_callback(inter,
    #                         embed=generate_embed(title=f'Balance of ***{user}*** now is {amount} 🪙'))

    @commands.slash_command(guild_ids=config.ADMIN_GUILDS + config.PUBLIC_TEST_GUILDS, description='Add weight to user')
    async def add_weight(self, inter, user: disnake.User = commands.Param(description='User or user\'s ID'),
                         amount: int = commands.Param(description='Amount of money', default=1)):
        await BotUtils.pre_command_check(inter)
        Pig.add_weight(user.id, amount)
        await send_callback(inter, embed=generate_embed(title=f'User ***{user}*** got {amount} kg'))

    @commands.slash_command(guild_ids=config.ADMIN_GUILDS, description='Add money to user')
    async def reset_last_feed(self, inter,
                              user: disnake.User = commands.Param(description='User or user\'s ID', default=None)):
        await BotUtils.pre_command_check(inter)
        if user is None:
            user = inter.author
        Pig.set_last_feed(user.id, 0)
        await send_callback(inter, embed=generate_embed(title=f'You reset last feed for {user}'))

    @commands.slash_command(guild_ids=config.ADMIN_GUILDS, description='Create user')
    async def create_user(self, inter,
                          user: disnake.User = commands.Param(description='User or user\'s ID', default=None)):
        await BotUtils.pre_command_check(inter)
        User.register_user_if_not_exists(user.id)
        await send_callback(inter, embed=generate_embed(title=f'User created: {user}'))

    @commands.slash_command(guild_ids=config.ADMIN_GUILDS, description='Add all posible skins to user')
    async def add_all_skins(self, inter,
                            user: disnake.User = commands.Param(description='User or user\'s ID', default=None)):
        await BotUtils.pre_command_check(inter)
        if user is None:
            user = inter.author
        User.register_user_if_not_exists(user.id)
        for item in Tech.get_all_items((('type', 'skin'),)):
            User.set_item_amount(user.id, item, 1)
        await send_callback(inter,
                            embed=generate_embed(title=f'User ***{user}*** got all skins'))

    @commands.slash_command(guild_ids=config.ADMIN_GUILDS + config.PUBLIC_TEST_GUILDS, description='Update shop')
    async def update_shop(self, inter):
        await BotUtils.pre_command_check(inter)
        Shop.add_shop_state()
        await send_callback(inter, embed=generate_embed(title=f'Shop updated'))

    @commands.slash_command(guild_ids=config.ADMIN_GUILDS + config.PUBLIC_TEST_GUILDS)
    async def _promocode(self, inter):
        if inter.author.id not in [1090715886056378398] + [inter.client.owner_id]:
            raise NotAllowedToUseCommand

    @_promocode.sub_command(description='Create promo code')
    async def create(self, inter, prise: str = commands.Param(description='Items that user will receive'),
                     max_uses: int = commands.Param(description='Max uses of promo code'),
                     promo_code_code: str = commands.Param(description='Promo code name', name='name',
                                                           default=None),
                     expires_in: int = commands.Param(description='Promocode will expire in seconds',
                                                      default=-1, large=True)):
        await BotUtils.pre_command_check(inter)
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
            if not Item.exists(item):
                await send_callback(inter,
                                    embed=generate_embed(title=f'Item "{item}" not exist',
                                                         color=utils_config.error_color))
                return
        if PromoCode.exists(promo_code_code):
            PromoCode.delete(promo_code_code)
        promo_code_code = PromoCode.create(max_uses, prise, expires_in=expires_in,
                                           code=promo_code_code)
        await send_callback(inter,
                            embed=generate_embed(title=f'Promo code "{promo_code_code}" created'))

    @commands.slash_command(guild_ids=config.ADMIN_GUILDS, description='Leave from a server')
    async def leave(self, inter, server: disnake.Guild = commands.Param(description='Server\'s ID')):
        await BotUtils.pre_command_check(inter)
        await server.leave()
        await send_callback(inter, embed=generate_embed(title=f'I left from ***{server}***'))

    @commands.slash_command(guild_ids=config.ADMIN_GUILDS, description='Check user')
    async def check(self, inter, user: disnake.User = commands.Param(description='User or id')):
        await BotUtils.pre_command_check(inter)
        found_in_guilds = []
        for guild in self.client.guilds:
            if user in guild.members:
                found_in_guilds.append(guild)
        embeds = []
        tf = Func.check_consecutive_timestamps(Pig.get_feed_history(user.id)[-40:], 6 * 3600, 4 * 3600)
        title = f'{len(found_in_guilds)}w{Pig.get_weight(user.id)}m{Item.get_amount("coins", user.id)}c{tf}\n'
        embed = generate_embed(title, '')
        User.register_user_if_not_exists(user.id)
        for guild in found_in_guilds:
            member = guild.get_member(user.id)
            embed.description += f'[{guild}]({guild.icon.url if guild.icon is not None else ""}).' \
                                 f'{guild.id}.' \
                                 f'm{len(guild.members)}r{len(member.roles)}.' \
                                 f'{"o" if member.id == guild.owner_id else "-"}<t:{round(guild.created_at.timestamp())}:R><t:{round(member.joined_at.timestamp())}:R>\n'
            if len(embed.description) >= 3900:
                embeds.append(embed)
                embed = generate_embed(title, '')
        embeds.append(embed)
        await BotUtils.pagination(inter, 'ru', embeds=embeds)

    # @commands.slash_command(guild_ids=config.ADMIN_GUILDS, description='Check user')
    # async def guild(self, inter, user: disnake.User = commands.Param(description='User or id')):
    #     await BotUtils.pre_command_check(inter)
    #     found_in_guilds = []
    #     for guild in self.client.guilds:
    #         if user in guild.members:
    #             found_in_guilds.append(guild)
    #     res_text = '-\n'
    #     for guild in found_in_guilds:
    #         member = guild.get_member(user.id)
    #         print(dir(member))
    #         res_text += f'[{guild}]({guild.icon.url}).' \
    #                     f'{guild.id}.' \
    #                     f'm{len(guild.members)}r{len(member.roles)}.' \
    #                     f'{"o" if member.id == guild.owner_id else "-"}<t:{round(guild.created_at())}:R><t:{round(member.joined_at.timestamp())}:R>\n'
    #     await send_callback(inter, res_text)

    @commands.slash_command(guild_ids=config.ADMIN_GUILDS, description='Bot servers')
    async def servers(self, inter):
        await BotUtils.pre_command_check(inter)
        # for i in self.client.get_all_members():
        #     print(dir(i))
        d = {}
        for guild in self.client.guilds:
            d[guild] = len(set([i for i in guild.members if not i.bot]))
        d = dict(sorted(d.items(), key=lambda x: x[1], reverse=True))
        embeds = []
        title = f'**{len(self.client.guilds)}** | ' \
                f'**{len(set([i for i in self.client.get_all_members() if not i.bot]))}**'
        embed = generate_embed(title, '')
        for i in d:
            embed.description += f"> [{i.id}]  `{d[i]}`| `{i}`\n"
            if len(embed.description) >= 4000:
                embeds.append(embed)
                embed = generate_embed(title, '')
        embeds.append(embed)
        await BotUtils.pagination(inter, 'en', embeds=embeds)
        await send_callback(inter, f'**{len(self.client.guilds)}** | '
                                   f'**{len(set([i for i in self.client.get_all_members() if not i.bot]))}**\n\n'
                                   f'{"".join([f"> [{guild.id}]  `{len(guild.members)}`| `{guild}`" for guild in d])}')
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
