# Movies REST API

A JWT-secured REST API for a PostgreSQL movie database, built with **FastAPI**, **SQLAlchemy**, and **Docker**, plus a Python ETL script that loads movie data from CSV into a normalized relational schema.

## Features

- **Full CRUD** (create, read, update, delete) endpoints for movies, with pagination
- **OAuth2 / JWT authentication**: log in once, receive a signed token that expires after 30 minutes; every movie endpoint requires it
- **bcrypt password hashing**, with constant-time checks so usernames can't be discovered by timing responses
- **Input validation** on every write with Pydantic models (types, lengths, and ranges)
- **SQL injection prevention** through parameterized queries
- **No secrets in code**: database URL, signing key, and password hash live in environment variables, and the app refuses to start without them
- **Normalized schema**: 7 tables (movies, actors, directors, genres, and three linking tables with foreign keys and cascading deletes)
- **Re-runnable ETL**: loading the same CSV twice won't create duplicates; bad rows are reported and skipped
- **Hardened container**: non-root user, health check, database not exposed to the host, API bound to localhost only

## Project structure

| File | Purpose |
|---|---|
| `crud.py` | FastAPI app and movie endpoints |
| `auth.py` | Password verification and JWT creation/validation |
| `movies_parse.py` | Creates the schema and loads `data/movies.csv` |
| `Dockerfile` / `docker-compose.yml` | Runs the API and PostgreSQL as containers |
| `.env.example` | Template for required settings |

## Quick start (Docker)

```bash
git clone https://github.com/BlaccHacc/The-ways-of-the-sensei.git
cd The-ways-of-the-sensei
cp .env.example .env          # then edit .env with real values (see comments inside)

docker compose up -d --build  # start PostgreSQL and the API
docker compose exec api python movies_parse.py   # create tables and load data/movies.csv
```

API docs (interactive): http://localhost:8000/docs

## Using the API

```bash
# 1. Log in and get a token
TOKEN=$(curl -s -X POST http://localhost:8000/token \
  -d "username=admin&password=YOUR_PASSWORD" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

# 2. Call a protected endpoint
curl -H "Authorization: Bearer $TOKEN" "http://localhost:8000/movies?limit=5"
```

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/health` | No | API and database status |
| POST | `/token` | No | Log in, returns a JWT |
| GET | `/movies?skip=0&limit=100` | Yes | List movies (max 500 per page) |
| GET | `/movies/{id}` | Yes | Get one movie |
| POST | `/movies` | Yes | Add a movie |
| PUT | `/movies/{id}` | Yes | Update a movie |
| DELETE | `/movies/{id}` | Yes | Delete a movie |

## Running without Docker

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python movies_parse.py
uvicorn crud:app --reload
```

## CSV format

`data/movies.csv` needs a header row. Supported columns: `movie_title`, `movie_description`, `release_year`, `runtime_minutes`, `rating`, `votes`, `revenue_millions`, `metascore`, `actors`, `directors`, `genre` (people and genres are comma-separated). The common IMDB dataset headers (`Title`, `Year`, `Actors`, `Director`, `Genre`, ...) also work.
