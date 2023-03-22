from app.sdk import ActionRequest, ActionResponse

request = ActionRequest(query='Test request', variables={'x': 1})


class Constants:
    """Изменяемые константы"""

    BAD_VALUE = [None, 'None', 'undefined']  # плохие значения переменной
    USER = 'phone'       #
    DESC = 'dance'       #
    DATE = 'date'        #


const = Constants()


def action(request: ActionRequest) -> ActionResponse:
    request.variables['test'] = 'success'
    request.variables.get(const.USER, const.BAD_VALUE[0])
    request.variables.get(const.DESC, const.BAD_VALUE[0])
    request.variables.get(const.DATE, const.BAD_VALUE[0])
    return ActionResponse(message=request.query, variables=request.variables)
