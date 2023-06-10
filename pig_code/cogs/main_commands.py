import random

import disnake
from disnake import OptionChoice

from ..core import *
from ..utils import *
from .. import modules


class MainCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    # @commands.slash_command(guild_ids=config.ADMIN_GUILDS)
    # async def test(self, inter):
    #     await BotUtils.pre_command_check(inter)
    #     for user_id in Tech.get_all_users():
    #         if User.get_language(user_id) == 'ru':
    #             Events.add(user_id, title='Хочешь получить буст?',
    #                        description='Ты можешь получить буст в 15% для веса хряка если находишься на '
    #                                    'сервере поддержки бота!\n'
    #                                    'Также там ты сможешь найти промокоды!\n\n'
    #                                    '*Вот ссылка: https://discord.gg/btYvZZTeQx*',
    #                        expires_in=60 * 60 * 36)

    @commands.slash_command(description=Localized(data=locales['help']['description']))
    async def help(self, inter):
        await modules.help.callbacks.help(inter)

    @commands.slash_command(description=Localized(data=locales['profile']['description']))
    async def profile(self, inter, user: disnake.User = commands.Param(default=None,
                                                                       name=Localized(data=locales['profile'][
                                                                           'user_var_name']),
                                                                       description=Localized(data=locales['profile'][
                                                                           'user_var_desc'])), ):
        await modules.other.callbacks.profile(inter, user)

    @commands.slash_command(description=Localized(data=locales['stats']['description']))
    async def stats(self, inter):
        await modules.other.callbacks.stats(inter)

    @commands.slash_command(description=Localized(data=locales['top']['description']))
    async def top(self, inter,
                  server_only: str = commands.Param(default='False',
                                                    name=Localized(data=locales['top']['server_var_name']),
                                                    description=Localized(
                                                        data=locales['top']['server_var_description']),
                                                    choices=BotUtils.bool_command_choice()
                                                    )
                  ):
        await modules.top.callbacks.top(inter,
                                        # True
                                        Func.str_to_bool(server_only)
                                        )

    @commands.slash_command(description=Localized(data=locales['inventory']['description']))
    async def inventory(self, inter):
        await modules.inventory.callbacks.inventory(inter)

    @commands.slash_command(description=Localized(data=locales['wardrobe']['description']))
    async def wardrobe(self, inter):
        await modules.wardrobe.callbacks.wardrobe(inter)

    @commands.slash_command(description=Localized(data=locales['shop']['description']))
    async def shop(self, inter):
        await modules.shop.callbacks.shop(inter)

    @commands.slash_command(description=Localized(data=locales['duel']['description']))
    async def duel(self, inter, user: disnake.User = commands.Param(
        name=Localized(data=locales['duel']['user_var_name']),
        description=Localized(data=locales['duel']['user_var_desc'])),
                   bet: int = commands.Param(min_value=3,
                                             name=Localized(data=locales['duel']['bet_var_name']),
                                             description=Localized(data=locales['duel']['bet_var_desc']))):
        await modules.duel.callbacks.duel(inter, user, bet)

    @commands.cooldown(2, 60)
    @commands.slash_command(description=Localized(data=locales['transfer_money']['description']))
    async def transfer_money(self, inter, user: disnake.User = commands.Param(
        name=Localized(data=locales['transfer_money']['user_var_name']),
        description=Localized(data=locales['transfer_money']['user_var_desc'])),
                             amount: int = commands.Param(min_value=1,
                                                          name=Localized(
                                                              data=locales['transfer_money']['amount_var_name']),
                                                          description=Localized(
                                                              data=locales['transfer_money']['amount_var_desc']))):
        await modules.other.callbacks.transfer_money(inter, user, amount)

    @commands.cooldown(1, 60)
    @commands.slash_command(description=Localized(data=locales['report']['description']))
    async def report(self, inter,
                     text: str = commands.Param(
                         name=Localized(data=locales['report']['text_var_name']),
                         description=Localized(data=locales['report']['text_var_desc'])),
                     attachment: disnake.Attachment = commands.Param(
                         name=Localized(data=locales['report']['attachment_var_name']),
                         description=Localized(
                             data=locales['report']['attachment_var_desc']),
                         default=None)):
        await modules.other.callbacks.report(inter, text, attachment)

    @commands.cooldown(3, 30)
    @commands.slash_command(description=Localized(data=locales['promo_code']['description']))
    async def promocode(self, inter,
                        code: str = commands.Param(
                            name=Localized(data=locales['promo_code']['code_var_name']),
                            description=Localized(data=locales['promo_code']['code_var_desc']))):
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

    @commands.cooldown(2, 20)
    @commands.slash_command(description=Localized(data=locales['say']['description']))
    async def say(self, inter,
                  text: str = commands.Param(name=Localized(data=locales['say']['text_var_name']),
                                             description=Localized(data=locales['say']['text_var_description']),
                                             max_length=2000),
                  # user: disnake.User = commands.Param(name=Localized(data=locales['say']['user_var_name']),
                  #                                     description=Localized(
                  #                                         data=locales['say']['user_var_description']),
                  #                                     default=None)
                  ):
        await modules.other.callbacks.say(inter, text)


def setup(client):
    client.add_cog(MainCommands(client))
