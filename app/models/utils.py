from datetime import datetime

from sqlalchemy import Column
from sqlmodel import TIMESTAMP, func


def get_sa_column():
    return Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=datetime.now(),
        server_default=func.now(),
    )
