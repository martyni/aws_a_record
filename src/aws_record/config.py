"""Config module for webapp (Flask + Flask-SQLAlchemy)."""

from __future__ import annotations

from pathlib import Path
from secrets import choice
import string
import os


# Project root: .../src/webapp/config.py -> .../src/webapp
BASE_DIR = Path(__file__).resolve().parent

# Where to store per-instance files (recommended by Flask)
# You can change this to BASE_DIR / "instance" if you prefer.
INSTANCE_DIR = BASE_DIR / "instance"
INSTANCE_DIR.mkdir(parents=True, exist_ok=True)

# Default locations
DEFAULT_SECRET_FILE = Path("~/.webapp.secret").expanduser()
DEFAULT_DB_FILE = INSTANCE_DIR / "webapp.sqlite3"


def _random_string(length: int, alphabet: str) -> str:
    return "".join(choice(alphabet) for _ in range(length))


def get_or_create_secret(
    secret_file: Path = DEFAULT_SECRET_FILE,
    secret_length: int = 32,
) -> str:
    """
    Read SECRET_KEY from secret_file if it exists; otherwise generate and save one.
    """
    secret_file = secret_file.expanduser()

    if secret_file.exists():
        secret = secret_file.read_text(encoding="utf-8").strip()
        if secret:
            return secret

    # Generate a strong secret
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{};:,.?/\\|~"
    secret = _random_string(secret_length, alphabet)

    secret_file.parent.mkdir(parents=True, exist_ok=True)
    secret_file.write_text(secret, encoding="utf-8")
    return secret


# Allow environment variable overrides (useful for production)
SECRET_KEY = os.getenv("SECRET_KEY") or get_or_create_secret()

DB_PATH = Path(
    os.getenv(
        "DATABASE_PATH",
        str(DEFAULT_DB_FILE))).expanduser().resolve()
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# Create the DB file if missing (SQLite will also create it, but touching
# is fine)
DB_PATH.touch(exist_ok=True)

# IMPORTANT: absolute SQLite path needs four slashes.
# Example: sqlite:////home/user/project/instance/webapp.sqlite3
SQLALCHEMY_DATABASE_URI = f"sqlite:////{DB_PATH.as_posix().lstrip('/')}" if os.name == "posix" else f"sqlite:///{DB_PATH}"  # pylint: disable=locally-disabled, multiple-statements, fixme, line-too-long


SQLALCHEMY_TRACK_MODIFICATIONS = False

# Optional: good defaults for SQLAlchemy engine behavior
SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_pre_ping": True,
}
