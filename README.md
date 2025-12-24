# Task Manager API (FastAPI + PostgreSQL)

A backend **Task Management REST API** built using **FastAPI** and **PostgreSQL**, demonstrating **production-style authentication**, **rate limiting**, and **clean architecture principles** beyond basic CRUD functionality.

This project focuses on real-world backend design patterns rather than infrastructure or deployment concerns.

---

## Features

### Task Management
- Create, read, update, and delete tasks
- Tasks are **user-scoped** (no cross-user access)
- Advanced querying support:
  - Filtering (`completed=true/false`)
  - Search (title and description)
  - Sorting (e.g., `created_at`, `title`)
  - Pagination with metadata

### Authentication & Security
- User signup and login
- Password hashing using **bcrypt**
- JWT **access tokens** (short-lived)
- **Refresh tokens** (long-lived, stored hashed in the database)
- Logout via refresh token revocation
- Access token refresh without re-authentication
- Rate limiting on authentication endpoints to prevent abuse

---

## Authentication Flow (Production-Style)

```
Login
 ├─ Access Token (short-lived JWT)
 └─ Refresh Token (long-lived, stored hashed)

Access token expires
 └─ Client calls /refresh → new access token

Logout
 └─ Refresh token revoked
    (existing access tokens expire naturally)
```

**Note:**  
Access tokens are stateless JWTs and are not revoked on logout.  
Logout prevents issuing *new* access tokens by revoking refresh tokens.  
This is a standard trade-off used in most real-world systems.

---

## Rate Limiting

Rate limiting is applied to **security-critical endpoints**:

| Endpoint   | Limit        |
|-----------|--------------|
| `/signup` | 3 requests / minute |
| `/login`  | 5 requests / minute |
| `/refresh`| 10 requests / minute |

Implemented at the API layer using **SlowAPI**.

> In large-scale systems, rate limiting is commonly handled by Redis-backed storage or an API Gateway.

---

## Task Query Examples

### Filtering
```
GET /tasks?completed=true
GET /tasks?completed=false
```

### Search
```
GET /tasks?search=meeting
```

### Sorting
```
GET /tasks?sort=created_at&order=desc
```

### Pagination
```
GET /tasks?page=1&page_size=10
```

### Response Format
```json
{
  "data": [...],
  "meta": {
    "page": 1,
    "page_size": 10,
    "total": 42
  }
}
```

---

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Passlib (bcrypt)
- PyJWT
- SlowAPI
- Python 3

---

## ▶️ How to Run Locally

```
uvicorn main:app --reload
```

API documentation available at:

```
http://127.0.0.1:8000/docs
```

---

## 📂 Project Structure

```
task_manager_api/
│── auth/                 # JWT, password hashing, auth dependencies
│── services/             # Business logic (tasks, users, auth)
│── models.py             # SQLAlchemy models
│── schemas.py            # Pydantic schemas
│── database.py           # Database engine and sessions
│── main.py               # FastAPI app and routes
│── README.md
```

---

## Key Design Decisions

- Stateless JWT access tokens for scalability
- Stateful refresh tokens stored hashed for logout and session control
- Service-layer query construction for filtering, search, sorting, and pagination
- Rate limiting applied at authentication boundaries
- Database-managed timestamps for consistency

---

## Future Improvements
- Redis-backed rate limiting
- Refresh token rotation
- Role-based access control
- Automated cleanup of expired refresh tokens
- Dockerization and CI
