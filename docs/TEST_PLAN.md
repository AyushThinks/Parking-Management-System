# Test Plan

| ID | Scenario | Expected result | Type |
|---|---|---|---|
| TC-01 | Register valid vehicle | Record saved and first free slot allocated | Positive |
| TC-02 | Registration contains lowercase/spaces | Stored registration normalized to uppercase without spaces | Positive |
| TC-03 | Blank registration | Validation error; no record saved | Negative |
| TC-04 | Duplicate active registration | Second entry rejected | Negative |
| TC-05 | All slots occupied | Further entry rejected with full message | Boundary |
| TC-06 | Exit active vehicle | Exit timestamp and fee saved; slot released | Positive |
| TC-07 | Exit unknown/already exited record | Friendly error; data unchanged | Negative |
| TC-08 | Delete active vehicle | Deletion rejected | Negative |
| TC-09 | Invalid capacity/rate | Settings not saved | Negative |
| TC-10 | Search by owner/vehicle/slot | Matching records displayed | Functional |
| TC-11 | CSV export | File has header and expected rows | Functional |
| TC-12 | Audit event after entry | Audit log contains entry action | Integrity |

Automated service tests are in `tests/test_service.py`. GUI acceptance tests should be executed manually on the target machine.
