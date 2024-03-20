import datetime

from pydantic import BaseModel

from models import Workload


class WorkerPostDTO(BaseModel):
    username: str
    age: int | None


class WorkerGetDTO(WorkerPostDTO):
    id: int


class WorkerRelDTO(WorkerGetDTO):
    resumes: list["ResumeGetDTO"]


class ResumePostDTO(BaseModel):
    title: str
    compensation: int | None
    # workload: Workload - вызывает ошибку. Пока не разобрался как исправить
    workload: str
    worker_id: int


class ResumeGetDTO(ResumePostDTO):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime


class ResumeRelDTO(ResumeGetDTO):
    worker: "WorkerGetDTO"
