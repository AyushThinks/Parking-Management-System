# SIPOC Process Map — Vehicle Parking

| Suppliers | Inputs | Process | Outputs | Customers |
|---|---|---|---|---|
| Driver | Vehicle registration, owner name, type | Validate details | Accepted/rejected entry | Driver |
| Parking attendant | Entry information | Find first free slot | Slot number and entry timestamp | Attendant and driver |
| Supervisor | Capacity and hourly rate | Store settings | Updated operating rules | Parking staff |
| Parking attendant | Active record and exit request | Calculate billed hours and fee | Exit receipt and released slot | Driver and supervisor |
| SQLite database | Saved parking records | Search and export | Filtered records / CSV | Supervisor |

**Process boundary:** from collecting vehicle details through slot assignment and exit recording. External payment processing and physical barrier control are out of scope.
