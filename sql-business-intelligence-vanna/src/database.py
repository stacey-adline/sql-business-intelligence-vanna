import re
import sqlite3
from pathlib import Path
from src.config import DATABASE_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS orders (
    row_id INTEGER PRIMARY KEY,
    order_id TEXT NOT NULL,
    order_date TEXT NOT NULL,
    ship_date TEXT NOT NULL,
    ship_mode TEXT,
    customer_id TEXT,
    customer_name TEXT,
    segment TEXT,
    country TEXT,
    city TEXT,
    state TEXT,
    postal_code TEXT,
    region TEXT,
    product_id TEXT,
    category TEXT,
    sub_category TEXT,
    product_name TEXT,
    sales REAL NOT NULL,
    quantity INTEGER NOT NULL,
    discount REAL NOT NULL,
    profit REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_orders_date ON orders(order_date);
CREATE INDEX IF NOT EXISTS idx_orders_region ON orders(region);
CREATE INDEX IF NOT EXISTS idx_orders_category ON orders(category);
"""

def get_connection(read_only=False):
    db_path = Path(DATABASE_PATH)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    if read_only:
        if not db_path.exists():
            raise FileNotFoundError("Database not found. Run: python -m src.seed_data")
        conn = sqlite3.connect(f"file:{db_path.resolve().as_posix()}?mode=ro", uri=True)
    else:
        conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def initialise_database():
    with get_connection() as conn:
        conn.executescript(SCHEMA)

def is_safe_read_query(sql: str) -> bool:
    """Allow one read-only SELECT/WITH statement; reject mutating SQL."""
    if not sql or not sql.strip():
        return False
    cleaned = re.sub(r"/\*.*?\*/|--[^\n]*", "", sql, flags=re.S).strip()
    if ";" in cleaned.rstrip(";"):
        return False
    normalized = cleaned.lstrip().lower()
    if not (normalized.startswith("select") or normalized.startswith("with")):
        return False
    forbidden = r"\b(insert|update|delete|drop|alter|create|replace|attach|detach|pragma|vacuum|reindex|transaction)\b"
    return re.search(forbidden, normalized, flags=re.I) is None

def run_read_query(sql: str):
    if not is_safe_read_query(sql):
        raise ValueError("Only a single read-only SELECT/WITH query is allowed.")
    with get_connection(read_only=True) as conn:
        return conn.execute(sql).fetchall()
