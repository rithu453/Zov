

# Zov — Finance Backend API

A simple backend built with FastAPI to manage **finance records (income/expense)** and **users**, with basic **role-based access control**.

---

## Tech Stack

* Python 3.10+
* FastAPI
* Uvicorn
* SQLAlchemy
* Pydantic
* SQLite (file-based database)

---

## Project Structure

```
app/
│
├── main.py                # Entry point (FastAPI app)
├── db/
│   └── database.py        # DB connection + session
├── models/                # SQLAlchemy models
│   ├── user.py
│   └── record.py
├── schemas/               # Request/response schemas
│   ├── user.py
│   └── record.py
├── routes/                # API routes
│   ├── users.py
│   ├── records.py
│   └── dashboard.py
└── middleware/
    └── role_check.py      # Role validation logic
```

---

## Setup

```bash
python -m venv .venv

# Activate (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## Run the Server

```bash
uvicorn app.main:app --reload
```

Access:

* API: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* Swagger Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Database

* SQLite database file: `finance.db`
* Automatically created when the server starts
* Tables are auto-generated

### Reset Database

1. Stop server
2. Delete `finance.db`
3. Restart server

---

## Roles & Access Control

The API uses a simple **header-based role system**.

### Required Header

```
role: admin | analyst | viewer
```

### Rules

* Missing `role` → `422 Unprocessable Entity`
* Invalid role → `403 Forbidden`

### Roles

* **admin**

  * Full access (create, update, delete)
* **analyst**

  * Read + dashboard access
* **viewer**

  * Read-only access

Note: No authentication (no login, no tokens). This is only for basic control.

---

## API Endpoints

### 1. Root

* `GET /`
  → Health check

---

### 2. Users (`/users`)

* `POST /users/`
  Create user

  ```json
  {
    "name": "string",
    "email": "string",
    "role": "admin | analyst | viewer"
  }
  ```

  * Status is set to `active` by default

* `GET /users/`
  List all users

* `PUT /users/{id}`
  Update user

* `PATCH /users/{id}/status?status=active|inactive`
  Change user status

* `DELETE /users/{id}`
  Requires: `role: admin`

---

### 3. Records (`/records`)

* `POST /records/`
  Requires: `admin`

  ```json
  {
    "amount": 1000,
    "type": "income | expense",
    "category": "string",
    "date": "YYYY-MM-DD",
    "notes": "optional"
  }
  ```

* `GET /records/`
  Requires: `admin | analyst | viewer`

  Query params:

  * `type`
  * `category`
  * `limit` (default: 10)
  * `offset` (default: 0)

* `PUT /records/{id}`
  Requires: `admin`

* `DELETE /records/{id}`
  Requires: `admin`

---

### 4. Dashboard (`/dashboard`)

Requires: `admin | analyst`

* `GET /dashboard/summary`
  → Total income, expense, net balance

* `GET /dashboard/category`
  → Category-wise totals

* `GET /dashboard/trends`
  → Monthly trends

  Note:

  * Uses first 7 characters of date (`YYYY-MM`)
  * Example: `2026-04-01`

---

## Example Requests

### Create User

```bash
curl -X POST http://127.0.0.1:8000/users/ \
-H "Content-Type: application/json" \
-d "{\"name\":\"Alice\",\"email\":\"alice@example.com\",\"role\":\"admin\"}"
```

---

### Create Record (Admin)

```bash
curl -X POST http://127.0.0.1:8000/records/ \
-H "Content-Type: application/json" \
-H "role: admin" \
-d "{\"amount\":1000,\"type\":\"income\",\"category\":\"Salary\",\"date\":\"2026-04-01\"}"
```

---

### Get Records (Viewer)

```bash
curl "http://127.0.0.1:8000/records/?type=expense&category=Food" \
-H "role: viewer"
```

---

### Dashboard Summary (Analyst)

```bash
curl http://127.0.0.1:8000/dashboard/summary \
-H "role: analyst"
```

---

## Error Handling

* `404` → Resource not found
* `422` → Validation error / Missing role header
* `403` → Role not allowed
* `500` → Server error