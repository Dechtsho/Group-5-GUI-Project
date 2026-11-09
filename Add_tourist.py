
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry

from db import add
from styles import COUNTRIES, DESTINATIONS, PURPOSES


ACCOMMODATIONS = [
    "Hotel",
    "Guesthouse",
    "Resort",
    "Homestay",
    "Lodge",
    "Other"
]


def show(app):

    app.set_page("Add Tourist", "Add Tourist")

    # Configure dropdown styles
    style = ttk.Style()

    style.configure(
        "Tourist.TCombobox",
        fieldbackground="#FFFFFF",
        background="#FFFFFF",
        foreground="#172033",
        arrowcolor="#2563EB",
        padding=8
    )

    style.map(
        "Tourist.TCombobox",
        fieldbackground=[("readonly", "#FFFFFF")],
        foreground=[("readonly", "#172033")],
        selectbackground=[("readonly", "#FFFFFF")],
        selectforeground=[("readonly", "#172033")]
    )

    # Main form
    form = app.card(app.content)
    form.pack(fill="both", expand=True)

    inner = tk.Frame(
        form,
        bg=app.c["surface"]
    )

    inner.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=20
    )

    inner.columnconfigure(0, weight=1)
    inner.columnconfigure(1, weight=1)

    # Form fields
    fields = [
        ("Full Name *", "full_name", "entry"),
        ("Country *", "country", "combo"),
        ("Passport Number *", "passport_number", "entry"),
        ("Arrival Date *", "arrival_date", "date"),
        ("Return Date *", "return_date", "date"),
        ("Accommodation", "accommodation", "accommodation"),
        ("Destination *", "destination", "destination"),
        ("Purpose of Visit", "purpose", "purpose"),
    ]

    widgets = {}

    for i, (label, key, kind) in enumerate(fields):

        col, row = i % 2, i // 2

        box = tk.Frame(
            inner,
            bg=app.c["surface"]
        )

        box.grid(
            row=row,
            column=col,
            sticky="ew",
            padx=15,
            pady=10
        )

        # Field labels
        tk.Label(
            box,
            text=label,
            bg=app.c["surface"],
            fg=app.c["text"],
            font=("Segoe UI", 10, "bold")
        ).pack(
            anchor="w",
            pady=(0, 7)
        )

        if kind == "combo":

            widget = ttk.Combobox(
                box,
                values=COUNTRIES,
                state="readonly",
                style="Tourist.TCombobox"
            )

        elif kind == "date":

            # Date fields with black text
            widget = DateEntry(
                box,
                width=25,
                background="#FFFFFF",
                foreground="black",
                headersbackground="#E5E7EB",
                headersforeground="black",
                selectbackground="#2563EB",
                selectforeground="white",
                normalbackground="#FFFFFF",
                normalforeground="black",
                borderwidth=1,
                date_pattern="dd/mm/yyyy",
                state="readonly",
                font=("Segoe UI", 10)
            )

        elif kind == "accommodation":

            widget = ttk.Combobox(
                box,
                values=ACCOMMODATIONS,
                state="readonly",
                style="Tourist.TCombobox"
            )

        elif kind == "destination":

            widget = ttk.Combobox(
                box,
                values=DESTINATIONS,
                state="readonly",
                style="Tourist.TCombobox"
            )

        elif kind == "purpose":

            widget = ttk.Combobox(
                box,
                values=PURPOSES,
                state="readonly",
                style="Tourist.TCombobox"
            )

        else:

            widget = tk.Entry(
                box,
                bg="#FFFFFF",
                fg="#172033",
                insertbackground="#172033",
                font=("Segoe UI", 10),
                relief="solid",
                bd=1,
                highlightthickness=1,
                highlightbackground="#CBD5E1",
                highlightcolor="#2563EB"
            )

        widget.pack(
            fill="x",
            ipady=7
        )

        widgets[key] = widget

    # Buttons
    buttons = tk.Frame(
        form,
        bg=app.c["surface"]
    )

    buttons.pack(
        side="bottom",
        fill="x",
        padx=25,
        pady=20
    )

    # Cancel button
    app.button(
        buttons,
        "Cancel",
        app.show_dashboard,
        False
    ).pack(
        side="right",
        padx=5
    )

    # Save Tourist button
    app.button(
        buttons,
        "Save Tourist",
        lambda: save(app, widgets),
        True
    ).pack(
        side="right",
        padx=5
    )


# Save Tourist Function
def save(app, widgets):

    # Collect information
    data = {
        key: widget.get().strip()
        for key, widget in widgets.items()
    }

    # Required fields
    required_fields = [
        "full_name",
        "country",
        "passport_number",
        "arrival_date",
        "return_date",
        "destination"
    ]

    for key in required_fields:

        if not data[key]:

            messagebox.showwarning(
                "Required Information",
                f"Please fill in {key.replace('_', ' ').title()}.",
                parent=app.root
            )

            return

    # Validate dates
    try:

        arrival = datetime.strptime(
            data["arrival_date"],
            "%d/%m/%Y"
        )

        return_date = datetime.strptime(
            data["return_date"],
            "%d/%m/%Y"
        )

    except ValueError:

        messagebox.showwarning(
            "Invalid Date",
            "Please select valid arrival and return dates.",
            parent=app.root
        )

        return

    # Check date order
    if return_date < arrival:

        messagebox.showwarning(
            "Invalid Date",
            "Return Date cannot be earlier than Arrival Date.",
            parent=app.root
        )

        return

    # Save tourist information
    try:

        ok, msg = add(data)

        if ok:

            messagebox.showinfo(
                "Success",
                "Tourist information saved successfully!",
                parent=app.root
            )

            app.show_records()

        else:

            messagebox.showerror(
                "Database Error",
                str(msg),
                parent=app.root
            )

    except Exception as e:

        messagebox.showerror(
            "Save Error",
            f"Unable to save tourist information:\n{e}",
            parent=app.root
        )
