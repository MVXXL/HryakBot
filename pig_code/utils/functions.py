import shutil

import requests

from ..core import *


def translate(locales, lang, format_options: dict = None):
    translated_text = 'translation_error'
    if type(locales) == dict:
        if lang not in locales:
            lang = 'en'
        if lang not in locales:
            lang = list(locales)[0]
        translated_text = locales[lang]
    elif type(locales) == str:
        translated_text = locales
    if format_options is not None:
        for k, v in format_options.items():
            translated_text = translated_text.replace('{'+k+'}', str(v))
    return translated_text

class Func:

    @staticmethod
    def random_choice_with_probability(dictionary):
        total_probability = sum(dictionary.values())
        random_number = random.uniform(0, total_probability)
        cumulative_probability = 0

        for key, probability in dictionary.items():
            cumulative_probability += probability
            if random_number <= cumulative_probability:
                return key

    @staticmethod
    def calculate_probabilities(dictionary, round_to: int = 2):
        total = sum(dictionary.values())
        probabilities = {}

        for key, value in dictionary.items():
            probability = (value / total) * 100
            probabilities[key] = round(probability, round_to)

        return probabilities

    @staticmethod
    def speed_test(func, **kwargs):
        start = datetime.datetime.now().timestamp()
        func(**kwargs)
        final = datetime.datetime.now().timestamp() - start
        return final

    @staticmethod
    def clear_cache(cache_id, params: tuple = None):
        if cache_id not in utils_config.db_caches:
            return
        if params is None:
            utils_config.db_caches[cache_id].clear()
            return
        try:
            utils_config.db_caches[cache_id].pop(params)
        except KeyError:
            pass

    @staticmethod
    def generate_temp_path(key_word: str, file_extension: str = 'png'):
        while True:
            path = f'{config.TEMP_FOLDER_PATH}/{key_word}_{Func.get_current_timestamp()}_{random.randrange(10000)}.{file_extension}'
            if not os.path.exists(path):
                break
        return path

    @staticmethod
    def sort_by_values(dictionary, reverse: bool = False):
        return {k: v for k, v in sorted(dictionary.items(), key=lambda x: x[1], reverse=reverse)}

    @staticmethod
    def add_log(log_type, **kwargs):
        current_time = datetime.datetime.now()
        log_entry = {
            'timestamp': str(current_time),
            'type': str(log_type),
        }
        for k, v in kwargs.items():
            if type(v) in [str, int, float, bool, list, dict, set]:
                log_entry[k] = v
        log_file_path = config.LOGS_PATH
        if os.path.exists(log_file_path):
            with open(log_file_path, "r") as log_file:
                try:
                    log_data = json.load(log_file)
                except json.decoder.JSONDecodeError:
                    log_data = []

            log_data.append(log_entry)
        else:
            log_data = [log_entry]

        with open(log_file_path, "w") as log_file:
            json.dump(log_data, log_file, indent=4, ensure_ascii=False)

    @staticmethod
    def get_command_name_and_options(ctx):
        try:
            sub_commands_types = ['OptionType.sub_command', 'OptionType.sub_command_group',
                                  'ApplicationCommandType.chat_input']
            if ctx.data.options and str(ctx.data.options[0].type) == sub_commands_types[1]:
                if ctx.data.options[0].options and str(ctx.data.options[0].options[0].type) == sub_commands_types[0]:
                    command_text = f'{ctx.data.name} {ctx.data.options[0].name} {ctx.data.options[0].options[0].name}'
                    options = ctx.data.options[0].options[0].options
                else:
                    command_text = f'{ctx.data.name} {ctx.data.options[0].name}'
                    options = ctx.data.options[0].options
            elif ctx.data.options and str(ctx.data.options[0].type) == sub_commands_types[0]:
                command_text = f'{ctx.data.name} {ctx.data.options[0].name}'
                options = ctx.data.options[0].options
            else:
                command_text = f'{ctx.data.name}'
                options = ctx.data.options
        except:
            command_text, options = ctx.data.name, ctx.data.options
        return command_text, options

    @staticmethod
    def str_to_bool(target):
        if target is None:
            return None
        return True if target.lower() in ['✅ true', 'true', '✅', 'yes', 'да', 'так'] else False

    @staticmethod
    def str_to_dict(target):
        if target is None:
            return None
        try:
            return json.loads(target.replace("'", '"'))
        except json.JSONDecodeError:
            return

    @staticmethod
    def clear_folder(path):
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')

    @staticmethod
    def generate_footer(inter, first_part: str = 'user', second_part: str = '', user: disnake.User = None):
        separator = ' ・ '
        if user is None:
            user = inter.author
        if second_part == 'com_name':
            second_part, options = Func.get_command_name_and_options(inter)
            second_part = f'/{second_part}'
        if first_part == 'user':
            first_part = user.display_name
        if not first_part or not second_part:
            separator = ''
        footer = f'{first_part}{separator}{second_part}'
        return footer

    @staticmethod
    def generate_footer_url(footer_url, user: disnake.User = None):
        if footer_url == 'user_avatar' and user is not None:
            if user.avatar is not None:
                footer_url = user.avatar.url
            else:
                footer_url = f'https://cdn.discordapp.com/embed/avatars/{user.default_avatar.key}.png'
        else:
            return None
        return footer_url


    @staticmethod
    def generate_prefix(prefix: str = 'scd', sep: str = '・', backticks: bool = False):
        if prefix is None or not prefix:
            return ''
        prefix_emoji = prefix
        if prefix == 'scd':
            prefix_emoji = '✅'
        elif prefix == 'error':
            prefix_emoji = '❌'
        elif prefix == 'warn':
            prefix_emoji = '⚠️'
        if not backticks:
            prefix = f'{prefix_emoji}{sep}'
        else:
            prefix = f'`{prefix_emoji}`{sep}'
        return prefix

    @staticmethod
    def translate_permissions(perms, lang):
        missing_perms = []
        for perm in perms:
            if perm in Locales.Permissions:
                missing_perms.append(Locales.Permissions[perm][lang])
            else:
                missing_perms.append(perm.replace('_', ' ').capitalize())
        return missing_perms

    @staticmethod
    def common_elements(list_of_lists):
        common_set = set(list_of_lists[0])
        for lst in list_of_lists[1:]:
            common_set = common_set.intersection(lst)
        return list(common_set)

    @staticmethod
    def numerate_list_as_text(elements_list: list, bold_number: bool = True) -> str:
        text = ''
        if len(elements_list) == 1:
            text += f'{elements_list[0].capitalize()}\n'
        else:
            for i, j in enumerate(elements_list):
                if bold_number:
                    text += f'**{i + 1}.** {j.capitalize()}\n'
                else:
                    text += f'{i + 1}. {j.capitalize()}\n'
        return text

    @staticmethod
    @cached(TTLCache(maxsize=10000, ttl=86400))
    def get_image_path_from_link(link: str, name: str = None):
        if name is None:
            name = random.randrange(10000, 99999)
        file_extension = 'png'
        if len(link.split('.')) > 1:
            if link.split('.')[-1] in ['png', 'webp', 'gif', 'jpg']:
                file_extension = link.split('.')[-1]
        path = Func.generate_temp_path(name, file_extension=file_extension)
        with open(path, 'wb') as f:
            f.write(requests.get(link).content)
        return path

    @staticmethod
    def get_changed_page_number(total_pages, cur_page, differ):
        if differ > 0:
            if cur_page + differ > total_pages:
                cur_page = 1
            else:
                cur_page += differ
        elif differ < 0:
            if cur_page + differ < 1:
                cur_page = total_pages
            else:
                cur_page += differ
        return cur_page

    @staticmethod
    def _dim(lst):
        if not type(lst) == list:
            return []
        try:
            return [len(lst)] + Func._dim(lst[0])
        except IndexError:
            return [len(lst)]

    @staticmethod
    def get_list_dim(lst):
        return len(Func._dim(lst))

    @staticmethod
    def startswith_list(string, lst: list[str]) -> bool:
        for i in lst:
            if string.startswith(i):
                return True
        return False

    @staticmethod
    def list_startswith(lst: list[str], prefix: str) -> bool:
        for i in lst:
            if i.startswith(prefix):
                return True
        return False

    @staticmethod
    def list_startswith_list(lst: list[str], prefix_list: str) -> bool:
        for prefix in prefix_list:
            if Func.list_startswith(lst, prefix):
                return True
        return False

    @staticmethod
    def select_random_items(items_dict, num: int):
        result = list(items_dict)
        if num >= len(result):
            return result
        return random.sample(sorted(result), num)

    @staticmethod
    def remove_keys(_dict: dict, keys: list):
        for key in keys:
            if key in _dict:
                del _dict[key]
        return _dict

    @staticmethod
    def get_current_timestamp():
        return round(datetime.datetime.now().timestamp())

    @staticmethod
    def field_inline_alternation(fields: list):
        for i in range(1, len(fields) + 1):
            fields[i - 1]['inline'] = False if i % 3 == 0 else True
        return fields

    # @staticmethod
    # def get_items_by_type(items_dict, include_only: str = None, not_include: str = None):
    #     return Func.get_items_by_key(items_dict, 'type', include_only, not_include)

    # @staticmethod
    # def check_consecutive_timestamps(timestamps: list, n: int, time: float = 5, start_time: int = 4) -> int:
    #     count = 0
    #     consecutive_count = 0
    #     for i in range(len(timestamps) - 1):
    #         current_timestamp = timestamps[i]
    #         next_timestamp = timestamps[i + 1]
    #
    #         if start_time <= next_timestamp - current_timestamp < time:
    #             count += 1
    #             if count >= n:
    #                 consecutive_count += 1
    #         else:
    #             count = 0
    #
    #     return consecutive_count

    @staticmethod
    def check_consecutive_timestamps(timestamps: list, time: float = 5, start_time: int = 4) -> int:
        count = 0
        n = 1  # Initialize n with 1
        for i in range(len(timestamps) - 1):
            current_timestamp = timestamps[i]
            next_timestamp = timestamps[i + 1]

            if start_time <= next_timestamp - current_timestamp < time:
                count += 1
                if count >= n:
                    n = count

            else:
                count = 0

        return n

    # @staticmethod
    # def is_2d_list(lst):
    #     if isinstance(lst, list) and len(lst) > 0:
    #         return all(isinstance(i, list) for i in lst) and all(len(i) > 0 for i in lst)
    #     return False
    #
    # @staticmethod
    # def is_3d_list(lst):
    #     if isinstance(lst, list) and len(lst) > 0:
    #         if isinstance(lst[0], list) and len(lst[0]) > 0:
    #             return isinstance(lst[0][0], list)
    #     return False
    #

    @staticmethod
    async def send_data_to_stats_channel(client, servers):
        channel = client.get_channel(config.BOT_STATS_CHANNEL)
        try:
            await channel.edit(name=str(re.sub(r'\d+', str(servers), str(channel))))
        except:
            pass

    @staticmethod
    def get_number_of_possible_skin_variations():
        num = 1
        for cat in os.listdir('bin/pig_skins'):
            num *= len(os.listdir(f'bin/pig_skins/{cat}'))
        return num

    @staticmethod
    def send_data_to_sdc(servers, shards: int = 1):
        requests.post('https://api.server-discord.com/v2/bots/1102273144733049003/stats',
                      headers={'Authorization': f'SDC {config.SDC_TOKEN}'},
                      json={'servers': servers,
                            'shards': shards
                            })

    @staticmethod
    def send_data_to_boticord(servers):
        requests.post('https://api.boticord.top/bots/1102273144733049003/stats',
                      headers={'Authorization': f'Bot {config.BOTICORD_TOKEN}'},
                      json={'servers': servers})

    @staticmethod
    def remove_empty_lists_from_list(lst):
        new_lst = []
        if Func.get_list_dim(lst) == 2:
            new_lst = []
            for i in lst:
                if i:
                    new_lst.append(i)
        elif Func.get_list_dim(lst) == 3:
            new_lst = []
            for i in lst:
                if i:
                    new_lst.append([])
                    for j in i:
                        if j:
                            new_lst[lst.index(i)].append(j)
        return new_lst

    @staticmethod
    def cut_text(text, chars, dots: bool = True):
        if len(text) > chars + 1:
            if dots:
                text = text[:chars - 3] + '...'
            else:
                text = text[:chars]
        return text

    #
    # @staticmethod
    # async def send_command_use_webhook(client, inter):
    #     color = config.main_color
    #     if inter.author.id != client.owner_id:
    #         color = config.default_avatars[int(inter.author.default_avatar.key)]['hex']
    #     options_text = ''
    #     raw_options_text = ''
    #     command_text, options = Func.get_command_name_and_options(inter)
    #     discohook_embed = discord_webhook.DiscordEmbed(title='Command used',
    #                                                    description=f'**User:** {inter.author}\n'
    #                                                                f'**Guild:** `{inter.guild}`\n'
    #                                                                f'**Channel:** `{inter.channel}`\n'
    #                                                                f'**Command:** `{command_text}`\n',
    #                                                    color=color)
    #     for i, option in enumerate(options):
    #         value = option.value
    #         if type(value) == disnake.Member or type(value) == disnake.User:
    #             value = value.id
    #         options_text += f'{option.name}: `{Func.cut_name(value, 20)}`\n'
    #         raw_options_text += f'{option.name}: {Func.cut_name(value, 500)} '
    #     if options_text:
    #         discohook_embed.add_embed_field(name='Options',
    #                                         value=f'{options_text}')
    #     discohook_embed.add_embed_field(name='Raw command',
    #                                     value=f'```/{command_text} {raw_options_text}```',
    #                                     inline=False)
    #     if inter.data.target is not None:
    #         discohook_embed.add_embed_field(name='Target',
    #                                         value=f'{inter.data.target}')
    #     discohook_embed.set_footer(
    #         text=f'Guild ID: {inter.guild.id}\nChannel ID: {inter.channel.id}\nUser ID: {inter.author.id}')
    #     await Func.send_webhook_embed(config.command_use_webhook, discohook_embed, str(inter.client.user), inter.client.user.avatar.url)
    #
    #
    # @staticmethod
    # def numerate_list_to_text(elements_list: list) -> str:
    #     text = ''
    #     for i, j in enumerate(elements_list):
    #         text += f'**{i + 1}.** {j.capitalize()}\n'
    #     return text
    #
    #
    # @staticmethod
    # async def send_webhook_embed(url: str, embed, username=None, avatar_url=None):
    #     webhook = discord_webhook.DiscordWebhook(url=url, username=username, avatar_url=avatar_url)
    #     webhook.add_embed(embed)
    #     while True:
    #         webhook_ex = webhook.execute()
    #         if webhook_ex.status_code == 200:
    #             break
    #         else:
    #             await asyncio.sleep(webhook_ex.json()['retry_after'] / 1000 + .2)
    #
    #
    # @staticmethod
    # def get_emojis(guild):
    #     emojis = utils_config.emojis
    #     if not guild.default_role.permissions.use_external_emojis:
    #         emojis = utils_config.unicode_emojis
    #     return emojis
    #
    #
    # @staticmethod
    # async def send_guild_join_log_message(client, guild):
    #     emojis = Func.get_emojis(guild)
    #     embed = discord_webhook.DiscordEmbed(title='Bot Joined The Guild',
    #                                          description=f'',
    #                                          color=config.main_color)
    #     if guild.icon is not None:
    #         embed.set_thumbnail(url=guild.icon.url)
    #     embed.add_embed_field(name='Name', value=str(guild))
    #     embed.add_embed_field(name='Owner',
    #                           value=f'{guild.owner.mention}')
    #     embed.add_embed_field(name='Created',
    #                           value=f'<t:{round(guild.created_at.timestamp())}:D>\n'
    #                                 f'<t:{round(guild.created_at.timestamp())}:R>')
    #     embed.add_embed_field(
    #         name=f'Members',
    #         value=f'{emojis["members"]} Total: **{guild.member_count}**\n'
    #               f'{emojis["member"]} Users: **{len([m for m in guild.members if not m.bot])}**\n'
    #               f'{emojis["bot"]} Bots: **{len([m for m in guild.members if m.bot])}**'
    #     )
    #     embed.set_footer(text=f'Guild ID: {guild.id} | Owner ID: {guild.owner_id}')
    #     await Func.send_webhook_embed(config.guild_join_webhook, embed,
    #                                   username=str(client.user), avatar_url=client.user.avatar.url)
