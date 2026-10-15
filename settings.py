import tkinter as tk
from tkinter import ttk, messagebox
from db import get_settings, save_settings

def show(app):
    app.set_page("Settings", "Settings")

    card=app.card(app.content)
    card.pack(fill="both",expand=True)

    inner=tk.Frame(card,bg=app.c["surface"])
    inner.pack(fill="both",expand=True,padx=30,pady=25)

    current=get_settings()
    dark=tk.BooleanVar(value=bool(current["dark_mode"]))
    notifications=tk.BooleanVar(value=bool(current["notifications"]))
    language=tk.StringVar(value=current["language"])

    app.label(inner,"Appearance",11,True).pack(anchor="w",pady=(5,10))
    tk.Checkbutton(
        inner,text="Dark Mode",
        variable=dark,
        command=lambda: app.set_dark_preview(dark.get()),
        bg=app.c["surface"],fg=app.c["text"],
        selectcolor=app.c["surface2"],
        activebackground=app.c["surface"],
        activeforeground=app.c["text"]
    ).pack(anchor="w")

    app.label(inner,"Notifications",11,True).pack(
        anchor="w",pady=(25,8))
    tk.Checkbutton(
        inner,text="Enable notifications",
        variable=notifications,
        bg=app.c["surface"],fg=app.c["text"],
        selectcolor=app.c["surface2"],
        activebackground=app.c["surface"],
        activeforeground=app.c["text"]
    ).pack(anchor="w")

    app.label(inner,"Language",11,True).pack(
        anchor="w",pady=(25,8))
    ttk.Combobox(
        inner,textvariable=language,
        values=["English","Dzongkha"],
        state="readonly",width=25
    ).pack(anchor="w")

    app.button(
        inner,"Save Settings",
        lambda: save(app,dark.get(),notifications.get(),language.get()),
        True
    ).pack(fill="x",pady=30)

def save(app,dark,notifications,language):
    save_settings(dark,notifications,language)

    if dark != app.dark:
        app.dark=dark
        app.rebuild()
    else:
        messagebox.showinfo("Settings","Settings saved successfully.")
