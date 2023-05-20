import random

from ..core import *
from ..utils import *
from .. import modules


class PigCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command()
    async def pig(self, inter):
        pass

    @commands.slash_command(description=Localized(data=locales['feed']['description']))
    async def feed(self, inter):
        await modules.pig.callbacks.pig_feed(inter)

    @commands.slash_command(description=Localized(data=locales['meat']['description']))
    async def meat(self, inter):
        await modules.pig.callbacks.meat(inter)

    @pig.sub_command(description=Localized(data=locales['rename']['description']))
    async def rename(self, inter, name: str = commands.Param(
        name=Localized(data=locales['rename']['name_var_name']),
        description=Localized(data=locales['rename']['name_var_desc']))):
        await modules.pig.callbacks.pig_rename(inter, name)


def setup(client):
    client.add_cog(PigCommands(client))
