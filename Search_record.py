import tkinter as tk
from tkinter import ttk
from db import search, get_all
from styles import DESTINATIONS

def show(app):
    app.set_page("Search Records", "Search Tourist Records")

    filters = app.card(app.content)
    filters.pack(fill="x", pady=(0,15))

    app.label(filters, "Search", 8, True).grid(
        row=0, column=0, padx=12, pady=(15,5), sticky="w")
    key = tk.Entry(filters, bg=app.c["surface2"], fg=app.c["text"],
                   insertbackground=app.c["text"], relief="flat",
                   highlightthickness=1,
                   highlightbackground=app.c["border"])
    key.grid(row=1,column=0,padx=12,pady=(0,15),sticky="ew")

    app.label(filters, "Destination", 8, True).grid(
        row=0,column=1,padx=12,pady=(15,5),sticky="w")
    dest = ttk.Combobox(filters, values=[""]+DESTINATIONS,
                        state="readonly")
    dest.grid(row=1,column=1,padx=12,pady=(0,15),sticky="ew")

    app.label(filters, "Arrival Date", 8, True).grid(
        row=0,column=2,padx=12,pady=(15,5),sticky="w")
    date = tk.Entry(filters, bg=app.c["surface2"], fg=app.c["text"],
                    insertbackground=app.c["text"], relief="flat",
                    highlightthickness=1,
                    highlightbackground=app.c["border"])
    date.grid(row=1,column=2,padx=12,pady=(0,15),sticky="ew")

    filters.columnconfigure(0, weight=3)
    filters.columnconfigure(1, weight=2)
    filters.columnconfigure(2, weight=2)

    results = app.card(app.content)
    results.pack(fill="both", expand=True)

    suggestions = tk.Listbox(
        results, bg=app.c["surface2"], fg=app.c["text"],
        selectbackground=app.c["primary"], relief="flat",
        height=4, highlightthickness=0
    )
    suggestions.pack(fill="x", padx=15, pady=(15,5))
    suggestions.pack_forget()

    tree = app.make_tree(results, [])

    def run_search(event=None):
        tree.delete(*tree.get_children())
        rows = search(key.get().strip(), dest.get(), date.get().strip())
        for r in rows:
            tree.insert("", "end", values=(
                r["id"], r["full_name"], r["country"],
                r["arrival_date"], r["destination"],
                r["passport_number"], r["purpose"]
            ))

    def autocomplete(event=None):
        term = key.get().strip()
        suggestions.delete(0, "end")
        if not term:
            suggestions.pack_forget()
            run_search()
            return

        matches = []
        for r in get_all():
            combined = (
                f"{r['full_name']} {r['country']} "
                f"{r['passport_number']} {r['destination']}"
            )
            if term.lower() in combined.lower():
                matches.append(
                    f"{r['full_name']}  •  {r['country']}  •  {r['destination']}"
                )

        if matches:
            for x in matches[:5]:
                suggestions.insert("end", x)
            suggestions.pack(fill="x", padx=15, pady=(15,5))
        else:
            suggestions.pack_forget()

        run_search()

    key.bind("<KeyRelease>", autocomplete)
    dest.bind("<<ComboboxSelected>>", run_search)
    date.bind("<KeyRelease>", run_search)

    run_search()