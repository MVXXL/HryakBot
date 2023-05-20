import random

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
        Pig.fix_pig_structure_for_all_users()
        Stats.fix_stats_structure_for_all_users()
        await self.client.change_presence(
            activity=disnake.Activity(type=disnake.ActivityType.watching, name=f'v{config.VERSION}'))
        aiocache.Cache(Cache.MEMORY)
        # Func.send_start_message(self.client, config.start_channel_webhook)

    @commands.Cog.listener()
    async def on_message_interaction(self, interaction):
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
                                                             'preview_skin']:
            item_action = interaction.component.custom_id.split(':')[0]
            item_id = interaction.component.custom_id.split(':')[1]
            if Inventory.get_item_amount(interaction.author.id, item_id) == 0:
                await modules.errors.callbacks.no_item(interaction)
                return
            match item_action:
                case 'sell_item':
                    await interaction.response.send_modal(
                        modal=modules.inventory.callbacks.SellItemModal(interaction, item_id))
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
        except:
            pass


def setup(client):
    client.add_cog(Events(client))
