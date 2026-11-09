import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from db import add
from styles import COUNTRIES, DESTINATIONS, PURPOSES

def show(app):
    app.set_page("Add Tourist", "Add Tourist")
    form = app.card(app.content)
    form.pack(fill="both", expand=True)

    inner = tk.Frame(form, bg=app.c["surface"])
    inner.pack(fill="both", expand=True, padx=25, pady=20)
    inner.columnconfigure(0, weight=1)
    inner.columnconfigure(1, weight=1)

    fields = [
        ("Full Name *", "full_name", "entry"),
        ("Country *", "country", "combo"),
        ("Passport Number *", "passport_number", "entry"),
        ("Arrival Date *", "arrival_date", "entry"),
        ("Accommodation", "accommodation", "entry"),
        ("Destination *", "destination", "combo"),
        ("Purpose of Visit", "purpose", "combo"),
    ]

    widgets = {}

    for i, (label, key, kind) in enumerate(fields):
        col, row = i % 2, i // 2
        box = tk.Frame(inner, bg=app.c["surface"])
        box.grid(row=row, column=col, sticky="ew",
                 padx=15, pady=9)

        app.label(box, label, 8, True).pack(anchor="w", pady=(0,5))

        if kind == "combo":
            values = COUNTRIES if key == "country" else (
                DESTINATIONS if key == "destination" else PURPOSES
            )
            widget = ttk.Combobox(box, values=values, state="readonly")
        else:
            widget = tk.Entry(
                box, bg=app.c["surface2"], fg=app.c["text"],
                insertbackground=app.c["text"], relief="flat",
                highlightthickness=1,
                highlightbackground=app.c["border"],
                highlightcolor=app.c["primary"]
            )
        widget.pack(fill="x", ipady=8)
        widgets[key] = widget

    buttons = tk.Frame(form, bg=app.c["surface"])
    buttons.pack(side="bottom", fill="x", padx=25, pady=20)

    app.button(buttons, "Cancel", app.show_dashboard, False).pack(
        side="right", padx=5)
    app.button(buttons, "Save Tourist",
               lambda: save(app, widgets), True).pack(
        side="right", padx=5)

def save(app, widgets):
    data = {k: w.get().strip() for k,w in widgets.items()}

    for key in ["full_name", "country", "passport_number",
                "arrival_date", "destination"]:
        if not data[key]:
            messagebox.showwarning("Required",
                                   "Please fill all required fields.")
            return

    try:
        datetime.strptime(data["arrival_date"], "%d/%m/%Y")
    except ValueError:
        messagebox.showwarning(
            "Invalid Date",
            "Enter the arrival date as DD/MM/YYYY."
        )
        return

    ok, msg = add(data)
    if ok:
        messagebox.showinfo("Success", msg)
        app.show_records()
    else:
        messagebox.showerror("Error", msg)
