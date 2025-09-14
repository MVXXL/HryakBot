import asyncio
import ssl
import logging

logging.basicConfig(level=logging.INFO)

def loop_exception_handler(loop, context):
    exc = context.get("exception")
    if isinstance(exc, ssl.SSLError) and "bad record mac" in str(exc).lower():
        logging.warning("[SSL] bad record mac caught: %s", exc)
        # you can schedule a retry or pool reset here, e.g.:
        # asyncio.create_task(reset_pool())
        return  # swallow it
    # fallback for everything else
    loop.default_exception_handler(context)

# install this **before** you start your bot
# Create and set a new event loop to avoid DeprecationWarning
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.set_exception_handler(loop_exception_handler)

from pig_code.core import *
from pig_code.utils.functions import Translator
from pig_code.utils import error_callbacks


class PigBot:

    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        if not config.TEST:
            self.bot = commands.AutoShardedBot(command_prefix='NO_PREFIX', intents=intents, strict_localization=True, shard_count=5,
                                               max_messages=1000, chunk_guilds_at_startup=False,
                                               activity=discord.Activity(
                                                   type=discord.ActivityType.watching,
                                                   name=f'/help'))
            # Set explicit owner so @commands.is_owner() recognizes this account
            self.bot.owner_id = 606371934170513428
        else:
            self.bot = commands.Bot(command_prefix='NO_PREFIX', intents=intents, strict_localization=True, chunk_guilds_at_startup=False)
            # Set explicit owner so @commands.is_owner() recognizes this account
            self.bot.owner_id = 606371934170513428

        self.bot.setup_hook = self.setup_hook

    async def setup_hook(self):
        cogs_path = 'pig_code/cogs'
        for file in os.listdir(cogs_path):
            if file.endswith('.py'):
                print(f"> Loading cog: {file}")
                await self.bot.load_extension(f'{cogs_path.replace("/", ".")}.{file[:-3]}')
        await self.bot.tree.set_translator(Translator())


    def run(self, token):
        self.bot.run(token)


bot_instance = PigBot()


@bot_instance.bot.tree.error
async def on_app_command_error(inter: discord.Interaction, error: discord.app_commands.AppCommandError) -> None:
    # If DB is down, avoid calling error callback (it uses DB for localization)
    err_txt = str(error)
    db_down_signatures = [
        'Connection pool not initialized',
        "Can't connect to MySQL server",
    ]
    if any(sig in err_txt for sig in db_down_signatures):
        try:
            if not inter.response.is_done():
                await inter.response.send_message("The database is temporarily unavailable. Please try again later.", ephemeral=True)
            else:
                await inter.followup.send("The database is temporarily unavailable. Please try again later.", ephemeral=True)
        except Exception:
            pass
        return
    await error_callbacks.error(error, inter)


bot_instance.run(config.TOKEN)


