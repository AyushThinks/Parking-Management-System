# PDCA Continuous Improvement Log

| Cycle | Plan | Do | Check | Act |
|---|---|---|---|---|
| 1 — Duplicate prevention | Prevent duplicate active registrations | Normalize registration and check active record before insert | Run duplicate-entry test | Retain validation and database index; log test evidence |
| 2 — Slot utilization | Avoid assigning occupied slots and show full status | Allocate the first free slot within capacity | Fill all configured slots and attempt another entry | Keep capacity-boundary regression test |
| 3 — Fee transparency | Make exit fees predictable | Bill started hours × hourly rate and show receipt | Verify receipt and formula against sample durations | Clarify billing rule in the user manual |

Document each future cycle with a dated issue, observed evidence, action owner and re-test result. Do not claim improvement percentages unless measurements support them.
