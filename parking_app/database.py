"""SQLite connection and schema management."""
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from parking_app.config import DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS parking_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_number TEXT NOT NULL,
    owner_name TEXT NOT NULL,
    vehicle_type TEXT NOT NULL CHECK(vehicle_type IN ('Car','Bike','SUV','Other')),
    slot_number INTEGER NOT NULL,
    entry_time TEXT NOT NULL,
    exit_time TEXT,
    duration_hours REAL,
    fee REAL,
    status TEXT NOT NULL DEFAULT 'Parked' CHECK(status IN ('Parked','Exited'))
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_active_vehicle
ON parking_records(vehicle_number) WHERE status = 'Parked';
CREATE UNIQUE INDEX IF NOT EXISTS idx_active_slot
ON parking_records(slot_number) WHERE status = 'Parked';
CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action TEXT NOT NULL,
    details TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""

@contextmanager
def connect(db_path: Path | str = DB_PATH):
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

def initialize_database(db_path: Path | str = DB_PATH) -> None:
    with connect(db_path) as con:
        con.executescript(SCHEMA)
        con.execute("INSERT OR IGNORE INTO settings(key,value) VALUES('slot_capacity','20')")
        con.execute("INSERT OR IGNORE INTO settings(key,value) VALUES('hourly_rate','30')")
