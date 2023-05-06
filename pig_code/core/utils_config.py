from . import config

default_pig = {'name': 'Hryak',
               'weight': 1,
               'last_feed': None,
               'genetic': {
                   'body': 'default',
                   'eyes': 'white',
                   'pupils': 'black',
               },
               'skins': {
                   'body': None,
                   'eyes': None,
                   'pupils': None,
                   'hat': None,
                   'glasses': None
               }}
pig_feed_cooldown = 4 * 60 ** 2 if not config.TEST else 10  # seconds
premium_pig_feed_cooldown = 2 * 60 ** 2 if not config.TEST else 5  # seconds

# text
start_text = '**I am alive!**'

# embed colors
main_color = 0xc7604c
error_color = 0xe32d2d
warn_color = 0xe0bb36
success_color = 0x2fc256
premium_color = 0x61dfff

# emojis
emojis = {'staff': '<:staff:1007465250834108427>',
          'partner': '<:partner:1007465369394487379>',
          'hypesquad_brilliance': '<:hypesquad_brilliance:1007465681568137247>',
          'hypesquad_balance': '<:hypesquad_balance:1007465700123742209>',
          'hypesquad_bravery': '<:hypesquad_bravery:1007465719505633372>',
          'bug_hunter': '<:bug_hunter:1007466422630363156>',
          'bug_hunter_level_2': '<:bug_hunter_level_2:1007466439332089886>',
          'early_supporter': '<:early_supporter:1007466552217571358>',
          'verified_bot': '<:verified_bot:1007467661124448276>',
          'verified_bot_developer': '<:verified_bot_developer:1007467678543401002>',
          'discord_certified_moderator': '<:discord_certified_moderator:1007467902263369768>',
          'spammer': '<:spammer:1007468048711680123>',
          'active_developer': '<:active_developer:1041023285766398042>',
          'dnd': '<:dnd:1007632630528888852>',
          'online': '<:online:1007632172775116841>',
          'idle': '<:idle:1007632550778384485>',
          'offline': '<:offline:1007632171713953882>',
          'members': '<:members:1007621633743278190>',
          'member': '<:member:1007622245629308978>',
          'bot': ' <:bot:1007621794452209704>',
          'channel': '<:channel:1007622900402094080>',
          'text': '<:text:1007622982216192082>',
          'voice': '<:voice:1007623010783612998>',
          'forum': '<:forum:1023381259910651976>',
          'rules': '<:rules:1007623895035162654>',
          'announcement': '<:announcement:1007623973267329084>',
          'stage': '<:stage:1007624031882706974>',
          'category': '<:category:1007640105474863134>',
          'owner': '<:owner:1007626031580053604>',
          'bot_2': '<:bot_2:1007646318610612264>',
          'role': '<:role:1007695977169309807>',
          'nitro_boost': '<:nitro_boost:1007647238136283296>',
          'role_blue': '<:blue_role:1007696004163846184>',
          'sticker': '<:sticker:1007698805589811291>',
          'switch_on': '<:switch_on:1007721597005738075>',
          'switch_off': '<:switch_off:1007721615158681640>',
          'loading': '<a:loading:1008371288634576926>',
          'x': '<:x_symbol:1025561561655410708>',
          'check_mark': '<:check_mark:1025561727850516542>',
          'warn': '<:warn:1101891342759641279>'
          }
unicode_emojis = {'staff': '🛠',
                  'partner': '🤝',
                  'hypesquad_brilliance': '',
                  'hypesquad_balance': '',
                  'hypesquad_bravery': '',
                  'bug_hunter': '',
                  'bug_hunter_level_2': '',
                  'early_supporter': '',
                  'verified_bot': '☑',
                  'verified_bot_developer': '',
                  'discord_certified_moderator': '🛡',
                  'spammer': '⚠️',
                  'active_developer': '',
                  'dnd': '⛔',
                  'online': '🟢>',
                  'idle': '🟡',
                  'offline': '⚪',
                  'members': '👥',
                  'member': '👤',
                  'bot': ' 🤖',
                  'channel': '',
                  'text': '',
                  'voice': '',
                  'forum': '',
                  'rules': '',
                  'announcement': '',
                  'stage': '',
                  'category': '',
                  'owner': '👑',
                  'bot_2': '🤖',
                  'role': '',
                  'nitro_boost': '',
                  'role_blue': '',
                  'sticker': '',
                  'switch_on': '✅',
                  'switch_off': '⛔',
                  'loading': '🔄',
                  'x': '❌',
                  'check_mark': '✅',
                  'warn': '⚠️'
                  }
