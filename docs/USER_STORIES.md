# User Stories and Acceptance Criteria

- As an attendant, I want to register an arriving vehicle so that it receives an available slot.
  - Acceptance: valid details are saved; slot number and entry time are shown.
- As an attendant, I want to see when parking is full so that I do not over-allocate spaces.
  - Acceptance: entry beyond configured capacity is rejected with a clear message.
- As an attendant, I want to record a vehicle exit so that the slot becomes available and fees are recorded.
  - Acceptance: exit timestamp, duration, fee and status are stored.
- As a supervisor, I want to search records so that I can answer parking queries.
  - Acceptance: search matches vehicle, owner or slot and status can be filtered.
- As a supervisor, I want to export records so that I can analyze operations.
  - Acceptance: CSV contains a header and one row per record.
- As a quality reviewer, I want audit events so that key actions can be traced.
  - Acceptance: vehicle entry/exit, settings changes, export and deletion are logged.
