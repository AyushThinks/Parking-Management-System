# User Manual

## Start the application
1. Install Python 3.10 or newer.
2. Open a terminal in the project root.
3. Run `python -m parking_app`.
4. The app creates `data/parking.db` automatically.

## Register a vehicle
1. Open **Vehicle Entry**.
2. Enter registration number, owner name and vehicle type.
3. Click **Allocate slot & save entry**.
4. Record the displayed slot number. Duplicate active registrations and full parking are rejected.

## Record vehicle exit
1. Open **Records & Exit** and filter to `Parked` if needed.
2. Select the vehicle row.
3. Click **Mark selected vehicle as exited / calculate fee**.
4. Confirm the action and review the receipt. Any started hour is billed as a full hour, with a minimum of one hour.

## Search and export
Search by registration number, owner, or slot. Select a status filter and click **Search / Filter**. Click **Export CSV** to save the full record history.

## Change settings
Open **Settings & Audit**. Set total capacity (1–500) and fee per started hour. The application prevents reducing capacity below the highest currently occupied slot number.

## Troubleshooting
- **Parking is full:** record an exit or increase capacity if authorized.
- **Duplicate vehicle:** search active records and confirm whether the vehicle is already parked.
- **Database error:** close other instances, check folder write permission and preserve a copy of the database before troubleshooting.
- **App will not launch:** check Python installation and Tkinter availability.
