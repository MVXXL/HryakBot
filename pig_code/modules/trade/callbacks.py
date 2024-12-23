from .embeds import trade_embed
from ...utils import *


async def trade(inter, user1, user2, trade_id: str = None, pre_command_check: bool = True):
    lang = User.get_language(inter.user.id)
    User.register_user_if_not_exists(user2.id)
    if pre_command_check:
        await Utils.pre_command_check(inter)
        if user1 == user2:
            await error_callbacks.default_error_callback(inter, translate(
                Locales.ErrorCallbacks.cant_trade_with_yourself_title, lang),
                                                         translate(Locales.ErrorCallbacks.cant_trade_with_yourself_desc,
                                                                   lang))
            return
        if user2.bot:
            await error_callbacks.default_error_callback(inter,
                                                         translate(Locales.ErrorCallbacks.bot_as_trade_user_title,
                                                                   lang),
                                                         translate(Locales.ErrorCallbacks.bot_as_trade_user_desc, lang))
            return
    if trade_id is None:
        m = await send_callback(inter, '🔃')
        trade_id = str(m.id)
        Trade.create(trade_id, user1.id, user2.id, m)
        await Utils.send_notification(user2, inter,
                                      translate(Locales.Trade.trade_invitation_title, User.get_language(user2.id)),
                                      translate(Locales.Trade.trade_invitation_desc, User.get_language(user2.id),
                                                format_options={'user': user1.display_name}),
                                      prefix_emoji='💰',
                                      url_label=translate(Locales.Global.message, User.get_language(user2.id)),
                                      url=m.jump_url, send_to_dm=True, create_command_notification=False,
                                      guild=inter.guild)
    if Trade.get_message(trade_id) is None:
        await error_callbacks.cannot_use_command_in_this_channel(inter)
        return
    agree_number = await Trade.get_agree_number(trade_id)
    if agree_number == 2 and Trade.get_status(trade_id) == 'in_process':
        Trade.set_status(trade_id, 'tax_processing')
    if Trade.get_status(trade_id) == 'in_process':
        try:
            await inter.response.defer()
        except discord.InteractionResponded:
            pass
        add_item_component = discord.ui.Select(placeholder=translate(Locales.Trade.add_item_placeholder, lang),
                                               custom_id='trade;add',
                                               options=[
                                                   discord.SelectOption(label=Item.get_name('coins', lang),
                                                                        value=f'coins;{trade_id}',
                                                                        emoji=Item.get_emoji('coins')),
                                                   discord.SelectOption(label=Item.get_name('hollars', lang),
                                                                        value=f'hollars;{trade_id}',
                                                                        emoji=Item.get_emoji('hollars')),
                                                   discord.SelectOption(
                                                       label=translate(Locales.Global.inventory, lang),
                                                       value=f'inventory;{trade_id}',
                                                       emoji='📦'),
                                                   discord.SelectOption(
                                                       label=translate(Locales.Global.wardrobe, lang),
                                                       value=f'wardrobe;{trade_id}',
                                                       emoji='🎭')
                                               ],
                                               row=0)
        agree_component = discord.ui.Button(style=discord.ButtonStyle.green,
                                            emoji='✅', label=f'{agree_number}/2',
                                            custom_id=f'trade;agree;{trade_id}',
                                            row=1)
        cancel_component = discord.ui.Button(style=discord.ButtonStyle.red,
                                             emoji='✖️', custom_id=f'trade;cancel;{trade_id}',
                                             row=1)
        clear_component = discord.ui.Button(style=discord.ButtonStyle.blurple,
                                            label=translate(Locales.Global.clear, lang),
                                            custom_id=f'trade;clear;{trade_id}',
                                            row=1)
        await send_callback(Trade.get_message(trade_id),
                            embed=await trade_embed(inter, trade_id, lang),
                            components=[add_item_component,
                                        agree_component, cancel_component, clear_component])
        return
    elif Trade.get_status(trade_id) == 'tax_processing':
        if Trade.get_tax_splitting_vote(trade_id, user1.id) == 'tax_split_1':
            Trade.set_tax_splitting(trade_id, 'tax_split_1')
            for item_id, amount in Utils.get_trade_total_tax(trade_id).items():
                Trade.add_tax_to_pay(trade_id, user1.id, item_id, amount)
        elif Trade.get_tax_splitting_vote(trade_id, user2.id) == 'tax_split_2':
            Trade.set_tax_splitting(trade_id, 'tax_split_2')
            for item_id, amount in Utils.get_trade_total_tax(trade_id).items():
                Trade.add_tax_to_pay(trade_id, user2.id, item_id, amount)
        elif Trade.get_total_tax_splitting_votes(trade_id, 'tax_split_equal') == 2:
            Trade.set_tax_splitting(trade_id, 'tax_split_equal')
            for item_id, amount in Utils.get_trade_total_tax(trade_id).items():
                Trade.add_tax_to_pay(trade_id, user1.id, item_id, amount // 2)
                amount //= 2
                Trade.add_tax_to_pay(trade_id, user2.id, item_id, amount)
        if Trade.get_tax_splitting(trade_id) is not None or not Utils.get_trade_total_tax(trade_id):
            Trade.set_status(trade_id, 'tax_processing_success')
        else:
            description = f'{translate(Locales.Trade.tax_splitting_process_desc, lang)}\n'
            for currency, amount in Utils.get_trade_total_tax(trade_id).items():
                description += f'\n> {Item.get_emoji(currency)}・{Item.get_name(currency, lang)} x{amount}'
            description += f'\n\n{translate(Locales.Trade.tax_splitting_process_who_pays_desc, lang)}'
            components = [
                discord.ui.Button(style=discord.ButtonStyle.blurple,
                                  label=f'{f"1/2 " if Trade.get_total_tax_splitting_votes(trade_id, 'tax_split_1') == 1 else ""}@{user1}',
                                  custom_id=f'trade;tax_split_1;{trade_id}',
                                  row=1),
                discord.ui.Button(style=discord.ButtonStyle.blurple,
                                  label=f'{f"1/2 " if Trade.get_total_tax_splitting_votes(trade_id, 'tax_split_2') == 1 else ""}@{user2}',
                                  custom_id=f'trade;tax_split_2;{trade_id}',
                                  row=1),
                discord.ui.Button(style=discord.ButtonStyle.blurple,
                                  label=f'{f"{Trade.get_total_tax_splitting_votes(trade_id, 'tax_split_equal')}/2 " if Trade.get_total_tax_splitting_votes(trade_id, 'tax_split_equal') > 0 else ""}Пополам',
                                  custom_id=f'trade;tax_split_equal;{trade_id}',
                                  row=1)
            ]
            await send_callback(Trade.get_message(trade_id), embed=generate_embed(translate(Locales.Trade.tax_splitting_process_title, lang),
                                                            description=description,
                                                            prefix=Func.generate_prefix("💸"),
                                                            thumbnail_url=await Func.get_image_path_from_link(
                                                                utils_config.image_links['trade']),
                                                            footer_url=inter.client.user.avatar.url,
                                                            footer=inter.client.user.display_name
                                                            ),
                                components=components)
            return
    if Trade.get_status(trade_id) == 'tax_processing_success':
        await asyncio.sleep(.5)
        if Trade.get_status(trade_id) == 'transferring':
            return
        Trade.set_status(trade_id, 'transferring')
        for user_id in [user1.id, user2.id]:
            total_items = Trade.get_items(trade_id, user_id)
            tax_to_pay = Trade.get_tax_to_pay(trade_id, user_id)
            for key, value in tax_to_pay.items():
                if key in total_items:
                    total_items[key]["amount"] += value["amount"]
                else:
                    total_items[key] = value
            for item_id, data in total_items.items():
                if Item.get_amount(item_id, user_id) < data['amount']:
                    await error_callbacks.not_enough_items(inter, item_id,
                                                           await User.get_user(inter.client, user_id),
                                                           thumbnail_url=await Func.get_image_path_from_link(
                                                               utils_config.image_links['trade']))
                    return

        for user_id in [user1.id, user2.id]:
            for item_id, data in Trade.get_items(trade_id, user_id).items():
                user_id_to_give = user1.id if user_id == user2.id else user2.id
                user_id_to_remove = user1.id if user_id != user2.id else user2.id
                amount = data['amount']
                User.transfer_item(user_id_to_remove, user_id_to_give, item_id, amount)
                if Item.get_amount(item_id, user_id_to_remove) <= 0 and Item.get_type(item_id) == 'skin':
                    Pig.remove_skin(user_id, item_id)
            for item_id, data in Trade.get_tax_to_pay(trade_id, user_id).items():
                amount_to_remove = data['amount']
                User.remove_item(user_id, item_id, amount_to_remove)
                if Item.get_amount(item_id, user_id) <= 0 and Item.get_type(item_id) == 'skin':
                    Pig.remove_skin(user_id, item_id)
        Trade.set_status(trade_id, 'success')
    if Trade.get_status(trade_id) == 'success':
        await send_callback(Trade.get_message(trade_id), embed=generate_embed(translate(Locales.Trade.scd_title, lang),
                                                        description=translate(Locales.Trade.scd_desc, lang,
                                                                              {'user1': user1.display_name,
                                                                               'user2': user2.display_name}),
                                                        prefix=Func.generate_prefix("scd"),
                                                        thumbnail_url=await Func.get_image_path_from_link(
                                                            utils_config.image_links['trade']),
                                                        footer_url=inter.client.user.avatar.url,
                                                        footer=inter.client.user.display_name
                                                        ))
