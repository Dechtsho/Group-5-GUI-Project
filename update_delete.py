import tkinter as tk
from tkinter import ttk, messagebox
from db import get_all, get_one, update, delete
from styles import COUNTRIES, DESTINATIONS, PURPOSES

def show(app, record_id=None):
    app.set_page("Update / Delete", "Update / Delete Record")

    list_card = app.card(app.content)
    list_card.pack(fill="x", pady=(0,15))

    rows = get_all()
    tree = app.make_tree(list_card, rows, height=6)

    form = app.card(app.content)
    form.pack(fill="both", expand=True)

    inner = tk.Frame(form, bg=app.c["surface"])
    inner.pack(fill="both", expand=True, padx=25, pady=15)
    inner.columnconfigure(0, weight=1)
    inner.columnconfigure(1, weight=1)

    fields = [
        ("Full Name","full_name","entry"),
        ("Country","country","combo"),
        ("Passport Number","passport_number","entry"),
        ("Arrival Date","arrival_date","entry"),
        ("Accommodation","accommodation","entry"),
        ("Destination","destination","combo"),
        ("Purpose of Visit","purpose","combo")
    ]

    widgets = {}

    for i,(label,key,kind) in enumerate(fields):
        col,row=i%2,i//2
        box=tk.Frame(inner,bg=app.c["surface"])
        box.grid(row=row,column=col,sticky="ew",padx=15,pady=7)
        app.label(box,label,8,True).pack(anchor="w",pady=(0,4))

        if kind=="combo":
            vals=COUNTRIES if key=="country" else (
                DESTINATIONS if key=="destination" else PURPOSES
            )
            w=ttk.Combobox(box,values=vals,state="readonly")
        else:
            w=tk.Entry(box,bg=app.c["surface2"],fg=app.c["text"],
                       insertbackground=app.c["text"],relief="flat",
                       highlightthickness=1,
                       highlightbackground=app.c["border"])
        w.pack(fill="x",ipady=7)
        widgets[key]=w

    def selected_id():
        item=tree.focus()
        if not item:
            return None
        return int(tree.item(item,"values")[0])

    def load(rid):
        row=get_one(rid)
        if not row:
            return
        for k,w in widgets.items():
            value=row[k] or ""
            if isinstance(w,ttk.Combobox):
                w.set(value)
            else:
                w.delete(0,"end")
                w.insert(0,value)

    def select(event=None):
        rid=selected_id()
        if rid:
            load(rid)

    tree.bind("<<TreeviewSelect>>", select)

    if record_id:
        for item in tree.get_children():
            if int(tree.item(item,"values")[0]) == record_id:
                tree.selection_set(item)
                tree.focus(item)
                load(record_id)
                break

    buttons=tk.Frame(form,bg=app.c["surface"])
    buttons.pack(side="bottom",fill="x",padx=25,pady=15)

    def do_update():
        rid=selected_id()
        if not rid:
            messagebox.showwarning("Select Record",
                                   "Please select a record.")
            return
        data={k:w.get().strip() for k,w in widgets.items()}
        ok,msg=update(rid,data)
        if ok:
            messagebox.showinfo("Updated",msg)
            show(app,rid)
        else:
            messagebox.showerror("Error",msg)

    def do_delete():
        rid=selected_id()
        if not rid:
            messagebox.showwarning("Select Record",
                                   "Please select a record.")
            return
        row=get_one(rid)
        if messagebox.askyesno(
            "Delete Confirmation",
            f"Are you sure you want to delete this record?\n\n"
            f"{row['full_name']} ({row['country']})"
        ):
            delete(rid)
            messagebox.showinfo("Deleted","Record deleted successfully.")
            show(app)

    app.button(buttons,"Delete",do_delete,True).pack(
        side="right",padx=5)
    app.button(buttons,"Update",do_update,True).pack(
        side="right",padx=5)