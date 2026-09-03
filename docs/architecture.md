# CloudPhoneBook Architecture

## Overview
CloudPhoneBook is a modern multi-tier, cloud-synchronized phonebook application designed to replace the legacy console C/MySQL phonebook project.

```
┌─────────────────────────────────────────────────────────────┐
│                 Desktop App (PySide6 / Qt)                  │
│  - Modern Dark / Light QSS Themes                           │
│  - Contacts Table with Instant Search & Column Sorting      │
│  - Local Cache & Secure Token Store                         │
└──────────────────────────────┬──────────────────────────────┘
                               │ HTTPS / JSON REST
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                 Backend REST API (FastAPI)                  │
│  - Routers: /auth, /contacts, /me/settings, /health         │
│  - Services & Repositories (Clean Architecture)             │
│  - Security: JWT Bearer Tokens, Salted Password Hashing     │
└──────────────────────────────┬──────────────────────────────┘
                               │ SQLAlchemy ORM 2.0
                               ▼
┌─────────────────────────────────────────────────────────────┐
│           Cloud Database (PostgreSQL / Supabase)            │
│  - users (id, email, password_hash, created_at)             │
│  - contacts (id, user_id, first_name, last_name, ...)       │
│  - user_settings (user_id, theme, table_layout_json, ...)   │
└─────────────────────────────────────────────────────────────┘
```

## Layers

1. **Shared Contracts (`packages/shared`)**:
   - Pydantic DTOs shared across client and server.
   - Standardized application error codes.

2. **Backend API (`services/api`)**:
   - `core/`: Config (`pydantic-settings`), Security (JWT + PBKDF2), Logging.
   - `db/`: SQLAlchemy engine, session generator, declarative models.
   - `repositories/`: Data access logic isolating DB queries.
   - `services/`: Business logic rules and validation.
   - `api/routes/`: FastAPI endpoints exposing HTTP REST resources.
   - `api/deps.py`: Dependency injection for DB session and authenticated user extraction.

3. **Desktop Client (`apps/desktop`)**:
   - Qt GUI structured with state stores, background HTTP API client, and local caching.
