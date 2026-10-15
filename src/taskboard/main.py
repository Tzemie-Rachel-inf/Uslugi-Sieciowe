from itertools import count
from typing import Literal

import uvicorn
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

TaskStatus = Literal["open", "done"]
TaskPriority = Literal["low", "medium", "high"]


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200, strip_whitespace=True)
    status: TaskStatus = "open"
    priority: TaskPriority = "medium"


class Task(BaseModel):
    id: int
    title: str
    status: TaskStatus
    priority: TaskPriority


app = FastAPI(title="TaskBoard")

TASKS: dict[int, Task] = {
    1: Task(id=1, title="Przygotować środowisko", status="done", priority="high"),
    2: Task(id=2, title="Przeczytać RFC 9110", status="open", priority="medium"),
}
NEXT_ID = count(start=3)


@app.get("/")
def root():
    return {"message": "Hello Web"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks")
def list_tasks(
    status: TaskStatus | None = None,
    limit: int = Query(default=20, ge=1),
):
    items = list(TASKS.values())
    if status is not None:
        items = [task for task in items if task.status == status]
    return {"items": items[:limit], "total": len(items)}


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = TASKS.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: TaskCreate):
    task_id = next(NEXT_ID)
    created_task = Task(id=task_id, **task.model_dump())
    TASKS[task_id] = created_task
    return created_task


def main() -> None:
    uvicorn.run("taskboard.main:app", host="127.0.0.1", port=8000)
