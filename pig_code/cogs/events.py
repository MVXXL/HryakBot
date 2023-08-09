import time

from ..other.item_components.item_components import item_components
from ..utils import *
from .. import modules


class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(self.client.user)
        # print(Func.get_number_of_possible_skin_variations())
        # print(User.get_pig(Tech.get_all_users()))
        # users = User.get_pig(Tech.get_all_users())
        # await self.client.change_presence(
        #     activity=disnake.Activity(type=disnake.ActivityType.watching, name=f'/help'))
        Tech.create_user_table()
        Tech.create_shop_table()
        Tech.create_promo_code_table()
        Tech.create_guild_table()
        Tech.create_families_table()
        Tech.create_trades_table()
        print('tables created')
        await Pig.fix_pig_structure_for_all_users()
        print('pig structure fixed')
        await Stats.fix_stats_structure_for_all_users()
        print('stats structure fixed')
        await Guild.fix_settings_structure_for_all_guilds()
        print('guild structure fixed')
        for guild in self.client.guilds:
            Guild.register_guild_if_not_exists(guild.id)
            await asyncio.sleep(0.1)
        print('guilds registered')
        aiocache.Cache(Cache.MEMORY)

    @commands.Cog.listener()
    async def on_message_interaction(self, interaction):
        if interaction.component.custom_id.startswith('in:'):
            return
        if interaction.message.interaction is not None:
            except_users = []
            if interaction.component.custom_id == 'add_to_trade':
                except_users.append(int(await Trades.get_user(interaction.client, interaction.values[0].split(':')[1], 1, fetch=False)))
                except_users.append(
                    int(await Trades.get_user(interaction.client, interaction.values[0].split(':')[1], 0, fetch=False)))
            if not BotUtils.check_if_right_user(interaction, except_users=except_users):
                await error_callbacks.wrong_component_clicked(interaction)
                return
        if interaction.component.custom_id == 'inventory_item_select':
            await modules.inventory.callbacks.inventory_item_selected(interaction, interaction.values[0])
        elif interaction.component.custom_id == 'add_to_trade':
            lang = User.get_language(interaction.author.id)
            action_object = interaction.values[0].split(':')[0]
            trade_id = interaction.values[0].split(':')[1]
            # if action_object == 'coins':
            #     async def update_trade_and_add_item(inter, item_id, amount):
            #         await inter.response.defer(ephemeral=True)
            #         await inter.delete_original_message()
            #         await interaction.delete_original_message()
            #         Trades.add_item_to_trade(trade_id, inter.author.id, item_id, amount)
            #         await modules.trade.callbacks.trade(interaction,
            #                                             await Trades.get_user(interaction.client, trade_id, 0),
            #                                             await Trades.get_user(interaction.client, trade_id, 1),
            #                                             trade_id=trade_id,
            #                                             pre_command_check=False)
            #
            #     await interaction.response.send_modal(
            #         modals.GetItemAmountModal(interaction, action_object, update_trade_and_add_item,
            #                                   f'Добавить монеты (комиссия {BotUtils.get_commission()} %)', 'Трейд'))
            if action_object == 'inventory':
                await modules.inventory.callbacks.inventory(interaction, pre_command_check=False,
                                                            select_item_component_id=f'add_item_to_trade:{trade_id}',
                                                            ephemeral=True, edit_original_message=False)
            if action_object == 'wardrobe':
                await modules.inventory.callbacks.wardrobe(interaction, pre_command_check=False,
                                                            select_item_component_id=f'add_item_to_trade:{trade_id}',
                                                            ephemeral=True, edit_original_message=False)
        elif interaction.component.custom_id.startswith('add_item_to_trade'):
            lang = User.get_language(interaction.author.id)
            action_object = interaction.values[0].split(':')[0]
            trade_id = interaction.component.custom_id.split(':')[1]
            async def update_trade_and_add_item(inter, item_id, amount):
                await inter.response.defer(ephemeral=True)
                await inter.delete_original_message()
                await interaction.delete_original_message()
                Trades.add_item_to_trade(trade_id, inter.author.id, item_id, amount)
                await modules.trade.callbacks.trade(interaction, await Trades.get_user(interaction.client, trade_id, 0),
                                                    await Trades.get_user(interaction.client, trade_id, 1), trade_id=trade_id,
                                                    pre_command_check=False)

            await interaction.response.send_modal(modals.GetItemAmountModal(interaction, action_object, update_trade_and_add_item, f'Добавить {Inventory.get_item_name(action_object, lang)}', 'Трейд'))
        elif interaction.component.custom_id == 'shop_item_select':
            await modules.shop.callbacks.shop_item_selected(interaction, interaction.values[0])
        elif interaction.component.custom_id == 'view_profile':
            await modules.other.callbacks.profile(interaction, await User.get_user(self.client, interaction.values[0]),
                                                  edit_original_message=False, ephemeral=True, pre_command_check=False)
        elif interaction.component.custom_id == 'view_family_profile':
            await modules.family.callbacks.family_profile(interaction, interaction.values[0])
        elif interaction.component.custom_id == 'view_profile_family_requests':
            await modules.other.callbacks.profile(interaction,
                                                  await User.get_user(self.client, interaction.values[0]),
                                                  edit_original_message=False, ephemeral=True,
                                                  pre_command_check=False,
                                                  _components=modules.family.components.accept_reject_user_to_family(
                                                      User.get_language(interaction.author.id), interaction.values[0], User.get_family(interaction.author.id)))
        elif len(interaction.component.custom_id.split(':')) == 2:
            lang = User.get_language(interaction.author.id)
            action_object = interaction.component.custom_id.split(':')[1]
            action = interaction.component.custom_id.split(':')[0]
            if action == 'back_to_inventory':
                match action_object:
                    case 'inventory':
                        await modules.inventory.callbacks.inventory(interaction)
                    case 'wardrobe':
                        await modules.inventory.callbacks.wardrobe(interaction)
                    case 'shop':
                        await modules.shop.callbacks.shop(interaction)
            elif action == 'preview_skin':
                await modules.other.callbacks.skin_preview(interaction, action_object)
            elif action == 'buy':
                await modules.shop.callbacks.shop_item_buy(interaction, action_object)
            elif action == 'wear_skin':
                await modules.inventory.callbacks.wardrobe_item_wear(interaction, action_object)
            elif action == 'remove_skin':
                await modules.inventory.callbacks.wardrobe_item_remove(interaction, action_object)
            elif action == 'like':
                if not User.have_like_by(action_object, interaction.author.id):
                    User.append_like(action_object, interaction.author.id)
                    await modules.other.callbacks.profile(interaction,
                                                          await User.get_user(interaction.client, action_object),
                                                          pre_command_check=False)
                else:
                    await send_callback(interaction,
                                        embed=generate_embed(Locales.ProfileLike.already_put_title[lang],
                                                             Locales.ProfileLike.already_put_desc[lang],
                                                             prefix=Func.generate_prefix('💔'), inter=interaction), ephemeral=True, edit_original_message=False)
                try:
                    await interaction.message.edit(components=None)
                except:
                    await send_callback(interaction,
                                        embed=generate_embed(Locales.ProfileLike.scd_title[lang],
                                                             Locales.ProfileLike.scd_desc[lang].format(user=await User.get_name(interaction.client, action_object)),
                                                             prefix=Func.generate_prefix('❤️'), inter=interaction), ephemeral=True, edit_original_message=False)
            elif action_object in item_components and action in item_components[action_object]:
                async def update_inventory():
                    if Inventory.get_item_amount(interaction.author.id, action_object) == 0:
                        if Inventory.is_skin(action_object):
                            await modules.inventory.callbacks.wardrobe(interaction, interaction.message)
                        else:
                            await modules.inventory.callbacks.inventory(interaction, interaction.message)
                    else:
                        await modules.inventory.callbacks.inventory_item_selected(interaction, action_object, interaction.message)

                # options = []
                # if 'options' in item_components[action_object][action]:
                #     options = item_components[action_object][action]['options']
                if Inventory.get_item_amount(interaction.author.id, action_object) <= 0:
                    await error_callbacks.no_item(interaction, action_object)
                    await update_inventory()
                    return
                result = await item_components[action_object][action]['func'](interaction, action_object,
                                                                              update_inventory)
                if result is None:
                    result = {}
                if 'callback' in item_components[action_object][action]:
                    embed = generate_embed(
                        title=item_components[action_object][action]['callback']['title'][lang],
                        description=item_components[action_object][action]['callback']['description'][lang].format(
                            **result),
                        prefix=Func.generate_prefix(item_components[action_object][action]['callback']['prefix']),
                        inter=interaction,
                    )
                    await send_callback(interaction, embed=embed,
                                        ephemeral=True, edit_original_message=False)
                    await update_inventory()
        elif len(interaction.component.custom_id.split(':')) == 3:
            lang = User.get_language(interaction.author.id)
            action = interaction.component.custom_id.split(':')[0]
            action_object1 = interaction.component.custom_id.split(':')[1]
            action_object2 = interaction.component.custom_id.split(':')[2]
            if action == 'accept_user_to_family':
                await modules.family.callbacks.accept_user_to_family(interaction, action_object1, action_object2)
            elif action == 'reject_user_to_family':
                await modules.family.callbacks.reject_user_to_family(interaction, action_object1, action_object2)
            elif action == 'family_member_kick':
                await modules.family.callbacks.family_member_kick(interaction, action_object1, action_object2)
            elif action == 'family_member_ban':
                await modules.family.callbacks.family_member_ban(interaction, action_object1, action_object2)
        elif interaction.component.custom_id == 'hide':
            await interaction.message.delete()

    # @commands.Cog.listener()
    # async def on_guild_join(self, guild):
    #     data.servers_data = DbFunc.check_guild_in_data(self.client, guild, data.servers_data)
    #     DbFunc.save_db(data.db, 'servers_data', data.servers_data)
    #     lang = data.servers_data[str(guild.id)]['lang']
    #     # await Func.send_join_message(self.client, guild, lang)
    #     await Func.send_guild_join_log_message(self.client, guild)
    #
    #

    @commands.Cog.listener()
    async def on_slash_command_error(self, inter, error):
        await error_callbacks.error(error, inter)

    @commands.Cog.listener()
    async def on_user_command_error(self, inter, error):
        await error_callbacks.error(error, inter)

    #
    @commands.Cog.listener()
    async def on_application_command(self, inter):
        # print(Func.get_command_name_and_options(inter))
        try:
            command_name, options = Func.get_command_name_and_options(inter)
            # print(inter.command)
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
        User.register_user_if_not_exists(guild.owner_id)
        Pig.create_pig_if_no_pig(guild.owner_id)
        if User.get_money(guild.owner_id) < 80 and \
                len(Func.get_items_by_key(User.get_inventory(guild.owner_id), 'type', 'skin')) < 1 and \
                len(Func.get_items_by_key(User.get_inventory(guild.owner_id), 'type', 'case')) < 1:
            User.add_item(guild.owner_id, 'common_case', 1)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: disnake.Guild):
        Func.add_log('guild_remove',
                     owner_id=guild.owner_id,
                     guild_name=str(guild),
                     guild_id=guild.id,
                     members=guild.member_count)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        join_channel = Guild.join_channel(member.guild.id)
        join_channel = member.guild.get_channel(join_channel)
        if join_channel is not None:
            await join_channel.send(Guild.join_message(member.guild.id).format(user=member.mention))


def setup(client):
    client.add_cog(Events(client))
