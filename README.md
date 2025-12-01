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

## Docker Compose Setup

This project includes Docker Compose configuration for easy deployment with all required services (PostgreSQL, Redis, and the API).

### Prerequisites

- Docker Engine 20.10 or higher
- Docker Compose 2.0 or higher

### Environment Configuration

Before running Docker Compose, ensure you have a `.env` file in the project root with the following variables:

```env
# Application
APP_PORT=8000
APP_HOST=0.0.0.0

# Database
POSTGRES_DB=your_database_name
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_PORT=5432

# Redis
REDIS_PORT=6379

# Other settings (auth, logging, etc.)
# ... add other required environment variables
```

### Running with Docker Compose

#### Start All Services

To start all services (API, PostgreSQL, and Redis):

```bash
docker-compose up -d
```

The `-d` flag runs containers in detached mode (in the background).

#### View Logs

To view logs from all services:

```bash
docker-compose logs -f
```

To view logs from a specific service:

```bash
docker-compose logs -f api
docker-compose logs -f db
docker-compose logs -f redis
```

#### Stop Services

To stop all services:

```bash
docker-compose down
```

To stop services and remove volumes (⚠️ **WARNING**: This will delete all database data):

```bash
docker-compose down -v
```

#### Rebuild and Restart

If you've made changes to the Dockerfile or need to rebuild the API image:

```bash
docker-compose up -d --build
```

#### Check Service Status

To see the status of all services:

```bash
docker-compose ps
```

### Accessing Services

- **API**: `http://localhost:8000` (or the port specified in `APP_PORT`)
- **API Documentation**: `http://localhost:8000/docs`
- **PostgreSQL**: `localhost:5432` (or the port specified in `POSTGRES_PORT`)
- **Redis**: `localhost:6379` (or the port specified in `REDIS_PORT`)

### Database Migrations

When running with Docker Compose, migrations are automatically applied when the API container starts (via `start.sh`). The script runs `alembic upgrade head` to apply all pending migrations.

**Note**: If you need to create new migrations, you should:

1. Run the application locally (not in Docker) to generate migrations
2. Commit the migration files to version control
3. The next time Docker Compose starts, the new migrations will be applied automatically

### Troubleshooting Docker Compose

#### Services Won't Start

1. **Check if ports are already in use**:
   ```bash
   # Windows
   netstat -ano | findstr :8000
   
   # Linux/Mac
   lsof -i :8000
   ```

2. **Check Docker logs**:
   ```bash
   docker-compose logs
   ```

3. **Verify environment variables**:
   Ensure all required variables are set in your `.env` file.

#### Database Connection Issues

- Verify the database container is healthy: `docker-compose ps`
- Check database logs: `docker-compose logs db`
- Ensure `DEPLOY_MODE=DOCKER` is set (automatically set by docker-compose)

#### Redis Connection Issues

- Verify Redis container is running: `docker-compose ps redis`
- Test Redis connection: `docker-compose exec redis redis-cli ping`
- Should return `PONG` if Redis is working

#### Rebuild After Code Changes

If you've made code changes and want to rebuild:

```bash
docker-compose up -d --build api
```

#### Clean Start

To completely reset everything (removes containers, volumes, and networks):

```bash
docker-compose down -v
docker-compose up -d --build
```

⚠️ **Warning**: This will delete all database data stored in Docker volumes.

### Docker Compose Services

The `docker-compose.yaml` file defines three services:

1. **api**: The FastAPI application
   - Builds from the Dockerfile in the project root
   - Depends on `db` and `redis` services
   - Automatically applies database migrations on startup
   - Health checks available at `/api/v1/health`

2. **db**: PostgreSQL 15 database
   - Persistent data stored in Docker volume `pg_data`
   - Health checks ensure database is ready before API starts

3. **redis**: Redis 7 cache
   - Used for caching and session management
   - Health checks ensure Redis is ready

All services are connected via a Docker network (`vote-network`) for internal communication.

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

