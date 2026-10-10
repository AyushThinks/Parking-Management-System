# System Architecture

```mermaid
flowchart TD
    A[Parking attendant] --> UI[Tkinter UI]
    UI --> V[Input validation]
    UI --> S[Parking service / business rules]
    S --> DB[(SQLite database)]
    S --> AL[Audit log]
    S --> CSV[CSV export]
    DB --> DASH[Dashboard and records]
```

## Module responsibilities
- `parking_app/ui.py`: forms, dashboard, tables, dialogs and user interactions.
- `parking_app/validators.py`: validation and normalization before data reaches persistence.
- `parking_app/service.py`: slot allocation, duplicate prevention, billing, record search, export and audit events.
- `parking_app/database.py`: SQLite schema, transactions and initialization.
- `parking_app/config.py`: paths and defaults.

## Main vehicle-entry flow
```mermaid
flowchart TD
    A[Enter vehicle details] --> B{Inputs valid?}
    B -- No --> C[Show validation message]
    B -- Yes --> D{Already parked?}
    D -- Yes --> E[Reject duplicate]
    D -- No --> F{Slot available?}
    F -- No --> G[Show parking full]
    F -- Yes --> H[Save record and audit event]
    H --> I[Refresh dashboard]
```
