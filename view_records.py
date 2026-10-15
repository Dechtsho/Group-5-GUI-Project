import tkinter as tk
from tkinter import messagebox
from _dbm import get_all, delete

def show(app):
    app.set_page("View Records", "Tourist Records")

    toolbar = tk.Frame(app.content, bg=app.c["bg"])
    toolbar.pack(fill="x", pady=(0, 12))

    app.button(toolbar, "+ Add Tourist",
               app.show_add_tourist, True).pack(side="right")

    card = app.card(app.content)
    card.pack(fill="both", expand=True)

    rows = get_all()

    if not rows:
        app.label(card,
                  "No tourist records found.",
                  12, True).pack(pady=35)
        app.label(card,
                  "Add a tourist using the 'Add Tourist' button.",
                  9, color=app.c["muted"]).pack()
        return

    tree = app.make_tree(card, rows)

    actions = tk.Frame(card, bg=app.c["surface"])
    actions.pack(fill="x", padx=12, pady=(0,12))

    def selected_id():
        item = tree.focus()
        if not item:
            return None
        return int(tree.item(item, "values")[0])

    def edit():
        rid = selected_id()
        if rid is None:
            messagebox.showwarning("Select Record",
                                   "Please select a record.")
            return
        app.show_update(rid)

    def remove():
        rid = selected_id() 
        if rid is None:
            messagebox.showwarning("Select Record",
                                   "Please select a record.")
            return
        row = next((r for r in rows if r["id"] == rid), None)
        if row and messagebox.askyesno(
            "Delete Confirmation",
            f"Delete this record?\n\n{row['full_name']} ({row['country']})"
        ):
            delete(rid)
            messagebox.showinfo("Deleted",
                                "Tourist record deleted successfully.")
            show(app)

    app.button(actions, "Delete Selected", remove, True).pack(
        side="right", padx=5)
    app.button(actions, "Update Selected", edit, False).pack(
        side="right", padx=5)
