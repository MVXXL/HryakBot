import discord

from ..core import *
from ..utils import *
from .. import modules


class MainCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @discord.app_commands.command(description=locale_str("help-desc"))
    @discord.app_commands.user_install()
    @discord.app_commands.guild_install()
    async def help(self, inter):
        await modules.help.callbacks.help(inter)

    @discord.app_commands.command(description=locale_str("profile-desc"))
    @discord.app_commands.rename(user=locale_str("profile-user-name"))
    @discord.app_commands.describe(user=locale_str("profile-user-desc"))
    @discord.app_commands.user_install()
    @discord.app_commands.guild_install()
    async def profile(self, inter, user: discord.User = None):
        await modules.other.callbacks.profile(inter, user)

    @discord.app_commands.command(description=locale_str("top-desc"))
    @discord.app_commands.rename(_global=locale_str("top-global-name"))
    @discord.app_commands.describe(_global=locale_str("top-global-desc"))
    @discord.app_commands.choices(_global=[
        discord.app_commands.Choice(name=locale_str('choice-true'), value='true'),
        discord.app_commands.Choice(name=locale_str('choice-false'), value='false')
    ])
    @discord.app_commands.guild_install()
    @commands.guild_only()
    async def top(self, inter, _global: str = 'false'):
        await modules.top.callbacks.top(inter, Func.str_to_bool(_global))

    @discord.app_commands.command(description=locale_str("buffs-desc"))
    @discord.app_commands.user_install()
    @discord.app_commands.guild_install()
    async def buffs(self, inter):
        await modules.buffs.callbacks.buffs(inter)

    @discord.app_commands.command(description=locale_str("inventory-desc"))
    @discord.app_commands.user_install()
    @discord.app_commands.guild_install()
    async def inventory(self, inter):
        await modules.inventory.callbacks.inventory(inter)

    @discord.app_commands.command(description=locale_str("wardrobe-desc"))
    @discord.app_commands.user_install()
    @discord.app_commands.guild_install()
    async def wardrobe(self, inter):
        await modules.inventory.callbacks.wardrobe(inter)

    @discord.app_commands.command(description=locale_str("shop-desc"))
    @discord.app_commands.user_install()
    @discord.app_commands.guild_install()
    async def shop(self, inter):
        await modules.shop.callbacks.shop(inter)

    @discord.app_commands.command(description=locale_str("duel-desc"))
    @discord.app_commands.rename(user=locale_str("duel-user-name"))
    @discord.app_commands.describe(user=locale_str("duel-user-desc"))
    @discord.app_commands.rename(bet=locale_str("duel-bet-name"))
    @discord.app_commands.describe(bet=locale_str("duel-bet-desc"))
    @discord.app_commands.user_install()
    @discord.app_commands.guild_install()
    @commands.guild_only()
    async def duel(self, inter, user: discord.User, bet: discord.app_commands.Range[int, 3, None]):
        await modules.duel.callbacks.duel(inter, user, bet)

    @commands.cooldown(2, 120, commands.BucketType.user)
    @discord.app_commands.command(description=locale_str("trade-desc"))
    @discord.app_commands.rename(user=locale_str("trade-user-name"))
    @discord.app_commands.describe(user=locale_str("trade-user-desc"))
    @discord.app_commands.user_install()
    @discord.app_commands.guild_install()
    @commands.guild_only()
    async def trade(self, inter, user: discord.User):
        await modules.trade.callbacks.trade(inter, inter.user, user)

    send = discord.app_commands.Group(name="send", description='-')

    @send.command(description=locale_str("send_money-desc"))
    @discord.app_commands.checks.cooldown(5, 60, key=lambda i: (i.user.id,))
    @discord.app_commands.rename(user=locale_str("send_money-user-name"))
    @discord.app_commands.describe(user=locale_str("send_money-user-desc"))
    @discord.app_commands.rename(amount=locale_str("send_money-amount-name"))
    @discord.app_commands.describe(amount=locale_str("send_money-amount-desc"))
    @discord.app_commands.rename(currency=locale_str("send_money-currency-name"))
    @discord.app_commands.describe(currency=locale_str("send_money-currency-desc"))
    @discord.app_commands.choices(currency=[
        discord.app_commands.Choice(name='🪙', value='coins'),
        discord.app_commands.Choice(name='💵', value='hollars')
    ])
    @discord.app_commands.rename(message=locale_str("send_money-message-name"))
    @discord.app_commands.describe(message=locale_str("send_money-message-desc"))
    @discord.app_commands.user_install()
    @discord.app_commands.guild_install()
    async def money(self, inter,
                    user: discord.User,
                    amount: discord.app_commands.Range[int, 1, None],
                    currency: str = 'coins',
                    message: discord.app_commands.Range[str, 1, 200] = None):
        await modules.other.callbacks.send_money(inter, user, amount, currency, message)

    @discord.app_commands.command(description=locale_str("report-desc"))
    @discord.app_commands.checks.cooldown(1, 60, key=lambda i: (i.user.id,))
    @discord.app_commands.rename(text=locale_str("report-text-name"))
    @discord.app_commands.describe(text=locale_str("report-text-desc"))
    @discord.app_commands.rename(attachment=locale_str("report-attachment-name"))
    @discord.app_commands.describe(attachment=locale_str("report-attachment-desc"))
    @discord.app_commands.user_install()
    @discord.app_commands.guild_install()
    async def report(self, inter, text: str, attachment: discord.Attachment = None):
        await modules.other.callbacks.report(inter, text, attachment)

    @discord.app_commands.command(description=locale_str("promocode-desc"))
    @discord.app_commands.checks.cooldown(3, 30, key=lambda i: (i.user.id,))
    @discord.app_commands.rename(code=locale_str("promocode-code-name"))
    @discord.app_commands.describe(code=locale_str("promocode-code-desc"))
    @discord.app_commands.user_install()
    @discord.app_commands.guild_install()
    async def promocode(self, inter, code: str):
        await modules.other.callbacks.promocode(inter, code)

    @discord.app_commands.command(description=locale_str("say-desc"))
    @discord.app_commands.rename(text=locale_str("say-text-name"))
    @discord.app_commands.describe(text=locale_str("say-text-desc"))
    @discord.app_commands.checks.cooldown(2, 120, key=lambda i: (i.user.id,))
    @discord.app_commands.guild_only()
    @discord.app_commands.checks.has_permissions(send_messages=True, view_channel=True)
    @discord.app_commands.checks.bot_has_permissions(send_messages=True)
    @discord.app_commands.guild_install()
    async def say(self, inter, text: discord.app_commands.Range[str, 1, 512]):
        await modules.other.callbacks.say(inter, text)


async def setup(client):
    await client.add_cog(MainCommands(client))
