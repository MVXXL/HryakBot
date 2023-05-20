import random

import disnake

from ..core import *
from ..utils import *
from .. import modules


class MainCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    # @commands.slash_command(guild_ids=config.ADMIN_GUILDS)
    # async def test(self, inter):
    #     await BotUtils.pre_command_check(inter)
    #     lang = User.get_language(inter.author.id)
    #     # Inventory.add_item(inter.author.id, Func.get_item_by_id('poop'), 10)
    #     await BotUtils.pagination(self.client, inter, lang,
    #                               components=[disnake.ui.Button(
    #                                   style=disnake.ButtonStyle.primary,
    #                                   emoji='🐷',
    #                                   custom_id='fdg',
    #                               )],
    #                               embeds=[Embeds.profile(inter, lang),
    #                                       Embeds.set_language(inter, lang),
    #                                       Embeds.pig_feed(inter, lang, 10, 1),
    #                                       Embeds.pig_rename(inter, lang)], hide_button=True)
    #     # await Callbacks.send_callback(inter, title='Hello')

    @commands.slash_command(description=Localized(data=locales['help']['description']))
    async def help(self, inter):
        await modules.help.callbacks.help(inter)

    @commands.slash_command(description=Localized(data=locales['profile']['description']))
    async def profile(self, inter, user: disnake.User = commands.Param( default=None,
                         name=Localized(data=locales['profile']['user_variable_name']),
                         description=Localized(data=locales['profile']['user_variable_desc'])),):
        await modules.other.callbacks.profile(inter, user)

    @commands.slash_command(description=Localized(data=locales['stats']['description']))
    async def stats(self, inter):
        await modules.other.callbacks.stats(inter)

    @commands.slash_command(description=Localized(data=locales['top']['description']))
    async def top(self, inter):
        await modules.top.callbacks.top(inter)

    @commands.slash_command(description=Localized(data=locales['inventory']['description']))
    async def inventory(self, inter):
        await modules.inventory.callbacks.inventory(inter)

    @commands.slash_command(description=Localized(data=locales['wardrobe']['description']))
    async def wardrobe(self, inter):
        await modules.wardrobe.callbacks.wardrobe(inter)

    # @commands.bot_has_permissions(administrator=True)
    @commands.slash_command(description=Localized(data=locales['shop']['description']))
    async def shop(self, inter):
        # Shop.add_shop_state(Func.select_random_items_by_method_of_obtaining('shop:daily', 3))
        # print(Shop.get_last_daily_shop())
        await modules.shop.callbacks.shop(inter)

    @commands.cooldown(2, 60)
    @commands.slash_command(description=Localized(data=locales['transfer_money']['description']))
    async def transfer_money(self, inter, user: disnake.User = commands.Param(
                         name=Localized(data=locales['transfer_money']['user_variable_title']),
                         description=Localized(data=locales['transfer_money']['user_variable_desc'])),
                             amount: int = commands.Param(
                         name=Localized(data=locales['transfer_money']['amount_variable_title']),
                         description=Localized(data=locales['transfer_money']['amount_variable_desc']))):
        # Shop.add_shop_state(Func.select_random_items_by_method_of_obtaining('shop:daily', 3))
        # print(Shop.get_last_daily_shop())
        await modules.other.callbacks.transfer_money(inter, user, amount)

    @commands.cooldown(1, 60)
    @commands.slash_command(description=Localized(data=locales['report']['description']))
    async def report(self, inter,
                     text: str = commands.Param(
                         name=Localized(data=locales['report']['text_variable_name']),
                         description=Localized(data=locales['report']['text_variable_desc'])),
                     attachment: disnake.Attachment = commands.Param(
                         name=Localized(data=locales['report']['attachment_variable_name']),
                         description=Localized(
                             data=locales['report']['attachment_variable_desc']),
                         default=None)):
        await modules.other.callbacks.report(inter, text, attachment)

    @commands.cooldown(2, 20)
    @commands.slash_command(description=Localized(data=locales['say']['description']))
    async def say(self, inter,
                  text: str = commands.Param(name=Localized(data=locales['say']['text_variable_name']),
                                             description=Localized(data=locales['say']['text_variable_description'])),
                  # user: disnake.User = commands.Param(name=Localized(data=locales['say']['user_variable_name']),
                  #                                     description=Localized(
                  #                                         data=locales['say']['user_variable_description']),
                  #                                     default=None)
                  ):
        await modules.other.callbacks.say(inter, text)


def setup(client):
    client.add_cog(MainCommands(client))
