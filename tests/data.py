dtime = '2023-04-12T10:09:44.28'
USERS = {
    'good_user': {
        'id': 1,
        'tg': '@tgadmin',
        'vk': '@vkadmin',
        'phone': '89991234567',
        'name': 'admin',
        'created_at': dtime,
    },
    'good_user2': {
        'id': 2,
        'tg': '@new_name',
        'vk': '@name2',
        'phone': '89991234567',
        'name': 'admin',
        'created_at': dtime,
    },
    'minimum_user': {'name': 'pipin', 'created_at': dtime},
    'bad_user': {
        'id': '',
        'tg': '',
        'vk': '',
        'phone': '',
        'name': '',
        'created_at': '',
    },
}


TASKS = {
    'good_task': {
        'user_id': 1,
        'description': 'Совещание',
        'place': 'Переговорная',
        'dtime': dtime,
        'created_at': dtime,
    },
    'good_task2': {
        'user_id': 1,
        'description': 'Встреча',
        'place': 'Новое место',
        'dtime': dtime,
        'created_at': dtime,
    },
    'bad_task1': {
        'user_id': 0,
        'description': 'Bad user_id',
        'place': '',
        'dtime': dtime,
        'created_at': dtime,
    },
    'bad_task2': {
        'user_id': 1,
        'description': None,
        'place': '',
        'dtime': dtime,
        'created_at': dtime,
    },
}
