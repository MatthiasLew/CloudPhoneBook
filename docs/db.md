# CloudPhoneBook Database Schema (ERD)

## Tables

### 1. `users`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | VARCHAR(36) / UUID | PRIMARY KEY | Unique user identifier |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL, INDEX | User login email |
| `hashed_password` | VARCHAR(255) | NOT NULL | Salted PBKDF2 / Bcrypt password hash |
| `created_at` | TIMESTAMPTZ | NOT NULL | Account creation timestamp |

### 2. `contacts`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | VARCHAR(36) / UUID | PRIMARY KEY | Unique contact identifier |
| `user_id` | VARCHAR(36) | FOREIGN KEY (`users.id` ON DELETE CASCADE), INDEX | Owner user ID |
| `first_name` | VARCHAR(100) | NOT NULL, INDEX | Contact first name |
| `last_name` | VARCHAR(100) | NOT NULL, INDEX | Contact last name |
| `phone` | VARCHAR(50) | NOT NULL, INDEX | Phone number |
| `email` | VARCHAR(255) | NULLABLE | Email address |
| `address` | VARCHAR(255) | NULLABLE | Street / postal address |
| `notes` | TEXT | NULLABLE | Additional notes / remarks |
| `created_at` | TIMESTAMPTZ | NOT NULL | Contact creation timestamp |
| `updated_at` | TIMESTAMPTZ | NOT NULL | Last update timestamp |

### 3. `user_settings`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `user_id` | VARCHAR(36) | PRIMARY KEY, FOREIGN KEY (`users.id` ON DELETE CASCADE) | Owner user ID |
| `theme` | VARCHAR(20) | NOT NULL, DEFAULT 'dark' | Active UI theme ('dark', 'light') |
| `table_layout_json` | JSON / JSONB | NOT NULL, DEFAULT '{}' | Column widths, default sort order |
| `updated_at` | TIMESTAMPTZ | NOT NULL | Last update timestamp |
