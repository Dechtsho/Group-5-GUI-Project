
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

from PIL import Image, ImageTk, ImageOps

import db
from styles import LIGHT, DARK

import dashboard
import Add_tourist
import view_records
import search_record
import reports
import update_delete
import settings
import mobileview
import dark_mode

from login import show_login


class TourismApp:

    def __init__(self, root):
        self.root = root

        saved = db.get_settings()
        self.dark = bool(saved["dark_mode"])
        self.c = DARK if self.dark else LIGHT
        self.current_page = "Dashboard"

        self.root.title("Tourism Record Keeping System")
        self.root.geometry("1280x820")
        self.root.minsize(1000, 650)

        # Keep logo image reference
        self.logo_image = None

        self.build_shell()
        self.show_dashboard()

    def rebuild(self):
        self.c = DARK if self.dark else LIGHT

        db.save_settings(
            self.dark,
            bool(db.get_settings()["notifications"]),
            db.get_settings()["language"]
        )

        self.build_shell()

        page = self.current_page

        if page == "Dashboard":
            self.show_dashboard()

        elif page == "Add Tourist":
            self.show_add_tourist()

        elif page == "View Records":
            self.show_records()

        elif page == "Search Records":
            self.show_search()

        elif page == "Reports":
            self.show_reports()

        elif page == "Update / Delete":
            self.show_update()

        elif page == "Settings":
            self.show_settings()

        else:
            self.show_dashboard()

    def build_shell(self):

        for w in self.root.winfo_children():
            w.destroy()

        self.root.configure(bg=self.c["bg"])

        style = ttk.Style(self.root)

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Treeview",
            background=self.c["surface"],
            foreground=self.c["text"],
            fieldbackground=self.c["surface"],
            rowheight=38,
            bordercolor=self.c["border"]
        )

        style.configure(
            "Treeview.Heading",
            background=self.c["nav"],
            foreground="white",
            font=("Segoe UI", 9, "bold")
        )

        style.map(
            "Treeview",
            background=[("selected", self.c["primary"])]
        )

        style.configure(
            "TCombobox",
            fieldbackground=self.c["surface"],
            background=self.c["surface"],
            foreground=self.c["text"]
        )

        # ==============================
        # SIDEBAR
        # ==============================

        self.sidebar = tk.Frame(
            self.root,
            bg=self.c["nav"],
            width=225
        )

        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Sidebar Logo and Application Title
        logo = tk.Frame(
            self.sidebar,
            bg=self.c["nav"]
        )

        logo.pack(
            fill="x",
            padx=18,
            pady=(20, 22)
        )

        # Load login background image as application logo
        logo_path = (
            Path(__file__).resolve().parent
            / "assets"
            / "login_background.jpg"
        )

        try:
            original_image = Image.open(logo_path).convert("RGB")

            # Resize image into a square logo
            resized_image = ImageOps.fit(
                original_image,
                (40, 40),
                method=Image.Resampling.LANCZOS
            )

            self.logo_image = ImageTk.PhotoImage(resized_image)

            # Display application logo
            tk.Label(
                logo,
                image=self.logo_image,
                bg=self.c["nav"],
                bd=0
            ).pack(side="left", padx=(0, 8))

        except (FileNotFoundError, OSError) as e:

            print("Logo image could not be loaded:", e)

            # Fallback triangle icon
            tk.Label(
                logo,
                text="▲",
                bg=self.c["nav"],
                fg="white",
                font=("Segoe UI", 20, "bold")
            ).pack(side="left", padx=(0, 8))

        # Application title
        tk.Label(
            logo,
            text="Tourism Record\nKeeping System",
            bg=self.c["nav"],
            fg="white",
            justify="left",
            font=("Segoe UI", 11, "bold")
        ).pack(side="left")

        # ==============================
        # NAVIGATION BUTTONS
        # ==============================

        self.nav_buttons = {}

        items = [
            ("⌂", "Dashboard", self.show_dashboard),
            ("＋", "Add Tourist", self.show_add_tourist),
            ("▣", "View Records", self.show_records),
            ("⌕", "Search Records", self.show_search),
            ("▤", "Reports", self.show_reports),
            ("✎", "Update / Delete", self.show_update),
            ("⚙", "Settings", self.show_settings),
        ]

        for icon, name, command in items:

            b = tk.Button(
                self.sidebar,
                text=f"  {icon}   {name}",
                command=command,
                bg=self.c["nav"],
                fg="#DDE9F5",
                activebackground=self.c["primary"],
                activeforeground="white",
                relief="flat",
                bd=0,
                anchor="w",
                font=("Segoe UI", 10),
                padx=12,
                pady=11,
                cursor="hand2"
            )

            b.pack(
                fill="x",
                padx=10,
                pady=2
            )

            self.nav_buttons[name] = b

        tk.Frame(
            self.sidebar,
            bg=self.c["nav"]
        ).pack(fill="both", expand=True)

        # ==============================
        # MOBILE VIEW
        # ==============================

        tk.Button(
            self.sidebar,
            text="  ◱   Mobile View",
            command=self.show_mobile,
            bg=self.c["nav"],
            fg="#DDE9F5",
            activebackground=self.c["primary"],
            activeforeground="white",
            relief="flat",
            bd=0,
            anchor="w",
            font=("Segoe UI", 10),
            padx=12,
            pady=11,
            cursor="hand2"
        ).pack(fill="x", padx=10, pady=2)

        # ==============================
        # DARK MODE
        # ==============================

        tk.Button(
            self.sidebar,
            text="  ☾   Dark Mode" if not self.dark else "  ☀   Light Mode",
            command=self.toggle_dark,
            bg=self.c["nav"],
            fg="#DDE9F5",
            activebackground=self.c["primary"],
            activeforeground="white",
            relief="flat",
            bd=0,
            anchor="w",
            font=("Segoe UI", 10),
            padx=12,
            pady=11,
            cursor="hand2"
        ).pack(fill="x", padx=10, pady=2)

        # ==============================
        # LOGOUT
        # ==============================

        tk.Button(
            self.sidebar,
            text="  ⇥   Logout",
            command=self.logout,
            bg=self.c["nav"],
            fg="#DDE9F5",
            activebackground=self.c["red"],
            activeforeground="white",
            relief="flat",
            bd=0,
            anchor="w",
            font=("Segoe UI", 10),
            padx=12,
            pady=11,
            cursor="hand2"
        ).pack(fill="x", padx=10, pady=(2, 18))

        # ==============================
        # MAIN CONTENT AREA
        # ==============================

        main = tk.Frame(
            self.root,
            bg=self.c["bg"]
        )

        main.pack(
            side="left",
            fill="both",
            expand=True
        )

        # ==============================
        # TOP BAR
        # ==============================

        self.topbar = tk.Frame(
            main,
            bg=self.c["surface"],
            height=62,
            highlightthickness=1,
            highlightbackground=self.c["border"]
        )

        self.topbar.pack(fill="x")
        self.topbar.pack_propagate(False)

        self.page_title = tk.Label(
            self.topbar,
            text="Dashboard",
            bg=self.c["surface"],
            fg=self.c["text"],
            font=("Segoe UI", 14, "bold")
        )

        self.page_title.pack(
            side="left",
            padx=25
        )

        tk.Label(
            self.topbar,
            text="●",
            bg=self.c["surface"],
            fg=self.c["green"]
        ).pack(side="right", padx=(8, 5))

        tk.Label(
            self.topbar,
            text="Admin",
            bg=self.c["surface"],
            fg=self.c["text"],
            font=("Segoe UI", 9, "bold")
        ).pack(side="right", padx=5)

        tk.Label(
            self.topbar,
            text="◉",
            bg=self.c["surface"],
            fg=self.c["muted"],
            font=("Segoe UI", 13)
        ).pack(side="right", padx=8)

        # ==============================
        # PAGE CONTENT
        # ==============================

        self.content = tk.Frame(
            main,
            bg=self.c["bg"]
        )

        self.content.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=22
        )

    # ==============================
    # SET PAGE
    # ==============================

    def set_page(self, title, active):

        for w in self.content.winfo_children():
            w.destroy()

        self.current_page = active
        self.page_title.configure(text=title)

        subtitle = {
            "Dashboard": "Overview of tourism records",
            "Add Tourist": "Enter new tourist information",
            "Tourist Records": "Manage and view all tourist records",
            "Search Tourist Records": "Search by name, country, passport number or destination",
            "Reports": "View and generate tourism statistics",
            "Update / Delete Record": "Edit or remove a tourist record",
            "Settings": "Customize your application"
        }.get(title, "")

        tk.Label(
            self.content,
            text=title,
            bg=self.c["bg"],
            fg=self.c["text"],
            font=("Segoe UI", 20, "bold")
        ).pack(anchor="w")

        if subtitle:

            tk.Label(
                self.content,
                text=subtitle,
                bg=self.c["bg"],
                fg=self.c["muted"],
                font=("Segoe UI", 9)
            ).pack(
                anchor="w",
                pady=(2, 18)
            )

        for name, b in self.nav_buttons.items():

            b.configure(
                bg=self.c["primary"] if name == active else self.c["nav"]
            )

    # ==============================
    # CARD
    # ==============================

    def card(self, parent):

        return tk.Frame(
            parent,
            bg=self.c["surface"],
            highlightthickness=1,
            highlightbackground=self.c["border"]
        )

    # ==============================
    # LABEL
    # ==============================

    def label(self, parent, text, size=9, bold=False, color=None):

        return tk.Label(
            parent,
            text=text,
            bg=self.c["surface"],
            fg=color or self.c["text"],
            font=(
                "Segoe UI",
                size,
                "bold" if bold else "normal"
            )
        )

    # ==============================
    # BUTTON
    # ==============================

    def button(self, parent, text, command, primary=True):

        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=self.c["primary"] if primary else self.c["surface"],
            fg="white" if primary else self.c["text"],
            activebackground=self.c["primary2"] if primary else self.c["surface2"],
            activeforeground="white" if primary else self.c["text"],
            relief="flat",
            bd=0,
            font=("Segoe UI", 9, "bold"),
            padx=15,
            pady=8,
            cursor="hand2"
        )

    # ==============================
    # TREEVIEW
    # ==============================

    def make_tree(self, parent, rows, height=8):

        cols = (
            "id",
            "name",
            "country",
            "date",
            "destination",
            "passport",
            "purpose"
        )

        tree = ttk.Treeview(
            parent,
            columns=cols,
            show="headings",
            height=height
        )

        headers = [
            ("id", "ID", 50),
            ("name", "Name", 170),
            ("country", "Country", 120),
            ("date", "Arrival Date", 115),
            ("destination", "Destination", 120),
            ("passport", "Passport No.", 145),
            ("purpose", "Purpose", 110)
        ]

        for col, text, width in headers:

            tree.heading(col, text=text)
            tree.column(col, width=width)

        tree.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=12
        )

        for r in rows:

            tree.insert(
                "",
                "end",
                values=(
                    r["id"],
                    r["full_name"],
                    r["country"],
                    r["arrival_date"],
                    r["destination"],
                    r["passport_number"],
                    r["purpose"]
                )
            )

        return tree

    # ==============================
    # NAVIGATION FUNCTIONS
    # ==============================

    def show_dashboard(self):
        dashboard.show(self)

    def show_add_tourist(self):
        Add_tourist.show(self)

    def show_records(self):
        view_records.show(self)

    def show_search(self):
        search_record.show(self)

    def show_reports(self):
        reports.show(self)

    def show_update(self, record_id=None):
        update_delete.show(self, record_id)

    def show_settings(self):
        settings.show(self)

    def show_mobile(self):
        mobileview.show_mobile(self)

    def toggle_dark(self):
        dark_mode.toggle(self)

    def set_dark_preview(self, value):
        # Used by Settings.
        # The actual application changes when saved.
        pass

    # ==============================
    # LOGOUT FUNCTION
    # ==============================

    def logout(self):

        if messagebox.askyesno(
            "Logout",
            "Do you want to logout?",
            parent=self.root
        ):

            # Remove dashboard widgets
            for widget in self.root.winfo_children():
                widget.destroy()

            # Return to login screen
            show_login(
                self.root,
                lambda: TourismApp(self.root)
            )


# ==============================
# START APPLICATION
# ==============================

def start():

    db.init_db()

    root = tk.Tk()

    # Display login first
    show_login(
        root,
        lambda: TourismApp(root)
    )

    # Main event loop
    root.mainloop()


if __name__ == "__main__":
    start()
