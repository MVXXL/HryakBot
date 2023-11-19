import disnake.ext.commands

from ..core import *
from ..utils import *
from .. import modules


class MainCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(description=Localized(data=Locales.Help.description))
    async def help(self, inter):
        await modules.help.callbacks.help(inter)

    @commands.slash_command(description=Localized(data=Locales.Profile.description))
    async def profile(self, inter, user: disnake.User = commands.Param(default=None,
                                                                       name=Localized(
                                                                           data=Locales.Profile.user_var_name),
                                                                       description=Localized(
                                                                           data=Locales.Profile.user_var_desc)), ):
        await modules.other.callbacks.profile(inter, user)

    # @commands.slash_command(description=Localized(data=Locales.Stats.description))
    # async def stats(self, inter):
    #     await modules.other.callbacks.stats(inter)

    @commands.slash_command(description=Localized(data=Locales.Top.description))
    @commands.guild_only()
    async def top(self, inter,
                  _global: str = commands.Param(default='False',
                                                    name=Localized(data=Locales.Top.server_var_name),
                                                    description=Localized(
                                                        data=Locales.Top.server_var_description),
                                                    choices=BotUtils.bool_command_choice()
                                                    )
                  ):
        await modules.top.callbacks.top(inter,
                                        # True
                                        Func.str_to_bool(_global)
                                        )

    #
    @commands.slash_command(description=Localized(data=Locales.Inventory.description))
    async def inventory(self, inter):
        await modules.inventory.callbacks.inventory(inter)

    @commands.slash_command(description=Localized(data=Locales.Wardrobe.description))
    async def wardrobe(self, inter):
        await modules.inventory.callbacks.wardrobe(inter)

    @commands.slash_command(description=Localized(data=Locales.Shop.description))
    async def shop(self, inter):
        await modules.shop.callbacks.shop(inter)

    @commands.slash_command(description=Localized(data=Locales.Duel.description))
    @commands.guild_only()
    async def duel(self, inter, user: disnake.User = commands.Param(
        name=Localized(data=Locales.Duel.user_var_name),
        description=Localized(data=Locales.Duel.user_var_desc)),
                   bet: int = commands.Param(min_value=3,
                                             name=Localized(data=Locales.Duel.bet_var_name),
                                             description=Localized(data=Locales.Duel.bet_var_desc))):
        await modules.duel.callbacks.duel(inter, user, bet)

    @commands.cooldown(2, 120, commands.BucketType.user)
    @commands.guild_only()
    @commands.slash_command(description=Localized(data=Locales.Trade.description))
    async def trade(self, inter, user: disnake.User = commands.Param(
        name=Localized(data=Locales.Trade.user_var_name),
        description=Localized(data=Locales.Trade.user_var_desc))):
        await modules.trade.callbacks.trade(inter, inter.author, user)

    @commands.slash_command()
    async def send(self, inter):
        pass

    @commands.cooldown(2, 60, commands.BucketType.user)
    @send.sub_command(description=Localized(data=Locales.TransferMoney.description))
    async def money(self, inter,
                             user: disnake.User = commands.Param(
                                 name=Localized(data=Locales.TransferMoney.user_var_name),
                                 description=Localized(data=Locales.TransferMoney.user_var_desc)),
                             amount: int = commands.Param(min_value=1,
                                                          name=Localized(
                                                              data=Locales.TransferMoney.amount_var_name),
                                                          description=Localized(
                                                              data=Locales.TransferMoney.amount_var_desc)),
                             message: str = commands.Param(
                                 name=Localized(data=Locales.TransferMoney.message_var_name),
                                 description=Localized(data=Locales.TransferMoney.message_var_desc),
                                 default=None, max_length=200),
                             ):
        await modules.other.callbacks.send_money(inter, user, amount, message)

    @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.slash_command(description=Localized(data=Locales.Report.description))
    async def report(self, inter,
                     text: str = commands.Param(
                         name=Localized(data=Locales.Report.text_var_name),
                         description=Localized(data=Locales.Report.text_var_desc)),
                     attachment: disnake.Attachment = commands.Param(
                         name=Localized(data=Locales.Report.attachment_var_name),
                         description=Localized(
                             data=Locales.Report.attachment_var_desc),
                         default=None)):
        await modules.other.callbacks.report(inter, text, attachment)

    # @commands.cooldown(1, 60)
    # @commands.slash_command(description=Localized(data=Locales.Idea.description))
    # async def idea(self, inter,
    #                  # title: str = commands.Param(
    #                  #     name=Localized(data=Locales.Idea.title_var_name),
    #                  #     description=Localized(data=Locales.Idea.title_var_desc), max_length=90),
    #                description: str = commands.Param(
    #                    name=Localized(data=Locales.Idea.description_var_name),
    #                    description=Localized(data=Locales.Idea.description_var_desc), max_length=3900),
    #                anonymous: str = commands.Param(default='False',
    #                                              name=Localized(data=Locales.Idea.anonymous_var_name),
    #                                              description=Localized(
    #                                                  data=Locales.Idea.anonymous_var_desc),
    #                                              choices=BotUtils.bool_command_choice()
    #                                              )
    #                  # attachment: disnake.Attachment = commands.Param(
    #                  #     name=Localized(data=Locales.Idea.attachment_var_name),
    #                  #     description=Localized(
    #                  #         data=Locales.Idea.attachment_var_desc),
    #                  #     default=None)
    #                ):
    #     await modules.other.callbacks.idea(inter, description, Func.str_to_bool(anonymous))

    @commands.cooldown(3, 30, type=commands.BucketType.user)
    @commands.slash_command(description=Localized(data=Locales.PromoCode.description))
    async def promocode(self, inter,
                        code: str = commands.Param(
                            name=Localized(data=Locales.PromoCode.code_var_name),
                            description=Localized(data=Locales.PromoCode.code_var_desc))):
        await modules.other.callbacks.promocode(inter, code)

    # @commands.cooldown(3, 30)
    # @commands.slash_command(description=Localized(data=locales['emotion']['description']))
    # async def emotion(self, inter,
    #                  emotion: str = commands.Param(
    #                      name=Localized(data=locales['emotion']['emotion_var_name']),
    #                      description=Localized(data=locales['emotion']['emotion_var_desc']),
    #                      choices=[
    #                          # alternatively:
    #                          # OptionChoice(Localized("Cat", key="OPTION_CAT"), "Cat")
    #                          OptionChoice(Localized('Sad', data=locales['emotion']['sad_choice']), "sad")
    #                      ]
    #                  )):
    #     print(emotion)
    # await modules.other.callbacks.promocode(inter, emotion)

    @commands.cooldown(2, 120, type=commands.BucketType.user)
    @commands.slash_command(description=Localized(data=Locales.Say.description))
    @commands.guild_only()
    @commands.bot_has_permissions(send_messages=True, view_channel=True)
    async def say(self, inter,
                  text: str = commands.Param(name=Localized(data=Locales.Say.text_var_name),
                                             description=Localized(data=Locales.Say.text_var_description),
                                             max_length=2000),
                  # user: disnake.User = commands.Param(name=Localized(data=locales['say']['user_var_name']),
                  #                                     description=Localized(
                  #                                         data=locales['say']['user_var_description']),
                  #                                     default=None)
                  ):
        await modules.other.callbacks.say(inter, text)


def setup(client):
    client.add_cog(MainCommands(client))
