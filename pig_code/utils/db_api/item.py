import random

from .connection import Connection
from .user import User
from ..functions import *
from ...core import *
from ...core.config import items_schema


class Item:

    @staticmethod
    def get_props(item_id):
        if item_id is None:
            return
        props = {}
        if len(item_id.split('.')) == 1:
            return
        for i in item_id.split('.')[1:]:
            props[i.split('=')[0]] = i.split('=')[1]
        return props

    @staticmethod
    def clean_id(item_id):
        if item_id is not None:
            return item_id.split('.')[0]

    @staticmethod
    def create(data: dict):
        params = []
        for value in data.values():
            if type(value) in [dict, list]:
                value = json.dumps(value, ensure_ascii=False)
            params.append(value)
        params = tuple(params)
        query = f"INSERT INTO {items_schema} ({', '.join([f'{i}' for i in data.keys()])}) " \
                f"VALUES ({', '.join(tuple(['%s' for _ in range(len(data))]))})"
        Connection.make_request(query,
                                params=params)

    @staticmethod
    def edit(item_id, data: dict):
        for k, v in data.items():
            if type(v) == dict:
                v = json.dumps(v)
            Connection.make_request(f"UPDATE {items_schema} SET {k} = %s WHERE id = %s",
                                    params=(v, item_id))
        Item.clear_get_data_cache()

    @staticmethod
    def delete(item_id: str):
        Connection.make_request(f"DELETE FROM {items_schema} WHERE id = {Item.clean_id(item_id)}")

    @staticmethod
    @cached(utils_config.db_caches['item.get_data'])
    def get_data(item_id: str, column: str, convert_to_type: type = None):
        if item_id is None:
            return
        result = Connection.make_request(
            f"SELECT {column} FROM {items_schema} WHERE id = %s",
            commit=False,
            fetch=True,
            params=(Item.clean_id(item_id),)
        )
        if result is not None:
            if convert_to_type == dict:
                result = json.loads(result)
            elif convert_to_type == bool:
                result = bool(result)
        return result

    @staticmethod
    def clear_get_data_cache(params: tuple=None):
        if params is not None:
            Func.clear_cache('item.get_data', params)
        else:
            Func.clear_cache('item.get_data')

    @staticmethod
    def exists(item_id):
        result = Connection.make_request(
            f"SELECT EXISTS(SELECT 1 FROM {items_schema} WHERE id = %s)",
            commit=False,
            fetch=True,
            params=(Item.clean_id(item_id),)
        )
        return bool(result)

    @staticmethod
    def transfer(item_id: str, user1_id, user2_id, amount: int = int, multiplier: float = 1):
        """
        :type multiplier: object
            Multiplier of items that will be given to the user_2
        """
        User.remove_item(user1_id, item_id, amount)
        User.add_item(user2_id, item_id, round(amount * multiplier))

    @staticmethod
    def get_name(item_id: str, lang: str = None):
        name = Item.get_data(item_id, 'name', convert_to_type=dict)
        if lang is not None:
            name = translate(name, lang)
        return name

    @staticmethod
    def get_description(item_id: str, lang: str = None):
        description = Item.get_data(item_id, 'description', convert_to_type=dict)
        if lang is not None:
            description = translate(description, lang)
        return description

    @staticmethod
    def get_type(item_id: str, lang: str = None):
        _type = Item.get_data(item_id, 'type')
        if lang is not None:
            _type = translate(Locales.ItemTypes[_type], lang)
        return _type

    @staticmethod
    def set_skin_config(item_id: str, new_config):
        new_config = json.dumps(new_config, ensure_ascii=False)
        Connection.make_request(
            f"UPDATE {items_schema} SET skin_config = %s WHERE id = '{item_id}'",
            params=(new_config,)
        )

    @staticmethod
    def get_skin_config(item_id: str):
        return Item.get_data(item_id, 'skin_config', convert_to_type=dict)

    @staticmethod
    def get_skin_type(item_id: str, lang: str = None):
        skin_config = Item.get_skin_config(item_id)
        skin_type = skin_config['type']
        if lang is not None:
            skin_type = translate(Locales.SkinTypes[skin_type], lang)
        return skin_type

    @staticmethod
    def get_not_compatible_skins(item_id: str):
        skin_config = Item.get_skin_config(item_id)
        if 'not_compatible_with' in skin_config:
            return skin_config['not_compatible_with']
        return []

    @staticmethod
    def get_skins_to_hide(item_id: str):
        skin_config = Item.get_skin_config(item_id)
        if 'hide' in skin_config:
            return skin_config['hide']
        return []

    @staticmethod
    def get_skin_layers(item_id: str):
        skin_config = Item.get_skin_config(item_id)
        layers = skin_config['layers']
        return layers

    @staticmethod
    def get_skin_layer(item_id: str, layer):
        layers = Item.get_skin_layers(item_id)
        return layers[layer]

    @staticmethod
    async def get_skin_layer_image_path(item_id: str, layer: str, type_: str = 'image'):
        layer = Item.get_skin_layer(item_id, layer)
        image = layer[type_]
        if type(image) == str:
            image = await Func.get_image_path_from_link(image)
        return image

    @staticmethod
    def get_skin_layer_shadow(item_id: str, layer):
        layer = Item.get_skin_layer(item_id, layer)
        if 'shadow' in layer:
            return layer['shadow']

    @staticmethod
    def get_skin_layer_before(item_id: str, layer):
        layer = Item.get_skin_layer(item_id, layer)
        if 'before' in layer:
            return layer['before']

    @staticmethod
    def get_skin_layer_after(item_id: str, layer):
        layer = Item.get_skin_layer(item_id, layer)
        if 'after' in layer:
            return layer['after']

    @staticmethod
    def get_skin_color(item_id: str):
        skin_config = Item.get_skin_config(item_id)
        if 'color' in skin_config:
            return skin_config['color']

    @staticmethod
    def get_skin_group(item_id: str):
        skin_config = Item.get_skin_config(item_id)
        if 'item_group' in skin_config:
            return skin_config['item_group']

    @staticmethod
    def get_skin_right_ear_line(item_id: str, type_: str):
        skin_config = Item.get_skin_config(item_id)
        if f'right_ear_line_{type_}' in skin_config:
            return skin_config[f'right_ear_line_{type_}']

    @staticmethod
    def get_skin_right_ear_line_type(item_id: str):
        skin_config = Item.get_skin_config(item_id)
        if f'right_ear_line' in skin_config:
            return skin_config[f'right_ear_line']


    @staticmethod
    def get_skin_eyes_outline_hex_color(item_id: str):
        skin_config = Item.get_skin_config(item_id)
        if 'eyes_outline_hex_color' in skin_config:
            return skin_config['eyes_outline_hex_color']

    @staticmethod
    def get_skin_right_eye_outline(item_id: str):
        skin_config = Item.get_skin_config(item_id)
        if 'right_eye_outline' in skin_config:
            return skin_config['right_eye_outline']

    @staticmethod
    def get_skin_left_eye_outline(item_id: str):
        skin_config = Item.get_skin_config(item_id)
        if 'left_eye_outline' in skin_config:
            return skin_config['left_eye_outline']


    @staticmethod
    def get_emoji(item_id: str):
        for i in range(10):
            e = Item.get_data(item_id, 'emoji')
            if e not in ['?', '?️']:
                break
            else:
                Item.clear_get_data_cache((item_id, 'emoji'))
        else:
            e = '❓'
        return e

    @staticmethod
    def clear_get_emoji_cache():
        Func.clear_cache('item.get_data')

    @staticmethod
    def get_inventory_type(item_id: str):
        return Item.get_data(item_id, 'inventory_type')

    @staticmethod
    def get_rarity(item_id: str, lang: str = None):
        rarity = Item.get_data(item_id, 'rarity')
        if lang is not None:
            rarity = translate(Locales.ItemRarities[rarity], lang)
        return rarity


    @staticmethod
    @aiocache.cached(ttl=86400)
    async def get_image_file_path(item_id: str):
        path = Func.generate_temp_path('img')
        if Item.get_data(item_id, 'image_file') is not None:
            async with aiofiles.open(path, 'wb') as file:
                await file.write(Item.get_data(item_id, 'image_file'))
            return path

    @staticmethod
    @aiocache.cached(ttl=86400)
    async def get_image_file_2_path(item_id: str):
        path = Func.generate_temp_path('img2')
        if Item.get_data(item_id, 'image_file_2') is not None:
            async with aiofiles.open(path, 'wb') as file:
                await file.write(Item.get_data(item_id, 'image_file_2'))
            return path

    @staticmethod
    def get_cooked_item_id(item_id: str):
        return Item.get_data(item_id, 'cooked_item_id')

    @staticmethod
    def get_market_price(item_id: str):
        if Item.get_props(item_id):
            return int(Item.get_props(item_id)['p'])
        return Item.get_data(item_id, 'market_price')

    @staticmethod
    def get_market_price_currency(item_id: str):
        if Item.get_props(item_id):
            return Item.get_props(item_id)['c']
        return Item.get_data(item_id, 'market_price_currency')

    @staticmethod
    def get_shop_category(item_id: str):
        return Item.get_data(item_id, 'shop_category')

    @staticmethod
    def get_shop_cooldown(item_id: str):
        result = Item.get_data(item_id, 'shop_cooldown', convert_to_type=dict)
        if result is not None:
            return int(list(result.keys())[0]), int(list(result.values())[0])
        return None, None

    @staticmethod
    def get_buffs(item_id: str):
        return Item.get_data(item_id, 'buffs', convert_to_type=dict)

    @staticmethod
    def get_case_drops(item_id: str):
        return Item.get_data(item_id, 'case_drops', convert_to_type=dict)

    @staticmethod
    def generate_case_drop(item_id: str):
        items_dropped = {}
        for i in Item.get_case_drops(item_id):
            if len(i) == 1 and i[0]['chance'] < 100:
                i.append({'items': [None], 'amount': [1, 1], 'chance': 100 - i[0]['chance']})
            items_dict_dropped = i[Func.random_choice_with_probability({n: j['chance'] for n, j in enumerate(i)})]
            items_dropped[random.choice(items_dict_dropped['items'])] = random.randrange(items_dict_dropped['amount'][0],
                                                                                     items_dict_dropped['amount'][1]) if \
            items_dict_dropped['amount'][0] != items_dict_dropped['amount'][1] else items_dict_dropped['amount'][0]
        return items_dropped

    @staticmethod
    def get_requirements(item_id: str):
        return Item.get_data(item_id, 'requirements', convert_to_type=dict)

    @staticmethod
    def get_all_allowed_users_by_requirements(client, item_id: str):
        requirements = Item.get_requirements(item_id)
        requirements_results = []
        for n, i in enumerate(requirements):
            requirements_results.append([])
            for j in i:
                if 'guild' in j:
                    guild = client.get_guild(j['guild'])
                    if guild is not None:
                        if 'role' in j:
                            role = guild.get_role(j['role'])
                            requirements_results[n] += [str(i.id) for i in role.members]
                        else:
                            requirements_results[n] += [str(i.id) for i in guild.members]
                if 'user' in j:
                    requirements_results[n].append(str(j['user']))
        return Func.common_elements(requirements_results)
        # requirements_results = []
        # for n, i in enumerate(requirements):
        #     requirements_results.append([])
        #     for j in i:
        #         if 'guild' in j:
        #             guild = client.get_guild(j['guild'])
        #             if guild is not None:
        #                 member = guild.get_member(int(user_id))
        #                 if 'role' in j:
        #                     role = guild.get_role(j['role'])
        #                     if member is not None and role.id in [i.id for i in member.roles]:
        #                         requirements_results[n].append(True)
        #                     else:
        #                         requirements_results[n].append(False)
        #                 else:
        #                     if member is not None:
        #                         requirements_results[n].append(True)
        #                     else:
        #                         requirements_results[n].append(False)
        #             else:
        #                 requirements_results[n].append(False)
        #         if 'user' in j:
        #             if int(user_id) == j['user']:
        #                 requirements_results[n].append(True)
        #             else:
        #                 requirements_results[n].append(False)
        # final_result = True
        # for i in [any(j) for j in requirements_results]:
        #     if i is False:
        #         final_result = False
        # return final_result

    @staticmethod
    def is_user_allowed_by_item_requirements(client, user_id, item_id: str):
        requirements = Item.get_requirements(item_id)
        requirements_results = []
        for n, i in enumerate(requirements):
            requirements_results.append([])
            for j in i:
                if 'guild' in j:
                    guild = client.get_guild(j['guild'])
                    if guild is not None:
                        member = guild.get_member(int(user_id))
                        if 'role' in j:
                            role = guild.get_role(j['role'])
                            if member is not None and role.id in [i.id for i in member.roles]:
                                requirements_results[n].append(True)
                            else:
                                requirements_results[n].append(False)
                        else:
                            if member is not None:
                                requirements_results[n].append(True)
                            else:
                                requirements_results[n].append(False)
                    else:
                        requirements_results[n].append(False)
                if 'user' in j:
                    if int(user_id) == j['user']:
                        requirements_results[n].append(True)
                    else:
                        requirements_results[n].append(False)
        final_result = True
        for i in [any(j) for j in requirements_results]:
            if i is False:
                final_result = False
        return final_result

    @staticmethod
    def is_salable(item_id: str):
        return Item.get_data(item_id, 'salable', convert_to_type=bool)

    @staticmethod
    def get_sell_price(item_id: str):
        return Item.get_data(item_id, 'sell_price')

    @staticmethod
    def get_sell_price_currency(item_id: str):
        return Item.get_data(item_id, 'sell_price_currency')

    @staticmethod
    def is_tradable(item_id: str):
        return Item.get_data(item_id, 'tradable', convert_to_type=bool)

    @staticmethod
    def get_amount(item_id, user_id=None):
        if Item.get_props(item_id):
            return int(Item.get_props(item_id)['a'])
        if user_id is not None:
            inventory = User.get_inventory(str(user_id))
            if item_id in inventory:
                return inventory[item_id]['amount']
        return 0

