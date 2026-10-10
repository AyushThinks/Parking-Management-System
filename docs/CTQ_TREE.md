# Critical to Quality (CTQ) Tree

| Customer need | Quality driver | Measurable CTQ / target | Verification |
|---|---|---|---|
| Find a space quickly | Correct slot allocation | No two active vehicles share a slot | Database constraint + test |
| Avoid duplicate records | Registration validation | Duplicate active vehicle entries rejected | Duplicate-entry test |
| Fair and understandable fee | Transparent fee calculation | Fee = started hours × configured rate | Fee rule test and exit receipt |
| Know current availability | Accurate dashboard | Available = capacity − active vehicles | Dashboard reconciliation |
| Retrieve records easily | Search and export | Search filters results; CSV includes all defined columns | Manual test and export check |
| Recover from mistakes | Clear error handling | Invalid input is not saved and displays a clear message | Negative tests |
