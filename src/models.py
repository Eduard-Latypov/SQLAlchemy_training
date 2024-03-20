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
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

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


class Base(DeclarativeBase):

    col_cnt = 3
    columns = tuple()

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.columns or idx < self.col_cnt:
                cols.append(str(getattr(self, col)))
        return ", ".join(cols)


class Workers(Base):
    __tablename__ = "workers"

    id: Mapped[int_pk]
    username: Mapped[str] = mapped_column(String(20))
    age: Mapped[int | None]
    resumes: Mapped[list["Resumes"]] = relationship(back_populates="worker")


class WorkloadEnum(enum.Enum):
    fulltime = "fulltime"
    parttime = "parttime"


class Resumes(Base):
    __tablename__ = "resumes"

    id: Mapped[int_pk]
    title: Mapped[str] = mapped_column(String(64))
    compensation: Mapped[int | None]
    workload: Mapped[WorkloadEnum]
    worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id", ondelete="CASCADE"))
    worker: Mapped["Workers"] = relationship(back_populates="resumes")
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


# metadata = MetaData()
#
# workers_table = Table(
#     "workers",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column(
#         "username",
#         String(20),
#     ),
#     Column("age", Integer),
# )

# resumes_table = Table(
#     "resumes",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("title", String(64)),
#     Column("compensation", Integer, nullable=True),
#     Column("workload", Enum(WorkloadEnum)),
#     Column("worker_id", ForeignKey("workers.id", ondelete="CASCADE")),
#     Column("created_at", TIMESTAMP, server_default=text("TIMEZONE('utc', now())")),
#     Column(
#         "updated_at",
#         TIMESTAMP,
#         server_default=text("TIMEZONE('utc', now())"),
#         onupdate=datetime.datetime.utcnow,
#     ),
# )
