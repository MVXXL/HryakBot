from ...core import *
from ...core import Locales
from ...utils import *
from ...utils import Func
from ...utils.discord_utils import generate_embed


async def trade_embed(inter, trade_id, lang):
    user1 = await Trade.get_user(inter.client, trade_id, 0)
    user2 = await Trade.get_user(inter.client, trade_id, 1)
    user1_data = Trade.get_user_data(trade_id, user1.id)
    user2_data = Trade.get_user_data(trade_id, user2.id)
    user1_items_list = DisUtils.get_items_in_str_list(user1_data["items"], lang)
    user2_items_list = DisUtils.get_items_in_str_list(user2_data["items"], lang)
    return generate_embed(
        translate(Locales.Global.trade, lang),
        fields=[{'name': user1.display_name,
                 'value': f'```{translate(Locales.Global.no_items, lang) if not user1_items_list else user1_items_list}```',
                 'inline': True},
                {'name': user2.display_name,
                 'value': f'```{translate(Locales.Global.no_items, lang) if not user2_items_list else user2_items_list}```',
                 'inline': True}],
        prefix=Func.generate_prefix("💰"),
        thumbnail_url=await Func.get_image_path_from_link(utils_config.image_links['trade']),
        footer_url=inter.client.user.avatar.url,
        footer='Hryak'
    )
