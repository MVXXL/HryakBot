from discord import Locale
from . import config

valid_discord_locales = ['en', 'ru']

full_names = {'en': 'English',
              'ru': 'Russian | Pусский',
              'uk': 'Ukrainian | Українська'}

big_texts = {}


class Locales:
    app_commands_locales = {
        'choice-true': {'en': '✅ True',
                        'ru': '✅ Да'},
        'choice-false': {'en': '❌ False',
                         'ru': '❌ Нет'},
        'help-desc': {'en': 'Get help for the bot',
                      'ru': 'Хряковое пособие и обучение'},
        'context-profile-name': {'en': 'Profile',
                                 'ru': 'Профиль'},
        'profile-desc': {'en': 'View players\'s profile',
                         'ru': 'Посмотреть профиль игрока'},
        'profile-user-name': {'en': 'user',
                              'ru': 'пользователь'},
        'profile-user-desc': {'en': 'The user whose profile you want to view',
                              'ru': 'Пользователь, у которого вы хотите посмотреть профиль'},
        'top-desc': {'en': 'Players top',
                     'ru': 'Топ игроков'},
        'top-global-name': {'en': 'global',
                            'ru': 'глобальный'},
        'top-global-desc': {'en': 'Display the global user leaderboard',
                            'ru': 'Показать глобальный топ пользователей'},
        'buffs-desc': {'en': 'Buffs applied to your pig',
                       'ru': 'Баффы, примененные к вашему Хряку'},
        'inventory-desc': {'en': 'View your inventory',
                           'ru': 'Посмотреть свой инвентарь'},
        'wardrobe-desc': {'en': 'Skins for your pig',
                          'ru': 'Скины для вашего хряка'},
        'shop-desc': {'en': 'View pig shop',
                      'ru': 'Заглянуть в магазин'},
        'quests-desc': {'en': 'View available quests',
                        'ru': 'Посмотреть доступные квесты'},
        'feed-desc': {
            'en': 'Feed your pig',
            'ru': 'Накормить своего хряка',
        },
        'butcher-desc': {'en': 'Harvest meat from your pig',
                         'ru': 'Снять немного сала с вашего хряка (ему не больно)'},
        'rename-desc': {'en': 'Rename your pig',
                        'ru': 'Переименовать своего хряка'},
        'rename-name-name': {'en': 'name',
                             'ru': 'имя'},
        'rename-name-desc': {'en': 'Choose a new name for your pig',
                             'ru': 'Новое имя для свинтуса'},
        'duel-desc': {'en': 'Arrange a duel between pigs',
                      'ru': 'Устроить дуэль между хряками'},
        'duel-user-name': {'en': 'user',
                           'ru': 'пользователь'},
        'duel-user-desc': {'en': 'Select the user you want to duel with',
                           'ru': 'Пользователь с которым вы хотите провести дуэль'},
        'duel-bet-name': {'en': 'bet',
                          'ru': 'ставка'},
        'duel-bet-desc': {'en': 'The number of coins you want to bet',
                          'ru': 'Количество монет, которое хотите поставить'},
        'trade-desc': {'en': 'Trade with user',
                       'ru': 'Торговать с пользователем'},
        'trade-user-name': {'en': 'user',
                            'ru': 'пользователь'},
        'trade-user-desc': {'en': 'The user you want to trade with',
                            'ru': 'Пользователь с которым вы хотите торговать'},
        'send_money-desc': {'en': 'Transfer money to another user',
                            'ru': 'Перевести деньги другом пользователю'},
        'send_money-user-name': {'en': 'user',
                                 'ru': 'пользователь'},
        'send_money-user-desc': {'en': 'User to whom you want to send money',
                                 'ru': 'Пользователь которому отправить деньги'},
        'send_money-amount-name': {'en': 'amount',
                                   'ru': 'количество'},
        'send_money-amount-desc': {'en': 'Amount of money to transfer',
                                   'ru': 'Количество денег для перевода'},
        'send_money-currency-name': {'en': 'currency',
                                     'ru': 'валюта'},
        'send_money-currency-desc': {'en': 'Currency you want to send',
                                     'ru': 'Валюта, которую вы хотите отправить'},
        'send_money-message-name': {'en': 'message',
                                    'ru': 'сообщение'},
        'send_money-message-desc': {'en': 'The message the user will receive',
                                    'ru': 'Сообщение, которое получит пользователь'},
        'report-desc': {'en': 'Report bug',
                        'ru': 'Сообщить о баге'},
        'report-text-name': {'en': 'text',
                             'ru': 'текст'},
        'report-text-desc': {'en': 'Describe a bug',
                             'ru': 'Описание бага'},
        'report-attachment-name': {'en': 'attachment',
                                   'ru': 'картинка'},
        'report-attachment-desc': {'en': 'Attach a screenshot',
                                   'ru': 'Скриншот с багом'},
        'promocode-desc': {'en': 'Use promo code',
                           'ru': 'Использовать промо код'},
        'promocode-code-name': {'en': 'code',
                                'ru': 'код'},
        'promocode-code-desc': {'en': 'Enter your promo code',
                                'ru': 'Введите ваш промо-код'},
        'say-desc': {'en': 'Make hryak say something',
                     'ru': 'Заставить хряка сказать что-то'},
        'say-text-name': {'en': 'text',
                          'ru': 'текст'},
        'say-text-desc': {'en': 'Use "\\\\" for a line break',
                          'ru': 'Используйте "\\\\" для перехода на следующую строку'},
        'say-user-name': {'en': 'user',
                          'ru': 'пользователь'},
        'say-user-desc': {'en': 'Speak for the user',
                          'ru': 'Говорить от лица пользователя'},
        'view-desc': {'en': 'View the appearance of your pig',
                      'ru': 'Посмотреть внешний вид хряка'},
        'view-user-name': {'en': 'user',
                           'ru': 'пользователь'},
        'view-user-desc': {'en': 'The user you want to see the pig of',
                           'ru': 'Пользователь, у которого вы хотите посмотреть хряка'},
        'language-desc': {
            'en': 'Change bot language',
            'ru': 'Изменить язык бота'
        },
        'language-language-name': {
            'en': 'language',
            'ru': 'язык'
        },
        'language-language-desc': {
            'en': 'The language that Hryak will speak',
            'ru': 'Язык, на котором Хряк будет хрюкать'
        },
        'settings-say-desc': {'en': 'Configuring the say command',
                              'ru': 'Настройка команды /say'},
        'settings-say-allow-name': {'en': 'allow',
                                    'ru': 'включить'},
        'settings-say-allow-desc': {'en': 'Just choose yes or no',
                                    'ru': 'Просто выбери да или нет'},
        'settings-top-desc': {'en': 'Configuring the leaderboard command',
                                      'ru': 'Настройка ко��анды /leaderboard'},
        'settings-top-participate-name': {'en': 'participate',
                                             'ru': 'участвовать'},
        'settings-top-participate-desc': {'en': 'Just choose yes or no',
                                                  'ru': 'Просто выбери да или нет'},
    }

    user_install_content = {
        'en': f'*[Feed and grow your pig!]({config.BOT_AUTH_LINK})*',
        'ru': f'*[Вырасти своего Хряка!]({config.BOT_AUTH_LINK})*'
    }

    class Feed:
        feed_scd_title = {
            'en': 'Your pig has been fed',
            'ru': 'Вы покормили своего хряка',
            'uk': 'Ви погодували свого хряка'
        }
        feed_scd_desc_list = {
            'en': ['**{pig}** has gained **{mass}** kg'],
            'ru': ['**{pig}** поправился на **{mass}** кг',
                   '**{pig}** набрал **{mass}** кг сала',
                   '**{pig}** стал больше на **{mass}** кг',
                   '**{pig}** прибавил **{mass}** кг'],
            'uk': ['**{pig}** набрала **{mass}** кг',
                   '**{pig}** здобула **{mass}** кг сала',
                   '**{pig}** стала більшою на **{mass}** кг',
                   '**{pig}** додала **{mass}** кг']
        }
        feed_fail_desc_list = {
            'en': ['Your **{pig}** vomited and lost **{mass}** kg'],
            'ru': ['Вашего **{pig}** стошнило и он похудел на **{mass}** кг'],
            'uk': ['Вашого **{pig}** стошнило і він схуд на **{mass}** кг']
        }
        pig_pooped_desc_list = {
            'en': ['**{pig}** has pooped, yielding **{poop}** 💩'],
            'ru': ['**{pig}** покакал и вы получили **{poop}** 💩',
                   '**{pig}** испражнился и вы получили **{poop}** 💩',
                   '**{pig}** справил нужду, и вы получили **{poop}** 💩'],
            'uk': ['**{pig}** покакав і ви отримали **{poop}** 💩',
                   '**{pig}** випорожнився і ви отримали **{poop}** 💩',
                   '**{pig}** зробив потребу, і ви отримали **{poop}** 💩']
        }
        total_pig_weight = {
            'en': "Your pig's weight: **{weight}** kg",
            'ru': 'Масса твоего хряка: **{weight}** кг',
            'uk': 'Вага вашого хряка: **{weight}** кг'
        }

    class Butcher:
        butcher_title = {'en': "You've harvested some meat",
                         'ru': 'Вы срезали немного сала',
                         'uk': 'Ви зрізали трохи сала'}
        butcher_desc_list = {'en': ["You've harvested some lard from **{pig}** and obtained **{meat}** 🥓"],
                             'ru': ['Вы срезали немного сала с **{pig}** и получили **{meat}** 🥓'],
                             'uk': ['Ви зрізали трохи сала з **{pig}** та отримали **{meat}** 🥓']}
        weight_lost_desc_list = {'en': ['**{pig}** lost **{weight_lost}** kg of weight'],
                                 'ru': ['**{pig}** потерял **{weight_lost}** кг веса'],
                                 'uk': ['**{pig}** втратив **{weight_lost}** кг ваги']}
        no_knife_desc = {'en': '*Planning to slice the meat barehanded? Better find a knife*',
                         'ru': '*Ты собираешся мясо руками снимать? Найди нож*',
                         'uk': "*Ти збираєшся м'ясо руками знімати? Знайди ніж*"}
        total_pig_weight = {'en': "Your pig's weight: **{weight}** kg",
                            'ru': 'Масса твоего хряка: **{weight}** кг',
                            "uk": 'Маса твого кнура: **{weight}** кг'}

    class Duel:
        invite_title = {'en': 'Invitation to a duel',
                        'ru': 'Приглашение на дуэль'}
        personal_invite_desc = {'en': '***{opponent}** was invited to duel with **{user}***\n\n'
                                      '- Bet: **{bet}** 🪙',
                                'ru': '***{opponent}** был приглашен на дуэль с **{user}***\n\n'
                                      '- Ставка: **{bet}** 🪙'}
        personal_invite_dm_desc = {'en': '***You** were invited to duel with **{user}***\n\n'
                                         '- Bet: **{bet}** 🪙',
                                   'ru': '***Вы** были приглашены на дуэль с **{user}***\n\n'
                                         '- Ставка: **{bet}** 🪙\n'}
        duel_canceled_title = {'en': 'Duel was canceled',
                               'ru': 'Дуэль была отменена'}
        opponent_reject_desc = {'en': '***{user}** declined duel invitation*',
                                'ru': '***{user}** отклонил приглашение на дуэль*'}
        no_money_for_bet_desc = {'en': "***{user}** is so poor that he didn't have enough money to bet*",
                                 'ru': '***{user}** настолько бедный, что ему не хватило денег на ставку*'}
        no_response_desc = {'en': "***{user}** did not come to the duel*",
                            'ru': '***{user}** не пришёл на дуэль*'}
        fight_is_starting_title = {'en': 'The duel will start in {time_to_start} s',
                                   'ru': 'Дуэль начнётся через {time_to_start} сек'}
        fight_is_starting_desc = {'en': '***{pig1}** is about to fight **{pig2}**. Who will win?*\n\n'
                                        '- *Here\'s what our experts think:*',
                                  'ru': '***{pig1}** собирается сразиться с **{pig2}**. Кто же победит?*\n\n'
                                        '- *Вот что думают наши эксперты:*'}
        fight_starting_field_value = {'en': '```Weight: {weight} kg\n'
                                            'Win chance: {chance} %```',
                                      'ru': '```Вес: {weight} кг\n'
                                            'Шанс на победу: {chance} %```'}
        fight_is_going_title = {'en': 'Duel is going...',
                                'ru': 'Идёт дуэль...'}
        fight_is_going_desc = {
            'en': "***{pig1}** and **{pig2}** fight each other brutally. It's not yet clear who will win*",
            'ru': '***{pig1}** и **{pig2}** брутально сражаются друг с другом. Ещё не ясно кто победит*'}
        fight_ended_title = {'en': 'Duel ended',
                             'ru': 'Дуэль окончена'}
        fight_ended_desc = {'en': '***{pig}** won the duel. Let\'s congratulate him*\n\n'
                                  '- *Its owner - **{user}** received **{money_earned}** 🪙*',
                            'ru': '***{pig}** выиграл дуэль. Давайте поздравим его*\n\n'
                                  '- *Его владелец - **{user}** получил **{money_earned}** 🪙*'}

    class Trade:
        scd_title = {'en': 'Successful trade',
                     'ru': 'Успешная торговля'}
        scd_desc = {'en': '*Trading between **{user1}** and **{user2}** was successful*',
                    'ru': '*Торговля между **{user1}** и **{user2}** прошла успешно*'}
        add_item_placeholder = {'en': 'Add item',
                                'ru': 'Добавить предмет'}
        cancel_title = {'en': 'Trade canceled',
                        'ru': 'Трэйд отменен'}
        cancel_desc = {'en': '***{user}** has canceled the trade*',
                       'ru': '*Пользователю **{user}** не понравилась сделка*'}
        trade_invitation_title = {'en': 'You have been invited to a trade',
                                  'ru': 'Вы были приглашены на торговлю'}
        trade_invitation_desc = {'en': '***{user}** invited you to trade*',
                                 'ru': '***{user}** пригласил вас, чтобы поторговаться*'}
        add_item_modal_title = {'en': 'Trade',
                                'ru': 'Трейд'}
        add_item_with_tax_modal_label = {'en': 'Add {item_name} (tax {tax}%)',
                                         'ru': 'Добавить {item_name} (налог {tax}%)'}
        add_item_modal_label = {'en': 'Add {item}',
                                'ru': 'Добавить {item}'}
        tax_splitting_process_title = {'en': 'Payment of taxes',
                                       'ru': 'Оплата налогов'}
        tax_splitting_process_desc = {'en': '*You need to pay some taxes in order to trade*',
                                      'ru': '*Вам нужно заплатить некоторое количество налогов, чтобы осуществить трейд*'}
        tax_splitting_process_who_pays_desc = {'en': '*You need to decide who will pay the tax*',
                                               'ru': '*Вам нужно решить, кто заплатит налог*'}
        split_equally = {'en': 'Split equally',
                            'ru': 'Пополам'}

    class SendMoney:
        scd_title = {'en': 'Transaction was successful',
                     'ru': 'Транзакция прошла успешно'}
        scd_desc = {'en': '***{money}** {currency_emoji} were sent to **{user}** account*',
                    'ru': '***{money}** {currency_emoji} были отправлены на счёт **{user}***'}
        cancel_title = {'en': 'Transaction was canceled',
                        'ru': 'Транзакция была отменена'}
        cancel_desc = {'en': "*You've decided against sending the money*",
                       'ru': '*Вы передумали отправлять свои деньги*'}
        event_title = {'en': 'You got some money',
                       'ru': 'Вам перевели деньги'}
        event_desc = {'en': '***{user}** has transferred **{money}** {currency_emoji} to your account*',
                      'ru': '***{user}** перевёл на ваш счёт **{money}** {currency_emoji}*'}
        confirm_desc = {'en': '*Are you sure you want to send **{money}** {currency_emoji} to **{user}**?*\n\n'
                              '- Tax is **{tax}** %\n'
                              '- **{money_with_tax}** {currency_emoji} will be charged from your account',
                        'ru': '*Вы точно хотите отправить **{money}** {currency_emoji} на счёт **{user}**?*\n\n'
                              '- Налог составляет **{tax}** %\n'
                              '- С вашего счёта снимут **{money_with_tax}** {currency_emoji}'}

    class Rename:
        scd_title = {'en': 'You renamed the pig',
                     'ru': 'Вы переименовали хряка'}
        scd_desc = {'en': '- *The new name of your pig: **{pig}***',
                    'ru': '- *Новое имя вашего хряка: **{pig}***'}

    class Profile:
        profile_title = {'en': 'Profile of {user}',
                         'ru': 'Профиль {user}'}
        user_profile_desc = {'en': '> Balance: **{coins}** 🪙 **{hollars}** 💵\n'
                                   '> Reputation: **{likes}** {rating_status} **|** {pos_amount} - {neg_amount}',
                             'ru': '> Баланс: **{coins}** 🪙 **{hollars}** 💵\n'
                                   '> Репутация: **{likes}** {rating_status} **|** {pos_amount} - {neg_amount}\n'}
        pig_profile_desc = {'en': '> Pig name: **{pig_name}**\n'
                                  '> Age: **{age}**\n'
                                  '> Weight: **{weight}** kg',
                            'ru': '> Имя хряка: **{pig_name}**\n'
                                  '> Возраст: **{age}**\n'
                                  '> Вес: **{weight}** кг'}
        family_profile_desc = {'en': '> Role: **{role}**',
                               'ru': '> Роль: **{role}**'}
        pig_field_title = {'en': 'Pig',
                           'ru': 'Свинтус'}
        pig_field_value = {'en': 'Pig name: **{pig_name}**\n'
                                 'Weight: **{weight}** kg',
                           'ru': 'Имя хряка: **{pig_name}**\n'
                                 'Вес: **{weight}** кг'}

    class View:
        title = {'en': 'Pig of {user}',
                 'ru': 'Хряк {user}'}

    class ProfileLike:
        scd_title = {'en': 'Liked',
                     'ru': 'Лайк поставлен'}
        scd_desc = {'en': "*You liked **{user}'s** profile*",
                    'ru': '*Вам понравился профиль **{user}***'}
        already_put_title = {'en': 'No no no',
                             'ru': 'Эй, нельзя'}
        already_put_desc = {'en': "*You can't like the same profile twice*",
                            'ru': '*Вы не можете поставить лайк 2 раза*'}

    class Top:
        best_of_the_bests = {'en': 'Best of the bests',
                             'ru': 'Лучшие из лучших'}
        also_not_bad = {'en': 'Also not bad',
                        'ru': 'Тоже неплохи'}
        weight_top_title = {'en': 'Weight top',
                            'ru': 'Топ по весу'}
        weight_top_desc = {'en': "*Featuring the world's heaviest pigs*",
                           'ru': '*Здесь у нас самые жирные Хряки в мире*'}
        coins_top_title = {'en': 'Money top',
                           'ru': 'Монетный топ'}
        coins_top_desc = {'en': '*Here we have the richest coin millionaires*',
                          'ru': '*Здесь у нас самые богатые монетные миллионеры*'}
        hollars_top_title = {'en': 'Dollar top',
                             'ru': 'Долларовый топ'}
        hollars_top_desc = {'en': '*Here we have the richest dollar millionaires*',
                            'ru': '*Здесь у нас самые богатые долларовые миллионеры*'}
        streak_top_title = {'en': 'Streak top',
                            'ru': 'Стриковый топ'}
        streak_top_desc = {'en': '*Here we have the hottest users*',
                           'ru': '*Здесь у нас самые горячие пользователи*'}
        your_position = {'en': '*Your current ranking: **{place}*** ',
                         'ru': '*Ваше место: **{place}***'}
        placeholder = {'en': 'View profile',
                       'ru': 'Посмотреть профиль'}

    class Buffs:
        main_page_title = {'en': 'Buffs',
                           'ru': 'Баффы'}
        main_page_desc = {'en': '*Buffs applied to your pig are shown here*',
                          'ru': '*Здесь показываются баффы, примененные к вашему Хряку*'}
        main_page_no_buffs_desc = {'en': '- *It seems you don\'t have any buffs applied*',
                                   'ru': '- *Кажется, у вас нету никаких примененных баффов*'}
        buff_expires_in = {'en': '  - *Expires <t:{expiration_timestamp}:R>*',
                           'ru': '  - *Истекает <t:{expiration_timestamp}:R>*'}
        weight_buffs_title = {'en': 'Weight gaining',
                              'ru': 'Массо-набор'}
        weight_buffs_desc = {'en': "*Your weight gain multipliers are shown here*",
                             'ru': '*Здесь показываются множители вашего весо-набирания*'}
        pooping_buffs_title = {'en': 'Manure quantity',
                               'ru': 'Количество навоза'}
        pooping_buffs_desc = {'en': "*This shows the multipliers for how much manure the pig will produce per feeding*",
                              'ru': '*Здесь показываются множители того, сколько Хряк будет производить навоза за 1 кормежку*'}
        vomit_chance_buffs_title = {'en': 'Chance of vomiting',
                                    'ru': 'Шанс тошноты'}
        vomit_chance_desc = {'en': "*Here you can see the chance that the pig will vomit while feeding*",
                             'ru': '*Здесь показываются шанс того что Хряка стошнит при кормежке*'}
        base_multiplier_value = {'en': "Base value: **{mult}%**",
                                 'ru': 'Базовое значение: **{mult}%**'}
        final_multiplier_value = {'en': "Final value: **{mult}%**",
                                  'ru': 'Финальное значение: **{mult}%**'}

    class Help:
        description = {'en-US': 'Get help for bot',
                       'ru': 'Хряковое пособие и обучение'}
        basic_help_title = {'en': 'Getting Started',
                            'ru': 'С чего начать?'}
        basic_help_desc = {
            'en': '*The main essence of the bot is feeding and clothing the pig*\n\n'
                  '1. To start playing, enter the command </feed:1118970976282095676>. Your pig will gain some weight, and you will also receive some manure in your inventory\n\n'
                  '2. To open the inventory, use </inventory:1107272196931461173>. In the inventory, you can sell and use your items\n'
                  '  - You can try to sell manure or open a case\n\n'
                  '3. Your balance and the weight of the pig will be displayed in </profile:1107272196931461171>\n\n'
                  '4. After earning money, you can spend it in </shop:1107272196931461175>\n'
                  '  - In the shop, you can buy various skins and boosts for the pig\n\n'
                  '5. To dress the pig, use </wardrobe:1107272196931461174>. Then select an item and press the **Wear** button\n\n'
                  f'> If you have additional questions, visit the [support server]({config.BOT_GUILDS[config.EN_BOT_GUILD_ID]['url']})',
            'ru': '*Основная суть бота в кормлении и одевании хряка*\n\n'
                  '1. Чтобы начать играть, введите команду </feed:1118970976282095676>. Ваш хряк наберёт несколько килограмм веса, а также вы получите немного навоза в ваш инвентарь\n\n'
                  '2. Чтобы открыть инвентарь, используйте </inventory:1107272196931461173>. В инвентаре можно продавать и использовать ваши предметы\n'
                  '  - Можете попробовать продать навоз либо открыть кейс\n\n'
                  '3. Ваш баланс и вес хряка будет отображаться в </profile:1107272196931461171>\n\n'
                  '4. После получения денег, вы можете потратить их в </shop:1107272196931461175>\n'
                  '  - В магазине вы сможете купить различные скины и бусты для хряка\n\n'
                  '5. Чтобы одеть хряка, используйте </wardrobe:1107272196931461174>. Затем выберите предмет и нажмите на кнопку **Надеть**\n\n'
                  f'> Если есть дополнительные вопросы, заходите на [сервер поддержки]({config.BOT_GUILDS[config.RU_BOT_GUILD_ID]['url']})'}

    class Say:
        not_allowed_title = {'en': 'Forbidden',
                             'ru': 'Нельзя'}
        not_allowed_desc = {
            'en': '*Command `/say` is currently disabled on this server. Ask the admin to enable it with `/settings say`*',
            'ru': '*Команда `/say` отключена на этом сервере. Попросите администрацию включить её при помощи `/settings say`*'}

    class SettingsSay:
        scd_content = {'en': '*Settings for the `/say` command have been changed and set to `{value}`*',
                    'ru': '*Настройки для команды `/say` изменены и выставлены на `{value}`*'}


    class SettingsTop:
        scd_content = {'en': '*Participation settings for the `/top` command have been changed and set to `{value}`*',
                    'ru': '*Настройки участия для команды `/top` изменены и выставлены на `{value}`*'}

    class Report:
        title = {
            'en': 'Report sent!',
            'ru': 'Ваш репорт был отправлен'}
        desc = {
            'en': "Thanks for contributing to the bot's development\n\n"
                  f"*Support server: {config.BOT_GUILDS[config.EN_BOT_GUILD_ID]['url']}*",
            'ru': 'Хряк доволен за твою помощь, спасибо\n\n'
                  f'*Сервер поддержки: {config.BOT_GUILDS[config.RU_BOT_GUILD_ID]['url']}*'}

    class ChooseLanguage:
        title = {'en': 'Choose language',
                 'ru': 'Сначала выбери язык'}
        desc = {'en': 'Select the language the bot will use',
                'ru': 'Выбери язык на котором бот будет хрюкать'}
        placeholder = {'en': 'Choose language',
                       'ru': 'Выберите язык'}

    class SetLanguage:
        scd_title = {
            'en': 'New bot language: **English**',
            'ru': 'Новый язык бота: **Русский**'
        }
        scd_desc = {
            'en': 'Now the bot will speak the language of freedom 🦅🦅',
            'ru': 'Теперь бот будет говорить на великом и могучем 💪'
        }

    class PromoCode:
        promo_code_used_error_title = {'en': 'You have already used this promo code',
                                       'ru': 'Вы уже использовали этот промо код'}
        promo_code_used_error_desc = {
            'en': "*Trying to be clever? Promo codes can't be used more than once*",
            'ru': '*Самый умный? Нельзя использовать один и тот же промо код несколько раз*'}
        promocode_not_exist_title = {'en': 'Invalid promo code',
                                     'ru': 'Недействительный промо код'}
        promocode_not_exist_desc = {
            'en': '*The entered promo code does not exist*',
            'ru': '*Такого промо кода не существует*'}
        cant_use_promocode_title = {'en': 'Invalid promo code',
                                    'ru': 'Невозможно использовать промокод'}
        cant_use_promocode_desc = {
            'en': "*For some reason you can't use this promo code*",
            'ru': '*По какой-то причине вы не можете использовать этот промокод*'}
        promocode_expired_title = {'en': 'Promo code has expired',
                                   'ru': 'Промо код истёк'}
        promocode_expired_desc = {
            'en': "*The promo code has expired and is therefore no longer valid.*",
            'ru': '*Срок годности промокода истёк, поэтому он больше не рабочий*'}
        promocode_used_too_many_times_title = {'en': 'Invalid promo code',
                                               'ru': 'Промо код использован'}
        promocode_used_too_many_times_desc = {
            'en': 'This promo code has already been used and is therefore no longer valid.',
            'ru': 'Этот промо код уже использовали, поэтому он больше недействителен'}
        promo_code_used_title = {'en': 'Promo code used',
                                 'ru': 'Промо код активирован'}
        you_got_desc = {'en': 'You got:',
                        'ru': 'Вы получили:'}

    class PoopEaten:
        not_enough_money_for_doctor_title = {'en': 'Not enough money',
                                             'ru': 'Недостаточно средств'}
        not_enough_money_for_doctor_desc = {'en': "You don't have enough money to pay the doctor\n\n"
                                                  '- *Doctor takes pity on a beggar like you and just walks away*',
                                            'ru': 'У вас не хватает денег, чтобы заплатить доктору\n\n'
                                                  '- *Доктор жалеет такого нищего как вы и просто уходит*'}
        ran_away_and_not_payed_title = {'en': 'You ran away',
                                        'ru': 'Вы сбежали'}
        ran_away_and_not_payed_desc = {'en': "*You managed to escape. It looks like no one is following you*",
                                       'ru': '*Вы смогли сбежать. Кажется никого позади нету*'}
        payed_to_doctor_title = {'en': 'You paid the doctor',
                                 'ru': 'Вы заплатили доктору'}
        payed_to_doctor_desc = {'en': '*The doctor took the money and left*',
                                'ru': '*Доктор взял деньги и уехал*'}

    class RateBot:
        title = {'en': 'Hey, do you like the bot?',
                 'ru': 'Эй, нравится бот?'}
        desc = {'en': 'If so, feel free to rate it on our website',
                'ru': 'Если да, то можешь оценить его на сайте'}
        later_btn = {'en': 'Later',
                     'ru': 'Позже'}
        support_btn = {'en': 'Support',
                       'ru': 'Оценить'}

    class Pagination:
        page = {'en': 'Page',
                'ru': 'Страница'}
        next = {'en': 'Next',
                'ru': 'Следующая'}
        previous = {'en': 'Previous',
                    'ru': 'Предыдущая'}
        select_category = {'en': 'Select category',
                            'ru': 'Выберите категорию'}
        wrong_user_title = {'en': 'Hey, it\'s not your message',
                            'ru': 'Эй, это не твоё сообщение'}
        wrong_user_desc = {'en': "*You cannot simply flip through other people's pages*",
                           'ru': '*Ты не можешь просто взять и листать чужие страницы*'}

    class Global:
        balance = {'en': 'Balance',
                   'ru': 'Баланс'}
        page = {'en': 'Page',
                'ru': 'Страница'}
        shop = {'en': 'Shop',
                'ru': 'Магазин'}
        money = {'en': 'Money',
                 'ru': 'Деньги'}
        clear = {'en': 'Clear',
                 'ru': 'Очистить'}
        inventory = {'en': 'Inventory',
                     'ru': 'Инвентарь'}
        wardrobe = {'en': 'Wardrobe',
                    'ru': 'Гардероб'}
        no_items = {'en': 'No items',
                    'ru': 'Нету предметов'}
        successfully = {'en': 'Successfully',
                        'ru': 'Успешно'}
        trade = {'en': 'Trade',
                 'ru': 'Торговля'}
        like = {'en': 'Like',
                'ru': 'Нравится'}
        kick = {'en': 'Kick',
                'ru': 'Выгнать'}
        ban = {'en': 'Ban',
               'ru': 'Бан'}
        date = {'en': 'Date',
                'ru': 'Дата'}
        requests = {'en': 'Requests',
                    'ru': 'Запросы'}
        sent = {'en': 'Sent',
                'ru': 'Отправлено'}
        are_you_sure = {'en': 'Are you sure?',
                        'ru': 'Вы уверены?'}
        cost = {'en': 'Cost',
                'ru': 'Цена'}
        cost_per_item = {'en': 'Price/pc',
                         'ru': 'Цена/шт'}
        price = {'en': 'Price',
                 'ru': 'Стоимость'}
        type = {'en': 'Type',
                'ru': 'Тип'}
        amount = {'en': 'Amount',
                  'ru': 'Количество'}
        description = {'en': 'Description',
                       'ru': 'Описание'}
        resource = {'en': 'Resource',
                    'ru': 'Ресурс'}
        head_owner = {'en': 'Owner',
                      'ru': 'Глава'}
        use = {'en': 'Use',
               'ru': 'Использовать'}
        sell = {'en': 'Sell',
                'ru': 'Продать'}
        run_away = {'en': 'Run away',
                    'ru': 'Сбежать'}
        kg = {'en': 'kg',
              'ru': 'кг'}
        pay = {'en': 'Pay',
               'ru': 'Заплатить'}
        preview = {'en': 'Preview',
                   'ru': 'Предосмотр'}
        wear = {'en': 'Wear',
                'ru': 'Надеть'}
        remove_cloth = {'en': 'Remove',
                        'ru': 'Снять'}
        rarity = {'en': 'Rarity',
                  'ru': 'Редкость'}
        accept = {'en': 'Accept',
                  'ru': 'Принять'}
        reject = {'en': 'Reject',
                  'ru': 'Отклонить'}
        buy = {'en': 'Buy',
               'ru': 'Купить'}
        reason = {'en': 'Reason',
                  'ru': 'Причина'}
        created = {'en': 'Created',
                   'ru': 'Создан'}
        owner = {'en': 'Owner',
                 'ru': 'Владелец'}
        icon = {'en': 'Icon',
                'ru': 'Аватарка'}
        nicknames = {'en': 'Nicknames',
                     'ru': 'Никнеймы'}
        no_icon = {'en': 'No Icon',
                   'ru': 'Без Аватарки'}
        need = {'en': 'Need',
                'ru': 'Нужно'}
        channels = {'en': 'Channels',
                    'ru': 'Каналы'}
        total = {'en': 'Total',
                 'ru': 'Всего'}
        open = {'en': 'Open',
                'ru': 'Открыть'}
        category = {'en': 'Category',
                    'ru': 'Категорий'}
        text = {'en': 'Text',
                'ru': 'Текстовых'}
        voice = {'en': 'Voice',
                 'ru': 'Голосовых'}
        forum = {'en': 'Forum',
                 'ru': 'Форум'}
        stage = {'en': 'Stage',
                 'ru': 'Трибуны'}
        members = {'en': 'Members',
                   'ru': 'Участники'}
        users = {'en': 'Users',
                 'ru': 'Людей'}
        bots = {'en': 'Bots',
                'ru': 'Ботов'}
        bot_roles = {'en': 'Bot roles',
                     'ru': 'Ролей ботов'}
        premium = {'en': 'Premium',
                   'ru': 'Премиум'}
        role = {'en': 'Role',
                'ru': 'Роль'}
        roles = {'en': 'Roles',
                 'ru': 'Роли'}
        bans = {'en': 'Bans',
                'ru': 'Баны'}
        messages = {'en': 'Messages',
                    'ru': 'Сообщения'}
        invites = {'en': 'Invites',
                   'ru': 'Приглашения'}
        expires = {'en': 'Expires',
                   'ru': 'Истекает'}
        animated = {'en': 'Animated',
                    'ru': 'Анимированых'}
        stickers = {'en': 'Stickers',
                    'ru': 'Стикеров'}
        no_emojis = {'en': 'No emojis',
                     'ru': 'Нету эмодзи'}
        emojis = {'en': 'Emojis',
                  'ru': 'Эмодзи'}
        system_channel = {'en': 'System channel',
                          'ru': 'Системный канал'}
        join_messages = {'en': 'Join messages',
                         'ru': 'Нач. сообщения'}
        join_replies = {'en': 'Join replies',
                        'ru': 'Ответы'}
        boost_messages = {'en': 'Boost messages',
                          'ru': 'Буст уведомления'}
        reminder = {'en': 'Reminder',
                    'ru': 'Напоминания'}
        limits = {'en': 'Limits',
                  'ru': 'Лимиты'}
        emojis_limit = {'en': 'Emojis limit',
                        'ru': 'Лимит эмодзи'}
        stickers_limit = {'en': 'Stickers limit',
                          'ru': 'Лимит стикеров'}
        bitrate_limit = {'en': 'Bitrate limit',
                         'ru': 'Лимит битрейта'}
        files_limit = {'en': 'Files limit',
                       'ru': 'Лимит файлов'}
        safety = {'en': 'Safety',
                  'ru': 'Безопасность'}
        mfa = {'en': 'MFA',
               'ru': 'MFA'}
        attempt = {'en': 'Attempt',
                   'ru': 'Попытка'}
        verification = {'en': 'Verification',
                        'ru': 'Верификация'}
        nsfw_level = {'en': 'NSFW level',
                      'ru': 'Уровень NSFW'}
        content_filter = {'en': 'Content filter',
                          'ru': 'Фильтр контента'}
        default_notifications = {'en': 'Default notifications',
                                 'ru': 'Уведомления по умолчанию'}
        other = {'en': 'Other',
                 'ru': 'Другое'}
        yes = {'en': 'Yes',
               'ru': 'Да'}
        no = {'en': 'No',
              'ru': 'Нет'}
        true_yes_command = {'en': '✅ True',
                            'ru': '✅ Да'}
        false_no_command = {'en': '❌ False',
                            'ru': '❌ Нет'}
        total_bans = {'en': 'Total Bans',
                      'ru': 'Всего банов'}
        total_invites = {'en': 'Total Invites',
                         'ru': 'Всего приглашений'}
        locale = {'en': 'Locale',
                  'ru': 'Язык'}
        rules = {'en': 'Rules',
                 'ru': 'Правила'}
        community = {'en': 'Community',
                     'ru': 'Комьюнити'}
        click = {'en': 'Click',
                 'ru': 'Нажми'}
        joined = {'en': 'Joined',
                  'ru': 'Присоединился'}
        name_ = {'en': 'Name',
                 'ru': 'Имя'}
        status = {'en': 'Status',
                  'ru': 'Статус'}
        play = {'en': 'Playing',
                'ru': 'Играет в'}
        stream = {'en': 'Streaming',
                  'ru': 'Стримит'}
        listen = {'en': 'Listening',
                  'ru': 'Слушает'}
        watching = {'en': 'Watching',
                    'ru': 'Смотрит'}
        competing = {'en': 'Competing in',
                     'ru': 'Соревнуется в'}
        never = {'en': 'Never',
                 'ru': 'Никогда'}
        total_members = {'en': 'Total members',
                         'ru': 'Всего участников'}
        position = {'en': 'Position',
                    'ru': 'Позиция'}
        last_update = {'en': 'Last update',
                       'ru': 'Последнее обновление'}
        uses = {'en': 'Uses',
                'ru': 'Использований'}
        cook = {'en': 'Cook',
                'ru': 'Приготовить'}
        total_roles = {'en': 'Total roles',
                       'ru': 'Всего ролей'}
        total_channels = {'en': 'Total channels',
                          'ru': 'Всего каналов'}
        template_info = {'en': 'Template info',
                         'ru': 'О шаблоне'}
        source_guild_id = {'en': 'Source server ID',
                           'ru': 'ID исходного сервера'}
        creator_id = {'en': 'Creator ID',
                      'ru': 'ID создателя'}
        your_number = {'en': 'Your number',
                       'ru': 'Ваше число'}
        numbers = {'en': 'Numbers',
                   'ru': 'Числа'}
        color = {'en': 'Color',
                 'ru': 'Цвет'}
        weight = {'en': 'Weight',
                  'ru': 'Вес'}
        template = {'en': 'Template',
                    'ru': 'Шаблон'}
        templates = {'en': 'Templates',
                     'ru': 'Шаблоны'}
        creator = {'en': 'Creator',
                   'ru': 'Создатель'}
        kilograms_short = {'en': 'kg',
                           'ru': 'кг'}
        options = {'en': 'Options',
                   'ru': 'Настройки'}
        mentionable = {'en': 'Mentionable',
                       'ru': 'Упоминаимая'}
        hoist = {'en': 'Hoist',
                 'ru': 'Отдельная'}
        integration = {'en': 'Integration',
                       'ru': 'Интеграция'}
        refresh = {'en': 'Refresh',
                   'ru': 'Обновить'}
        reload = {'en': 'Reload',
                  'ru': 'Перезагрузить'}
        links = {'en': 'Links',
                 'ru': 'Ссылки'}
        title = {'en': 'Title',
                 'ru': 'Заголовок'}
        footer = {'en': 'Footer',
                  'ru': 'Нижний текст'}
        image_url = {'en': 'Image URL',
                     'ru': 'Ссылка на картинку'}
        thumbnail_url = {'en': 'Thumbnail URL',
                         'ru': 'Ссылка на маленькую картинку'}
        stats = {'en': 'Stats',
                 'ru': 'Статистика'}
        all_skins = {'en': 'All skins',
                     'ru': 'Все скины'}
        all_items = {'en': 'All items',
                     'ru': 'Все вещи'}
        everything = {'en': 'Everything',
                      'ru': 'Показать всё'}
        got_it_btn = {'en': 'Got it',
                      'ru': 'Хорошо'}
        choose_category = {'en': 'Select category',
                           'ru': 'Выберите категорию'}
        none = {'en': 'No',
                'ru': 'Нету'}
        message = {'en': 'Message',
                   'ru': 'Сообщение'}
        you_have_amount = {'en': 'You have: {max_amount}',
                           'ru': 'У вас есть: {max_amount}'}

    class ErrorCallbacks:
        pig_feed_cooldown_title = {'en': 'Your pig is not yet hungry',
                                   'ru': 'Ваш хряк ещё не голоден'}
        pig_feed_cooldown_desc = {'en': '***{pig}** will be hungry again **<t:{timestamp}:R>***',
                                  'ru': '***{pig}** проголодается **<t:{timestamp}:R>***'}
        pig_butcher_cooldown_title = {'en': 'You are so cruel',
                                      'ru': 'Вы слишком жестокие'}
        pig_butcher_cooldown_desc = {'en': "You can't butcher **{pig}** so often\n\n"
                                           "Try again **<t:{timestamp}:R>**",
                                     'ru': 'Вы не можете так часто снимать сало с **{pig}**\n\n'
                                           '*Попробуйте ещё раз **<t:{timestamp}:R>***'}
        pig_breed_cooldown_title = {'en': 'Calm down',
                                    'ru': 'Успокойся'}
        pig_breed_cooldown_desc = {'en': "**{pig}** is too tired and can't have kids\n"
                                         "Try again **<t:{timestamp}:R>**",
                                   'ru': '**{pig}** слишком устал и не может заводить детей\n\n'
                                         '*Попробуйте ещё раз **<t:{timestamp}:R>***'}
        shop_buy_cooldown_title = {'en': 'Product is out of stock',
                                   'ru': 'Товар закончился'}
        shop_buy_cooldown_desc = {'en': "**{item}** is out of stock\n\n"
                                        "*New product will arrive **<t:{timestamp}:R>***",
                                  'ru': '**{item}** закончился и его больше нету на складе\n\n'
                                        '*Новый товар привезут **<t:{timestamp}:R>***'}
        wrong_component_clicked_title = {'en': "It's not your message",
                                         'ru': 'Это не ваше сообщение'}
        wrong_component_clicked_desc = {'en': "*You can't push tie people's buttons*",
                                        'ru': '*Ты не можешь нажимать на чужие кнопки*'}
        skin_not_compatible_title = {'en': "Can't be worn",
                                     'ru': 'Нельзя надеть'}
        skin_not_compatible_desc = {
            'en': '***{skin1}** conflicts with **{skin2}**\n\n> Remove **{skin2}** to put on **{skin1}***',
            'ru': '***{skin1}** конфликтует с **{skin2}**\n\n> Снимите **{skin2}**, чтобы надеть **{skin1}***'}
        not_enough_money_title = {'en': 'Not enough money',
                                  'ru': 'Недостаточно денег'}
        not_enough_money_desc = {'en': "*You don't have enough money to do this*",
                                 'ru': '*У вас не достаточно денег, чтобы сделать это*'}
        item_is_not_in_shop_title = {'en': 'No item',
                                     'ru': 'Нету предмета'}
        item_is_not_in_shop_desc = {'en': '*This item is not in the shop. Try updating the command*',
                                    'ru': '*Этого предмета нету в магазине. Попробуйте обновить команду*'}
        no_item_title = {'en': "You don't have a {item}",
                         'ru': 'У вас нету предмета "{item}"'}
        no_item_desc = {'en': "*Unfortunately, you couldn't find this item in your storage*",
                        'ru': '*К сожалению, вы не смогли найти этот предмет у себя в хранилище*'}
        not_enough_item_title = {'en': "Not enough items",
                                 'ru': 'У вас не хватает предметов'}
        not_enough_item_desc = {'en': "*Unfortunately, you couldn't find enough amount in your storage:*\n\n"
                                      "> {item_emoji}・{item}",
                                'ru': '*К сожалению, вы не смогли найти нужное количество у себя в хранилище:*\n\n'
                                      '> {item_emoji}・{item}'}
        user_not_enough_item_title = {'en': "Not enough items",
                                      'ru': 'Не хватает предметов'}
        user_not_enough_item_desc = {'en': "*Unfortunately, **{user}** couldn't find enough amount in his storage*\n\n"
                                           "> {item_emoji}・{item}",
                                     'ru': '*К сожалению, **{user}** не смог найти нужное количество у себя в хранилище:*\n\n'
                                           '> {item_emoji}・{item}'}
        not_allowed_to_use_command_title = {'en': "You are not allowed to use this command",
                                            'ru': 'Вам не разрешено использовать эту команду'}
        not_allowed_to_use_command_desc = {'en': "*You need special permission to use the command*",
                                           'ru': '*Вам нужно специальное разрешение, чтобы использовать команду*'}
        nsfw_required_title = {'en': "You are not allowed to use this command",
                               'ru': 'Это NSFW команда'}
        nsfw_required_desc = {'en': "*You need to be in an NSFW channel to use the command*",
                              'ru': '*Вам нужно находится в NSFW канале, чтобы использовать команду*'}
        no_private_message_title = {'en': "Servers only",
                                    'ru': 'Только для серверов'}
        no_private_message_desc = {'en': "*You need to be on the server to use the command*",
                                   'ru': '*Вам нужно находится на сервере, чтобы использовать команду*'}
        not_owner_desc = {'en': "*Only the bot owner can use this command*",
                          'ru': '*Только владелец бота может использовать эту команду*'}
        bot_as_opponent_duel_title = {'en': "Are you playing against a bot?",
                                      'ru': 'Ты против бота играешь?'}
        bot_as_opponent_duel_desc = {
            'en': "*I'll tell you a secret, bots don't know how to participate in duels. They can't even press a button.*",
            'ru': '*Расскажу секрет, боты не умеют участвовать в дуэлях. Они даже на кнопку нажать не могут*'}
        bot_as_partner_breed_title = {'en': "Going to have kids with a bot?",
                                      'ru': 'Собрался завести детей с ботом?'}
        bot_as_partner_breed_desc = {
            'en': "*The future is not close enough for you to breed with robots*",
            'ru': '*Будущее не настолько близко, чтобы вы могли заводить потомство с роботами*'}
        cant_play_with_yourself_duel_title = {'en': "Going to play by yourself?",
                                              'ru': 'Собрался играть сам с собой?'}
        cant_play_with_yourself_duel_desc = {'en': "*I thought users wouldn't choose themselves as opponents. "
                                                   "I think I was wrong*",
                                             'ru': '*Я думал что пользователи не станут выбирать самого себя в качестве соперника. '
                                                   'Кажется, я ошибался*'}
        cant_breed_with_yourself_title = {'en': "Hey hey hey",
                                          'ru': 'Воу воу воу'}
        cant_breed_with_yourself_desc = {
            'en': "*I understand that you love yourself so much that you chose yourself as a partner, but unfortunately you can’t*",
            'ru': '*Я понимаю что вы любите себя настолько сильно что выбрали себя в качестве партнёра, но так к сожалению нельзя*'}
        cant_trade_with_yourself_title = {'en': "You can't trade with yourself",
                                          'ru': 'Нельзя торговать с собой'}
        cant_trade_with_yourself_desc = {
            'en': "*What are you going to inject yourself? Like \"Hey Me, let me sell you 10 coins for 10 coins\"?*",
            'ru': '*Что ты себе впаривать собрался? Типо "Эй Я, давай я тебе продам 10 монет за 10 монет"?*'}
        bot_as_trade_user_title = {'en': "Can't trade with a bot",
                                   'ru': 'Нельзя торговать с ботом'}
        bot_as_trade_user_desc = {
            'en': "Hey, seriously. I'm already tired of reminding users that they can't interact with bots",
            'ru': '*Эй, ну серьезно. Мне уже надоело напоминать пользователям что они не могут взаимодействовать с ботами*'}
        cooldown_title = {'en': "Cooldown",
                          'ru': 'Притормози'}
        cooldown_desc = {'en': 'You use the command too often\n\n'
                               '- *Try again **<t:{timestamp}:R>***',
                         'ru': 'Ты слишком часто используешь команду\n\n'
                               '- *Попробуй ещё раз **<t:{timestamp}:R>***'}
        no_mangal_to_cook = {'en': '*How are you going to roast the meat? Buy a grill!*',
                             'ru': '*Как ты собираешься жарить мясо? Купи мангал!*'}
        user_in_black_list_title = {'en': "You are in black list",
                                    'ru': 'Вы в чёрном списке'}
        user_in_black_list_desc = {'en': "*You are blacklisted by the bot, so you cannot use it*",
                                   'ru': '*Вы находитесь в чёрном списке бота, поэтому не можете использовать его.\n\n'
                                         f'- Если вы считаете что это ошибка, то заходите на [сервер поддержки]({config.BOT_GUILDS[config.RU_BOT_GUILD_ID]['url']})*'}
        unknown_error_title = {'en': "Unknown error",
                               'ru': 'Неизвестная ошибка'}
        unknown_error_desc = {
            'en': "*Oops, something seems to have gone wrong. You can report it via the </report:1106680848167739493> command*",
            'ru': '*Упс, кажется что-то пошло не так. Вы можете сообщить об этом через команду </report:1106680848167739493>*'}
        bot_missing_perms_title = {'en': "The bot doesn't have enough permissions",
                                   'ru': 'У хряка не достаточно прав'}
        bot_missing_perms_desc = {'en': "*Give the bot the following permissions:*",
                                  'ru': '*Выдайте боту следующие права:*'}
        user_missing_perms_title = {'en': "You have no rights",
                                    'ru': 'У вас нет прав'}
        user_missing_perms_desc = {'en': "*You don't have the following permissions:*",
                                   'ru': '*У вас не хватает следующих прав:*'}
        forbidden_title = {'en': "Forbidden",
                           'ru': 'Что-то пошло не так'}
        forbidden_desc = {
            'en': "This probably happened because the bot did not have enough permissions. Double-check whether the Hryak has all the necessary permissions",
            'ru': '*Вероятно это случилось потому-что у бота не достаточно прав. Перепроверьте есть ли у Хряка все нужные права*'}
        modal_input_is_not_number_title = {'en': 'Invalid input',
                                           'ru': 'Неверный ввод'}
        modal_input_is_not_number_desc = {
            'en': "*What you entered does not look like a number, but it would be better a number*",
            'ru': '*То что ты ввёл не похоже на число, а лучше бы это было числом*'}
        bot_is_restarting_title = {'en': 'Bot is restarting',
                                   'ru': 'Бот перезагружается'}
        bot_is_restarting_desc = {
            'en': "*The bot is currently restarting, some functions may not work*",
            'ru': '*В данный момент бот перезагружается, некоторые функции могут не работать*'}
        cannot_use_command_in_this_channel_title = {'en': 'The command is not available',
                                                    'ru': 'Команда не доступна'}
        cannot_use_command_in_this_channel_desc = {
            'en': "*This command cannot be used in this channel*",
            'ru': '*Эту команду нельзя использовать в этом канале*'}

    Permissions = {'add_reactions': {'en': 'Add reactions', 'ru': 'Добавлять реакции'},
                   'administrator': {'en': 'Administrator', 'ru': 'Администратор'},
                   'attach_files': {'en': 'Attach files', 'ru': 'Прикреплять файлы'},
                   'ban_members': {'en': 'Ban members', 'ru': 'Банить'},
                   'change_nickname': {'en': 'Change nickname', 'ru': 'Изменять имя'},
                   'connect': {'en': 'Connect', 'ru': 'Подключатся'},
                   'create_forum_threads': {'en': 'Create forum threads', 'ru': 'Создавать ветки на форуме'},
                   'create_instant_invite': {'en': 'Create instant invite', 'ru': 'Создавать приглашение'},
                   'create_private_threads': {'en': 'Create private threads', 'ru': 'Создавать приватные ветки'},
                   'create_public_threads': {'en': 'Create public threads', 'ru': 'Создавать публичные ветки'},
                   'deafen_members': {'en': 'Deafen members', 'ru': 'Отключать звук'},
                   'embed_links': {'en': 'Embed links', 'ru': 'Вставить ссылки'},
                   'external_emojis': {'en': 'External emojis', 'ru': 'Внешние эмодзи'},
                   'external_stickers': {'en': 'External stickers', 'ru': 'Внешние стикеры'},
                   'kick_members': {'en': 'Kick members', 'ru': 'Исключать участников'},
                   'manage_channels': {'en': 'Manage channels', 'ru': 'Управлять каналами'},
                   'manage_emojis': {'en': 'Manage emojis', 'ru': 'Управлять эмодзи'},
                   'manage_emojis_and_stickers': {'en': 'Manage emojis and stickers',
                                                  'ru': 'Управлять смайликами и стикерами'},
                   'manage_events': {'en': 'Manage events', 'ru': 'Управлять событиями'},
                   'manage_guild': {'en': 'Manage guild', 'ru': 'Управлять сервером'},
                   'manage_messages': {'en': 'Manage messages', 'ru': 'Управлять сообщениями'},
                   'manage_nicknames': {'en': 'Manage nicknames', 'ru': 'Управлять именами'},
                   'manage_permissions': {'en': 'Manage permissions', 'ru': 'Управлять правами'},
                   'manage_roles': {'en': 'Manage roles', 'ru': 'Управлять ролями'},
                   'manage_threads': {'en': 'Manage threads', 'ru': 'Управлять ветками'},
                   'manage_webhooks': {'en': 'Manage webhooks', 'ru': 'Управлять вэб-хуками'},
                   'mention_everyone': {'en': 'Mention everyone', 'ru': 'Упоминать everyone'},
                   'moderate_members': {'en': 'Moderate members', 'ru': 'Управлять учатниками'},
                   'move_members': {'en': 'Move members', 'ru': 'Перемещать участников'},
                   'mute_members': {'en': 'Mute members', 'ru': 'Заглушать участников'},
                   'priority_speaker': {'en': 'Priority speaker', 'ru': 'Приоритетный режим'},
                   'read_message_history': {'en': 'Read message history', 'ru': 'Читать историю сообщений'},
                   'read_messages': {'en': 'Read messages', 'ru': 'Читать сообщения'},
                   'request_to_speak': {'en': 'Request to speak', 'ru': 'Попросить выступить'},
                   'send_messages': {'en': 'Send messages', 'ru': 'Отправлять сообщения'},
                   'send_messages_in_threads': {'en': 'Send messages in threads',
                                                'ru': 'Отправлять сообщения в ветки'},
                   'send_tts_messages': {'en': 'Send tts messages', 'ru': 'Отправлять tts сообщения'},
                   'speak': {'en': 'Speak', 'ru': 'Говорить'},
                   'start_embedded_activities': {'en': 'Start embedded activities',
                                                 'ru': 'Начинать встроенные действия'},
                   'stream': {'en': 'Stream', 'ru': 'Стримить'},
                   'use_application_commands': {'en': 'Use application commands', 'ru': 'Использовать команды'},
                   'use_embedded_activities': {'en': 'Use embedded activities',
                                               'ru': 'Использовать встроенные активности'},
                   'use_external_emojis': {'en': 'Use external emojis', 'ru': 'Использовать внешние смайлики'},
                   'use_external_stickers': {'en': 'Use external stickers', 'ru': 'Использовать внешние стикеры'},
                   'use_slash_commands': {'en': 'Use slash commands', 'ru': 'Использовать слэш-команды'},
                   'use_voice_activation': {'en': 'Use voice activation', 'ru': 'Использовать режим рации'},
                   'view_audit_log': {'en': 'View audit log', 'ru': 'Просмотр журнала аудита'},
                   'view_channel': {'en': 'View channel', 'ru': 'Просмотр канала'},
                   'view_guild_insights': {'en': 'View guild insights', 'ru': 'Просмотр статистики сервера'}}

    # _____________________________________________________________________________________

    class Inventory:
        inventory_title = {'en': 'Inventory',
                           'ru': 'Инвентарь'}
        inventory_empty_desc = {'en': '*Your inventory is empty*',
                                'ru': '*Ваш инвентарь пуст*'}
        select_item_placeholder = {'en': 'Choose item',
                                   'ru': 'Выберите предмет'}

    class InventoryItemSellModal:
        label = {'en': 'Number of items you want to sell',
                 'ru': 'Количество предметов для продажи'}
        placeholder = {'en': 'You have: {max_amount}',
                       'ru': 'У вас есть: {max_amount}'}
        title = {'en': 'Item selling',
                 'ru': 'Продажа'}

    class InventoryItemSold:
        title = {'en': 'Item sold',
                 'ru': 'Предмет продан'}
        desc = {'en': "*You sold **{item} x{amount}** and received **{money}** 🪙*",
                'ru': '*Вы продали **{item} x{amount}** и получили **{money}** 🪙*'}

    class InventoryItemCookModal:
        label = {'en': 'Amount of items to cook',
                 'ru': 'Количество предметов для готовки'}
        placeholder = {'en': 'You have: {max_amount}',
                       'ru': 'У вас есть: {max_amount}'}
        title = {'en': 'Cooking',
                 'ru': 'Готовка'}

    class InventoryItemCooked:
        title = {'en': 'Item cooked',
                 'ru': 'Предмет приготовлен'}
        desc = {'en': '*You cooked **{item} x{amount}***',
                'ru': '*Вы приготовили **{item} x{amount}***'}

    class ItemUsed:
        ate_poop_and_poisoned_title = {'en': 'You ate poop',
                                       'ru': 'Вы сьели какаху'}
        ate_poop_and_poisoned_desc = {
            'en': 'You ate poop. You liked its taste, but unfortunately you got poisoned\n\n'
                  '*- A doctor came to you and cured you, but now he asks 5 🪙 for treatment*',
            'ru': 'Вы сьели какашку. Вам понравился её вкус, но к сожалению вы отравились\n\n'
                  '*- К вам пришёл доктор и вылечил вас, но теперь он просит 5 🪙 за лечение*'}
        ate_poop_and_dizzy_title = {'en': 'You ate poop',
                                    'ru': 'Вы сьели какаху'}
        ate_poop_and_dizzy_desc = {
            'en': '*> You ate poop. You felt dizzy and almost fell, but overall everything was fine*',
            'ru': '*> Вы сьели какашку. У вас закрутилась голова и вы чуть не упали, но в целом всё хорошо*'}
        ate_poop_and_question_title = {'en': 'You ate poop',
                                       'ru': 'Вы сьели какаху'}
        ate_poop_and_question_desc = {
            'en': '*> Out of your curiosity, you ate poop. There is only one question left, why?*',
            'ru': '*> Из своего любопытства вы сьели какаху. Остается лишь один вопрос, зачем?*'}
        ate_poop_and_dad_title = {'en': 'You ate poop',
                                  'ru': 'Вы сьели какаху'}
        ate_poop_and_dad_desc = {
            'en': '*> After the meal, you went outside to breathe some fresh air where you saw your father. He turned around silently and left*',
            'ru': '*> После трапезы, вы вышли подышать свежим воздухом где увидели своего отца. Он молча развернулся и ушел*'}
        laxative_title = {'en': 'You used laxative',
                          'ru': 'Вы использовали слабительное'}
        laxative_desc = {
            'en': '**{pig}** will produce more manure on the next **{step}** feedings',
            'ru': '**{pig}** будет давать больше навоза следующие **{step}** кормёжек'}
        case_title = {'en': 'You got:',
                      'ru': 'Вы получили:'}

    class Wardrobe:
        wardrobe_title = {'en': 'Wardrobe',
                          'ru': 'Гардероб'}
        wardrobe_empty_desc = {'en': '*Your wardrobe is empty*',
                               'ru': '*Ваш гардероб пуст*'}
        select_item_placeholder = {'en': 'Choose item',
                                   'ru': 'Выберите предмет'}

    class WardrobeItemChooseLayerToWear:
        title = {'en': 'Choose parts to wear',
                 'ru': 'Выберите части для надевания'}
        desc = {'en': 'This skin can be worn in parts. Choose the pieces you wish to equip',
                'ru': 'Вы можете надеть этот скин частично. Выберите части, которые хотите надеть'}
        wear_all_option = {'en': 'Wear all',
                           'ru': 'Надеть всё'}

    class WardrobeItemWear:
        title = {'en': 'You put on {item}',
                 'ru': 'Вы надели {item}'}
        desc_list = {'en': ['*This **{item}** looks fantastic on you!*'],
                     'ru': ['*Этот **{item}** вам очень идёт!*']}

    class WardrobeItemRemove:
        title = {'en': 'You removed {item}',
                 'ru': 'Вы сняли {item}'}
        desc = {'en': "*Now you don't wear **{item}***",
                'ru': '*Теперь вы не носите **{item}***'}

    class WardrobeItemPreview:
        title = {'en': 'Preview mode',
                 'ru': 'Режим предосмотра'}
        desc = {'en': "*Imagine wearing **{item}** - this is how it would look*",
                'ru': '*Вот как будет выглядеть **{item}**, если вы его наденете*'}

    class Shop:
        shop_empty_desc = {'en': '*Shop is empty now*',
                           'ru': '*Магазин сейчас пустой*'}
        main_page_title = {'en': 'Магазин',
                           'ru': 'Shop'}
        main_page_desc = {'en': '*Welcome to the store, where you can purchase anything at any time*\n\n'
                                '**Choose one of the categories below:**',
                          'ru': '*Добро пожаловать в магазин. Тут вы можете купить что угодно и когда угодно*\n\n'
                                '**Выберите одну из категорий ниже:**'}
        buy_hollars_description = {'en': '💵 | *You can buy **Hryak-Dollars** **[here](https://boosty.to/brevnoo.en)***',
                                   'ru': '💵 | *Вы можете покупать **Хряк-Доллары** **[на этом сайте](https://boosty.to/brevnoo)***'}
        titles = {
            'daily_shop': {'en': 'Daily shop',
                           'ru': 'Ежедневный магазин'},
            'case_shop': {'en': 'Case shop',
                          'ru': 'Кейсы'},
            'consumables_shop': {'en': 'Consumables',
                                 'ru': 'Расходники'},
            'tools_shop': {'en': 'Tools',
                           'ru': 'Инструменты'},
            'premium_skins_shop': {'en': 'Premium skins',
                                   'ru': 'Премиум скины'},
            'coins_shop': {'en': 'Buy coins',
                           'ru': 'Купить монеты'},
            'donation_shop': {'en': 'Donate',
                              'ru': 'Донат'},
        }
        donation_shop_title = {
            'en': 'Support me',
            'ru': 'Поддержка'
        }
        # donation_shop_desc = {
        #     'en': 'Sorry, donation is temporarily unavailable. The service on which I accepted donations is broken and I\'m trying to solve this problem\n'
        #           '- Creator of the Hryak',
        #     'ru': '*Сорян, донат временно недоступен. Сервис на котором я принимал донаты сломался и я пытаюсь решить эту проблему*\n'
        #           '- Создатель Хряка'}
        donation_shop_desc = {
            'en': 'Hi, if you suddenly want to support me with a donation, and in return get some money, here is the link: [buymeacoffee.com](https://buymeacoffee.com/brevnoo/extras)\n\n'
                  'Of course you don\'t have to support me, but I would be pleased. Thx anyways <:pigWatermelon:1284935022758854719>',
            'ru': 'Здарова! Если вдруг хочешь поддержать меня донатом и в ответ получить немного игровой валюты, вот ссылка: [buymeacoffee.com](https://buymeacoffee.com/brevnoo/extras)\n\n'
                  'Естественно, ты не обязан меня поддерживать, но мне будет приятно. В любом случае, спасибо <:pigWatermelon:1284935022758854719>'}

    class PremiumShop:
        main_page_title = {'en': 'Donation page',
                           'ru': 'Страница доната'}
        main_page_desc = {
            'en': '*Sup, this is a donation page. Here you can buy game currency, thereby saving the creator of the Hryak from starvation*\n\n'
                  '- Select the product below that you want to buy',
            'ru': '*Здарова, это страница доната. Здесь можно купить игровую валюту, тем самым спасая создателя Хряка от голодной смерти*\n\n'
                  '- Выберите товар ниже, который хотите купить'}
        main_page_select_placeholder = {'en': 'Select product',
                                        'ru': 'Выберите товар'}
        main_page_select_option_hollars = {'en': 'Hryak-dollars',
                                           'ru': 'Хряк-доллары'}
        main_page_select_option_coins = {'en': 'Coins',
                                         'ru': 'Монеты'}
        buy_hollars_page_title = {'en': 'Donation page',
                                  'ru': 'Покупка валюты'}
        buy_hollars_page_desc = {
            'en': '*Hryak-dollars are the best currency in the game. For it you can buy coins or premium skins*\n\n'
                  '- 1 dollar = {amount} hryak-dollars',
            'ru': '*Хряк-доллары - это лучшая валюта в игре. За неё вы можете покупать монеты либо же эксклюзивные скины*\n\n'
                  '- 1 рубль = {amount} хряк-доллар'}
        buy_hollars_button_label = {'en': 'Select quantity',
                                    'ru': 'Выберите количество'}
        get_amount_of_hollars_modal_title = {'en': 'Buying page',
                                             'ru': 'Покупка'}
        get_amount_of_hollars_modal_label = {'en': 'Amount',
                                             'ru': 'Количество'}
        get_amount_of_hollars_modal_placeholder = {'en': 'Enter the number of hryak-dollars',
                                                   'ru': 'Введите количество хряк-долларов'}
        buy_coins_page_title = {'en': 'Donation page',
                                'ru': 'Покупка монет'}
        buy_coins_page_desc = {
            'en': '*Coins are the main currency in the game. You can buy most items and skins with it*\n\n'
                  '- Select the quantity you need below',
            'ru': '*Монеты - основная валюта в игре. За неё можно купить большинство предметов и скинов*\n\n'
                  '- Выберите нужное вам количество ниже'}
        select_coins_option_label = {
            'en': 'Coins x{amount}',
            'ru': 'Монеты x{amount}'}
        select_coins_option_desc = {
            'en': 'Price: {price}{currency}',
            'ru': 'Цена: {price}{currency}'}
        select_coins_placeholder = {
            'en': '',
            'ru': 'Выберите количество'}
        select_payment_method_title = {'en': 'Payment method',
                                       'ru': 'Способ оплаты'}
        select_payment_method_desc = {'en': '*Choose a payment method below*',
                                      'ru': '*Выберите способ оплаты ниже. Если вас не устраивают тарифы в каком либо способе оплаты, просто попробуйте другой способ*'}
        payment_methods_descs = {
            'aaio': {'en': '- Instant delivery\n'
                           '- A lot of payment methods\n',
                     'ru': '- Моментальная выдача\n'
                           '- Множество способов оплаты\n'
                           '- Доступны русские и украинские карточки\n'},
            'boosty': {'en': '- Issuance may take up to a day\n'
                             '- Minimum amount 0.1 dollar\n',
                       'ru': '- Выдача может занимать до суток\n'
                             '- Минимальная сумма 10 рублей\n'},
            'donatepay': {'en': '- Issuance may take up to a day\n'
                                '- Minimum amount 0.1 dollar\n',
                          'ru': '- Выдача может занимать до суток\n'
                                '- Минимальная сумма 10 рублей\n'},
            'donatello': {'en': '- Issuance may take up to a day\n'
                                '- Cryptocurrency\n',
                          'ru': '- Выдача может занимать до суток\n'
                                '- Доступны украинские карточки\n'
                                '- Рекомендуется для украинцев\n'}
        }
        pay_below_title = {'en': 'Payment',
                           'ru': 'Оплата'}
        pay_below_desc = {'en': '*Pay for your order below*\n'
                                f'- If you have any problems, write to the developer in DM: @{config.DEVELOPER_USERNAME}\n\n'
                                '⚠️ Carefully follow the instructions that will be given',
                          'ru': '*Оплатите ваш заказ ниже*\n'
                                f'- Если у вас возникли проблемы, обратитесь на [сервер поддержки]({config.BOT_GUILDS[config.RU_BOT_GUILD_ID]['url']})\n\n'
                                '⚠️ Чётко следуйте инструкциям, которые будут указаны'}
        aaio_pay_title = {'en': 'AAIO payment',
                          'ru': 'Оплата AAIO'}
        aaio_pay_desc = {'en': ''
                               '- Pay for your order using this link: [link]({url})\n'
                               '  - Order number: {order_id}',
                         'ru': '*На некоторые способы оплаты может быть увеличенная минимальная сумма. Я знаю что это не удобно, но ничего не могу с этим поделать*\n\n'
                               '- Оплатите заказ по этой ссылке: [ссылка]({url})\n'
                               '  - Номер заказа: {order_id}'}
        boosty_pay_title = {'en': 'Boosty',
                            'ru': 'Boosty'}
        boosty_pay_desc = {'en': '- Send {amount}{currency} via this link: [link](https://boosty.to/brevnoo/donate)\n'
                                 '- In the "message" field, enter the order number\n'
                                 ' > Order number: {order_id}',
                           'ru': '- Отправьте {amount}{currency} по этой ссылке: [ссылка](https://boosty.to/brevnoo/donate)\n'
                                 '- В поле "сообщение" введите номер заказа\n'
                                 ' > Номер заказа: {order_id}'}
        donatepay_pay_title = {'en': 'DonatePay',
                               'ru': 'DonatePay'}
        donatepay_pay_desc = {
            'en': '- Send {amount}{currency} via this link: [link](https://new.donatepay.ru/@brevnoo)\n'
                  '- In the "message" field, enter the order number\n'
                  ' > Order number: {order_id}',
            'ru': '- Отправьте {amount}{currency} по этой ссылке: [ссылка](https://new.donatepay.ru/@brevnoo)\n'
                  '- В поле "сообщение стримеру" введите номер заказа\n'
                  ' > Номер заказа: {order_id}'}
        donatello_pay_title = {'en': 'Donatello',
                               'ru': 'Donatello'}
        donatello_pay_desc = {'en': '- Send {amount}{currency} via this link: [link](https://donatello.to/brevnoo)\n'
                                    '- In the "message" field, enter the order number\n'
                                    ' > Order number: {order_id}\n\n'
                                    '*Payment method "Mono", accepts all cards*',
                              'ru': '- Отправьте {amount}{currency} по этой ссылке: [ссылка](https://donatello.to/brevnoo)\n'
                                    '- В поле "сообщение" введите номер заказа\n'
                                    ' > Номер заказа: {order_id}\n\n'
                                    '*Способ оплаты "Моно", принимает все карточки*'}
        item_give_notification_title = {'en': 'Donation paid',
                                        'ru': 'Донат оплачен'}
        item_give_notification_desc = {'en': '*You received items for your donation:*\n\n'
                                             '{items}\n\n'
                                             '*Thank you for your support 💝*',
                                       'ru': '*Вы получили предметы за ваш донат:*\n\n'
                                             '{items}\n\n'
                                             '*Спасибо за вашу поддержку 💝*'}

    class ShopItemBought:
        title = {'en': 'You bought {item}',
                 'ru': 'Вы купили {item}'}
        desc = {'en': "*We hope you enjoy your purchase. (Refunds are not available)*",
                'ru': '*Надеюсь, вам понравится ваша покупка. (Деньги не возвращаем)*'}

    class JoinMessageSet:
        description = {'en': 'Set message when user joins server',
                       'ru': 'Установить сообщение, когда пользователь заходит на сервер'}
        channel_var_name = {'en': 'channel',
                            'ru': 'канал'}
        channel_var_desc = {'en': 'The channel where the message will be sent',
                            'ru': 'Канал, в который будет отправляться сообщение'}
        message_var_name = {'en': 'message',
                            'ru': 'сообщение'}
        message_var_desc = {
            'en': 'The message that will be sent when the participant enters. Use {user} to mention',
            'ru': 'Сообщение, которое будет отправляться при заходе участника. Используйте {user} для упоминания'}
        scd_title = {'en': 'Great, the channel is set: {channel}',
                     'ru': 'Отлично, канал установлен: {channel}'}
        scd_desc = {'en': '*This is the message that will appear:*\n\n{message}',
                    'ru': '*Вот сообщение которое будет выводится:*\n\n{message}'}
        reset_scd_title = {'en': 'Join message reset',
                           'ru': 'Приветственное сообщение сброшено'}

    class JoinMessageReset:
        description = {'en': 'Reset greeting message settings',
                       'ru': 'Сбросить настройки для приветственного сообщения'}
        scd_title = {'en': 'Join message reset',
                     'ru': 'Приветственное сообщение сброшено'}

