
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
import csv

from db import get_all


def show(app):

    app.set_page("Reports", "Tourism Reports")

    # ==================================
    # DATE RANGE CONTROLS
    # ==================================

    controls = app.card(app.content)
    controls.pack(fill="x", pady=(0, 15))

    app.label(
        controls,
        "Date Range",
        8,
        True
    ).pack(
        side="left",
        padx=15,
        pady=15
    )

    from_date = tk.Entry(
        controls,
        bg=app.c["surface2"],
        fg=app.c["text"],
        insertbackground=app.c["text"],
        relief="flat",
        width=14
    )

    from_date.pack(
        side="left",
        padx=5,
        pady=15,
        ipady=6
    )

    from_date.insert(0, "01/01/2026")

    app.label(
        controls,
        "to",
        8,
        color=app.c["muted"]
    ).pack(
        side="left",
        padx=3
    )

    to_date = tk.Entry(
        controls,
        bg=app.c["surface2"],
        fg=app.c["text"],
        insertbackground=app.c["text"],
        relief="flat",
        width=14
    )

    to_date.pack(
        side="left",
        padx=5,
        pady=15,
        ipady=6
    )

    to_date.insert(0, "31/12/2026")

    # Generate Report Button
    app.button(
        controls,
        "Generate Report",
        lambda: generate_report(),
        True
    ).pack(
        side="right",
        padx=15,
        pady=15
    )

    # ==================================
    # REPORT DISPLAY AREA
    # ==================================

    body = app.card(app.content)
    body.pack(
        fill="both",
        expand=True
    )

    # Store filtered records for CSV export
    filtered_rows = []

    # ==================================
    # DATE CONVERSION
    # ==================================

    def convert_date(date_value):

        if not date_value:
            return None

        formats = [
            "%d/%m/%Y",
            "%Y-%m-%d"
        ]

        for fmt in formats:

            try:
                return datetime.strptime(
                    date_value,
                    fmt
                ).date()

            except ValueError:
                continue

        return None

    # ==================================
    # GENERATE REPORT
    # ==================================

    def generate_report():

        nonlocal filtered_rows

        start_text = from_date.get().strip()
        end_text = to_date.get().strip()

        # Validate date range
        try:

            start = datetime.strptime(
                start_text,
                "%d/%m/%Y"
            ).date()

            end = datetime.strptime(
                end_text,
                "%d/%m/%Y"
            ).date()

        except ValueError:

            messagebox.showwarning(
                "Invalid Date",
                "Please enter dates in DD/MM/YYYY format.\n\n"
                "Example: 01/01/2026",
                parent=app.root
            )

            return

        if start > end:

            messagebox.showwarning(
                "Invalid Date Range",
                "The start date cannot be later than the end date.",
                parent=app.root
            )

            return

        # Get all tourist records
        rows = get_all()

        # Filter records according to arrival date
        filtered_rows = []

        for r in rows:

            arrival = convert_date(r["arrival_date"])

            if arrival is None:
                continue

            if start <= arrival <= end:
                filtered_rows.append(r)

        # Clear previous report
        for widget in body.winfo_children():
            widget.destroy()

        # ==================================
        # NO RECORDS FOUND
        # ==================================

        if not filtered_rows:

            app.label(
                body,
                "No tourist records found for this date range.",
                12,
                True
            ).pack(pady=45)

            app.label(
                body,
                "Try selecting a different date range.",
                9,
                color=app.c["muted"]
            ).pack()

            return

        # ==================================
        # REPORT SUMMARY
        # ==================================

        app.label(
            body,
            f"Total Tourist Arrivals: {len(filtered_rows)}",
            12,
            True
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 5)
        )

        # Country and destination cards
        left = app.card(body)

        left.pack(
            side="left",
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        right = app.card(body)

        right.pack(
            side="left",
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        app.label(
            left,
            "Tourist Arrivals by Country",
            10,
            True
        ).pack(
            anchor="w",
            padx=15,
            pady=12
        )

        app.label(
            right,
            "Popular Destinations",
            10,
            True
        ).pack(
            anchor="w",
            padx=15,
            pady=12
        )

        # Count tourist arrivals by country
        countries = {}

        # Count tourist arrivals by destination
        destinations = {}

        for r in filtered_rows:

            country = r["country"] or "Unknown"
            destination = r["destination"] or "Unknown"

            countries[country] = (
                countries.get(country, 0) + 1
            )

            destinations[destination] = (
                destinations.get(destination, 0) + 1
            )

        # Display country and destination statistics
        for parent, data in [
            (left, countries),
            (right, destinations)
        ]:

            for name, count in sorted(
                data.items(),
                key=lambda x: x[1],
                reverse=True
            ):

                row = tk.Frame(
                    parent,
                    bg=app.c["surface"]
                )

                row.pack(
                    fill="x",
                    padx=15,
                    pady=5
                )

                app.label(
                    row,
                    name,
                    9
                ).pack(
                    side="left"
                )

                app.label(
                    row,
                    str(count),
                    9,
                    True,
                    color=app.c["primary"]
                ).pack(
                    side="right"
                )

    # ==================================
    # EXPORT CSV
    # ==================================

    export = tk.Frame(
        app.content,
        bg=app.c["bg"]
    )

    export.pack(
        fill="x",
        pady=(12, 0)
    )

    app.button(
        export,
        "Export CSV",
        lambda: export_csv(filtered_rows, app),
        False
    ).pack(
        side="right"
    )

    # Generate initial report
    generate_report()


# =========================================
# EXPORT FILTERED RECORDS TO CSV
# =========================================

def export_csv(rows, app=None):

    if not rows:

        messagebox.showinfo(
            "No Data",
            "There are no tourist records to export.",
            parent=app.root if app else None
        )

        return

    path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[
            ("CSV files", "*.csv")
        ],
        initialfile="tourism_report.csv"
    )

    if not path:
        return

    try:

        with open(
            path,
            "w",
            newline="",
            encoding="utf-8"
        ) as f:

            writer = csv.writer(f)

            writer.writerow([
                "Serial Number",
                "Name",
                "Country",
                "Arrival Date",
                "Destination",
                "Passport",
                "Purpose"
            ])

            for index, r in enumerate(rows, start=1):

                writer.writerow([
                    index,
                    r["full_name"],
                    r["country"],
                    r["arrival_date"],
                    r["destination"],
                    r["passport_number"],
                    r["purpose"]
                ])

        messagebox.showinfo(
            "Export Complete",
            "CSV report exported successfully.",
            parent=app.root if app else None
        )

    except Exception as e:

        messagebox.showerror(
            "Export Failed",
            f"Unable to export the report:\n{e}",
            parent=app.root if app else None
        )
