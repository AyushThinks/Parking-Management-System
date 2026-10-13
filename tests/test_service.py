"""Automated tests for core parking business rules."""
import tempfile
import unittest
from pathlib import Path
from parking_app.service import ParkingService

class ParkingServiceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.db = Path(self.temp.name) / "test.db"
        self.service = ParkingService(self.db)
        self.service.update_settings(2, 25)

    def tearDown(self):
        self.temp.cleanup()

    def test_vehicle_entry_allocates_first_available_slot(self):
        first = self.service.park_vehicle("hr 26 ab 1234", "Asha", "Car")
        second = self.service.park_vehicle("DL-01-X-5555", "Ravi", "Bike")
        self.assertEqual(first["slot_number"], 1)
        self.assertEqual(second["slot_number"], 2)
        self.assertEqual(first["vehicle_number"], "HR26AB1234")

    def test_duplicate_active_vehicle_is_rejected(self):
        self.service.park_vehicle("UP-16-AB-1234", "Asha", "Car")
        with self.assertRaisesRegex(ValueError, "already parked"):
            self.service.park_vehicle("up-16-ab-1234", "Asha", "Car")

    def test_full_parking_rejects_third_vehicle(self):
        self.service.park_vehicle("HR01AA1", "Asha", "Car")
        self.service.park_vehicle("HR01AA2", "Ravi", "Bike")
        with self.assertRaisesRegex(ValueError, "Parking is full"):
            self.service.park_vehicle("HR01AA3", "Neha", "SUV")

    def test_required_fields_are_validated(self):
        with self.assertRaisesRegex(ValueError, "registration number is required"):
            self.service.park_vehicle("", "Asha", "Car")

    def test_active_vehicle_cannot_be_deleted(self):
        record = self.service.park_vehicle("HR01AA1", "Asha", "Car")
        with self.assertRaisesRegex(ValueError, "active vehicle cannot be deleted"):
            self.service.delete_record(record["id"])

    def test_settings_reject_invalid_capacity(self):
        with self.assertRaises(ValueError): self.service.update_settings(0, 30)

    def test_audit_log_is_written(self):
        self.service.park_vehicle("HR01AA1", "Asha", "Car")
        self.assertEqual(self.service.audit_logs()[0]["action"], "VEHICLE_ENTRY")

    def test_vehicle_exit_calculates_fee_and_frees_slot(self):
        first = self.service.park_vehicle("HR26AB1000", "Asha", "Car")
        self.assertEqual(first["slot_number"], 1)

        # Exit vehicle and verify fee calculation (hourly_rate = 25, duration >= 1 hr)
        receipt = self.service.exit_vehicle(first["id"])
        self.assertEqual(receipt["status"] if "status" in receipt else receipt["id"], first["id"])
        self.assertEqual(receipt["duration_hours"], 1)
        self.assertEqual(receipt["fee"], 25.0)

        # Check records updated
        records = self.service.list_records(status="Exited")
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["status"], "Exited")

        # Slot 1 should now be free for the next vehicle
        second = self.service.park_vehicle("DL01X9999", "Ravi", "Bike")
        self.assertEqual(second["slot_number"], 1)

    def test_exit_nonexistent_or_already_exited_vehicle_raises_error(self):
        with self.assertRaisesRegex(ValueError, "Active parking record not found"):
            self.service.exit_vehicle(9999)

        record = self.service.park_vehicle("HR01AA1", "Asha", "Car")
        self.service.exit_vehicle(record["id"])
        with self.assertRaisesRegex(ValueError, "Active parking record not found"):
            self.service.exit_vehicle(record["id"])

    def test_delete_exited_record(self):
        record = self.service.park_vehicle("HR01AA1", "Asha", "Car")
        self.service.exit_vehicle(record["id"])
        self.service.delete_record(record["id"])
        self.assertEqual(len(self.service.list_records()), 0)

        with self.assertRaisesRegex(ValueError, "Record does not exist"):
            self.service.delete_record(record["id"])

    def test_list_records_search_and_filter(self):
        self.service.park_vehicle("HR01AA1111", "Asha Sharma", "Car")
        r2 = self.service.park_vehicle("DL02BB2222", "Ravi Verma", "Bike")
        self.service.exit_vehicle(r2["id"])

        self.assertEqual(len(self.service.list_records(status="Parked")), 1)
        self.assertEqual(len(self.service.list_records(status="Exited")), 1)
        self.assertEqual(len(self.service.list_records(search="Asha")), 1)
        self.assertEqual(len(self.service.list_records(search="2222")), 1)

    def test_export_csv(self):
        self.service.park_vehicle("HR01AA1111", "Asha", "Car")
        csv_path = Path(self.temp.name) / "export_test.csv"
        count = self.service.export_csv(csv_path)
        self.assertEqual(count, 1)
        self.assertTrue(csv_path.exists())
        content = csv_path.read_text(encoding="utf-8-sig")
        self.assertIn("vehicle_number", content)
        self.assertIn("HR01AA1111", content)

    def test_database_persistence_across_service_instances(self):
        self.service.park_vehicle("HR01AA1111", "Asha", "Car")

        # New service instance on the same SQLite database file
        new_service = ParkingService(self.db)
        records = new_service.list_records()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["vehicle_number"], "HR01AA1111")
        self.assertEqual(new_service.get_settings()["hourly_rate"], 25.0)

    def test_dashboard_metrics(self):
        dash_initial = self.service.dashboard()
        self.assertEqual(dash_initial["total_slots"], 2)
        self.assertEqual(dash_initial["occupied"], 0)
        self.assertEqual(dash_initial["available"], 2)
        self.assertEqual(dash_initial["today_income"], 0.0)

        record = self.service.park_vehicle("HR01AA1111", "Asha", "Car")
        dash_parked = self.service.dashboard()
        self.assertEqual(dash_parked["occupied"], 1)
        self.assertEqual(dash_parked["available"], 1)

        self.service.exit_vehicle(record["id"])
        dash_exited = self.service.dashboard()
        self.assertEqual(dash_exited["occupied"], 0)
        self.assertEqual(dash_exited["available"], 2)
        self.assertEqual(dash_exited["today_income"], 25.0)

if __name__ == "__main__":
    unittest.main()
