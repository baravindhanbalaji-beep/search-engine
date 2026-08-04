from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

DATA_DIR = PROJECT_ROOT / "data"
PAGE_DIR = DATA_DIR / "pages"

DATABASE_DIR = PROJECT_ROOT / "database"
DB_PATH = DATABASE_DIR / "search_engine.db"

LOG_DIR = PROJECT_ROOT / "logs"