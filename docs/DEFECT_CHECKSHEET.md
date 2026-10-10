# Defect Log and Checksheet

Use this template during actual testing. The example rows below are **test categories**, not claims that defects were observed.

| Date | Test case | Defect category | Count | Severity (1–5) | Status | Evidence / fix |
|---|---|---|---:|---:|---|---|
| YYYY-MM-DD | Duplicate active vehicle | Data integrity | 0 | 4 | Not observed / update after test | Test duplicate registration twice |
| YYYY-MM-DD | Capacity boundary | Slot allocation | 0 | 5 | Not observed / update after test | Fill all slots and attempt one more entry |
| YYYY-MM-DD | Invalid form input | Validation | 0 | 3 | Not observed / update after test | Try blank/invalid values |
| YYYY-MM-DD | Fee rounding | Billing | 0 | 4 | Not observed / update after test | Check entry/exit around hour boundaries |
| YYYY-MM-DD | CSV export | Reporting | 0 | 2 | Not observed / update after test | Compare row count and columns |
| YYYY-MM-DD | Search filters | Usability | 0 | 2 | Not observed / update after test | Search owner, vehicle and status |

After testing, replace the placeholder date/status and enter actual counts. Use the resulting frequencies for Pareto analysis.
