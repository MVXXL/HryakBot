from ..core import *
from ..utils import *
from .. import modules


class PigCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(description=Localized(data=Locales.Feed.description))
    async def feed(self, inter):
        await modules.pig.callbacks.pig_feed(inter)

    @commands.slash_command(description=Localized(data=Locales.Meat.description))
    async def meat(self, inter):
        await modules.pig.callbacks.meat(inter)

    #
    @commands.slash_command(description=Localized(data=Locales.Rename.description))
    async def rename(self, inter, name: str = commands.Param(
        name=Localized(data=Locales.Rename.name_var_name),
        description=Localized(data=Locales.Rename.name_var_desc))):
        await modules.pig.callbacks.pig_rename(inter, name)

    @commands.slash_command(description=Localized(data=Locales.Breed.description))
    # @commands.is_nsfw()
    async def breed(self, inter, user: disnake.User = commands.Param(
        name=Localized(data=Locales.Breed.user_var_name),
        description=Localized(data=Locales.Breed.user_var_desc))):
        await modules.breed.callbacks.breed(inter, user)

    @commands.slash_command(description=Localized(data=Locales.Pregnancy.description))
    async def pregnancy(self, inter):
        await modules.breed.callbacks.pregnancy(inter)

    # @commands.slash_command(description=Localized(data=locales['grunt']['description']))
    # async def grunt(self, inter, name: str = commands.Param(
    #     name=Localized(data=locales['rename']['name_var_name']),
    #     description=Localized(data=locales['rename']['name_var_desc']))):
    #     await modules.pig.callbacks.pig_rename(inter, name)


def setup(client):
    client.add_cog(PigCommands(client))
