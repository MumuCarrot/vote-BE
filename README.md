# Vote Backend

A FastAPI-based backend application for voting systems.

## Prerequisites

- Python 3.11 or higher
- PostgreSQL 12 or higher
- Redis (for caching and session management)
- pip (Python package manager)

## Project Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd vote-BE
```

### 2. Create Virtual Environment

Create and activate a virtual environment:

**On Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**On Linux/Mac:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Configure the .env file as specified in .env.example.

## Running the Application

### Development Mode

Run the application using Uvicorn:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at `http://localhost:8000`

### API Documentation

## Database Migrations

This project uses Alembic for database migrations.

### Running Migrations

#### Apply All Pending Migrations

To apply all pending migrations to the database:

```bash
alembic upgrade head
```

### Creating New Migrations

#### Auto-generate Migration from Models

To automatically generate a migration based on model changes:

```bash
alembic revision --autogenerate -m "description of changes"
```

**Important:** Review the generated migration file in `migrations/versions/` before applying it to ensure it matches your intentions.

#### Create Empty Migration

To create an empty migration file for manual editing:

```bash
alembic revision -m "description of changes"
```

Then edit the generated file in `migrations/versions/` to add your migration logic.

### Committing Migrations

1. **Review the Migration File**

   Before committing, always review the generated migration file in `migrations/versions/` to ensure:
   - The changes are correct
   - No sensitive data is included
   - The migration is reversible (if possible)

2. **Test the Migration Locally**

   ```bash
   # Apply the migration
   alembic upgrade head
   
   # Test rollback (optional)
   alembic downgrade -1
   alembic upgrade head
   ```

3. **Commit to Git**

   ```bash
   git add migrations/versions/<migration_file>.py
   git commit -m "Add migration: description of changes"
   git push
   ```

4. **Apply in Other Environments**

   After pushing, other developers or deployment environments should run:

   ```bash
   alembic upgrade head
   ```

### Migration Best Practices

- Always review auto-generated migrations before applying
- Test migrations on a development database first
- Keep migrations small and focused on a single change
- Never edit existing migration files that have been applied to production
- Create a new migration to fix issues instead of modifying old ones
- Document complex migrations with comments in the migration file

## Project Structure

```
vote-BE/
├── app/
│   ├── core/           # Core configuration and settings
│   ├── db/             # Database configuration
│   ├── dependencies/   # Dependency injection
│   ├── exceptions/     # Custom exceptions
│   ├── http/           # HTTP utilities
│   ├── models/         # SQLAlchemy models
│   ├── repository/     # Data access layer
│   ├── routers/        # API routes
│   ├── schemas/        # Pydantic schemas
│   ├── services/       # Business logic
│   ├── utils/          # Utility functions
│   └── main.py         # Application entry point
├── migrations/         # Alembic migrations
│   ├── versions/       # Migration files
│   └── env.py          # Alembic environment configuration
├── alembic.ini         # Alembic configuration
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

The project uses pre-commit hooks. Install them:

```bash
pre-commit install
```

## Troubleshooting

### Database Connection Issues

- Verify PostgreSQL is running: `pg_isready`
- Check database credentials in `.env`
- Ensure the database exists

### Migration Issues

- Ensure you're using the correct database URL in `.env`
- Check that all model imports are correct in `migrations/env.py`
- Verify the migration file syntax is correct

### Redis Connection Issues

- Verify Redis is running: `redis-cli ping`
- Check Redis host and port in `.env`

## License

[Add your license information here]

