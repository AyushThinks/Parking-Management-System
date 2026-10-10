"""Business rules for parking operations."""
import csv
from datetime import datetime
from pathlib import Path
from parking_app.config import DB_PATH
from parking_app.database import connect, initialize_database
from parking_app.validators import validate_vehicle, validate_settings

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

def now_text() -> str:
    return datetime.now().replace(microsecond=0).strftime(TIME_FORMAT)

class ParkingService:
    def __init__(self, db_path: Path | str = DB_PATH):
        self.db_path = Path(db_path)
        initialize_database(self.db_path)

    def _audit(self, con, action: str, details: str) -> None:
        con.execute("INSERT INTO audit_log(action,details,created_at) VALUES(?,?,?)", (action, details, now_text()))

    def get_settings(self) -> dict:
        with connect(self.db_path) as con:
            values = {r["key"]: r["value"] for r in con.execute("SELECT key,value FROM settings")}
        return {"slot_capacity": int(values.get("slot_capacity", 20)), "hourly_rate": float(values.get("hourly_rate", 30))}

    def update_settings(self, capacity, hourly_rate) -> None:
        slots, rate = validate_settings(capacity, hourly_rate)
        with connect(self.db_path) as con:
            highest = con.execute("SELECT COALESCE(MAX(slot_number),0) FROM parking_records WHERE status='Parked'").fetchone()[0]
            if highest > slots:
                raise ValueError(f"Cannot reduce capacity below active slot number {highest}.")
            con.execute("INSERT OR REPLACE INTO settings(key,value) VALUES('slot_capacity',?)", (str(slots),))
            con.execute("INSERT OR REPLACE INTO settings(key,value) VALUES('hourly_rate',?)", (str(rate),))
            self._audit(con, "SETTINGS_UPDATED", f"Capacity={slots}; hourly_rate={rate}")

    def dashboard(self) -> dict:
        settings = self.get_settings()
        with connect(self.db_path) as con:
            occupied = con.execute("SELECT COUNT(*) FROM parking_records WHERE status='Parked'").fetchone()[0]
            today = datetime.now().strftime("%Y-%m-%d")
            income = con.execute("SELECT COALESCE(SUM(fee),0) FROM parking_records WHERE status='Exited' AND exit_time LIKE ?", (today + "%",)).fetchone()[0]
        return {"total_slots": settings["slot_capacity"], "occupied": occupied,
                "available": max(0, settings["slot_capacity"] - occupied), "active_vehicles": occupied,
                "today_income": float(income), "hourly_rate": settings["hourly_rate"]}

    def park_vehicle(self, vehicle_number: str, owner_name: str, vehicle_type: str) -> dict:
        number, owner, kind = validate_vehicle(vehicle_number, owner_name, vehicle_type)
        with connect(self.db_path) as con:
            duplicate = con.execute("SELECT id FROM parking_records WHERE vehicle_number=? AND status='Parked'", (number,)).fetchone()
            if duplicate:
                raise ValueError(f"Vehicle {number} is already parked (record #{duplicate['id']}).")
            settings = {r["key"]: r["value"] for r in con.execute("SELECT key,value FROM settings")}
            capacity = int(settings.get("slot_capacity", 20))
            occupied = {r[0] for r in con.execute("SELECT slot_number FROM parking_records WHERE status='Parked'")}
            slot = next((n for n in range(1, capacity + 1) if n not in occupied), None)
            if slot is None:
                raise ValueError("Parking is full. No slot is currently available.")
            entry = now_text()
            cur = con.execute("INSERT INTO parking_records(vehicle_number,owner_name,vehicle_type,slot_number,entry_time) VALUES(?,?,?,?,?)", (number, owner, kind, slot, entry))
            self._audit(con, "VEHICLE_ENTRY", f"{number} assigned slot {slot}")
            return {"id": cur.lastrowid, "vehicle_number": number, "owner_name": owner, "vehicle_type": kind, "slot_number": slot, "entry_time": entry}

    def exit_vehicle(self, record_id: int) -> dict:
        with connect(self.db_path) as con:
            row = con.execute("SELECT * FROM parking_records WHERE id=? AND status='Parked'", (record_id,)).fetchone()
            if not row:
                raise ValueError("Active parking record not found. Refresh the list and try again.")
            exit_time = datetime.now().replace(microsecond=0)
            entry_time = datetime.strptime(row["entry_time"], TIME_FORMAT)
            seconds = max(0, (exit_time - entry_time).total_seconds())
            duration = max(1, int((seconds + 3599) // 3600))
            settings = {r["key"]: r["value"] for r in con.execute("SELECT key,value FROM settings")}
            rate = float(settings.get("hourly_rate", 30))
            fee = round(duration * rate, 2)
            exit_text = exit_time.strftime(TIME_FORMAT)
            con.execute("UPDATE parking_records SET exit_time=?,duration_hours=?,fee=?,status='Exited' WHERE id=?", (exit_text, duration, fee, record_id))
            self._audit(con, "VEHICLE_EXIT", f"{row['vehicle_number']} exited slot {row['slot_number']}; fee={fee}")
            return {"id": record_id, "vehicle_number": row["vehicle_number"], "owner_name": row["owner_name"], "slot_number": row["slot_number"], "entry_time": row["entry_time"], "exit_time": exit_text, "duration_hours": duration, "fee": fee}

    def list_records(self, search: str = "", status: str = "All") -> list[dict]:
        sql = "SELECT * FROM parking_records WHERE 1=1"
        params: list = []
        if status in ("Parked", "Exited"):
            sql += " AND status=?"; params.append(status)
        term = (search or "").strip()
        if term:
            sql += " AND (vehicle_number LIKE ? OR owner_name LIKE ? OR CAST(slot_number AS TEXT) LIKE ?)"
            params.extend([f"%{term}%"] * 3)
        sql += " ORDER BY id DESC"
        with connect(self.db_path) as con:
            return [dict(r) for r in con.execute(sql, params).fetchall()]

    def delete_record(self, record_id: int) -> None:
        with connect(self.db_path) as con:
            row = con.execute("SELECT vehicle_number,status FROM parking_records WHERE id=?", (record_id,)).fetchone()
            if not row:
                raise ValueError("Record does not exist.")
            if row["status"] == "Parked":
                raise ValueError("An active vehicle cannot be deleted. Record its exit first.")
            con.execute("DELETE FROM parking_records WHERE id=?", (record_id,))
            self._audit(con, "RECORD_DELETED", f"Deleted record #{record_id} ({row['vehicle_number']})")

    def export_csv(self, output_path: Path | str) -> int:
        records = self.list_records()
        fields = ["id", "vehicle_number", "owner_name", "vehicle_type", "slot_number", "entry_time", "exit_time", "duration_hours", "fee", "status"]
        path = Path(output_path); path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="", encoding="utf-8-sig") as file:
            writer = csv.DictWriter(file, fieldnames=fields); writer.writeheader()
            writer.writerows({key: row.get(key) for key in fields} for row in records)
        with connect(self.db_path) as con:
            self._audit(con, "CSV_EXPORTED", f"Exported {len(records)} records to {path.name}")
        return len(records)

    def audit_logs(self, limit: int = 100) -> list[dict]:
        with connect(self.db_path) as con:
            return [dict(r) for r in con.execute("SELECT * FROM audit_log ORDER BY id DESC LIMIT ?", (limit,))]
