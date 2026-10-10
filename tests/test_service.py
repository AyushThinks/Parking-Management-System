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

if __name__ == "__main__": unittest.main()
