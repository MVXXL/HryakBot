from ..core import *
from ..utils import *
from .. import modules


class UserCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.user_command(name=Localized(data=locales['profile']['user_app_name']))
    async def profile(self, inter, user: disnake.User):
        await modules.other.callbacks.profile(inter, user)


def setup(client):
    client.add_cog(UserCommands(client))
