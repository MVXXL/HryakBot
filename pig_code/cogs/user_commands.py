from ..core import *
from ..utils import *
from .. import modules


class UserCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.user_command(name=Localized(data=locales['profile']['user_app_name']))
    async def profile(self, inter, user: disnake.User):
        await modules.other.callbacks.profile(inter, user, ephemeral=True)

    # @commands.user_command(name=Localized(data=locales['duel']['user_app_name']))
    # async def duel(self, inter, user: disnake.User):
    #     await modules.duel.callbacks.duel(inter, user)


def setup(client):
    client.add_cog(UserCommands(client))
