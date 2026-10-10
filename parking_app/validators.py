"""Input validation helpers (Poka-Yoke: prevent errors before saving)."""
import re

VEHICLE_TYPES = ("Car", "Bike", "SUV", "Other")

def normalize_vehicle_number(value: str) -> str:
    return re.sub(r"\s+", "", value or "").upper()

def validate_vehicle(vehicle_number: str, owner_name: str, vehicle_type: str) -> tuple[str, str, str]:
    number = normalize_vehicle_number(vehicle_number)
    owner = (owner_name or "").strip()
    kind = (vehicle_type or "").strip()
    if not number:
        raise ValueError("Vehicle registration number is required.")
    if len(number) > 20 or not re.fullmatch(r"[A-Z0-9-]+", number):
        raise ValueError("Use only letters, digits, and hyphens in the registration number.")
    if not owner:
        raise ValueError("Owner name is required.")
    if len(owner) > 80:
        raise ValueError("Owner name must be 80 characters or fewer.")
    if kind not in VEHICLE_TYPES:
        raise ValueError("Choose a valid vehicle type.")
    return number, owner, kind

def validate_settings(capacity: str | int, hourly_rate: str | float) -> tuple[int, float]:
    try:
        slots = int(capacity)
        rate = float(hourly_rate)
    except (TypeError, ValueError) as exc:
        raise ValueError("Capacity must be a whole number and hourly fee must be numeric.") from exc
    if slots < 1 or slots > 500:
        raise ValueError("Slot capacity must be between 1 and 500.")
    if rate < 0 or rate > 100000:
        raise ValueError("Hourly fee must be between ₹0 and ₹100,000.")
    return slots, rate
