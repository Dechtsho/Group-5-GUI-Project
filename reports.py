import tkinter as tk
from tkinter import filedialog, messagebox
import csv
from db import get_all

def show(app):
    app.set_page("Reports", "Tourism Reports")

    controls = app.card(app.content)
    controls.pack(fill="x", pady=(0,15))

    app.label(controls, "Date Range", 8, True).pack(
        side="left", padx=15, pady=15)

    from_date = tk.Entry(controls, bg=app.c["surface2"],
                         fg=app.c["text"], relief="flat", width=14)
    from_date.pack(side="left", padx=5, pady=15, ipady=6)
    from_date.insert(0, "01/01/2026")

    app.label(controls, "to", 8, color=app.c["muted"]).pack(
        side="left", padx=3)

    to_date = tk.Entry(controls, bg=app.c["surface2"],
                       fg=app.c["text"], relief="flat", width=14)
    to_date.pack(side="left", padx=5, pady=15, ipady=6)
    to_date.insert(0, "31/12/2026")

    rows = get_all()

    body = app.card(app.content)
    body.pack(fill="both", expand=True)

    if not rows:
        app.label(body,
                  "No data available for reporting.",
                  12, True).pack(pady=45)
        app.label(body,
                  "Reports will automatically display data after tourists are added.",
                  9, color=app.c["muted"]).pack()
    else:
        left = app.card(body)
        left.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        right = app.card(body)
        right.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        app.label(left, "Tourist Arrivals by Country", 10, True).pack(
            anchor="w", padx=15, pady=12)
        app.label(right, "Popular Destinations", 10, True).pack(
            anchor="w", padx=15, pady=12)

        countries = {}
        destinations = {}
        for r in rows:
            countries[r["country"]] = countries.get(r["country"], 0) + 1
            destinations[r["destination"]] = destinations.get(
                r["destination"], 0) + 1

        for parent, data in [(left,countries),(right,destinations)]:
            for name, count in sorted(data.items(),
                                      key=lambda x:x[1], reverse=True):
                row = tk.Frame(parent, bg=app.c["surface"])
                row.pack(fill="x", padx=15, pady=5)
                app.label(row, name, 9).pack(side="left")
                app.label(row, str(count), 9, True,
                          color=app.c["primary"]).pack(side="right")

    export = tk.Frame(app.content, bg=app.c["bg"])
    export.pack(fill="x", pady=(12,0))

    app.button(export, "Export CSV",
               lambda: export_csv(rows), False).pack(side="right")

def export_csv(rows):
    if not rows:
        messagebox.showinfo("No Data",
                            "There are no tourist records to export.")
        return

    path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        initialfile="tourism_report.csv"
    )
    if not path:
        return

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "ID","Name","Country","Arrival Date",
            "Destination","Passport","Purpose"
        ])
        for r in rows:
            writer.writerow([
                r["id"],r["full_name"],r["country"],
                r["arrival_date"],r["destination"],
                r["passport_number"],r["purpose"]
            ])

    messagebox.showinfo("Export Complete",
                        "CSV report exported successfully.")