
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry

from db import get_all, get_one, update, delete
from styles import COUNTRIES, DESTINATIONS, PURPOSES


ACCOMMODATIONS = [
    "Hotel", "Guesthouse", "Resort",
    "Homestay", "Lodge", "Other"
]


def show(app, record_id=None):

    app.set_page("Update / Delete Record", "Update / Delete")

    # ==================================
    # RECORD TABLE
    # ==================================

    list_card = app.card(app.content)
    list_card.pack(fill="x", pady=(0, 8))

    tree = app.make_tree(
        list_card,
        get_all(),
        height=2
    )

    # ==================================
    # FORM CARD
    # ==================================

    form = app.card(app.content)
    form.pack(fill="both", expand=True)

    inner = tk.Frame(
        form,
        bg=app.c["surface"]
    )

    inner.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=8
    )

    inner.columnconfigure(0, weight=1)
    inner.columnconfigure(1, weight=1)

    # ==================================
    # FORM FIELDS
    # ==================================

    fields = [
        ("Full Name", "full_name", "entry"),
        ("Country", "country", "country"),
        ("Passport Number", "passport_number", "entry"),
        ("Arrival Date", "arrival_date", "date"),
        ("Accommodation", "accommodation", "accommodation"),
        ("Destination", "destination", "destination"),
        ("Purpose of Visit", "purpose", "purpose")
    ]

    widgets = {}

    for i, (label, key, kind) in enumerate(fields):

        row = i // 2
        col = i % 2

        box = tk.Frame(
            inner,
            bg=app.c["surface"]
        )

        box.grid(
            row=row,
            column=col,
            sticky="ew",
            padx=12,
            pady=6
        )

        app.label(
            box,
            label,
            9,
            True
        ).pack(
            anchor="w",
            pady=(0, 3)
        )

        if kind == "country":

            widget = ttk.Combobox(
                box,
                values=COUNTRIES,
                state="readonly"
            )

        elif kind == "date":

            widget = DateEntry(
                box,
                width=20,
                date_pattern="dd/mm/yyyy",
                state="readonly",
                background=app.c["primary"],
                foreground="white",
                borderwidth=1
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
            ipady=4
        )

        widgets[key] = widget

    # ==================================
    # RECORD SELECTION
    # ==================================

    def selected_id():

        item = tree.focus()

        if not item:
            return None

        values = tree.item(item, "values")

        if not values:
            return None

        return int(values[0])

    # ==================================
    # LOAD RECORD INTO FORM
    # ==================================

    def load(rid):

        record = get_one(rid)

        if not record:
            return

        for key, widget in widgets.items():

            value = record[key] or ""

            if key == "arrival_date":

                try:
                    widget.set_date(
                        datetime.strptime(
                            value,
                            "%d/%m/%Y"
                        )
                    )
                except ValueError:
                    try:
                        widget.set_date(value)
                    except (ValueError, TypeError):
                        pass

            elif isinstance(widget, ttk.Combobox):

                widget.set(value)

            else:

                widget.delete(0, tk.END)
                widget.insert(0, value)

    def select_record(event=None):

        rid = selected_id()

        if rid:
            load(rid)

    tree.bind(
        "<<TreeviewSelect>>",
        select_record
    )

    # Load requested record
    if record_id:

        for item in tree.get_children():

            values = tree.item(item, "values")

            if int(values[0]) == record_id:

                tree.selection_set(item)
                tree.focus(item)
                tree.see(item)

                load(record_id)
                break

    # ==================================
    # BUTTON AREA
    # ==================================

    buttons = tk.Frame(
        form,
        bg=app.c["surface"]
    )

    buttons.pack(
        side="bottom",
        fill="x",
        padx=20,
        pady=8
    )

    # ==================================
    # UPDATE
    # ==================================

    def do_update():

        rid = selected_id()

        if not rid:

            messagebox.showwarning(
                "Select Record",
                "Please select a tourist record first.",
                parent=app.root
            )
            return

        data = {
            key: widget.get().strip()
            for key, widget in widgets.items()
        }

        required = [
            "full_name",
            "country",
            "passport_number",
            "arrival_date",
            "destination"
        ]

        for key in required:

            if not data[key]:

                messagebox.showwarning(
                    "Required",
                    f"Please enter {key.replace('_', ' ').title()}.",
                    parent=app.root
                )
                return

        try:

            datetime.strptime(
                data["arrival_date"],
                "%d/%m/%Y"
            )

        except ValueError:

            messagebox.showwarning(
                "Invalid Date",
                "Please select a valid arrival date.",
                parent=app.root
            )
            return

        try:

            ok, msg = update(rid, data)

            if ok:

                messagebox.showinfo(
                    "Updated",
                    msg,
                    parent=app.root
                )

                show(app, rid)

            else:

                messagebox.showerror(
                    "Update Failed",
                    msg,
                    parent=app.root
                )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e),
                parent=app.root
            )

    # ==================================
    # DELETE
    # ==================================

    def do_delete():

        rid = selected_id()

        if not rid:

            messagebox.showwarning(
                "Select Record",
                "Please select a tourist record first.",
                parent=app.root
            )
            return

        record = get_one(rid)

        if not record:
            return

        confirm = messagebox.askyesno(
            "Delete Confirmation",
            f"Delete this tourist record?\n\n"
            f"{record['full_name']} ({record['country']})",
            parent=app.root
        )

        if not confirm:
            return

        try:

            ok, msg = delete(rid)

            if ok:

                messagebox.showinfo(
                    "Deleted",
                    msg,
                    parent=app.root
                )

                show(app)

            else:

                messagebox.showerror(
                    "Delete Failed",
                    msg,
                    parent=app.root
                )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e),
                parent=app.root
            )

    # ==================================
    # ACTION BUTTONS
    # ==================================

    app.button(
        buttons,
        "Delete",
        do_delete,
        True
    ).pack(
        side="right",
        padx=5
    )

    app.button(
        buttons,
        "Update",
        do_update,
        True
    ).pack(
        side="right",
        padx=5
    )
