import json
import os
import time

import discord_webhook
import disnake

from ..core.items.item_components.item_components import item_components
from ..utils import *
from .. import modules


class Events(commands.Cog):
    def __init__(self, client):
        self.client = client
        aiocache.Cache(Cache.MEMORY)
        if not config.TEST or config.PUBLIC_TEST:
            init_data = {'start': Func.get_current_timestamp()}
            if config.HOSTING_TYPE == 'pc':
                init_data['pid'] = os.getpid()
            with open(config.INIT_DATA_PATH, 'w') as f:
                f.write(json.dumps(init_data))
        handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, os.getpid())
        win32process.SetPriorityClass(handle, win32process.HIGH_PRIORITY_CLASS)
        # Tech.create_user_table()
        # Tech.create_shop_table()
        # Tech.create_promo_code_table()
        # Tech.create_guild_table()
        # Tech.create_families_table()
        # Tech.create_trades_table()
        # Tech.create_items_table()
        if not config.TEST:
            Func.clear_folder(config.TEMP_FOLDER_PATH)

    @commands.Cog.listener()
    async def on_ready(self):
        print(self.client.user)
        Tech.create_user_table()
        Tech.create_shop_table()
        Tech.create_promo_code_table()
        Tech.create_guild_table()
        Tech.create_families_table()
        Tech.create_trades_table()
        Tech.create_items_table()
        print('tables created')
        Guild.register([guild.id for guild in self.client.guilds])
        print('guilds registered')
        # await Pig.fix_pig_structure_for_all_users()
        # print('pig structure fixed')
        # await Stats.fix_stats_structure_for_all_users()
        # print('stats structure fixed')
        # await Tech.fix_settings_structure_for_all_users()
        # print('settings structure fixed')
        # await Guild.fix_settings_structure_for_all_guilds()
        # print('guild structure fixed')

    @commands.Cog.listener()
    async def on_message_interaction(self, interaction):
        User.register_user_if_not_exists(interaction.author.id)
        custom_id_params = interaction.component.custom_id.split(';')
        try:
            Func.add_log('interaction',
                         custom_id_params=custom_id_params,
                         interaction_values=interaction.values,
                         user=interaction.author.id)
        except:
            Func.add_log('fail_to_log_interaction')
        if custom_id_params[0] == 'in':
            return
        allowed_users = []
        custom_id_params = interaction.component.custom_id.split(';')
        lang = User.get_language(interaction.author.id)
        if custom_id_params[0] == 'trade':
            trade_id = None
            if custom_id_params[1] == 'add':
                trade_id = interaction.values[0].split(';')[1]
            elif custom_id_params[1] in ['agree', 'cancel', 'clear', 'add_item']:
                trade_id = custom_id_params[2]
            user1_id = await Trade.get_user(interaction.client, trade_id, 0, fetch=False)
            user2_id = await Trade.get_user(interaction.client, trade_id, 1, fetch=False)
            allowed_users.append(int(user1_id))
            allowed_users.append(int(user2_id))
        if interaction.message.interaction is not None:
            if not BotUtils.check_if_right_user(interaction, except_users=allowed_users):
                await error_callbacks.wrong_component_clicked(interaction)
                return
        if custom_id_params[0] == 'trade':
            if custom_id_params[1] == 'add':
                interaction_values_params = interaction.values[0].split(';')
                action_object = interaction_values_params[0]
                trade_id = interaction_values_params[1]
                user1 = await Trade.get_user(interaction.client, trade_id, 0)
                user2 = await Trade.get_user(interaction.client, trade_id, 1)
                if action_object == 'coins':
                    async def update_trade_and_add_item(inter, item_id, amount):
                        await inter.response.defer(ephemeral=True)
                        await inter.delete_original_message()
                        Trade.add_item(trade_id, inter.author.id, item_id, amount)
                        await modules.trade.callbacks.trade(interaction,
                                                            user1,
                                                            user2,
                                                            trade_id=trade_id,
                                                            pre_command_check=False)

                    await interaction.response.send_modal(
                        modals.GetItemAmountModal(interaction, action_object, update_trade_and_add_item,
                                                  f'Добавить монеты (комиссия {BotUtils.get_commission(interaction.author, user1 if user1.id != interaction.author.id else user2)} %)',
                                                  'Трейд',
                                                  max_amount=Item.get_amount('coins',
                                                                             interaction.author.id) - Trade.get_item_amount(
                                                      trade_id, interaction.author.id, 'coins')))
                if action_object == 'inventory':
                    await modules.inventory.callbacks.inventory(interaction, pre_command_check=False,
                                                                select_item_component_id=f'trade;add_item;{trade_id}',
                                                                ephemeral=True, edit_original_message=False,
                                                                tradable_items_only=True)
                if action_object == 'wardrobe':
                    await modules.inventory.callbacks.wardrobe(interaction, pre_command_check=False,
                                                               select_item_component_id=f'trade;add_item;{trade_id}',
                                                               ephemeral=True, edit_original_message=False,
                                                               tradable_items_only=True)
            elif custom_id_params[1] in ['agree', 'cancel', 'clear', 'add_item']:
                trade_id = custom_id_params[2]
                user1_id = await Trade.get_user(interaction.client, trade_id, 0, fetch=False)
                user2_id = await Trade.get_user(interaction.client, trade_id, 1, fetch=False)
                if custom_id_params[1] == 'agree':
                    await interaction.response.defer()
                    Trade.set_agree(trade_id, interaction.author.id,
                                    True if not Trade.is_agree(trade_id, interaction.author.id) else False)
                    await modules.trade.callbacks.trade(interaction,
                                                        await Trade.get_user(interaction.client, trade_id, 0),
                                                        await Trade.get_user(interaction.client, trade_id, 1),
                                                        trade_id=trade_id,
                                                        pre_command_check=False)
                elif custom_id_params[1] == 'cancel':
                    await error_callbacks.default_error_callback(interaction,
                                                                 translate(Locales.Trade.cancel_title, lang),
                                                                 translate(Locales.Trade.cancel_desc, lang).format(
                                                                     user=interaction.author.display_name),
                                                                 thumbnail_file=await Func.get_image_path_from_link(
                                                                     utils_config.image_links['trade']))
                elif custom_id_params[1] == 'clear':
                    await interaction.response.defer()
                    Trade.set_agree(trade_id, user1_id, False)
                    Trade.set_agree(trade_id, user2_id, False)
                    Trade.clear_items(trade_id, interaction.author.id)
                    await modules.trade.callbacks.trade(interaction,
                                                        await Trade.get_user(interaction.client, trade_id, 0),
                                                        await Trade.get_user(interaction.client, trade_id, 1),
                                                        trade_id=trade_id,
                                                        pre_command_check=False)
                elif custom_id_params[1] == 'add_item':
                    action_object = interaction.values[0].split(';')[0]

                    async def add_item_and_update_trade(inter, item_id, amount):
                        await inter.response.defer(ephemeral=True)
                        await inter.delete_original_message()
                        await interaction.delete_original_message()
                        Trade.add_item(trade_id, inter.author.id, item_id, amount)
                        await modules.trade.callbacks.trade(interaction,
                                                            await Trade.get_user(interaction.client, trade_id, 0),
                                                            await Trade.get_user(interaction.client, trade_id, 1),
                                                            trade_id=trade_id,
                                                            pre_command_check=False)

                    await interaction.response.send_modal(
                        modals.GetItemAmountModal(interaction, action_object, add_item_and_update_trade,
                                                  f'Добавить {Item.get_name(action_object, lang)}', 'Трейд',
                                                  max_amount=Item.get_amount(action_object,
                                                                             interaction.author.id) - Trade.get_item_amount(
                                                      trade_id, interaction.author.id, action_object)))
        if custom_id_params[0] in ['like', 'dislike']:
            if custom_id_params[0] == 'like':
                User.append_rate(custom_id_params[1], interaction.author.id, 1)
            elif custom_id_params[0] == 'dislike':
                User.append_rate(custom_id_params[1], interaction.author.id, -1)
            await modules.other.callbacks.profile(interaction,
                                                  await User.get_user(interaction.client, custom_id_params[1]),
                                                  pre_command_check=False)
        if custom_id_params[0] == 'family':
            if custom_id_params[1] == 'view_profile':
                await modules.family.callbacks.family_profile(interaction, interaction.values[0])
            elif custom_id_params[1] == 'join_requests':
                if custom_id_params[2] == 'view_profile':
                    await modules.other.callbacks.profile(interaction,
                                                          await User.get_user(self.client, interaction.values[0]),
                                                          edit_original_message=False, ephemeral=True,
                                                          pre_command_check=False,
                                                          _components=modules.family.components.accept_reject_user_to_family(
                                                              User.get_language(interaction.author.id),
                                                              interaction.values[0],
                                                              User.get_family(interaction.author.id)))
                elif custom_id_params[2] == 'accept':
                    await modules.family.callbacks.accept_user_to_family(interaction, custom_id_params[3],
                                                                         custom_id_params[4])
                elif custom_id_params[2] == 'reject':
                    await modules.family.callbacks.reject_user_to_family(interaction, custom_id_params[3],
                                                                         custom_id_params[4])
            elif custom_id_params[1] == 'kick_user':
                await modules.family.callbacks.family_member_kick(interaction, custom_id_params[2], custom_id_params[3])
            elif custom_id_params[1] == 'ban_user':
                await modules.family.callbacks.family_member_ban(interaction, custom_id_params[2], custom_id_params[3])
        # if interaction.component.custom_id == 'inventory_item_select':
        #     await modules.inventory.callbacks.inventory_item_selected(interaction, interaction.values[0])
        # elif interaction.component.custom_id == 'wardrobe_item_select':
        #     await modules.inventory.callbacks.wardrobe_item_selected(interaction, interaction.values[0])
        # elif interaction.component.custom_id == 'shop_item_select':
        #     await modules.shop.callbacks.shop_item_selected(interaction, interaction.values[0])
        elif custom_id_params[0] == 'view_profile':
            await modules.other.callbacks.profile(interaction, await User.get_user(self.client, interaction.values[0]),
                                                  edit_original_message=False, ephemeral=True, pre_command_check=False)
        if custom_id_params[0] == 'item_select':
            if custom_id_params[1] == 'inventory':
                await modules.inventory.callbacks.inventory_item_selected(interaction, interaction.values[0],
                                                                          category=custom_id_params[2],
                                                                          page=int(custom_id_params[3]))
            elif custom_id_params[1] == 'wardrobe':
                await modules.inventory.callbacks.wardrobe_item_selected(interaction, interaction.values[0],
                                                                         category=custom_id_params[2],
                                                                         page=int(custom_id_params[3]))
            elif custom_id_params[1] == 'shop':
                await modules.shop.callbacks.shop_item_selected(interaction, interaction.values[0],
                                                                category=custom_id_params[2],
                                                                page=int(custom_id_params[3]))
        if custom_id_params[0] == 'back_to_inventory':
            if custom_id_params[1] == 'inventory':
                await modules.inventory.callbacks.inventory(interaction, init_category=custom_id_params[2],
                                                            init_page=int(custom_id_params[3]))
            if custom_id_params[1] == 'wardrobe':
                await modules.inventory.callbacks.wardrobe(interaction, init_category=custom_id_params[2],
                                                           init_page=int(custom_id_params[3]))
            if custom_id_params[1] == 'shop':
                await modules.shop.callbacks.shop(interaction, init_category=custom_id_params[2],
                                                  init_page=int(custom_id_params[3]))
        # elif len(interaction.component.custom_id.split(';')) == 2:
        #     lang = User.get_language(interaction.author.id)
        #     action_object = interaction.component.custom_id.split(';')[1]
        #     action = interaction.component.custom_id.split(';')[0]
        #     if action == 'back_to_inventory':
        #         match action_object:
        #             case 'inventory':
        #                 await modules.inventory.callbacks.inventory(interaction)
        #             case 'wardrobe':
        #                 await modules.inventory.callbacks.wardrobe(interaction)
        #             case 'shop':
        #                 await modules.shop.callbacks.shop(interaction)
        elif custom_id_params[0] == 'preview_skin':
            await modules.other.callbacks.skin_preview(interaction, custom_id_params[1])
        elif custom_id_params[0] == 'buy':
            await modules.shop.callbacks.shop_item_buy(interaction, custom_id_params[1])
        elif custom_id_params[0] == 'wear_skin':
            await modules.inventory.callbacks.wardrobe_item_wear(interaction, custom_id_params[1],
                                                                 category=custom_id_params[2],
                                                                 page=int(custom_id_params[3]))
        elif custom_id_params[0] == 'remove_skin':
            await modules.inventory.callbacks.wardrobe_item_remove(interaction, custom_id_params[1],
                                                                   category=custom_id_params[2],
                                                                   page=int(custom_id_params[3]))
        elif len(custom_id_params) > 1 and custom_id_params[1] in item_components and custom_id_params[0] in \
                item_components[custom_id_params[1]]:
            async def update_inventory():
                if Item.get_amount(custom_id_params[1], interaction.author.id) == 0:
                    if Item.get_inventory_type(custom_id_params[1]) == 'wardrobe':
                        await modules.inventory.callbacks.wardrobe(interaction, interaction.message,
                                                                   init_category=custom_id_params[2],
                                                                   init_page=int(custom_id_params[3]))
                    elif Item.get_inventory_type(custom_id_params[1]) == 'inventory':
                        await modules.inventory.callbacks.inventory(interaction, interaction.message,
                                                                    init_category=custom_id_params[2],
                                                                    init_page=int(custom_id_params[3]))
                else:
                    await modules.inventory.callbacks.inventory_item_selected(interaction, custom_id_params[1],
                                                                              interaction.message)

            if Item.get_amount(custom_id_params[1], interaction.author.id) <= 0:
                await error_callbacks.no_item(interaction, custom_id_params[1])
                await update_inventory()
                return
            result = await item_components[custom_id_params[1]][custom_id_params[0]]['func'](interaction,
                                                                                             custom_id_params[1],
                                                                                             update_inventory)
            if result is None:
                result = {}
            if 'callback' in item_components[custom_id_params[1]][custom_id_params[0]]:
                embed = generate_embed(
                    title=translate(item_components[custom_id_params[1]][custom_id_params[0]]['callback']['title'],
                                    lang),
                    description=translate(
                        item_components[custom_id_params[1]][custom_id_params[0]]['callback']['description'], lang,
                        format_options=result),
                    prefix=Func.generate_prefix(
                        item_components[custom_id_params[1]][custom_id_params[0]]['callback']['prefix']),
                    inter=interaction,
                )
                await send_callback(interaction, embed=embed,
                                    ephemeral=True, edit_original_message=False)
                await update_inventory()
        elif interaction.component.custom_id == 'hide':
            await interaction.message.delete()

    @commands.Cog.listener()
    async def on_slash_command_error(self, inter, error):
        await error_callbacks.error(error, inter)

    @commands.Cog.listener()
    async def on_user_command_error(self, inter, error):
        await error_callbacks.error(error, inter)

    @commands.Cog.listener()
    async def on_application_command(self, inter):
        User.register_user_if_not_exists(inter.author.id)
        try:
            command_name, options = Func.get_command_name_and_options(inter)
            Stats.add_commands_used(inter.author.id, command_name)
            is_dm = True if inter.guild is None else False
            Func.add_log('command_used',
                         user_name=str(inter.author),
                         user_id=inter.author.id,
                         guild_name=str(inter.guild) if not is_dm else None,
                         guild_id=inter.guild.id if not is_dm else None,
                         channel_name=str(inter.channel) if not is_dm else 'DM',
                         channel_id=inter.channel.id,
                         command=command_name,
                         options=options)
        except Exception as e:
            print(e)
            raise e

    @commands.Cog.listener()
    async def on_guild_join(self, guild: disnake.Guild):
        Guild.register_guild_if_not_exists(guild.id)
        Func.add_log('guild_join',
                     owner_id=guild.owner_id,
                     guild_name=str(guild),
                     guild_id=guild.id,
                     members=guild.member_count)
        # User.register_user_if_not_exists(guild.owner_id)
        # if User.get_money(guild.owner_id) < 80 and \
        #         len(Func.get_items_by_key(User.get_inventory(guild.owner_id), 'type', 'skin')) < 1 and \
        #         len(Func.get_items_by_key(User.get_inventory(guild.owner_id), 'type', 'case')) < 1:
        #     User.add_item(guild.owner_id, 'common_case', 1)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.channel_id == config.BOT_HALYAVA_CHANNEL:
            if payload.emoji.name == '✅' and payload.member.id in [461480892188065792, 715575898388037676,
                                                                   778291476073414656]:
                money = random.randrange(80, 120)
                if datetime.datetime.now().day in [1, 2, 3]:
                    money *= 2
                message = await self.client.get_channel(payload.channel_id).fetch_message(payload.message_id)
                User.add_item(message.author.id, 'coins', money)
                await message.reply(f'*Выдана награда: **{money}** 🪙*')

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: disnake.Guild):
        Func.add_log('guild_remove',
                     owner_id=guild.owner_id,
                     guild_name=str(guild),
                     guild_id=guild.id,
                     members=guild.member_count)

    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member):
        join_channel = Guild.join_channel(member.guild.id)
        join_channel = member.guild.get_channel(join_channel)
        if join_channel is not None:
            await join_channel.send(Guild.join_message(member.guild.id).format(user=member.mention))
        if member.guild.id == config.BOT_GUILD:
            if (Pig.get_weight(member.id) < 1.5 and User.get_age(member.id) < 3600) or \
                    Func.get_current_timestamp() - member.created_at.timestamp() < 7 * 24 * 3600:
                await member.add_roles(member.guild.get_role(config.NOT_VERIFIED_ROLE))

    @commands.Cog.listener()
    async def on_message(self, message):
        print(message.type)
        if message.type == disnake.MessageType.premium_guild_subscription:
            print(f'boost - {message}\n' * 50)

    @commands.Cog.listener()
    async def on_mention(self, message):
        print('<Mentioned>')

    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     print(message)
    #     print(message.content)


def setup(client):
    client.add_cog(Events(client))
