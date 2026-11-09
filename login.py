
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
from PIL import Image, ImageTk


# Get the project folder location
BASE_DIR = Path(__file__).resolve().parent

# Find the login background image
ASSETS_DIR = BASE_DIR / "assets"

IMAGE_FILES = [
    "login_background_clean.png",
    "login_background.jpg",
    "login_background_clean.jpg"
]

BG_PATH = None

for filename in IMAGE_FILES:
    path = ASSETS_DIR / filename
    if path.exists():
        BG_PATH = path
        break


def show_login(root, on_success):

    root.title("Tourism Record Keeping System - Login")
    root.geometry("1280x820")
    root.minsize(1000, 650)
    root.configure(bg="#10243A")

    # Background image label
    background_label = tk.Label(root, bg="#10243A")
    background_label.place(
        x=0, y=0,
        relwidth=1,
        relheight=1
    )

    background_label.lower()

    # Keep a reference to the background image
    background_label.image = None

    # Resize background image when window size changes
    def resize_background(event=None):

        if event is not None and event.widget != root:
            return

        if BG_PATH is not None:
            try:
                image = Image.open(BG_PATH)

                width = root.winfo_width()
                height = root.winfo_height()

                if width < 1 or height < 1:
                    return

                image = image.resize(
                    (width, height),
                    Image.Resampling.LANCZOS
                )

                photo = ImageTk.PhotoImage(image)

                background_label.configure(image=photo)
                background_label.image = photo

            except Exception as e:
                print("Background image error:", e)

    root.bind("<Configure>", resize_background)
    root.after(100, resize_background)

    # Login panel
    login_frame = tk.Frame(
        root,
        bg="white",
        width=380,
        height=430
    )

    login_frame.place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )

    login_frame.pack_propagate(False)

    # Application title
    tk.Label(
        login_frame,
        text="Tourism Record",
        bg="white",
        fg="#173B5E",
        font=("Segoe UI", 23, "bold")
    ).pack(pady=(35, 0))

    tk.Label(
        login_frame,
        text="Keeping System",
        bg="white",
        fg="#173B5E",
        font=("Segoe UI", 18, "bold")
    ).pack(pady=(0, 8))

    tk.Label(
        login_frame,
        text="Please login to continue",
        bg="white",
        fg="#777777",
        font=("Segoe UI", 10)
    ).pack(pady=(0, 25))

    # Username
    tk.Label(
        login_frame,
        text="Username",
        bg="white",
        fg="#333333",
        font=("Segoe UI", 10, "bold")
    ).pack(anchor="w", padx=40)

    username_entry = tk.Entry(
        login_frame,
        font=("Segoe UI", 11),
        relief="solid",
        bd=1
    )

    username_entry.pack(
        fill="x",
        padx=40,
        ipady=9,
        pady=(5, 15)
    )

    # Password
    tk.Label(
        login_frame,
        text="Password",
        bg="white",
        fg="#333333",
        font=("Segoe UI", 10, "bold")
    ).pack(anchor="w", padx=40)

    password_entry = tk.Entry(
        login_frame,
        font=("Segoe UI", 11),
        show="*",
        relief="solid",
        bd=1
    )

    password_entry.pack(
        fill="x",
        padx=40,
        ipady=9,
        pady=(5, 10)
    )

    # Error message label
    error_label = tk.Label(
        login_frame,
        text="",
        bg="white",
        fg="red",
        font=("Segoe UI", 9)
    )

    error_label.pack()

    # Login button function
    def login(event=None):

        username = username_entry.get().strip()
        password = password_entry.get()

        if username == "admin" and password == "Admin@123":

            # Remove login screen event bindings
            root.unbind("<Configure>")
            root.unbind("<Return>")

            # Remove login screen widgets
            for widget in root.winfo_children():
                widget.destroy()

            # Open the dashboard directly
            on_success()

        else:
            error_label.config(
                text="Incorrect username or password. Please try again."
            )

            password_entry.delete(0, tk.END)
            password_entry.focus_set()

    # Login button
    login_button = tk.Button(
        login_frame,
        text="LOGIN",
        command=login,
        bg="#1769AA",
        fg="white",
        activebackground="#0F4F85",
        activeforeground="white",
        font=("Segoe UI", 11, "bold"),
        relief="flat",
        bd=0,
        cursor="hand2"
    )

    login_button.pack(
        fill="x",
        padx=40,
        pady=(15, 10),
        ipady=10
    )

    # Press Enter to login
    root.bind("<Return>", login)

    username_entry.focus_set()
