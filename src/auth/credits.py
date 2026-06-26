import sqlite3
import os
from src.cost_config import FREE_RUNS, STAR_BONUS_RUNS
from src.auth.github_api import has_starred, has_forked, validate_username

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "pipeline_runs.db")


def _conn():
    return sqlite3.connect(DB_PATH)


def _init_users_table():
    with _conn() as c:
        c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                github_username TEXT PRIMARY KEY,
                runs_used INTEGER DEFAULT 0,
                has_forked INTEGER DEFAULT 0,
                has_starred INTEGER DEFAULT 0,
                using_byok INTEGER DEFAULT 0,
                first_seen TEXT,
                last_seen TEXT
            )
        """)


def get_or_create_user(username: str) -> dict:
    _init_users_table()
    from datetime import datetime
    now = datetime.utcnow().isoformat()
    with _conn() as c:
        row = c.execute(
            "SELECT * FROM users WHERE github_username=?", (username,)
        ).fetchone()
        if not row:
            c.execute(
                "INSERT INTO users VALUES (?,0,0,0,0,?,?)",
                (username, now, now)
            )
            row = c.execute(
                "SELECT * FROM users WHERE github_username=?", (username,)
            ).fetchone()
        else:
            c.execute("UPDATE users SET last_seen=? WHERE github_username=?", (now, username))

    cols = ["github_username", "runs_used", "has_forked", "has_starred", "using_byok", "first_seen", "last_seen"]
    return dict(zip(cols, row))


def refresh_github_status(username: str) -> dict:
    _init_users_table()
    forked = 1 if has_forked(username) else 0
    starred = 1 if has_starred(username) else 0
    with _conn() as c:
        c.execute(
            "UPDATE users SET has_forked=?, has_starred=? WHERE github_username=?",
            (forked, starred, username)
        )
    return {"has_forked": bool(forked), "has_starred": bool(starred)}


def get_credits(username: str) -> dict:
    user = get_or_create_user(username)
    max_free = FREE_RUNS + (STAR_BONUS_RUNS if user["has_starred"] else 0)
    runs_used = user["runs_used"]
    remaining = max(0, max_free - runs_used)
    can_run_free = remaining > 0
    needs_byok = not can_run_free and not user["using_byok"]
    return {
        "runs_used": runs_used,
        "max_free_runs": max_free,
        "remaining_free": remaining,
        "can_run_free": can_run_free,
        "needs_byok": needs_byok,
        "using_byok": bool(user["using_byok"]),
        "has_forked": bool(user["has_forked"]),
        "has_starred": bool(user["has_starred"]),
    }


def record_run(username: str):
    _init_users_table()
    with _conn() as c:
        c.execute(
            "UPDATE users SET runs_used = runs_used + 1 WHERE github_username=?",
            (username,)
        )


def enable_byok(username: str):
    _init_users_table()
    with _conn() as c:
        c.execute(
            "UPDATE users SET using_byok=1 WHERE github_username=?",
            (username,)
        )


def can_run(username: str, byok_key: str = None) -> tuple[bool, str]:
    credits = get_credits(username)
    if credits["can_run_free"]:
        return True, "free"
    if byok_key:
        enable_byok(username)
        return True, "byok"
    return False, "no_credits"
