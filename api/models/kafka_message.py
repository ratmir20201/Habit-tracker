import datetime

from database.base import Base
from models.mixins.id_int_pk import IdIntPkMixin
from sqlalchemy import Date, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column


class KafkaMessage(Base, IdIntPkMixin):
    """Модель kafka сообщения."""

    telegram_id: Mapped[int] = mapped_column(unique=True)
    date: Mapped[datetime.datetime] = mapped_column(Date)

    __table_args__ = (
        UniqueConstraint(
            "telegram_id",
            "date",
            name="unique_telegram_id_date_message",
        ),
    )
