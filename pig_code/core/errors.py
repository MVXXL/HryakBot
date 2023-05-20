from disnake.ext.commands import CommandError, CommandInvokeError


# class UserInBlackList(Exception):
#     pass
#
#
# class GuildInBlackList(Exception):
#     pass

class UserInBlackList(CommandError):
    def __init__(self, user):
        self.user = user
        super().__init__(f"User {user} is in black list")


class PigFeedCooldown(CommandError):
    pass

class PigMeatCooldown(CommandError):
    pass

class NoMoney(CommandError):
    pass

class NoItemInInventory(CommandError):
    pass
class NoItemInIInventory(CommandError):
    def __init__(self, item):
        self.item = item
        super().__init__(f"{item} not in inventory")


class PaginationWrongUser(CommandError):
    def __init__(self, user):
        self.user = user
        super().__init__(f"User {user} can't change page")


class NotUserComponentClicked(CommandError):
    def __init__(self, user):
        self.user = user
        super().__init__(f"User {user} clicked the component that doesn't belong him")


# class ModalInputNotDigit(CommandError):
#     def __init__(self):
#         super().__init__(f"Input should be a number")


# class MissingPermissions(Exception):
#     pass
#
#
# class TemplateNotFound(Exception):
#     pass
#
#
# class NicknamesNotFound(Exception):
#     pass
#
#
# class NoEmojis(Exception):
#     pass
#
#
# class BadRoleToAdd(Exception):
#     pass
#
#
# class TopRoleError(Exception):
#     pass
#
#
# class NotPremiumUser(Exception):
#     pass
