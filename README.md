# pswdgen-api

Dockerized FastAPI microservice that generates passwords + Ed25519 SSH keys and estimates password entropy/crack time. Built for “ship-it” workflows: GitHub Actions CI runs lint + unit tests in a container, and CD publishes versioned images to GitHub Container Registry (GHCR) on `main`.

## API

Interactive OpenAPI docs:
- `GET /docs` (Swagger UI)
- `GET /openapi.json`

Endpoints:
- `GET /generate-pass`
  - Query: `length` (int, default `8`), `useUpper`/`useLower`/`useSpecial`/`useDigits` (bool, default `true`)
  - Returns: `{ password, entropy, crack_time }`
- `GET /generate-ssh`
  - Query: `name` (string, optional, max 64) — appended as the key comment
  - Returns: `{ private_key, public_key }` (OpenSSH formats)
- `GET /calculate-strength`
  - Query: `password` (string, default empty)
  - Returns: `{ entropy, crack_time }`

Examples:
```bash
curl "http://localhost:8000/generate-pass?length=24&useSpecial=false"
curl "http://localhost:8000/generate-ssh?name=me@laptop"
curl "http://localhost:8000/calculate-strength?password=correct%20horse%20battery%20staple"
```

## Deploy

### Run with Docker (from source)
```bash
docker build -t pswdgen-api:local .
docker run --rm -p 8000:8000 pswdgen-api:local
```

### Run with Docker (from GHCR)
```bash
docker pull ghcr.io/<github-owner>/pswdgen-api:latest
docker run --rm -p 8000:8000 ghcr.io/<github-owner>/pswdgen-api:latest
```

## Local development
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Note: `/generate-pass` uses Python’s `random` module (not a cryptographically secure RNG).
