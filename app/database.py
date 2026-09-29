from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import aiosqlite

@dataclass(slots=True)
class Task:
    id: int
    user_id: int
    text: str
    completed: bool
    created_at: str
    completed_at: str | None

class Database:
    def __init__(self, path: str):
        self.path = path

    async def connect(self):
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        db = await aiosqlite.connect(self.path)
        db.row_factory = aiosqlite.Row
        await db.execute("PRAGMA journal_mode=WAL")
        await db.execute("PRAGMA foreign_keys=ON")
        await db.execute("""CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            text TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            completed_at TEXT)""")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_tasks_user_status ON tasks(user_id, completed, id)")
        await db.commit()
        return db

    async def add_task(self, user_id: int, text: str) -> int:
        async with await self.connect() as db:
            cur = await db.execute(
                "INSERT INTO tasks(user_id,text,created_at) VALUES(?,?,?)",
                (user_id, text, datetime.now(timezone.utc).isoformat()),
            )
            await db.commit()
            return int(cur.lastrowid)

    async def list_tasks(self, user_id: int) -> list[Task]:
        async with await self.connect() as db:
            cur = await db.execute(
                "SELECT id,user_id,text,completed,created_at,completed_at "
                "FROM tasks WHERE user_id=? AND completed=0 ORDER BY id",
                (user_id,),
            )
            rows = await cur.fetchall()
        return [
            Task(r["id"], r["user_id"], r["text"], bool(r["completed"]), r["created_at"], r["completed_at"])
            for r in rows
        ]

    async def complete_task(self, user_id: int, task_id: int) -> bool:
        async with await self.connect() as db:
            cur = await db.execute(
                "UPDATE tasks SET completed=1,completed_at=? "
                "WHERE id=? AND user_id=? AND completed=0",
                (datetime.now(timezone.utc).isoformat(), task_id, user_id),
            )
            await db.commit()
            return cur.rowcount == 1
