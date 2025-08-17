# backend/app/utils/migrate_sqlite.py
from sqlalchemy import text
from sqlalchemy.engine import Engine

# columns we added in phase 2
NEEDED_COLS = {
    "temperature": "ALTER TABLE weather_history ADD COLUMN temperature FLOAT",
    "humidity":    "ALTER TABLE weather_history ADD COLUMN humidity FLOAT",
    "recorded_at": "ALTER TABLE weather_history ADD COLUMN recorded_at DATETIME",
}

def ensure_history_columns(engine: Engine) -> None:
    """
    Dev-only helper for SQLite: if your DB existed before Phase 2,
    add the new columns so models match the table. Safe to call every startup.
    """
    try:
        with engine.connect() as conn:
            cols = conn.execute(text("PRAGMA table_info(weather_history)")).fetchall()
            existing = {row[1] for row in cols}  # column name is index 1
            to_add = [sql for col, sql in NEEDED_COLS.items() if col not in existing]
            for ddl in to_add:
                conn.execute(text(ddl))
            if to_add:
                conn.commit()
    except Exception:
        # if table doesn't exist yet, create_all will handle it, so ignore here
        pass
