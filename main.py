from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Pydantic model
class TaskCreate(BaseModel):
    title: str
    description: str
    is_complete: bool

# Ensure the database table exists
def create_table():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        is_complete INTEGER NOT NULL DEFAULT 0
    )
    """)
    conn.commit()
    conn.close()

create_table()

# Create task
@app.post("/tasks")
async def create_task(task: TaskCreate):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tasks (title, description, is_complete)
        VALUES (?, ?, ?)
    """, (task.title, task.description, int(task.is_complete)))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return {"message": "Task created.", "id": new_id}

# Get all tasks
@app.get("/tasks")
async def get_tasks():
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    conn.close()

    tasks = [{
        "id": row["id"],
        "title": row["title"],
        "description": row["description"],
        "is_complete": "Complete" if row["is_complete"] == 1 else "Incomplete"
    } for row in rows]

    return {"tasks": tasks}

# Get one task
@app.get("/tasks/{task_id}")
async def get_task(task_id: int):
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Task not found.")

    return {
        "id": row["id"],
        "title": row["title"],
        "description": row["description"],
        "is_complete": "Complete" if row["is_complete"] == 1 else "Incomplete"
    }

# Update entire task
@app.put("/tasks/{task_id}")
async def update_task(task_id: int, updatedData: TaskCreate):
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tasks
        SET title = ?, description = ?, is_complete = ?
        WHERE id = ?
    """, (updatedData.title, updatedData.description, int(updatedData.is_complete), task_id))

    conn.commit()

    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    changed_task = cursor.fetchone()

    if changed_task is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Error updating task.")

    conn.close()

    return {
        "message": "Task updated.",
        "task": {
            "id": changed_task["id"],
            "title": changed_task["title"],
            "description": changed_task["description"],
            "is_complete": "Complete" if changed_task["is_complete"] == 1 else "Incomplete"
        }
    }

# Mark task complete
@app.patch("/tasks/{task_id}/complete")
async def toggle_task_completion(task_id: int, is_complete: bool = Body(...)):
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()

    if task is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found.")

    cursor.execute("""
        UPDATE tasks
        SET is_complete = ?
        WHERE id = ?
    """, (int(is_complete), task_id))
    conn.commit()

    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    updated_task = cursor.fetchone()
    conn.close()

    return {
        "message": "Task marked complete." if is_complete else "Task marked incomplete.",
        "task": {
            "id": updated_task["id"],
            "title": updated_task["title"],
            "description": updated_task["description"],
            "is_complete": "Complete" if updated_task["is_complete"] == 1 else "Incomplete"
        }
    }

# Delete task
@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()

    if task is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found.")

    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

    return {"message": "Task deleted."}
