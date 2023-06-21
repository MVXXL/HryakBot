import os
import random
import threading

import disnake

from ..core import *
from ..utils import *
from .. import modules


class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(self.client.user)
        Tech.create_user_table()
        Tech.create_shop_table()
        Tech.create_promo_code_table()
        Tech.create_guild_table()
        Pig.fix_pig_structure_for_all_users()
        Stats.fix_stats_structure_for_all_users()
        for guild in self.client.guilds:
            Guild.register_guild_if_not_exists(guild.id)
        await self.client.change_presence(
            activity=disnake.Activity(type=disnake.ActivityType.watching, name=f'/help'))
        # gen = {'body': 'default_1',
        #        'eyes': 'white_eyes',
        #        'pupils': 'black_pupils'}
        # skins = {'body': None,
        #          'tattoo': None,
        #          'eyes': None,
        #          'pupils': None,
        #          'hat': None,
        #          'glasses': None,
        #          'tie': None,
        #          'legs': None,
        #          '_nose': None}
        # print(Func.get_items_by_types(items, include_only=['skin:body']))
        # for body in Func.get_items_by_types(items, include_only=['skin:body']):
        #     skins['body'] = body
        # for hat in Func.get_items_by_types(items, include_only=['skin:hat']):
        #     skins['hat'] = hat
        #     for glasses in Func.get_items_by_types(items, include_only=['skin:glasses']):
        #         skins['glasses'] = glasses
        #         for pupils in Func.get_items_by_types(items, include_only=['skin:pupils']):
        #             skins['pupils'] = pupils
        #             for _nose in Func.get_items_by_types(items, include_only=['skin:_nose']):
        #                 skins['_nose'] = _nose
        #                 for tie in Func.get_items_by_types(items, include_only=['skin:tie']):
        #                     skins['tie'] = tie
        #                     for legs in Func.get_items_by_types(items, include_only=['skin:legs']):
        #                         skins['legs'] = legs
        #                         for eyes in Func.get_items_by_types(items, include_only=['skin:eyes']):
        #                             skins['eyes'] = eyes
        #                             for tattoo in Func.get_items_by_types(items, include_only=['skin:tattoo']):
        #                                 skins['tattoo'] = tattoo
        # def thread_pig():
        #     while True:
        #         copy_skins = skins.copy()
        #         for i in skins.keys():
        #             if i in ['legs', 'body']:
        #                 continue
        #             skin = random.choice(list(Func.get_items_by_types(items, include_only=[i]).keys()) + [None])
        #             copy_skins[i] = skin
        #         file_name = '.'.join([str(i) for i in copy_skins.values()])
        #         path = f'pig_code/cogs/pig_skins/{file_name}.png'
        #         if not os.path.exists(path):
        #             Func.build_pig(tuple(copy_skins.items()), genetic=tuple(gen.items()),
        #                            output_path=path)
        # threading.Thread(target=thread_pig).start()
        # threading.Thread(target=thread_pig).start()
        # threading.Thread(target=thread_pig).start()
        aiocache.Cache(Cache.MEMORY)
        # Func.send_start_message(self.client, config.start_channel_webhook)

    @commands.Cog.listener()
    async def on_message_interaction(self, interaction):
        if interaction.component.custom_id.startswith('in:'):
            return
        if interaction.message.interaction is not None:
            if not BotUtils.check_if_right_user(interaction):
                await modules.errors.callbacks.wrong_component_clicked(interaction)
                return
        if interaction.component.custom_id == 'inventory_item_select':
            await modules.inventory.callbacks.inventory_item_selected(interaction, interaction.values[0])
        elif interaction.component.custom_id == 'wardrobe_item_select':
            await modules.wardrobe.callbacks.wardrobe_item_selected(interaction, interaction.values[0])
        elif interaction.component.custom_id == 'shop_item_select':
            await modules.shop.callbacks.shop_item_selected(interaction, interaction.values[0])
        elif interaction.component.custom_id == 'guild_select':
            await modules.other.callbacks.guild_info(interaction, interaction.values[0])
        elif interaction.component.custom_id == 'view_profile':
            await modules.other.callbacks.profile(interaction, await User.get_user(self.client, interaction.values[0]),
                                                  edit_original_message=False, ephemeral=True, pre_command_check=False)
        elif interaction.component.custom_id.split(':')[0] in ['sell_item', 'use_item', 'wear_skin', 'remove_skin',
                                                               'preview_skin', 'cook_item']:
            item_action = interaction.component.custom_id.split(':')[0]
            item_id = interaction.component.custom_id.split(':')[1]
            if Inventory.get_item_amount(interaction.author.id, item_id) == 0:
                await modules.errors.callbacks.no_item(interaction)
                return
            match item_action:
                case 'sell_item':
                    await interaction.response.send_modal(
                        modal=modules.inventory.callbacks.SellItemModal(interaction, item_id))
                case 'cook_item':
                    if Inventory.get_item_amount(interaction.author.id, 'grill') == 0:
                        await modules.errors.callbacks.error(
                            NoItemInInventory('grill', locales['error_callbacks']['no_mangal_to_cook'], ephemeral=True,
                                              edit_original_message=False), interaction)
                    await interaction.response.send_modal(
                        modal=modules.inventory.callbacks.CookItemModal(interaction, item_id))
                case 'use_item':
                    await modules.inventory.callbacks.inventory_item_used(interaction, item_id)
                case 'wear_skin':
                    await modules.wardrobe.callbacks.wardrobe_item_wear(interaction, item_id)
                case 'remove_skin':
                    await modules.wardrobe.callbacks.wardrobe_item_remove(interaction, item_id)
                case 'preview_skin':
                    await modules.wardrobe.callbacks.wardrobe_item_preview(interaction, item_id)
        elif interaction.component.custom_id.split(':')[0] in ['preview_shop_skin', 'buy']:
            item_action = interaction.component.custom_id.split(':')[0]
            item_id = interaction.component.custom_id.split(':')[1]
            match item_action:
                case 'buy':
                    await modules.shop.callbacks.shop_item_buy(interaction, item_id)
                case 'preview_shop_skin':
                    await modules.wardrobe.callbacks.wardrobe_item_preview(interaction, item_id,
                                                                           update_item_selected_embed=False)
        elif interaction.component.custom_id.split(':')[0] == 'back_to_inventory':
            action_object = interaction.component.custom_id.split(':')[1]
            match action_object:
                case 'inventory':
                    await modules.inventory.callbacks.inventory(interaction)
                case 'wardrobe':
                    await modules.wardrobe.callbacks.wardrobe(interaction)
                case 'shop':
                    await modules.shop.callbacks.shop(interaction)
        elif interaction.component.custom_id.split(':')[0] == 'wardrobe_category_choose':
            action_object = interaction.values[0]
            if action_object == 'skin:all':
                include_only = 'skin'
            else:
                include_only = action_object
            await modules.inventory.callbacks.inventory_embed(interaction, include_only=[include_only],
                                                              inventory_type='wardrobe')
        elif interaction.component.custom_id.split(':')[0] == 'shop_category_choose':
            action_object = interaction.values[0]
            await modules.shop.callbacks.shop(interaction, category=action_object)
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
        await modules.errors.callbacks.error(error, inter)

    @commands.Cog.listener()
    async def on_user_command_error(self, inter, error):
        await modules.errors.callbacks.error(error, inter)

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
        if User.get_money(guild.owner_id) < 80 and \
            len(Func.get_items_by_key(User.get_inventory(guild.owner_id), 'type', 'skin')) < 1 and \
                len(Func.get_items_by_key(User.get_inventory(guild.owner_id), 'type', 'case')) < 1:
            Inventory.add_item(guild.id, 'common_case', 1)


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
