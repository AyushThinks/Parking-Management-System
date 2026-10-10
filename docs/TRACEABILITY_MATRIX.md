# Requirements Traceability Matrix

| Requirement | Implementation | Test/evidence |
|---|---|---|
| FR-01 vehicle entry | `ParkingService.park_vehicle`, Vehicle Entry tab | TC-01 |
| FR-02 duplicate prevention | `validators.py`, partial unique index | TC-02, TC-04 |
| FR-03 slot allocation | `ParkingService.park_vehicle` | TC-01 |
| FR-04 capacity boundary | service full-capacity check | TC-05 |
| FR-05/06 fee calculation | `ParkingService.exit_vehicle` | TC-06 and manual fee boundary check |
| FR-07 record list | `ParkingService.list_records` | Manual record-history check |
| FR-08 search/filter | Records & Exit tab | TC-10 |
| FR-09 CSV export | `ParkingService.export_csv` | TC-11 |
| FR-10 active-delete prevention | `ParkingService.delete_record` | TC-08 |
| FR-11 settings validation | `validators.validate_settings` | TC-09 |
| FR-12 audit trail | `_audit` and Settings & Audit tab | TC-12 |
