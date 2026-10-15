import tkinter as tk
from db import get_all

def show(app):
    app.set_page("Dashboard", "Dashboard")
    rows = get_all()
    total = len(rows)
    international = sum(1 for r in rows if r["country"] != "Bhutan")
    domestic = total - international

    cards = tk.Frame(app.content, bg=app.c["bg"])
    cards.pack(fill="x", pady=(0, 18))

    metrics = [
        ("◉", "Total Tourists", total, app.c["primary"]),
        ("◎", "International", international, app.c["green"]),
        ("●", "Domestic", domestic, app.c["purple"]),
        ("▣", "This Month", 0, app.c["yellow"]),
    ]

    for icon, title, value, color in metrics:
        card = app.card(cards)
        card.pack(side="left", fill="x", expand=True, padx=(0, 12))
        tk.Label(card, text=icon, bg=app.c["surface"], fg=color,
                 font=("Segoe UI", 18)).pack(side="left", padx=15, pady=15)
        box = tk.Frame(card, bg=app.c["surface"])
        box.pack(side="left", pady=12)
        app.label(box, title, 8, color=app.c["muted"]).pack(anchor="w")
        app.label(box, str(value), 20, True).pack(anchor="w")

    middle = tk.Frame(app.content, bg=app.c["bg"])
    middle.pack(fill="both", expand=True)

    chart_card = app.card(middle)
    chart_card.pack(side="left", fill="both", expand=True, padx=(0, 10))
    app.label(chart_card, "Tourist Arrivals (Last 6 Months)",
              10, True).pack(anchor="w", padx=18, pady=15)

    canvas = tk.Canvas(chart_card, bg=app.c["surface"], highlightthickness=0)
    canvas.pack(fill="both", expand=True, padx=10, pady=5)
    draw_empty_chart(canvas, app)

    country_card = app.card(middle)
    country_card.pack(side="left", fill="both", expand=True)
    app.label(country_card, "Tourists by Country",
              10, True).pack(anchor="w", padx=18, pady=15)

    donut = tk.Canvas(country_card, bg=app.c["surface"], highlightthickness=0)
    donut.pack(fill="both", expand=True)
    draw_empty_donut(donut, app)

    recent = app.card(app.content)
    recent.pack(fill="both", expand=True, pady=(15, 0))
    app.label(recent, "Recent Tourist Records",
              10, True).pack(anchor="w", padx=18, pady=12)

    if not rows:
        app.label(recent,
                  "No tourist records yet. Use 'Add Tourist' to create the first record.",
                  10, color=app.c["muted"]).pack(pady=25)
    else:
        app.make_tree(recent, rows[:5])

def draw_empty_chart(canvas, app):
    def draw(event=None):
        canvas.delete("all")
        w = max(canvas.winfo_width(), 420)
        h = max(canvas.winfo_height(), 220)
        x0, y0, x1, y1 = 55, 20, w-25, h-45
        for i in range(5):
            y = y0 + i*(y1-y0)/4
            canvas.create_line(x0, y, x1, y, fill=app.c["border"])
        months = ["Apr", "May", "Jun", "Jul", "Aug", "Sep"]
        pts = []
        for i, m in enumerate(months):
            x = x0 + i*(x1-x0)/5
            y = y1 - (y1-y0)*0.05
            pts.append((x, y))
            canvas.create_oval(x-3,y-3,x+3,y+3,
                               fill=app.c["primary"], outline="")
            canvas.create_text(x, y1+18, text=m,
                               fill=app.c["muted"], font=("Segoe UI",8))
        canvas.create_line(*sum(([a,b] for a,b in pts), []),
                           fill=app.c["primary"], width=2)
        canvas.create_text(w/2, h/2, text="No arrival data yet",
                           fill=app.c["muted"], font=("Segoe UI",10))
    canvas.bind("<Configure>", draw)
    canvas.after(80, draw)

def draw_empty_donut(canvas, app):
    def draw(event=None):
        canvas.delete("all")
        w = max(canvas.winfo_width(), 350)
        h = max(canvas.winfo_height(), 220)
        cx, cy = w*.38, h*.5
        r = min(75, h*.32)
        canvas.create_oval(cx-r, cy-r, cx+r, cy+r,
                           outline=app.c["border"], width=18)
        canvas.create_text(cx, cy-5, text="0",
                           fill=app.c["text"], font=("Segoe UI",20,"bold"))
        canvas.create_text(cx, cy+18, text="Total",
                           fill=app.c["muted"], font=("Segoe UI",8))
        canvas.create_text(w*.70, h*.5, text="No country data yet",
                           fill=app.c["muted"], font=("Segoe UI",9))
    canvas.bind("<Configure>", draw)
    canvas.after(80, draw)
