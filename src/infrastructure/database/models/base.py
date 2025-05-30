# pylint: disable=E1102

from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, registry


class Base(DeclarativeBase):
    registry = registry(
        type_annotation_map={
            datetime: DateTime(timezone=True),
        }
    )


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
