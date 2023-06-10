from ..core import *
from ..utils import *
from .. import modules


class SetupCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.cooldown(3, 3, commands.BucketType.user)
    @commands.slash_command(description=Localized(data=locales['set_language']['description']))
    async def language(self, inter, language: str = commands.Param(
        name=Localized(data=locales['set_language']['language_var_name']),
        choices=[bot_locale.full_names[i] for i in bot_locale.valid_discord_locales])):
        await modules.other.callbacks.set_language(inter, language)

    @commands.has_guild_permissions(administrator=True)
    @commands.slash_command()
    async def join_message(self, inter):
        pass

    @join_message.sub_command(description=Localized(data=locales['join_message_set']['description']))
    async def set(self, inter,
                  channel: disnake.TextChannel = commands.Param(
                      name=Localized(data=locales['join_message_set']['channel_var_name']),
                      description=Localized(data=locales['join_message_set']['channel_var_desc'])),
                  message: str = commands.Param(max_length=500,
                                                name=Localized(
                                                    data=locales['join_message_set']['message_var_name']),
                                                description=Localized(
                                                    data=locales['join_message_set']['message_var_desc']))
                  ):
        await modules.other.callbacks.set_join_message(inter, channel, message)

    @join_message.sub_command(description=Localized(data=locales['join_message_reset']['description']))
    async def reset(self, inter):
        await modules.other.callbacks.reset_join_message(inter)


def setup(client):
    client.add_cog(SetupCommands(client))
