required_options = ['id', 'type', 'cost', 'emoji']

items = {
    'poop': {'name': {'en': 'Poops',
                      'ru': 'Какашки'},
             'desc': {
                 'en': 'Pure, and most importantly, natural manure',
                 'ru': 'Чистый, а самое главное натуральный навоз'
             },
             'components': ['use', 'sell'],
             'type': 'resource',
             'cost': 1,
             'rarity': '1',
             'emoji': '💩',
             'image_url': 'https://cdn.discordapp.com/attachments/933356358097580103/1103395362389119007/1f4a9.png'},
    'cylinder': {'name': {'en': 'Cylinder',
                          'ru': 'Цилиндр'},
                 'desc': {
                     'en': 'Very fashionable top hat',
                     'ru': 'Очень модный цилиндр'
                 },
                 'type': 'skin:hat',
                 'rarity': '3',
                 'emoji': '🎩'},
    'z_cap_white': {'name': {'en': 'White Z cap',
                             'ru': 'Белая Z кепка'},
                    'desc': {
                        'en': 'White cap with letter Z',
                        'ru': 'Белая кепка с буквой Z'
                    },
                    'type': 'skin:hat',
                    'rarity': '2',
                    'emoji': '🧢',
                    'not_draw': []},
    'pixel_glasses': {'name': {'en': 'Pixel Glasses',
                               'ru': 'Пикскельные очки'},
                      'desc': {
                          'en': 'Cool pixel glasses',
                          'ru': 'Крутые пиксельные очки'
                      },
                      'type': 'skin:glasses',
                      'rarity': '4',
                      'emoji': '🕶️',
                      'not_draw': ['eyes', 'pupils']},
    'amogus_glasses': {'name': {'en': 'Amogus face',
                               'ru': 'Лицо амогуса'},
                      'desc': {
                          'en': 'Feel like a real amogus',
                          'ru': 'Почувствуй себя настоящим амогусом'
                      },
                      'type': 'skin:glasses',
                      'rarity': '5',
                      'emoji': '📮',
                      'not_draw': ['eyes', 'pupils', 'nose']},
}
