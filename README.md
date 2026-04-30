# Os Paga Lanche API

FastAPI API for saving game users, scores, and run durations.

## Stack

- Python 3.13
- FastAPI
- SQLAlchemy
- PostgreSQL
- Docker Compose

## API Docs

When the API is running, open:

- Swagger UI: http://localhost:8000/docs
- OpenAPI JSON: http://localhost:8000/openapi.json
- Health check: http://localhost:8000/health

Protected endpoints require the `X-API-Key` header.

## Environment

Create a local `.env` file from the example:

```bash
cp .env.example .env
```

Recommended local values:

```env
API_KEY=change-me
DATABASE_URL=postgresql+psycopg://paga_lanche:paga_lanche@db:5432/paga_lanche
POSTGRES_DB=paga_lanche
POSTGRES_USER=paga_lanche
POSTGRES_PASSWORD=paga_lanche
```

Use a stronger `API_KEY` before exposing the API publicly.

## Run With Docker Compose

This is the recommended local setup because it starts both the API and PostgreSQL.

```bash
docker compose up --build
```

The API will be available at:

```text
http://localhost:8000
```

Stop the services:

```bash
docker compose down
```

Stop services and remove the local database volume:

```bash
docker compose down -v
```

## Run Locally Without Docker

You need a running PostgreSQL database and a `DATABASE_URL` that points to it.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export API_KEY=change-me
export DATABASE_URL=postgresql+psycopg://paga_lanche:paga_lanche@localhost:5432/paga_lanche
uvicorn src.main:app --reload
```

## Authentication

Send the API key in this header:

```http
X-API-Key: change-me
```

Example:

```bash
curl -H "X-API-Key: change-me" http://localhost:8000/users
```

In Swagger UI, click `Authorize` and enter the configured API key.

## Endpoints

Public:

- `GET /`
- `GET /health`
- `GET /docs`
- `GET /openapi.json`

Users:

- `POST /users`
- `GET /users`
- `GET /users/{username}`
- `GET /users/{username}/runs`
- `DELETE /users/{username}`

Runs:

- `POST /runs`
- `GET /runs`
- `GET /runs/{run_id}`
- `DELETE /runs/{run_id}`

## Example Flow

Create a user:

```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -H "X-API-Key: change-me" \
  -d '{"username":"leo"}'
```

Create a run:

```bash
curl -X POST http://localhost:8000/runs \
  -H "Content-Type: application/json" \
  -H "X-API-Key: change-me" \
  -d '{"username":"leo","score":120,"duration":45}'
```

List a user's runs:

```bash
curl -H "X-API-Key: change-me" http://localhost:8000/users/leo/runs
```

## Database Tables

Tables are created automatically on application startup with:

```python
Base.metadata.create_all(bind=engine)
```

No migration tool is configured yet.

## Troubleshooting

If the API returns `401`, check that the `X-API-Key` header matches `API_KEY`.

If the API cannot connect to the database, confirm that `DATABASE_URL` is correct and that PostgreSQL is healthy:

```bash
docker compose ps
docker compose logs db
```

If dependencies are stale after changing `requirements.txt`, rebuild:

```bash
docker compose build --no-cache api
```

## Hosting Notes

The Dockerfile respects the platform `PORT` environment variable and falls back to
`8000` locally.

For a simple Railway deployment, configure:

- `API_KEY`
- `DATABASE_URL`

On Railway, `DATABASE_URL` must come from the Railway PostgreSQL service. Do not
use the local Compose host `db` in production.

The database tables will be created automatically when the API starts.

Railway setup guide:

```text
docs/railway-deploy.md
```
