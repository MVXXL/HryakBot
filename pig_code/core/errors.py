from discord.ext.commands import CommandError, CommandInvokeError


class UserInBlackList(CommandError):
    def __init__(self, user):
        self.user = user
        super().__init__(f"User {user} is in black list")

class NotBotOwner(CommandError):
    def __init__(self, user):
        self.user = user
        super().__init__(f"User {user} is not a bot owner")
