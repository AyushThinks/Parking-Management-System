"""Central application settings."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "parking.db"
DEFAULT_SLOT_CAPACITY = 20
DEFAULT_HOURLY_RATE = 30.0
CURRENCY_SYMBOL = "₹"
APP_NAME = "ParkEase | Parking Management"
