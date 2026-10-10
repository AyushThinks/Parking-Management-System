# Failure Mode and Effects Analysis (FMEA)

Scale: Severity (S), Occurrence (O), Detection difficulty (D): 1 = low/easy, 10 = high/difficult. RPN = S × O × D. These are initial illustrative ratings; revise them based on actual tests and user feedback.

| Failure mode | Effect | Possible cause | Existing/preventive control | S | O | D | RPN | Recommended action |
|---|---|---|---|---:|---:|---:|---:|---|
| Duplicate vehicle entry | Conflicting active records | Attendant repeats entry | Pre-add query and unique partial index | 7 | 4 | 3 | 84 | Keep duplicate-entry regression test |
| Slot assigned twice | Two vehicles compete for space | Concurrent/incorrect allocation | Unique partial index on active slot | 8 | 3 | 3 | 72 | Test constraint failure and user feedback |
| Invalid registration text | Search/report mismatch | Typing errors | Normalization and validation | 5 | 5 | 3 | 75 | Add examples to user manual |
| Parking full but entry accepted | Over-capacity operation | Capacity check omitted | Free-slot search and full check | 8 | 3 | 4 | 96 | Test full-capacity scenario |
| Incorrect fee | Customer dispute | Wrong rounding/rate | Central fee calculation rule | 7 | 4 | 5 | 140 | Add controlled clock tests in future |
| Active record deleted | Lost operational state | Accidental deletion | Service blocks active deletion | 8 | 2 | 3 | 48 | Keep confirmation and deletion test |
| Database unavailable | Operation fails | File permissions/lock | Transaction rollback and friendly UI error | 6 | 3 | 4 | 72 | Add backup/recovery procedure |

## Priority
The highest initial RPN is incorrect fee (140), followed by over-capacity entry (96). Prioritize fee test coverage and full-capacity regression testing. Ratings are assumptions for planning, not measured defect probabilities.
