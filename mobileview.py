import tkinter as tk

def show_mobile(app):
    # Tkinter is a desktop GUI toolkit. This module provides a mobile-sized
    # responsive preview of the same application style.
    win = tk.Toplevel(app.root)
    win.title("Mobile Responsive View")
    win.geometry("390x760")
    win.minsize(320,600)
    win.configure(bg=app.c["bg"])

    top=tk.Frame(win,bg=app.c["nav"],height=58)
    top.pack(fill="x")
    top.pack_propagate(False)

    tk.Label(top,text="☰",bg=app.c["nav"],fg="white",
             font=("Segoe UI",18,"bold")).pack(side="left",padx=15)
    tk.Label(top,text="Tourism Record System",
             bg=app.c["nav"],fg="white",
             font=("Segoe UI",10,"bold")).pack(side="left")
    tk.Label(top,text="●",bg=app.c["nav"],fg=app.c["green"],
             font=("Segoe UI",10)).pack(side="right",padx=15)

    content=tk.Frame(win,bg=app.c["bg"])
    content.pack(fill="both",expand=True,padx=14,pady=14)

    tk.Label(content,text="Dashboard",bg=app.c["bg"],fg=app.c["text"],
             font=("Segoe UI",18,"bold")).pack(anchor="w")
    tk.Label(content,text="Responsive mobile layout",
             bg=app.c["bg"],fg=app.c["muted"],
             font=("Segoe UI",8)).pack(anchor="w",pady=(0,12))

    for title,value,color in [
        ("Total Tourists","0",app.c["primary"]),
        ("International","0",app.c["green"]),
        ("Domestic","0",app.c["purple"]),
        ("This Month","0",app.c["yellow"])
    ]:
        card=tk.Frame(content,bg=app.c["surface"],
                      highlightthickness=1,
                      highlightbackground=app.c["border"])
        card.pack(fill="x",pady=5)
        tk.Label(card,text=title,bg=app.c["surface"],
                 fg=app.c["muted"],font=("Segoe UI",8)).pack(
                     anchor="w",padx=15,pady=(10,0))
        tk.Label(card,text=value,bg=app.c["surface"],
                 fg=color,font=("Segoe UI",18,"bold")).pack(
                     anchor="w",padx=15,pady=(0,10))

    card=tk.Frame(content,bg=app.c["surface"],
                  highlightthickness=1,
                  highlightbackground=app.c["border"])
    card.pack(fill="both",expand=True,pady=8)
    tk.Label(card,text="Tourist Records",
             bg=app.c["surface"],fg=app.c["text"],
             font=("Segoe UI",10,"bold")).pack(anchor="w",
                                                padx=15,pady=15)
    tk.Label(card,text="No records available",
             bg=app.c["surface"],fg=app.c["muted"],
             font=("Segoe UI",9)).pack(pady=30)