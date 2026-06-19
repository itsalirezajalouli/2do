from uuid import uuid4
from datetime import datetime, timezone
from sqlmodel import Session, select, and_
from db.models import Task, Plan, Status, Priority
from db.engine import get_engine


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def create_task(plan_uuid: str, title: str) -> Task | None:
    engine = get_engine()
    with Session(engine) as session:
        plan = session.get(Plan, plan_uuid)
        if not plan:
            return None
        existing = session.exec(
            select(Task).where(
                and_(Task.plan_uuid == plan_uuid, Task.title == title)
            )
        ).first()
        if existing:
            return None
        tasks = plan.tasks or []
        idx = len(tasks) + 1
        now = _now()
        task = Task(
            uuid=str(uuid4()),
            plan_uuid=plan_uuid,
            idx=idx,
            title=title,
            status=Status.PENDING,
            created_at=now,
            updated_at=now,
        )
        session.add(task)
        tasks.append(task.uuid)
        plan.tasks = tasks
        plan.updated_at = now
        session.add(plan)
        session.commit()
        session.refresh(task)
        return task


def get_tasks(plan_uuid: str | None = None) -> list[Task]:
    engine = get_engine()
    with Session(engine) as session:
        if plan_uuid:
            statement = select(Task).where(Task.plan_uuid == plan_uuid)
        else:
            statement = select(Task)
        return list(session.exec(statement).all())


def get_task(uuid: str) -> Task | None:
    engine = get_engine()
    with Session(engine) as session:
        return session.get(Task, uuid)


def get_task_by_plan_and_idx(plan_uuid: str, idx: int) -> Task | None:
    engine = get_engine()
    with Session(engine) as session:
        statement = select(Task).where(
            and_(Task.plan_uuid == plan_uuid, Task.idx == idx)
        )
        return session.exec(statement).first()


def delete_task(uuid: str) -> bool:
    engine = get_engine()
    with Session(engine) as session:
        task = session.get(Task, uuid)
        if not task:
            return False
        plan = session.get(Plan, task.plan_uuid)
        now = _now()
        if plan and plan.tasks:
            plan.tasks = [t for t in plan.tasks if t != uuid]
            plan.updated_at = now
            session.add(plan)
        session.delete(task)
        session.commit()
        return True


def update_task(
    uuid: str,
    title: str | None = None,
    status: Status | None = None,
    priority: Priority | None = None,
) -> Task | None:
    engine = get_engine()
    with Session(engine) as session:
        task = session.get(Task, uuid)
        if not task:
            return None
        if title is not None:
            task.title = title
        if status is not None:
            task.status = status
        if priority is not None:
            task.priority = priority
        task.updated_at = _now()
        session.add(task)
        session.commit()
        session.refresh(task)
        return task
