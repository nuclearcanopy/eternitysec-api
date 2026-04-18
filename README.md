# eternitysec

fastapi service for password generation, ssh key generation, and totp storage and code generation.

base url is `http://localhost:8000` by default.

## run

### docker

build:

```bash
docker build -t eternitysec:local .
```

run:

```bash
docker run --rm -p 8000:8000 -e TOTP_ENCRYPTION_KEY="$(python -c 'import os; print(os.urandom(32).hex())')" eternitysec:local
```

notes:
- `TOTP_ENCRYPTION_KEY` is required at process start.
- it must be 32 bytes hex (64 hex chars).
- keep the same key if you want to decrypt previously stored secrets.
- the service creates `database.db` in the working directory.

persist totp data with docker:

```bash
mkdir -p data && touch data/database.db
docker run --rm -p 8000:8000 \
  -e TOTP_ENCRYPTION_KEY="..." \
  -v "$(pwd)/data/database.db:/app/database.db" \
  eternitysec:local
```

### local

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export TOTP_ENCRYPTION_KEY="$(python -c 'import os; print(os.urandom(32).hex())')"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## openapi

- `get /docs`
- `get /openapi.json`

## errors and limits

common responses:
- `422` for request validation errors (fastapi).
- `429` for rate limit errors (slowapi).

totp auth errors:
- `401` with `{"detail":"Invalid credentials"}` when the client number or pin is wrong.

rate limits:
- `post /totp/account`: `3/hour`
- `delete /totp/account`: `1/hour`
- `post /totp/secret`: `1/sec`
- `delete /totp/secret`: `1/sec`
- `get /totp/codes`: `3/minute`
- `get /totp/codes_encrypted`: `3/minute`

## endpoints

### password

`get /generate-pass`

query:
- `length` (int, default `8`)
- `useUpper` (bool, default `true`)
- `useLower` (bool, default `true`)
- `useSpecial` (bool, default `true`)
- `useDigits` (bool, default `true`)

responses:
- `200` returns `{"password": "...", "entropy": <float>, "crack_time": "<string>"}`
- `400` returns `{"detail":"All options disabled"}` when all `use*` flags are `false`

example:

```bash
curl "http://localhost:8000/generate-pass?length=24&useSpecial=false"
```

`get /calculate-strength`

query:
- `password` (string, default empty)

response:
- `200` returns `{"entropy": <float>, "crack_time": "<string>"}`

example:

```bash
curl "http://localhost:8000/calculate-strength?password=correct%20horse%20battery%20staple"
```

notes:
- `/generate-pass` uses `random.choices`, not a cryptographically secure rng.
- crack time is a rough estimate based on a fixed guesses-per-second constant.

### ssh

`get /generate-ssh`

query:
- `name` (string, default empty, max 64). it is appended to the public key as the comment.

response:
- `200` returns:
  - `private_key` (openssh private key, pem text)
  - `public_key` (openssh public key, single line)
  - `sha_fingerprint` (sha256 fingerprint string, `SHA256:...`)

example:

```bash
curl "http://localhost:8000/generate-ssh?name=me@laptop"
```

### totp

totp data is stored in sqlite in `database.db`.
pins are hashed with argon2.
secrets are encrypted with aes-gcm using `TOTP_ENCRYPTION_KEY`.

`post /totp/account`

body:

```json
{ "pin": "123456" }
```

response:
- `200` returns `{"client_number":"<16 digits>"}`

`post /totp/secret`

body:

```json
{ "number": "<16 digits>", "pin": "123456", "label": "github", "secret": "JBSWY3DPEHPK3PXP" }
```

notes:
- `secret` should be a base32 totp secret.
- it is encrypted before it is stored.

response:
- `200` returns `{"status":"ok"}`
- `401` on invalid credentials

`get /totp/codes`

query:
- `number` (string, 16 digits)
- `pin` (string, min 6 chars)

response:
- `200` returns `{"codes":[{"label":"...", "code":"123456"}]}`
- `401` on invalid credentials

example:

```bash
curl "http://localhost:8000/totp/codes?number=0000000000000000&pin=123456"
```

`get /totp/codes_encrypted`

query:
- `number`
- `pin`

response:
- `200` returns `{"secrets":[{"label":"...", "encrypted_secret":"<base64>"}]}`
- `401` on invalid credentials

`delete /totp/secret`

body:

```json
{ "number": "<16 digits>", "pin": "123456", "label": "github" }
```

response:
- `200` returns `{"status":"ok"}`
- `401` on invalid credentials

`delete /totp/account`

body:

```json
{ "number": "<16 digits>", "pin": "123456" }
```

response:
- `200` returns `{"status":"ok"}`
- `401` on invalid credentials
