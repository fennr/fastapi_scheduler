from fastapi import HTTPException


class SchedulerException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


class UserException(SchedulerException):
    """
    Класс пользовательских ошибок
    """


class TaskException(SchedulerException):
    """
    Класс ошибок задач
    """


class RemindException(SchedulerException):
    """
    Класс ошибок напоминаний
    """


class UserExist(UserException):
    ...


class UserNotFound(UserException):
    ...


class TaskNotFound(TaskException):
    ...


class RemindNotFound(RemindException):
    ...
