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


class PlayWithYourselfDuel(CommandError):
    pass


class BotAsOpponentDuel(CommandError):
    pass


class BreedWithYourself(CommandError):
    pass


class BotAsPartnerBreed(CommandError):
    pass


class PigFeedCooldown(CommandError):
    pass


class PigMeatCooldown(CommandError):
    pass


class PigBreedCooldown(CommandError):
    def __init__(self, user=None):
        self.user = user
        super().__init__(f"User {user} breed cd")


class LanguageNotSupported(CommandError):
    pass


class NoMoney(CommandError):
    pass


# class NoItemInInventory(CommandError):
#     pass

class NotAllowedToUseCommand(CommandError):
    pass


class NoItemInInventory(CommandError):
    def __init__(self, item, desc: dict = None, ephemeral: bool = False, edit_original_message: bool = True):
        self.item = item
        self.desc = desc
        self.ephemeral = ephemeral
        self.edit_original_message = edit_original_message
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
