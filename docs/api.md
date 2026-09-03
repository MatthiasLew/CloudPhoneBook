# CloudPhoneBook API Specification

Base URL: `http://localhost:8000/api/v1`  
Interactive OpenAPI documentation (Swagger): `http://localhost:8000/docs`

---

## Authentication (`/auth`)

### 1. Register User
- **Method**: `POST /auth/register`
- **Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "securepassword"
  }
  ```
- **Response**: `201 Created`
  ```json
  {
    "id": "uuid-string",
    "email": "user@example.com",
    "created_at": "2026-09-03T11:00:00Z"
  }
  ```

### 2. Login
- **Method**: `POST /auth/login`
- **Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "securepassword"
  }
  ```
- **Response**: `200 OK`
  ```json
  {
    "access_token": "eyJhbGci...",
    "token_type": "bearer",
    "expires_in_seconds": 86400
  }
  ```

### 3. Current User Profile
- **Method**: `GET /auth/me`
- **Headers**: `Authorization: Bearer <access_token>`
- **Response**: `200 OK`

---

## Contacts (`/contacts`)

All contact endpoints require `Authorization: Bearer <access_token>`.

### 1. List / Search Contacts
- **Method**: `GET /contacts?query={search}&limit=50&offset=0`
- **Query Parameters**:
  - `query` (optional): case-insensitive search matching first name, last name, phone, email, or address.
  - `limit` (default: 50): items per page.
  - `offset` (default: 0): pagination offset.
- **Response**: `200 OK`
  ```json
  {
    "items": [
      {
        "id": "uuid",
        "user_id": "uuid",
        "first_name": "Jan",
        "last_name": "Kowalski",
        "phone": "+48 501 111 222",
        "email": "jan@example.com",
        "address": "Warszawa",
        "notes": "Team lead",
        "created_at": "2026-09-03T10:00:00Z",
        "updated_at": "2026-09-03T10:00:00Z"
      }
    ],
    "total": 1,
    "limit": 50,
    "offset": 0
  }
  ```

### 2. Create Contact
- **Method**: `POST /contacts`
- **Body**:
  ```json
  {
    "first_name": "Anna",
    "last_name": "Nowak",
    "phone": "+48 502 222 333",
    "email": "anna@example.com",
    "address": "Krakow",
    "notes": "PM"
  }
  ```
- **Response**: `201 Created`

### 3. Get Contact
- **Method**: `GET /contacts/{contact_id}`
- **Response**: `200 OK` / `404 Not Found`

### 4. Update Contact
- **Method**: `PUT /contacts/{contact_id}`
- **Body**: Partial or full fields to update.
- **Response**: `200 OK`

### 5. Delete Contact
- **Method**: `DELETE /contacts/{contact_id}`
- **Response**: `204 No Content`

---

## User Settings (`/me/settings`)

### 1. Get User Settings
- **Method**: `GET /me/settings`
- **Response**: `200 OK`
  ```json
  {
    "theme": "dark",
    "table_layout_json": {
      "sort_column": "first_name",
      "sort_order": "asc"
    },
    "updated_at": "2026-09-03T10:00:00Z"
  }
  ```

### 2. Update User Settings
- **Method**: `PUT /me/settings`
- **Body**:
  ```json
  {
    "theme": "light",
    "table_layout_json": {}
  }
  ```
- **Response**: `200 OK`

---

## Health (`/health`)
- **Method**: `GET /health`
- **Response**: `200 OK`
  ```json
  {
    "status": "ok",
    "database": "healthy"
  }
  ```
