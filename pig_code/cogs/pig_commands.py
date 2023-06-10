import random

from ..core import *
from ..utils import *
from .. import modules


class PigCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(description=Localized(data=locales['feed']['description']))
    async def feed(self, inter):
        await modules.pig.callbacks.pig_feed(inter)

    @commands.slash_command(description=Localized(data=locales['meat']['description']))
    async def meat(self, inter):
        await modules.pig.callbacks.meat(inter)

    @commands.slash_command(description=Localized(data=locales['rename']['description']))
    async def rename(self, inter, name: str = commands.Param(
        name=Localized(data=locales['rename']['name_var_name']),
        description=Localized(data=locales['rename']['name_var_desc']))):
        await modules.pig.callbacks.pig_rename(inter, name)

    @commands.slash_command(description=Localized(data=locales['inventory']['description']))
    # @commands.is_nsfw()
    async def breed(self, inter, user: disnake.User = commands.Param(
        name=Localized(data=locales['breed']['user_var_name']),
        description=Localized(data=locales['breed']['user_var_desc']))):
        await modules.pig.callbacks.breed(inter, user)

    # @commands.slash_command(description=Localized(data=locales['grunt']['description']))
    # async def grunt(self, inter, name: str = commands.Param(
    #     name=Localized(data=locales['rename']['name_var_name']),
    #     description=Localized(data=locales['rename']['name_var_desc']))):
    #     await modules.pig.callbacks.pig_rename(inter, name)


def setup(client):
    client.add_cog(PigCommands(client))
