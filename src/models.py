import datetime
import os
import sys
import enum
from typing import Annotated

from sqlalchemy import (
    String,
    ForeignKey,
    text,
    Table,
    MetaData,
    Column,
    Integer,
    TIMESTAMP,
    Enum,
)
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

    def __str__(self):
        return f"{self.id}: {self.username} {self.age} years"


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


metadata = MetaData()

workers_table = Table(
    "workers",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "username",
        String(20),
    ),
    Column("age", Integer),
)

resumes_table = Table(
    "resumes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(64)),
    Column("compensation", Integer, nullable=True),
    Column("workload", Enum(Workload)),
    Column("worker_id", ForeignKey("workers.id", ondelete="CASCADE")),
    Column("created_at", TIMESTAMP, server_default=text("TIMEZONE('utc', now())")),
    Column(
        "updated_at",
        TIMESTAMP,
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow,
    ),
)
