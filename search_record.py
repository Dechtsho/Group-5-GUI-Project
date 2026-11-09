
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from db import search
from styles import DESTINATIONS


def show(app):
    app.set_page("Search Records", "Search Tourist Records")

    # Search filters
    filters = app.card(app.content)
    filters.pack(fill="x", pady=(0, 15))

    # Tourist Name - Normal search bar
    app.label(filters, "Tourist Name", 8, True).grid(
        row=0, column=0, padx=12, pady=(15, 5), sticky="w"
    )

    key = tk.Entry(
        filters,
        bg=app.c["surface2"],
        fg=app.c["text"],
        insertbackground=app.c["text"],
        relief="flat",
        highlightthickness=1,
        highlightbackground=app.c["border"]
    )
    key.grid(
        row=1, column=0, padx=12, pady=(0, 15), sticky="ew"
    )

    # Destination dropdown
    app.label(filters, "Destination", 8, True).grid(
        row=0, column=1, padx=12, pady=(15, 5), sticky="w"
    )

    dest = ttk.Combobox(
        filters,
        values=[""] + DESTINATIONS,
        state="readonly"
    )
    dest.grid(
        row=1, column=1, padx=12, pady=(0, 15), sticky="ew"
    )

    # Arrival Date - Calendar picker
    app.label(filters, "Arrival Date", 8, True).grid(
        row=0, column=2, padx=12, pady=(15, 5), sticky="w"
    )

    date = DateEntry(
        filters,
        width=15,
        background=app.c["primary"],
        foreground="white",
        borderwidth=0,
        date_pattern="yyyy-mm-dd"
    )
    date.grid(
        row=1, column=2, padx=12, pady=(0, 15), sticky="ew"
    )

    filters.columnconfigure(0, weight=3)
    filters.columnconfigure(1, weight=2)
    filters.columnconfigure(2, weight=2)

    # Search results
    results = app.card(app.content)
    results.pack(fill="both", expand=True)

    tree = app.make_tree(results, [])

    def run_search(event=None):
        tree.delete(*tree.get_children())

        rows = search(
            key.get().strip(),
            dest.get(),
            date.get_date().strftime("%Y-%m-%d")
            if date.get() else ""
        )

        for r in rows:
            tree.insert("", "end", values=(
                r["id"],
                r["full_name"],
                r["country"],
                r["arrival_date"],
                r["destination"],
                r["passport_number"],
                r["purpose"]
            ))

    # Search automatically
    key.bind("<KeyRelease>", run_search)
    dest.bind("<<ComboboxSelected>>", run_search)
    date.bind("<<DateEntrySelected>>", run_search)

    # Initial display
    run_search()
