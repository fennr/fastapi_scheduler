import requests

from app.sdk import ActionRequest, ActionResponse

request = ActionRequest(query='Test request', variables={'x': 1})


class Constants:
    """Изменяемые константы"""

    BAD_VALUE = [None, 'None', 'undefined']  # плохие значения переменной
    ACTION = 'action'       # Действие
    USER = 'mobile_phone'   # Логин
    DESC = 'dance'          # Описание
    DATE = 'date'         # Дата


c = Constants()


def send_action(user: str, description: str, dtime: str) -> int:
    day, month = dtime.split('.')
    dtime = f'2023-{month}-{day}T12:00:00.000Z'
    endpoint = 'http://172.17.0.1:9301/task'
    if user and description and dtime:
        r = requests.post(
            url=endpoint,
            json={
                'user': user,
                'description': description,
                'dtime': dtime,
            },
        )
        return r.status_code
    return 404


def get_user_action(user: str) -> str:
    endpoint = f'http://172.17.0.1:9301/task/{user}'
    if user:
        r = requests.get(
            url=endpoint,
        )
        schedule = r.json()
        message = ''
        for train in schedule:
            message += f'{train["description"]}: {train["dtime"][:10]}\n'
        return message
    return ''


def schedule_action(request: ActionRequest) -> ActionResponse:
    try:

        user = request.variables.get(c.USER, c.BAD_VALUE[0])
        description = request.variables.get(c.DESC, c.BAD_VALUE[0])
        date = request.variables.get(c.DATE, c.BAD_VALUE[0])
        action = request.variables.get(c.ACTION, c.BAD_VALUE[0])

        if action == 'send':
            status_code = send_action(user, description, date)
            if status_code == 201:
                return ActionResponse(message='Запись успешно добавлена')
        elif action == 'get_by_user':
            message = get_user_action(user)
            if message:
                return ActionResponse(message=message)

        return ActionResponse(
            message=request.query, variables=request.variables
        )

    except Exception as e:
        print(e)
        return ActionResponse(
            message=request.query, variables=request.variables
        )
