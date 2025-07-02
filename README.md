# 🧠 FastAPI Task Manager API

A simple, fully functional task management REST API built with **FastAPI**, **Pydantic**, and **SQLite3**.

---

## 🚀 Tech Stack

- **FastAPI** – High-performance Python web framework  
- **Pydantic** – Data validation with Python type hints  
- **SQLite3** – Lightweight, file-based database

---

## 📦 Features

- Create, view, update, and delete tasks  
- Input validation with Pydantic models  
- Auto-generated Swagger and ReDoc docs  
- Minimal setup and no external database required

---

## 📬 API Endpoints

| Method | Endpoint                    | Description               |
|--------|-----------------------------|---------------------------|
| GET    | `/tasks`                    | Get all tasks             |
| GET    | `/tasks/{task_id}`          | Get task by ID            |
| POST   | `/tasks`                    | Create new task           |
| PUT    | `/tasks/{task_id}`          | Replace task              |
| PATCH  | `/tasks/{task_id}/complete` | Toggle task completion    |
| DELETE | `/tasks/{task_id}`          | Delete task               |

---

## 🧾 Example Payload

```json
{
  "title": "Write README",
  "description": "Summarize project features",
  "is_complete": false
}
```

---

## ⚙️ Setup

1. **Clone the repo**

```bash
git clone https://github.com/therealoganh/fastapi-task-manager.git
cd fastapi-task-manager
```

2. **Install dependencies**

```bash
pip install fastapi
```

3. **Run the app**

```bash
python main.py
```

Then open your browser at:

- Swagger UI → `http://localhost:8000/docs`  
- ReDoc → `http://localhost:8000/redoc`

---



