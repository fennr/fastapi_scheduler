import uuid
from typing import Optional


class ActionRequest:
    """Имитация Request NC"""

    def __init__(
        self,
        query: str,
        entities: Optional[list] = None,
        variables: dict = {},
        session_id: str = uuid.uuid4().hex,
    ):
        self.query = query
        self.entities = entities
        self.variables = variables
        self.session_id = session_id

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(query='{self.query}',"
            f"entities={self.entities},"
            f"variables={self.variables},"
            f"session_id={self.session_id})"
        )


class Entity:
    """Имитация Entity"""

    def __init__(self, text, parsing, entity, start, end, confidence, extractor):
        self.text: str = text
        self.parsing: dict = parsing
        self.entity: str = entity
        self.start: int = start
        self.end: int = end
        self.confidence: float = confidence
        self.extractor: str = extractor


class ActionResponse:
    """Имитация Response"""

    def __init__(self, message: str = "", variables: dict = {}, repeat: bool = False):
        self.message: str = message
        self.variables = variables
        self.repeat = repeat

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(message='{self.message}',"
            f"variables={self.variables},"
            f"repeat={self.repeat})"
        )
