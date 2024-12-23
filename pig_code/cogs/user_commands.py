from ..core import *
from ..utils import *
from .. import modules


class UserCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.profile_ctx_menu = discord.app_commands.ContextMenu(
            name=locale_str('context-profile-name'),
            callback=self.profile,
        )
        self.client.tree.add_command(self.profile_ctx_menu)

    async def profile(self, inter, user: discord.User):
        await modules.other.callbacks.profile(inter, user, ephemeral=True)


async def setup(client):
    await client.add_cog(UserCommands(client))
