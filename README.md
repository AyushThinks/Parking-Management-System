# ParkEase — Parking Management System

A Python + Tkinter desktop application for managing parking slots, vehicle entry/exit, fee calculation, and parking history. Built for BBAT104 Fundamentals of TQM.

## Features
- Dashboard showing total, occupied, and available slots and active vehicles
- Vehicle entry with unique registration validation and automatic slot allocation
- Vehicle exit with duration-based fee calculation and receipt details
- Search/filter parking records, view history, and export records to CSV
- Configurable slot capacity and hourly fee
- SQLite persistence, input validation, audit log, friendly error messages
- TQM artefacts: SRS, SIPOC, CTQ tree, FMEA/RPN, defect checksheet, Pareto and Fishbone analysis, PDCA log

## Requirements
- Python 3.10+
- Tkinter (included with most standard Windows Python installations)
- Optional: `matplotlib` for charts (`pip install matplotlib`)

## Run on Windows
1. Extract the project folder.
2. Open PowerShell in the folder.
3. Run `python -m parking_app`.

Database is created automatically at `data/parking.db` on first launch.

## Run tests
`python -m unittest discover -s tests -v`

## Generate TQM charts
`python reports/generate_sqc_charts.py` (requires matplotlib).

## GitHub
Create a public repository named `BBAT104_TQM_<RegNo>`, then follow `docs/GITHUB_WORKFLOW.md` to push this repository. The included history has 30 meaningful project commits for demonstration; continue making your own commits as you develop and test the project.

## Important academic note
The guidelines assign a Quality Goal (Q01–Q20) based on the allotment sheet. This starter implements a balanced set of quality features; adjust the selected five features to match your individually assigned goal before submission. Replace sample defect counts and assumptions with observations from your own testing.
