# Software Requirements Specification (SRS)

## 1. Purpose
ParkEase helps a small parking facility allocate spaces, record vehicle entry and exit, calculate parking charges, and retrieve parking history. It is a desktop educational prototype for BBAT104 Fundamentals of TQM.

## 2. Scope
Included: vehicle entry, automatic slot assignment, vehicle exit, fee calculation, search/filter, CSV export, settings, audit trail, dashboard and SQLite storage. Excluded: online payments, number-plate camera integration, multi-branch cloud sync, and real-time gate hardware.

## 3. Users
- Parking attendant: registers arrivals, marks exits, searches records.
- Supervisor: changes capacity and hourly rate, reviews logs and exports records.

## 4. Functional requirements
FR-01: The system shall register a vehicle with registration number, owner and type.
FR-02: The system shall normalize registration numbers and reject invalid or duplicate active vehicles.
FR-03: The system shall allocate the lowest available slot within configured capacity.
FR-04: The system shall reject entries when no slot is available.
FR-05: The system shall calculate billed hours by rounding any started hour up to a minimum of one hour.
FR-06: The system shall calculate fees from billed hours and configured hourly rate.
FR-07: The system shall display active and historical records.
FR-08: The system shall filter records by vehicle number, owner, slot and status.
FR-09: The system shall export records to CSV.
FR-10: The system shall prevent deleting an active parking record.
FR-11: The system shall validate capacity and fee settings.
FR-12: The system shall record important actions in an audit log.

## 5. Non-functional requirements
- Usability: labels and confirmation messages are clear.
- Reliability: transactions are committed or rolled back atomically.
- Data integrity: database constraints prevent duplicate active slots and vehicle registrations.
- Maintainability: UI, validation, configuration, persistence and business logic are separated.
- Portability: Python 3.10+ on systems with Tkinter.
- Performance target: typical local record searches should complete within 2 seconds for up to 10,000 records; this is a target to verify, not a measured result.

## 6. Assumptions and constraints
One local desktop instance is used at a time. Fees are billed per started hour. A parking record is retained after exit for reporting. SQLite database is local and should be backed up by the user.

## 7. Acceptance criteria
All functional requirements are manually demonstrated; automated service tests pass; invalid input and full-capacity cases show understandable errors; exports open as CSV; TQM artefacts are completed using observed project/test data.
