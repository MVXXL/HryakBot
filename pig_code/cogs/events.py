from ..core import *
from ..utils import *
from .. import modules


class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(self.client.user)
        Tech.create_table()
        Pig.fix_pig_structure_for_all_users()
        # Inventory.fix_items_in_inventory_for_all_users()
        await self.client.change_presence(
            activity=disnake.Activity(type=disnake.ActivityType.watching, name=f'v{config.VERSION}'))
        # Func.send_start_message(self.client, config.start_channel_webhook)

    @commands.Cog.listener()
    async def on_slash_command_error(self, inter, error):
        lang = User.get_language(inter.author.id)
        await modules.errors.callbacks.error(error, lang, inter)

    @commands.Cog.listener()
    async def on_message_interaction(self, interaction):
        if interaction.message.interaction is not None:
            right_user = interaction.message.interaction.user.id == interaction.author.id
            if not right_user:
                await modules.errors.callbacks.wrong_component_clicked(interaction)
                return
        if interaction.component.custom_id == 'inventory_item_select':
            await modules.inventory.callbacks.inventory_item_selected(interaction, interaction.values[0])
        elif interaction.component.custom_id.split(':')[0] == 'sell_item':
            item_id = interaction.component.custom_id.split(':')[1]
            if Inventory.get_item_amount(interaction.author.id, item_id) == 0:
                await modules.errors.callbacks.no_item(interaction)
            else:
                await interaction.response.send_modal(modal=modules.inventory.callbacks.SellItemModal(interaction, item_id))
        elif interaction.component.custom_id.split(':')[0] == 'use_item':
            item_id = interaction.component.custom_id.split(':')[1]
            if Inventory.get_item_amount(interaction.author.id, item_id) == 0:
                await modules.errors.callbacks.no_item(interaction)
            else:
                await modules.inventory.callbacks.inventory_item_used(interaction, item_id)
        # elif interaction.component.custom_id.split(':')[0] == 'pay':
        #     amount_to_pay = int(interaction.component.custom_id.split(':')[1])
        #     if User.get_money(interaction.author.id) >= amount_to_pay:
        #         User.add_money(interaction.author.id, -amount_to_pay)
        #     else:
        #         await Callbacks.not_enough_money(interaction)
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
    # @commands.Cog.listener()
    # async def on_user_command_error(self, inter, error):
    #     lang = data.servers_data[str(inter.guild.id)]['lang']
    #     await ErrorCallback.error_callback(error, lang, inter)
    #
    # @commands.Cog.listener()
    # async def on_application_command(self, inter):
    #     try:
    #         await Func.send_command_use_webhook(self.client, inter)
    #     except:
    #         pass


def setup(client):
    client.add_cog(Events(client))
