from .embeds import trade_embed
from ...utils import *


async def trade(inter, user1, user2, trade_id: str = None, pre_command_check: bool = True):
    lang = User.get_language(inter.author.id)
    User.register_user_if_not_exists(user2.id)
    if pre_command_check:
        await BotUtils.pre_command_check(inter)
        if user1 == user2:
            await error_callbacks.default_error_callback(inter, translate(Locales.ErrorCallbacks.cant_trade_with_yourself_title, lang),
                                                         translate(Locales.ErrorCallbacks.cant_trade_with_yourself_desc, lang))
            return
        if user2.bot:
            await error_callbacks.default_error_callback(inter, translate(Locales.ErrorCallbacks.bot_as_trade_user_title, lang),
                                                         translate(Locales.ErrorCallbacks.bot_as_trade_user_desc, lang))
            return
    if trade_id is None:
        m = await send_callback(inter, '🔃')
        trade_id = str(m.id)
        Trade.create(trade_id, user1.id, user2.id)
        await BotUtils.send_notification(inter, user2,
                                         translate(Locales.Trade.trade_invitation_title, User.get_language(user2.id)),
                                         translate(Locales.Trade.trade_invitation_desc, User.get_language(user2.id),
                                                   format_options={'user': user1.display_name}),
                                         prefix='💰',
                                         url_label=translate(Locales.Global.message, User.get_language(user2.id)),
                                         url=m.jump_url, send_to_dm=True, create_command_notification=False,
                                         guild=inter.guild)
    agree_number = await Trade.get_agree_number(inter.client, trade_id)
    transferred = False
    transfer = True
    if agree_number == 2:
        for i in range(2):
            for user_id in [user1.id, user2.id]:
                data = Trade.get_user_data(trade_id, user_id)['items']
                for item_id in data:
                    amount_to_give = Trade.get_item_amount(trade_id, user_id, item_id)
                    amount_to_remove = amount_to_give
                    if item_id == 'coins':
                         amount_to_remove = BotUtils.get_amount_with_commission(amount_to_give, BotUtils.get_commission(user1 if user_id == inter.author.id else user2, user1 if user_id != inter.author.id else user2))
                    if i == 0:
                        if Item.get_amount(item_id, user_id) < amount_to_remove:
                            Trade.set_agree(trade_id, user1.id, False)
                            Trade.set_agree(trade_id, user2.id, False)
                            agree_number = await Trade.get_agree_number(inter.client, trade_id)
                            await error_callbacks.not_enough_item(inter, item_id, await User.get_user(inter.client, user_id))
                            transfer = False
                            break
                    else:
                        if transfer:
                            user_id_to_give = user1.id if user_id == user2.id else user2.id
                            user_id_to_remove = user1.id if user_id != user2.id else user2.id
                            User.add_item(user_id_to_give, item_id, amount_to_give)
                            User.remove_item(user_id_to_remove, item_id, amount_to_remove)
                            transferred = True
    if transferred:
        await send_callback(inter, embed=generate_embed(Locales.Global.successfully[lang],
                                                        description=Locales.Trade.scd_desc[lang].format(user1=user1.display_name, user2=user2.display_name),
                                                        prefix=Func.generate_prefix("scd"),
                                                        thumbnail_file=await Func.get_image_path_from_link(utils_config.image_links['trade']),
                                                        footer_url=inter.client.user.avatar.url,
                                                        footer=inter.client.user.display_name
                                                        ))
        return
    try:
        await inter.response.defer()
    except disnake.InteractionResponded:
        pass
    add_item_component = disnake.ui.StringSelect(placeholder=Locales.Trade.add_item_placeholder[lang],
                                                 custom_id='trade;add',
                                                 options=[disnake.SelectOption(label=Locales.Global.money[lang],
                                                                               value=f'coins;{trade_id}'),
                                                          disnake.SelectOption(label=Locales.Global.inventory[lang],
                                                                               value=f'inventory;{trade_id}'),
                                                          disnake.SelectOption(label=Locales.Global.wardrobe[lang],
                                                                               value=f'wardrobe;{trade_id}')
                                                          ])
    agree_component = disnake.ui.Button(style=disnake.ButtonStyle.green,
                                        emoji='✅', label=f'{agree_number}/2',
                                        custom_id=f'trade;agree;{trade_id}')
    cancel_component = disnake.ui.Button(style=disnake.ButtonStyle.red,
                                        emoji='✖️', custom_id=f'trade;cancel;{trade_id}')
    clear_component = disnake.ui.Button(style=disnake.ButtonStyle.blurple, label=Locales.Global.clear[lang],
                                        custom_id=f'trade;clear;{trade_id}')
    await send_callback(inter if not Trade.exists(trade_id) else inter.client.get_message(int(trade_id)), embed=await trade_embed(inter, trade_id, lang),
                        components=[[add_item_component],
                                    [agree_component, cancel_component, clear_component]])
