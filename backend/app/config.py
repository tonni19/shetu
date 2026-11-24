# FILE:        backend/app/config.py
# PURPOSE:     One place that reads settings from environment variables, with safe defaults
#              for a student laptop. Every other module imports `settings` from here.
# OWNER:       Maruf (board row T1)
# DEPENDS ON:  nothing
# USED BY:     app/db.py (database address), app/main.py (session secret, allowed origins)
# STATUS:      REAL
# DATA:        No secrets in this file. Real values go in backend/.env (git-ignored) or the shell.
# AI NOTE:     The default secret key is only for local development. It is printed as a warning
#              at start-up so nobody deploys it by accident. Never commit a real key.

import os
from dataclasses import dataclass, field

DEV_SECRET = "dev-only-change-me"


def _split(value: str) -> list[str]:
    """Turn "a, b" into ["a", "b"], ignoring blanks. Used for the list of allowed origins."""
    return [part.strip() for part in value.split(",") if part.strip()]


@dataclass(frozen=True)
class Settings:
    # Where the SQLite database file lives. Relative paths are relative to where uvicorn starts
    # (normally the backend/ folder). Tests replace this with a temporary file.
    database_url: str = field(default_factory=lambda: os.getenv("SHETU_DATABASE_URL", "sqlite:///./shetu.db"))

    # Signs the session cookie so a user cannot forge "I am the manager". See app/main.py.
    secret_key: str = field(default_factory=lambda: os.getenv("SHETU_SECRET_KEY", DEV_SECRET))

    # Browser origins allowed to call the API directly (CORS). The React dev server runs on
    # port 5173. If Tonni's Vite app uses a proxy for /api (recommended), CORS is not even needed.
    cors_origins: list[str] = field(
        default_factory=lambda: _split(os.getenv("SHETU_CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"))
    )


settings = Settings()
