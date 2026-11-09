
import tkinter as tk
from datetime import datetime, date


# =========================================
# DASHBOARD
# =========================================

def show(app):

    app.set_page("Dashboard", "Dashboard")

    rows = get_all_records()

    total = len(rows)

    # Count international and domestic tourists
    international = sum(
        1 for r in rows
        if (r["country"] or "").strip().lower() != "bhutan"
    )

    domestic = total - international

    # Count tourists arriving this month
    today = date.today()

    this_month = sum(
        1 for r in rows
        if get_arrival_date(r["arrival_date"])
        and get_arrival_date(r["arrival_date"]).month == today.month
        and get_arrival_date(r["arrival_date"]).year == today.year
    )

    # ==================================
    # SUMMARY CARDS
    # ==================================

    cards = tk.Frame(
        app.content,
        bg=app.c["bg"]
    )

    cards.pack(
        fill="x",
        pady=(0, 18)
    )

    metrics = [
        ("◉", "Total Tourists", total, app.c["primary"]),
        ("◎", "International", international, app.c["green"]),
        ("●", "Domestic", domestic, app.c["purple"]),
        ("▣", "This Month", this_month, app.c["yellow"]),
    ]

    for icon, title, value, color in metrics:

        card = app.card(cards)

        card.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 12)
        )

        tk.Label(
            card,
            text=icon,
            bg=app.c["surface"],
            fg=color,
            font=("Segoe UI", 18)
        ).pack(
            side="left",
            padx=15,
            pady=15
        )

        box = tk.Frame(
            card,
            bg=app.c["surface"]
        )

        box.pack(
            side="left",
            pady=12
        )

        app.label(
            box,
            title,
            8,
            color=app.c["muted"]
        ).pack(anchor="w")

        app.label(
            box,
            str(value),
            20,
            True
        ).pack(anchor="w")

    # ==================================
    # MIDDLE SECTION
    # ==================================

    middle = tk.Frame(
        app.content,
        bg=app.c["bg"]
    )

    middle.pack(
        fill="both",
        expand=True
    )

    # ==================================
    # TOURIST ARRIVALS CHART
    # ==================================

    chart_card = app.card(middle)

    chart_card.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(0, 10)
    )

    app.label(
        chart_card,
        "Tourist Arrivals (Last 6 Months)",
        10,
        True
    ).pack(
        anchor="w",
        padx=18,
        pady=15
    )

    canvas = tk.Canvas(
        chart_card,
        bg=app.c["surface"],
        highlightthickness=0
    )

    canvas.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=5
    )

    draw_arrivals_chart(canvas, app, rows)

    # ==================================
    # TOURISTS BY COUNTRY
    # ==================================

    country_card = app.card(middle)

    country_card.pack(
        side="left",
        fill="both",
        expand=True
    )

    app.label(
        country_card,
        "Tourists by Country",
        10,
        True
    ).pack(
        anchor="w",
        padx=18,
        pady=15
    )

    donut = tk.Canvas(
        country_card,
        bg=app.c["surface"],
        highlightthickness=0
    )

    donut.pack(
        fill="both",
        expand=True
    )

    draw_country_donut(donut, app, rows)

    # ==================================
    # RECENT TOURIST RECORDS
    # ==================================

    recent = app.card(app.content)

    recent.pack(
        fill="both",
        expand=True,
        pady=(15, 0)
    )

    app.label(
        recent,
        "Recent Tourist Records",
        10,
        True
    ).pack(
        anchor="w",
        padx=18,
        pady=12
    )

    if not rows:

        app.label(
            recent,
            "No tourist records yet. Use 'Add Tourist' to create the first record.",
            10,
            color=app.c["muted"]
        ).pack(pady=25)

    else:

        # get_all() returns oldest records first.
        # Reverse the list to display the newest five records.
        recent_rows = list(reversed(rows))[:5]

        app.make_tree(recent, recent_rows)


# =========================================
# GET TOURIST RECORDS
# =========================================

def get_all_records():

    from db import get_all

    return get_all()


# =========================================
# CONVERT ARRIVAL DATE
# =========================================

def get_arrival_date(value):

    if not value:
        return None

    formats = [
        "%d/%m/%Y",
        "%Y-%m-%d"
    ]

    for fmt in formats:

        try:
            return datetime.strptime(
                value,
                fmt
            ).date()

        except ValueError:
            continue

    return None


# =========================================
# GET LAST SIX MONTHS
# =========================================

def get_last_six_months():

    today = date.today()

    months = []

    for i in range(5, -1, -1):

        month = today.month - i
        year = today.year

        while month <= 0:
            month += 12
            year -= 1

        months.append((year, month))

    return months


# =========================================
# DRAW TOURIST ARRIVALS CHART
# =========================================

def draw_arrivals_chart(canvas, app, rows):

    months = get_last_six_months()

    month_counts = {
        month: 0 for month in months
    }

    # Count tourist arrivals in each month
    for r in rows:

        arrival = get_arrival_date(
            r["arrival_date"]
        )

        if arrival:

            key = (arrival.year, arrival.month)

            if key in month_counts:
                month_counts[key] += 1

    def draw(event=None):

        canvas.delete("all")

        w = max(canvas.winfo_width(), 420)
        h = max(canvas.winfo_height(), 220)

        x0 = 50
        y0 = 25
        x1 = w - 25
        y1 = h - 45

        counts = list(month_counts.values())

        max_count = max(counts) if counts else 0

        # Avoid division by zero
        chart_max = max(1, max_count)

        # Draw horizontal grid lines and labels
        for i in range(5):

            y = y0 + i * (y1 - y0) / 4

            value = round(
                chart_max * (4 - i) / 4
            )

            canvas.create_line(
                x0,
                y,
                x1,
                y,
                fill=app.c["border"]
            )

            canvas.create_text(
                x0 - 12,
                y,
                text=str(value),
                fill=app.c["muted"],
                font=("Segoe UI", 8),
                anchor="e"
            )

        points = []

        # Draw monthly points
        for i, (year, month) in enumerate(months):

            x = x0 + i * (x1 - x0) / 5

            count = month_counts[(year, month)]

            y = y1 - (
                count / chart_max
            ) * (y1 - y0)

            points.append((x, y))

            # Month labels
            month_name = datetime(
                year,
                month,
                1
            ).strftime("%b")

            canvas.create_text(
                x,
                y1 + 20,
                text=month_name,
                fill=app.c["muted"],
                font=("Segoe UI", 8)
            )

            # Display count above each point
            canvas.create_text(
                x,
                y - 13,
                text=str(count),
                fill=app.c["text"],
                font=("Segoe UI", 8)
            )

        # Draw connecting line
        if len(points) > 1:

            coordinates = []

            for x, y in points:
                coordinates.extend([x, y])

            canvas.create_line(
                *coordinates,
                fill=app.c["primary"],
                width=2,
                smooth=True
            )

        # Draw data points
        for x, y in points:

            canvas.create_oval(
                x - 4,
                y - 4,
                x + 4,
                y + 4,
                fill=app.c["primary"],
                outline=""
            )

        if max_count == 0:

            canvas.create_text(
                (x0 + x1) / 2,
                (y0 + y1) / 2,
                text="No arrival data yet",
                fill=app.c["muted"],
                font=("Segoe UI", 10)
            )

    canvas.bind(
        "<Configure>",
        draw
    )

    canvas.after(80, draw)


# =========================================
# DRAW TOURISTS BY COUNTRY DONUT CHART
# =========================================

def draw_country_donut(canvas, app, rows):

    countries = {}

    # Count tourists from each country
    for r in rows:

        country = (r["country"] or "").strip()

        if not country:
            country = "Unknown"

        countries[country] = (
            countries.get(country, 0) + 1
        )

    # Sort countries by tourist count
    sorted_countries = sorted(
        countries.items(),
        key=lambda x: x[1],
        reverse=True
    )

    # Chart colours
    colors = [
        app.c["primary"],
        app.c["green"],
        app.c["purple"],
        app.c["yellow"],
        "#E76F51",
        "#2A9D8F",
        "#8D6E63",
        "#607D8B"
    ]

    def draw(event=None):

        canvas.delete("all")

        w = max(canvas.winfo_width(), 350)
        h = max(canvas.winfo_height(), 220)

        total = sum(countries.values())

        cx = w * 0.32
        cy = h * 0.48

        radius = min(
            70,
            h * 0.30,
            w * 0.19
        )

        # No records available
        if total == 0:

            canvas.create_oval(
                cx - radius,
                cy - radius,
                cx + radius,
                cy + radius,
                outline=app.c["border"],
                width=18
            )

            canvas.create_text(
                cx,
                cy - 5,
                text="0",
                fill=app.c["text"],
                font=("Segoe UI", 20, "bold")
            )

            canvas.create_text(
                cx,
                cy + 18,
                text="Total",
                fill=app.c["muted"],
                font=("Segoe UI", 8)
            )

            canvas.create_text(
                w * 0.72,
                cy,
                text="No country data yet",
                fill=app.c["muted"],
                font=("Segoe UI", 9)
            )

            return

        # Draw donut segments
        start_angle = 90

        for index, (country, count) in enumerate(
            sorted_countries
        ):

            extent = (
                count / total
            ) * 360

            color = colors[index % len(colors)]

            canvas.create_arc(
                cx - radius,
                cy - radius,
                cx + radius,
                cy + radius,
                start=start_angle,
                extent=extent,
                style="arc",
                outline=color,
                width=18
            )

            start_angle += extent

        # Donut centre text
        canvas.create_text(
            cx,
            cy - 5,
            text=str(total),
            fill=app.c["text"],
            font=("Segoe UI", 20, "bold")
        )

        canvas.create_text(
            cx,
            cy + 18,
            text="Total",
            fill=app.c["muted"],
            font=("Segoe UI", 8)
        )

        # Country legend
        legend_x = w * 0.60
        legend_y = max(25, cy - len(sorted_countries) * 11)

        for index, (country, count) in enumerate(
            sorted_countries
        ):

            color = colors[index % len(colors)]

            y = legend_y + index * 25

            canvas.create_oval(
                legend_x,
                y,
                legend_x + 9,
                y + 9,
                fill=color,
                outline=""
            )

            canvas.create_text(
                legend_x + 16,
                y + 4,
                text=country,
                fill=app.c["text"],
                font=("Segoe UI", 8),
                anchor="w"
            )

            canvas.create_text(
                w - 15,
                y + 4,
                text=str(count),
                fill=app.c["muted"],
                font=("Segoe UI", 8),
                anchor="e"
            )

    canvas.bind(
        "<Configure>",
        draw
    )

    canvas.after(80, draw)
