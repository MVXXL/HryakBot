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


def setup(client):
    client.add_cog(SetupCommands(client))
