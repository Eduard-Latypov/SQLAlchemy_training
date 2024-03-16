import datetime
import os
import sys
import enum
from typing import Annotated

from sqlalchemy import String, ForeignKey, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


int_pk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[
    datetime.datetime,
    mapped_column(server_default=text("TIMEZONE('utc', now())")),
]
updated_at = Annotated[
    datetime.datetime,
    mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow,
    ),
]


class Model(DeclarativeBase):
    pass


class Workers(Model):
    __tablename__ = "workers"

    id: Mapped[int_pk]
    username: Mapped[str] = mapped_column(String(20))
    age: Mapped[int | None]


class Workload(enum.Enum):
    fulltime = "fulltime"
    parttime = "parttime"


class Resumes(Model):
    __tablename__ = "resumes"

    id: Mapped[int_pk]
    title: Mapped[str] = mapped_column(String(64))
    compensation: Mapped[int | None]
    workload: Mapped[Workload]
    worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id", ondelete="CASCADE"))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
