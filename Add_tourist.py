
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
            pady=9
        )

        app.label(
            box,
            label,
            8,
            True
        ).pack(
            anchor="w",
            pady=(0, 5)
        )

        if kind == "combo":

            widget = ttk.Combobox(
                box,
                values=COUNTRIES,
                state="readonly"
            )

        elif kind == "date":

            widget = DateEntry(
                box,
                width=25,
                background=app.c["primary"],
                foreground="white",
                borderwidth=1,
                date_pattern="dd/mm/yyyy",
                state="readonly"
            )

        elif kind == "accommodation":

            widget = ttk.Combobox(
                box,
                values=ACCOMMODATIONS,
                state="readonly"
            )

        elif kind == "destination":

            widget = ttk.Combobox(
                box,
                values=DESTINATIONS,
                state="readonly"
            )

        elif kind == "purpose":

            widget = ttk.Combobox(
                box,
                values=PURPOSES,
                state="readonly"
            )

        else:

            widget = tk.Entry(
                box,
                bg=app.c["surface2"],
                fg=app.c["text"],
                insertbackground=app.c["text"],
                relief="flat",
                highlightthickness=1,
                highlightbackground=app.c["border"],
                highlightcolor=app.c["primary"]
            )

        widget.pack(
            fill="x",
            ipady=8
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

    app.button(
        buttons,
        "Cancel",
        app.show_dashboard,
        False
    ).pack(
        side="right",
        padx=5
    )

    app.button(
        buttons,
        "Save Tourist",
        lambda: save(app, widgets),
        True
    ).pack(
        side="right",
        padx=5
    )


def save(app, widgets):

    data = {
        k: w.get().strip()
        for k, w in widgets.items()
    }

    # Required fields
    required_fields = [
        "full_name",
        "country",
        "passport_number",
        "arrival_date",
        "end_date",
        "destination"
    ]

    for key in required_fields:

        if not data[key]:

            messagebox.showwarning(
                "Required",
                f"Please fill {key.replace('_', ' ').title()}.",
                parent=app.root
            )

            return

    # Convert dates
    try:

        arrival = datetime.strptime(
            data["arrival_date"],
            "%d/%m/%Y"
        )

        end = datetime.strptime(
            data["end_date"],
            "%d/%m/%Y"
        )

    except ValueError:

        messagebox.showwarning(
            "Invalid Date",
            "Please select valid dates.",
            parent=app.root
        )

        return

    # Check date order
    if end < arrival:

        messagebox.showwarning(
            "Invalid End Date",
            "End Date cannot be earlier than Arrival Date.",
            parent=app.root
        )

        return

    # Save tourist information
    ok, msg = add(data)

    if ok:

        messagebox.showinfo(
            "Success",
            msg,
            parent=app.root
        )

        app.show_records()

    else:

        messagebox.showerror(
            "Error",
            msg,
            parent=app.root
        )
