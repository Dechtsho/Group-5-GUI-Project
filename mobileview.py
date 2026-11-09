
import tkinter as tk
from tkinter import ttk, messagebox

import dashboard
import Add_tourist
import view_records
import search_record
import reports
import update_delete
import settings


class MobileAppProxy:
    """
    Provides a mobile-sized interface while reusing
    the existing desktop application modules.
    """

    def __init__(self, app, win):

        self.app = app
        self.root = win
        self.win = win

        self.c = app.c
        self.dark = app.dark

        self.current_page = "Dashboard"
        self.nav_buttons = {}

        self.menu_visible = False
        self.page_title = None

        self.build_interface()

    # ==================================
    # BUILD MOBILE INTERFACE
    # ==================================

    def build_interface(self):

        self.win.configure(bg=self.c["bg"])

        # Top navigation bar
        self.topbar = tk.Frame(
            self.win,
            bg=self.c["nav"],
            height=58
        )

        self.topbar.pack(fill="x")
        self.topbar.pack_propagate(False)

        # Menu button
        self.menu_button = tk.Button(
            self.topbar,
            text="☰",
            command=self.toggle_menu,
            bg=self.c["nav"],
            fg="white",
            font=("Segoe UI", 18, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2"
        )

        self.menu_button.pack(side="left", padx=12)

        # Application title
        tk.Label(
            self.topbar,
            text="Tourism Record System",
            bg=self.c["nav"],
            fg="white",
            font=("Segoe UI", 10, "bold")
        ).pack(side="left")

        # Status indicator
        tk.Label(
            self.topbar,
            text="●",
            bg=self.c["nav"],
            fg=self.c["green"],
            font=("Segoe UI", 10)
        ).pack(side="right", padx=15)

        # Navigation menu
        self.menu_frame = tk.Frame(
            self.win,
            bg=self.c["surface"],
            highlightthickness=1,
            highlightbackground=self.c["border"]
        )

        # Menu buttons
        menu_items = [
            ("⌂", "Dashboard", self.show_dashboard),
            ("＋", "Add Tourist", self.show_add_tourist),
            ("▣", "View Records", self.show_records),
            ("⌕", "Search Records", self.show_search),
            ("▤", "Reports", self.show_reports),
            ("✎", "Update / Delete", self.show_update),
            ("⚙", "Settings", self.show_settings)
        ]

        for icon, name, command in menu_items:

            btn = tk.Button(
                self.menu_frame,
                text=f"{icon}   {name}",
                command=lambda n=name, c=command: self.navigate(n, c),
                bg=self.c["surface"],
                fg=self.c["text"],
                activebackground=self.c["primary"],
                activeforeground="white",
                anchor="w",
                relief="flat",
                bd=0,
                padx=15,
                pady=10,
                font=("Segoe UI", 10),
                cursor="hand2"
            )

            btn.pack(fill="x", padx=5, pady=1)

            self.nav_buttons[name] = btn

        # Dark mode
        tk.Button(
            self.menu_frame,
            text="☾   Dark / Light Mode",
            command=self.toggle_dark,
            bg=self.c["surface"],
            fg=self.c["text"],
            activebackground=self.c["primary"],
            activeforeground="white",
            anchor="w",
            relief="flat",
            bd=0,
            padx=15,
            pady=10,
            font=("Segoe UI", 10),
            cursor="hand2"
        ).pack(fill="x", padx=5)

        # Logout
        tk.Button(
            self.menu_frame,
            text="⇥   Logout",
            command=self.logout,
            bg=self.c["surface"],
            fg=self.c["red"],
            activebackground=self.c["red"],
            activeforeground="white",
            anchor="w",
            relief="flat",
            bd=0,
            padx=15,
            pady=10,
            font=("Segoe UI", 10),
            cursor="hand2"
        ).pack(fill="x", padx=5, pady=(0, 5))

        # ==================================
        # SCROLLABLE PAGE AREA
        # ==================================

        self.canvas = tk.Canvas(
            self.win,
            bg=self.c["bg"],
            highlightthickness=0
        )

        self.scrollbar = ttk.Scrollbar(
            self.win,
            orient="vertical",
            command=self.canvas.yview
        )

        self.canvas.configure(
            yscrollcommand=self.scrollbar.set
        )

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.content = tk.Frame(
            self.canvas,
            bg=self.c["bg"]
        )

        self.content_window = self.canvas.create_window(
            (0, 0),
            window=self.content,
            anchor="nw"
        )

        self.content.bind(
            "<Configure>",
            self.update_scroll
        )

        self.canvas.bind(
            "<Configure>",
            self.resize_content
        )

        self.canvas.bind_all(
            "<MouseWheel>",
            self.mouse_scroll
        )

    # ==================================
    # SCROLLING
    # ==================================

    def update_scroll(self, event=None):

        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )

    def resize_content(self, event):

        self.canvas.itemconfigure(
            self.content_window,
            width=event.width
        )

    def mouse_scroll(self, event):

        self.canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    # ==================================
    # NAVIGATION MENU
    # ==================================

    def toggle_menu(self):

        if self.menu_visible:

            self.menu_frame.pack_forget()
            self.menu_visible = False

        else:

            self.menu_frame.pack(
                fill="x",
                before=self.canvas
            )

            self.menu_visible = True

    def navigate(self, name, command):

        self.menu_frame.pack_forget()
        self.menu_visible = False

        command()

    # ==================================
    # PAGE MANAGEMENT
    # ==================================

    def set_page(self, title, active):

        for widget in self.content.winfo_children():
            widget.destroy()

        self.current_page = active

        self.page_title = title

        self.canvas.yview_moveto(0)

        # Page heading
        tk.Label(
            self.content,
            text=title,
            bg=self.c["bg"],
            fg=self.c["text"],
            font=("Segoe UI", 18, "bold")
        ).pack(
            anchor="w",
            padx=12,
            pady=(15, 2)
        )

        subtitle = {
            "Dashboard": "Overview of tourism records",
            "Add Tourist": "Enter new tourist information",
            "Tourist Records": "Manage and view tourist records",
            "Search Tourist Records": "Search tourist records",
            "Reports": "Tourism statistics and reports",
            "Update / Delete Record": "Edit or remove records",
            "Settings": "Customize your application"
        }.get(title, "")

        if subtitle:

            tk.Label(
                self.content,
                text=subtitle,
                bg=self.c["bg"],
                fg=self.c["muted"],
                font=("Segoe UI", 9)
            ).pack(
                anchor="w",
                padx=12,
                pady=(0, 12)
            )

        # Highlight active navigation item
        for name, button in self.nav_buttons.items():

            button.configure(
                bg=self.c["primary"] if name == active
                else self.c["surface"],
                fg="white" if name == active
                else self.c["text"]
            )

    # ==================================
    # CARD
    # ==================================

    def card(self, parent):

        return tk.Frame(
            parent,
            bg=self.c["surface"],
            highlightthickness=1,
            highlightbackground=self.c["border"]
        )

    # ==================================
    # LABEL
    # ==================================

    def label(
        self,
        parent,
        text,
        size=9,
        bold=False,
        color=None
    ):

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

    # ==================================
    # BUTTON
    # ==================================

    def button(
        self,
        parent,
        text,
        command,
        primary=True
    ):

        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=self.c["primary"] if primary
            else self.c["surface"],
            fg="white" if primary
            else self.c["text"],
            activebackground=self.c["primary2"] if primary
            else self.c["surface2"],
            activeforeground="white",
            relief="flat",
            bd=0,
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=8,
            cursor="hand2"
        )

    # ==================================
    # TREEVIEW
    # ==================================

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

        frame = tk.Frame(
            parent,
            bg=self.c["surface"]
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=8
        )

        tree = ttk.Treeview(
            frame,
            columns=cols,
            show="headings",
            height=height
        )

        headers = [
            ("id", "ID", 40),
            ("name", "Name", 120),
            ("country", "Country", 95),
            ("date", "Arrival Date", 100),
            ("destination", "Destination", 105),
            ("passport", "Passport No.", 110),
            ("purpose", "Purpose", 100)
        ]

        for col, heading, width in headers:

            tree.heading(col, text=heading)

            tree.column(
                col,
                width=width,
                minwidth=60,
                stretch=False
            )

        x_scroll = ttk.Scrollbar(
            frame,
            orient="horizontal",
            command=tree.xview
        )

        y_scroll = ttk.Scrollbar(
            frame,
            orient="vertical",
            command=tree.yview
        )

        tree.configure(
            xscrollcommand=x_scroll.set,
            yscrollcommand=y_scroll.set
        )

        tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

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

    # ==================================
    # NAVIGATION FUNCTIONS
    # ==================================

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

    # ==================================
    # DARK MODE
    # ==================================

    def toggle_dark(self):

        self.menu_frame.pack_forget()
        self.menu_visible = False

        # Toggle the main application theme
        self.app.toggle_dark()

        self.c = self.app.c
        self.dark = self.app.dark

        # Refresh mobile interface
        self.refresh()

    # ==================================
    # REFRESH CURRENT PAGE
    # ==================================

    def refresh(self):

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

    # ==================================
    # REBUILD
    # ==================================

    def rebuild(self):

        self.c = self.app.c
        self.dark = self.app.dark

        self.refresh()

    # ==================================
    # LOGOUT
    # ==================================

    def logout(self):

        if messagebox.askyesno(
            "Logout",
            "Do you want to logout?",
            parent=self.win
        ):

            self.win.destroy()
            self.app.logout()


# ======================================
# OPEN MOBILE VIEW
# ======================================

def show_mobile(app):

    win = tk.Toplevel(app.root)

    win.title("Tourism Record Keeping - Mobile View")

    win.geometry("390x760")
    win.minsize(320, 600)

    # Create mobile application
    mobile_app = MobileAppProxy(app, win)

    # Display actual dashboard
    mobile_app.show_dashboard()

    # Keep window reference
    app.mobile_window = win
    app.mobile_app = mobile_app

    return win
