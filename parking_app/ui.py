"""Tkinter interface for ParkEase."""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from parking_app.config import APP_NAME, CURRENCY_SYMBOL
from parking_app.service import ParkingService

class ParkingApp:
    def __init__(self, service=None):
        self.service = service or ParkingService()
        self.root = tk.Tk()
        self.root.title(APP_NAME)
        self.root.geometry("1120x720")
        self.root.minsize(950, 620)
        self.root.configure(bg="#f4f7fb")
        self._style()
        self._build()
        self.refresh_all()

    def _style(self):
        style = ttk.Style(self.root)
        try: style.theme_use("clam")
        except tk.TclError: pass
        style.configure("Treeview", rowheight=28, font=("Segoe UI", 9), background="white", fieldbackground="white")
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"), background="#e8eef7")
        style.configure("TButton", padding=(10, 6), font=("Segoe UI", 9))
        style.configure("TLabel", font=("Segoe UI", 9))

    def _build(self):
        header = tk.Frame(self.root, bg="#102a43", padx=22, pady=16)
        header.pack(fill="x")
        tk.Label(header, text="ParkEase", font=("Segoe UI", 22, "bold"), fg="white", bg="#102a43").pack(side="left")
        tk.Label(header, text="PARKING MANAGEMENT SYSTEM", font=("Segoe UI", 10), fg="#c9d8e8", bg="#102a43").pack(side="left", padx=16, pady=(7, 0))
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", expand=True, padx=16, pady=14)
        self.dashboard_tab = ttk.Frame(self.tabs, padding=14)
        self.entry_tab = ttk.Frame(self.tabs, padding=14)
        self.records_tab = ttk.Frame(self.tabs, padding=14)
        self.settings_tab = ttk.Frame(self.tabs, padding=14)
        self.tabs.add(self.dashboard_tab, text="Dashboard")
        self.tabs.add(self.entry_tab, text="Vehicle Entry")
        self.tabs.add(self.records_tab, text="Records & Exit")
        self.tabs.add(self.settings_tab, text="Settings & Audit")
        self._build_dashboard(); self._build_entry(); self._build_records(); self._build_settings()
        tk.Label(self.root, text="BBAT104 • Fundamentals of TQM • Input validation and audit logging enabled", bg="#f4f7fb", fg="#52667a", font=("Segoe UI", 8)).pack(fill="x", padx=18, pady=(0, 8))

    def _build_dashboard(self):
        ttk.Label(self.dashboard_tab, text="Operations overview", font=("Segoe UI", 17, "bold")).pack(anchor="w", pady=(0, 12))
        self.metrics = tk.Frame(self.dashboard_tab, bg="#f4f7fb")
        self.metrics.pack(fill="x")
        self.metric_labels = {}
        for key, title in [("total_slots", "Total slots"), ("occupied", "Occupied"), ("available", "Available"), ("today_income", "Today's income")]:
            card = tk.Frame(self.metrics, bg="white", padx=18, pady=16, highlightbackground="#dbe4ee", highlightthickness=1)
            card.pack(side="left", fill="both", expand=True, padx=(0, 10))
            tk.Label(card, text=title, bg="white", fg="#52667a", font=("Segoe UI", 10)).pack(anchor="w")
            value = tk.Label(card, text="—", bg="white", fg="#102a43", font=("Segoe UI", 23, "bold")); value.pack(anchor="w", pady=(8, 0))
            self.metric_labels[key] = value
        ttk.Label(self.dashboard_tab, text="Currently parked vehicles", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(24, 8))
        self.active_tree = self._tree(self.dashboard_tab, [("vehicle_number", "Vehicle", 150), ("owner_name", "Owner", 180), ("vehicle_type", "Type", 90), ("slot_number", "Slot", 70), ("entry_time", "Entry time", 180)])
        ttk.Button(self.dashboard_tab, text="Refresh dashboard", command=self.refresh_all).pack(anchor="e", pady=10)

    def _build_entry(self):
        ttk.Label(self.entry_tab, text="Register vehicle entry", font=("Segoe UI", 17, "bold")).pack(anchor="w", pady=(0, 6))
        ttk.Label(self.entry_tab, text="Required fields are validated before a slot is allocated.").pack(anchor="w", pady=(0, 18))
        form = ttk.Frame(self.entry_tab, padding=18); form.pack(anchor="nw", fill="x")
        self.vehicle_var = tk.StringVar(); self.owner_var = tk.StringVar(); self.type_var = tk.StringVar(value="Car")
        fields = [("Registration number", self.vehicle_var), ("Owner name", self.owner_var)]
        for row, (label, variable) in enumerate(fields):
            ttk.Label(form, text=label).grid(row=row, column=0, sticky="w", pady=9, padx=(0, 20))
            ttk.Entry(form, textvariable=variable, width=38).grid(row=row, column=1, sticky="w", pady=9)
        ttk.Label(form, text="Vehicle type").grid(row=2, column=0, sticky="w", pady=9, padx=(0, 20))
        ttk.Combobox(form, textvariable=self.type_var, values=("Car", "Bike", "SUV", "Other"), state="readonly", width=35).grid(row=2, column=1, sticky="w", pady=9)
        ttk.Button(form, text="Allocate slot & save entry", command=self.register_vehicle).grid(row=3, column=1, sticky="w", pady=(18, 8))
        ttk.Button(form, text="Clear form", command=self.clear_entry).grid(row=3, column=1, sticky="w", padx=(205, 0), pady=(18, 8))
        self.entry_result = ttk.Label(self.entry_tab, text="", font=("Segoe UI", 11, "bold")); self.entry_result.pack(anchor="w", padx=20, pady=8)

    def _build_records(self):
        ttk.Label(self.records_tab, text="Parking records", font=("Segoe UI", 17, "bold")).pack(anchor="w", pady=(0, 12))
        toolbar = ttk.Frame(self.records_tab); toolbar.pack(fill="x", pady=(0, 10))
        self.search_var = tk.StringVar(); self.status_var = tk.StringVar(value="All")
        ttk.Label(toolbar, text="Search").pack(side="left")
        search_entry = ttk.Entry(toolbar, textvariable=self.search_var, width=28); search_entry.pack(side="left", padx=7)
        search_entry.bind("<Return>", lambda _event: self.refresh_records())
        ttk.Combobox(toolbar, textvariable=self.status_var, values=("All", "Parked", "Exited"), state="readonly", width=12).pack(side="left", padx=6)
        ttk.Button(toolbar, text="Search / Filter", command=self.refresh_records).pack(side="left", padx=4)
        ttk.Button(toolbar, text="Export CSV", command=self.export_csv).pack(side="right", padx=4)
        ttk.Button(toolbar, text="Delete selected exited record", command=self.delete_selected).pack(side="right", padx=4)
        self.records_tree = self._tree(self.records_tab, [("id", "ID", 55), ("vehicle_number", "Vehicle", 115), ("owner_name", "Owner", 130), ("vehicle_type", "Type", 70), ("slot_number", "Slot", 55), ("entry_time", "Entry", 150), ("exit_time", "Exit", 150), ("fee", "Fee (₹)", 75), ("status", "Status", 80)])
        ttk.Button(self.records_tab, text="Mark selected vehicle as exited / calculate fee", command=self.exit_selected).pack(anchor="w", pady=10)

    def _build_settings(self):
        ttk.Label(self.settings_tab, text="Parking settings", font=("Segoe UI", 17, "bold")).pack(anchor="w", pady=(0, 12))
        settings = self.service.get_settings()
        form = ttk.Frame(self.settings_tab, padding=14); form.pack(anchor="nw")
        self.capacity_var = tk.StringVar(value=str(settings["slot_capacity"]))
        self.rate_var = tk.StringVar(value=str(settings["hourly_rate"]))
        ttk.Label(form, text="Total parking slots (1–500)").grid(row=0, column=0, sticky="w", padx=(0, 18), pady=8)
        ttk.Entry(form, textvariable=self.capacity_var, width=20).grid(row=0, column=1, pady=8)
        ttk.Label(form, text="Fee per started hour (₹)").grid(row=1, column=0, sticky="w", padx=(0, 18), pady=8)
        ttk.Entry(form, textvariable=self.rate_var, width=20).grid(row=1, column=1, pady=8)
        ttk.Button(form, text="Save settings", command=self.save_settings).grid(row=2, column=1, sticky="w", pady=12)
        ttk.Label(self.settings_tab, text="Recent audit events", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(16, 8))
        self.audit_tree = self._tree(self.settings_tab, [("id", "ID", 55), ("action", "Action", 160), ("details", "Details", 480), ("created_at", "Time", 180)])

    def _tree(self, parent, columns):
        frame = ttk.Frame(parent); frame.pack(fill="both", expand=True)
        keys = [c[0] for c in columns]
        tree = ttk.Treeview(frame, columns=keys, show="headings", selectmode="browse")
        for key, title, width in columns:
            tree.heading(key, text=title); tree.column(key, width=width, minwidth=45, anchor="w")
        scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview); tree.configure(yscrollcommand=scroll.set)
        tree.pack(side="left", fill="both", expand=True); scroll.pack(side="right", fill="y")
        return tree

    @staticmethod
    def _fill(tree, records, columns):
        tree.delete(*tree.get_children())
        for record in records:
            values = [record.get(key, "") for key in columns]
            tree.insert("", "end", iid=str(record.get("id", "")), values=values)

    def refresh_all(self):
        try:
            data = self.service.dashboard()
            for key in ("total_slots", "occupied", "available"):
                self.metric_labels[key].configure(text=str(data[key]))
            self.metric_labels["today_income"].configure(text=f"{CURRENCY_SYMBOL}{data['today_income']:.2f}")
            self._fill(self.active_tree, self.service.list_records(status="Parked"), ["vehicle_number", "owner_name", "vehicle_type", "slot_number", "entry_time"])
            self.refresh_records(); self.refresh_audit()
        except Exception as exc:
            messagebox.showerror("Unable to refresh", str(exc))

    def refresh_records(self):
        records = self.service.list_records(self.search_var.get(), self.status_var.get())
        self._fill(self.records_tree, records, ["id", "vehicle_number", "owner_name", "vehicle_type", "slot_number", "entry_time", "exit_time", "fee", "status"])

    def refresh_audit(self):
        self._fill(self.audit_tree, self.service.audit_logs(), ["id", "action", "details", "created_at"])

    def register_vehicle(self):
        try:
            record = self.service.park_vehicle(self.vehicle_var.get(), self.owner_var.get(), self.type_var.get())
            self.entry_result.configure(text=f"Success: {record['vehicle_number']} allocated slot {record['slot_number']} (record #{record['id']}).", foreground="#18794e")
            self.clear_entry(); self.refresh_all()
            messagebox.showinfo("Vehicle registered", f"Vehicle: {record['vehicle_number']}\nSlot: {record['slot_number']}\nEntry: {record['entry_time']}")
        except (ValueError, Exception) as exc:
            messagebox.showerror("Entry not saved", str(exc))

    def clear_entry(self):
        self.vehicle_var.set(""); self.owner_var.set(""); self.type_var.set("Car")

    def _selected_id(self):
        selected = self.records_tree.selection()
        if not selected:
            messagebox.showwarning("Select a record", "Please select a record from the table first."); return None
        try: return int(selected[0])
        except ValueError: return None

    def exit_selected(self):
        record_id = self._selected_id()
        if record_id is None: return
        if not messagebox.askyesno("Confirm vehicle exit", "Mark this vehicle as exited and calculate its parking fee?"): return
        try:
            result = self.service.exit_vehicle(record_id)
            messagebox.showinfo("Exit receipt", f"Vehicle: {result['vehicle_number']}\nSlot: {result['slot_number']}\nDuration billed: {result['duration_hours']} hour(s)\nTotal fee: {CURRENCY_SYMBOL}{result['fee']:.2f}\nExit time: {result['exit_time']}")
            self.refresh_all()
        except Exception as exc: messagebox.showerror("Exit failed", str(exc))

    def delete_selected(self):
        record_id = self._selected_id()
        if record_id is None: return
        if not messagebox.askyesno("Confirm delete", "Delete this exited record? This cannot be undone."): return
        try: self.service.delete_record(record_id); self.refresh_all()
        except Exception as exc: messagebox.showerror("Delete failed", str(exc))

    def export_csv(self):
        path = filedialog.asksaveasfilename(title="Export parking records", defaultextension=".csv", filetypes=[("CSV files", "*.csv")], initialfile="parking_records.csv")
        if not path: return
        try:
            count = self.service.export_csv(path); messagebox.showinfo("Export complete", f"Exported {count} record(s) to:\n{path}")
        except Exception as exc: messagebox.showerror("Export failed", str(exc))

    def save_settings(self):
        try:
            self.service.update_settings(self.capacity_var.get(), self.rate_var.get())
            self.refresh_all(); messagebox.showinfo("Settings saved", "Parking settings updated successfully.")
        except Exception as exc: messagebox.showerror("Invalid settings", str(exc))

    def run(self):
        self.root.mainloop()
