
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry

from db import search
from styles import DESTINATIONS


def show(app):

    app.set_page("Search Records", "Search Tourist Records")

    # ==================================
    # SEARCH FILTERS
    # ==================================

    filters = app.card(app.content)
    filters.pack(fill="x", pady=(0, 15))

    # Tourist Name
    app.label(
        filters,
        "Tourist Name",
        8,
        True
    ).grid(
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
    app.label(
        filters,
        "Destination",
        8,
        True
    ).grid(
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

    # Arrival Date
    app.label(
        filters,
        "Arrival Date",
        8,
        True
    ).grid(
        row=0, column=2, padx=12, pady=(15, 5), sticky="w"
    )

    date = DateEntry(
        filters,
        width=15,
        background=app.c["primary"],
        foreground="white",
        borderwidth=0,
        date_pattern="dd/mm/yyyy"
    )

    date.grid(
        row=1, column=2, padx=12, pady=(0, 5), sticky="ew"
    )

    # Date filter checkbox
    use_date = tk.BooleanVar(value=False)

    date_check = tk.Checkbutton(
        filters,
        text="Filter by arrival date",
        variable=use_date,
        bg=app.c["surface"],
        fg=app.c["text"],
        activebackground=app.c["surface"],
        activeforeground=app.c["text"],
        selectcolor=app.c["surface2"],
        font=("Segoe UI", 8),
        command=lambda: run_search()
    )

    date_check.grid(
        row=2, column=2, padx=12, pady=(0, 12), sticky="w"
    )

    filters.columnconfigure(0, weight=3)
    filters.columnconfigure(1, weight=2)
    filters.columnconfigure(2, weight=2)

    # ==================================
    # SEARCH RESULTS
    # ==================================

    results = app.card(app.content)
    results.pack(fill="both", expand=True)

    tree = app.make_tree(results, [])

    # ==================================
    # SEARCH FUNCTION
    # ==================================

    def run_search(event=None):

        tree.delete(*tree.get_children())

        # Apply arrival date only when checkbox is selected
        arrival_date = ""

        if use_date.get():
            arrival_date = date.get_date().strftime("%d/%m/%Y")

        rows = search(
            keyword=key.get().strip(),
            destination=dest.get().strip(),
            arrival_date=arrival_date
        )

        # Display serial numbers starting from 1
        for index, r in enumerate(rows, start=1):

            tree.insert(
                "",
                "end",
                values=(
                    index,
                    r["full_name"],
                    r["country"],
                    r["arrival_date"],
                    r["destination"],
                    r["passport_number"],
                    r["purpose"]
                )
            )

    # ==================================
    # AUTOMATIC SEARCH
    # ==================================

    # Search while typing a tourist name
    key.bind("<KeyRelease>", run_search)

    # Search when destination changes
    dest.bind("<<ComboboxSelected>>", run_search)

    # Automatically enable date filtering when a date is selected
    def date_selected(event=None):

        use_date.set(True)
        run_search()

    date.bind("<<DateEntrySelected>>", date_selected)

    # Initial display: show all records
    run_search()
