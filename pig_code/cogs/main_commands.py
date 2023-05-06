import random


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

    @commands.slash_command(description=Localized(data=locales['profile']['description']))
    async def profile(self, inter):
        await modules.other.callbacks.profile(inter)

    @commands.slash_command(description=Localized(data=locales['inventory']['description']))
    async def inventory(self, inter):
        await modules.inventory.callbacks.inventory(inter, self.client)

    @commands.slash_command(description=Localized(data=locales['wardrobe']['description']))
    async def wardrobe(self, inter):
        await modules.wardrobe.callbacks.wardrobe(inter, self.client)

    # @commands.slash_command(description=Localized(data=locales['about']['description']))
    # async def about(self, inter):
    #     lang = await Func.pre_command(inter, data.servers_data, data.black_list)
    #     await Func.send_callback(inter,
    #                              title=locales['about']['title'][lang],
    #                              description=f"{locales['about']['text'][lang]}\n\n"
    #                                          f"{random.choice(locales['about']['random_frases'][lang])}",
    #                              thumbnail_url=self.client.user.avatar.url,
    #                              footer=Func.gen_footer(inter), footer_url='user')
    #
    #
    # @commands.slash_command(description=Localized(data=locales['report']['description']))
    # async def report(self, inter,
    #                  text: str = commands.Param(
    #                      name=Localized(data=locales['report']['text_variable_name']),
    #                      description=Localized(data=locales['report']['text_variable_desc'])),
    #                  attachment: disnake.Attachment = commands.Param(
    #                      name=Localized(data=locales['report']['attachment_variable_name']),
    #                      description=Localized(
    #                          data=locales['report']['attachment_variable_desc']),
    #                      default=None)):
    #     lang = await Func.pre_command(inter, data.servers_data, data.black_list)
    #     Func.cooldown(inter, 1, 10, pro_rate=2)
    #     discohook_embed = discord_webhook.DiscordEmbed(title='Bug Report', color=config.main_color,
    #                                                    description=text)
    #     webhook = discord_webhook.DiscordWebhook(url=config.REPORT_WEBHOOK,
    #                                              username='Bug Report')
    #     if attachment is not None:
    #         discohook_embed.set_image(url=attachment.url)
    #     discohook_embed.set_footer(text=f'ID: {inter.author.id}')
    #     webhook.add_embed(discohook_embed)
    #     webhook.execute()
    #     await Func.send_callback(inter, title=locales['report']['scd'][lang], color=config.success_color,
    #                              description=f"*{locales['report']['scd_desc'][lang]}*",
    #                              footer=Func.gen_footer(inter), footer_url='user', prefix='scd')


def setup(client):
    client.add_cog(MainCommands(client))
