from ..core import *
from ..utils import *
from .. import modules


class SetupCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.cooldown(3, 3, commands.BucketType.user)
    @commands.slash_command(description=Localized(data=Locales.SetLanguage.description))
    async def language(self, inter, language: str = commands.Param(
        name=Localized(data=Locales.SetLanguage.language_var_name),
        choices=[bot_locale.full_names[i] for i in bot_locale.valid_discord_locales])):
        await modules.other.callbacks.set_language(inter, language)

    @commands.has_guild_permissions(administrator=True)
    @commands.slash_command()
    @commands.guild_only()
    async def join_message(self, inter):
        pass

    @join_message.sub_command(description=Localized(data=Locales.JoinMessageSet.description))
    async def set(self, inter,
                  channel: disnake.TextChannel = commands.Param(
                      name=Localized(data=Locales.JoinMessageSet.channel_var_name),
                      description=Localized(data=Locales.JoinMessageSet.channel_var_desc)),
                  message: str = commands.Param(max_length=500,
                                                name=Localized(
                                                    data=Locales.JoinMessageSet.message_var_name),
                                                description=Localized(
                                                    data=Locales.JoinMessageSet.message_var_desc))
                  ):
        await modules.other.callbacks.set_join_message(inter, channel, message)

    @join_message.sub_command(description=Localized(data=Locales.JoinMessageReset.description))
    async def reset(self, inter):
        await modules.other.callbacks.reset_join_message(inter)

    @commands.has_guild_permissions(administrator=True)
    @commands.slash_command()
    async def settings(self, inter):
        pass

    @settings.sub_command(description=Localized(data=Locales.SettingsSay.description))
    @commands.guild_only()
    async def say(self, inter,
                  allow: str = commands.Param(
                      name=Localized(data=Locales.SettingsSay.allow_var_name),
                      description=Localized(data=Locales.SettingsSay.allow_var_description),
                  choices=BotUtils.bool_command_choice())
                  ):
        await modules.other.callbacks.settings_say(inter, Func.str_to_bool(allow))


def setup(client):
    client.add_cog(SetupCommands(client))
