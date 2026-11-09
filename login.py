import tkinter as tk
from tkinter import messagebox
from pathlib import Path

# Pillow is required for resizing the background image
try:
    from PIL import Image, ImageTk
except ImportError:
    raise ImportError(
        "Pillow is required. Install it using:\n\n"
        "pip install pillow"
    )


# =========================================================
# FIND BACKGROUND IMAGE
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

background_options = [
    BASE_DIR / "assets" / "login_background_clean.png",
    BASE_DIR / "assets" / "login_background.jpg",
    BASE_DIR / "assets" / "login_background_clean.jpg"
]

BG = None

for image_path in background_options:
    if image_path.exists():
        BG = image_path
        break


# =========================================================
# LOGIN PAGE
# =========================================================

def show_login(on_success):

    root = tk.Tk()

    root.title("Tourism Record Keeping System - Login")

    # Window size
    root.geometry("1280x760")

    # Minimum window size
    root.minsize(900, 600)


    # =====================================================
    # BACKGROUND
    # =====================================================

    if BG is None:

        messagebox.showerror(
            "Background Image Not Found",
            "The tourism background image could not be found.\n\n"
            "Please make sure your image is inside:\n\n"
            "assets/login_background_clean.png"
        )

        root.destroy()
        return

    # Open background image
    original_image = Image.open(BG).convert("RGB")

    # Background label
    background_label = tk.Label(
        root,
        bd=0,
        highlightthickness=0
    )

    background_label.place(
        x=0,
        y=0,
        relwidth=1,
        relheight=1
    )


    # =====================================================
    # RESIZE BACKGROUND IMAGE
    # =====================================================

    def resize_background(event=None):

        window_width = root.winfo_width()
        window_height = root.winfo_height()

        if window_width < 1 or window_height < 1:
            return

        # Original image dimensions
        image_width, image_height = original_image.size

        # Calculate scale
        scale = max(
            window_width / image_width,
            window_height / image_height
        )

        # New image size
        new_width = int(image_width * scale)
        new_height = int(image_height * scale)

        # Resize image
        resized = original_image.resize(
            (new_width, new_height),
            Image.Resampling.LANCZOS
        )

        # Crop image to fit window
        left = (new_width - window_width) // 2
        top = (new_height - window_height) // 2

        right = left + window_width
        bottom = top + window_height

        resized = resized.crop(
            (left, top, right, bottom)
        )

        # Convert to Tkinter image
        photo = ImageTk.PhotoImage(resized)

        # Display image
        background_label.configure(image=photo)

        # Keep image reference
        background_label.image = photo


    # Resize whenever window size changes
    root.bind(
        "<Configure>",
        resize_background
    )

    # Initial background
    root.after(
        100,
        resize_background
    )


    # =====================================================
    # LOGIN PANEL
    # =====================================================

    panel = tk.Frame(
        root,
        bg="white",
        highlightthickness=1,
        highlightbackground="#DCE5EE"
    )

    panel.place(
        relx=0.5,
        rely=0.5,
        anchor="center",
        width=420,
        height=500
    )


    # =====================================================
    # LOGO
    # =====================================================

    tk.Label(
        panel,
        text="▲",
        bg="white",
        fg="#173D60",
        font=("Segoe UI", 28, "bold")
    ).pack(
        pady=(22, 2)
    )


    # =====================================================
    # APPLICATION TITLE
    # =====================================================

    tk.Label(
        panel,
        text="Tourism Record Keeping System",
        bg="white",
        fg="#173D60",
        font=("Segoe UI", 14, "bold")
    ).pack()


    tk.Label(
        panel,
        text="Explore  •  Record  •  Manage",
        bg="white",
        fg="#718096",
        font=("Segoe UI", 9)
    ).pack(
        pady=(2, 20)
    )


    # =====================================================
    # LOGIN TITLE
    # =====================================================

    tk.Label(
        panel,
        text="Login to your account",
        bg="white",
        fg="#18324B",
        font=("Segoe UI", 11, "bold")
    ).pack(
        anchor="w",
        padx=45
    )


    # =====================================================
    # USERNAME LABEL
    # =====================================================

    tk.Label(
        panel,
        text="Username",
        bg="white",
        fg="#18324B",
        font=("Segoe UI", 9, "bold")
    ).pack(
        anchor="w",
        padx=45,
        pady=(15, 5)
    )


    # =====================================================
    # USERNAME ENTRY
    # =====================================================

    user = tk.Entry(
        panel,
        bg="#F8FAFC",
        fg="#18324B",
        insertbackground="#18324B",
        relief="flat",
        highlightthickness=1,
        highlightbackground="#DCE5EE",
        highlightcolor="#087FF5",
        font=("Segoe UI", 10)
    )

    user.pack(
        fill="x",
        padx=45,
        ipady=10
    )


    # =====================================================
    # USERNAME ERROR MESSAGE
    # =====================================================

    username_error = tk.Label(
        panel,
        text="",
        bg="white",
        fg="#D93025",
        font=("Segoe UI", 8)
    )

    username_error.pack(
        anchor="w",
        padx=45,
        pady=(3, 0)
    )


    # =====================================================
    # PASSWORD LABEL
    # =====================================================

    tk.Label(
        panel,
        text="Password",
        bg="white",
        fg="#18324B",
        font=("Segoe UI", 9, "bold")
    ).pack(
        anchor="w",
        padx=45,
        pady=(10, 5)
    )


    # =====================================================
    # PASSWORD ENTRY
    # =====================================================

    password = tk.Entry(
        panel,
        bg="#F8FAFC",
        fg="#18324B",
        insertbackground="#18324B",
        relief="flat",
        highlightthickness=1,
        highlightbackground="#DCE5EE",
        highlightcolor="#087FF5",
        font=("Segoe UI", 10),
        show="•"
    )

    password.pack(
        fill="x",
        padx=45,
        ipady=10
    )


    # =====================================================
    # PASSWORD ERROR MESSAGE
    # =====================================================

    password_error = tk.Label(
        panel,
        text="",
        bg="white",
        fg="#D93025",
        font=("Segoe UI", 8)
    )

    password_error.pack(
        anchor="w",
        padx=45,
        pady=(3, 0)
    )


    # =====================================================
    # LOGIN FUNCTION
    # =====================================================

    def login():

        username = user.get().strip()
        entered_password = password.get()

        # Clear previous error messages
        username_error.config(text="")
        password_error.config(text="")


        # -------------------------------------------------
        # EMPTY USERNAME
        # -------------------------------------------------

        if username == "":

            username_error.config(
                text="Please enter your username."
            )

            user.focus_set()

            return


        # -------------------------------------------------
        # WRONG USERNAME
        # -------------------------------------------------

        if username != "admin":

            username_error.config(
                text="Incorrect username."
            )

            user.focus_set()

            return


        # -------------------------------------------------
        # EMPTY PASSWORD
        # -------------------------------------------------

        if entered_password == "":

            password_error.config(
                text="Please enter your password."
            )

            password.focus_set()

            return


        # -------------------------------------------------
        # WRONG PASSWORD
        # -------------------------------------------------

        if entered_password != "Admin@123":

            password_error.config(
                text="Wrong password."
            )

            password.focus_set()

            return


        # -------------------------------------------------
        # LOGIN SUCCESSFUL
        # -------------------------------------------------

        messagebox.showinfo(
            "Login Successful",
            "Welcome to the Tourism Record Keeping System!"
        )

        root.destroy()

        on_success()


    # =====================================================
    # LOGIN BUTTON
    # =====================================================

    login_button = tk.Button(
        panel,
        text="Login",
        command=login,
        bg="#087FF5",
        fg="white",
        activebackground="#0566D6",
        activeforeground="white",
        relief="flat",
        bd=0,
        font=("Segoe UI", 10, "bold"),
        cursor="hand2"
    )

    login_button.pack(
        fill="x",
        padx=45,
        pady=(15, 8),
        ipady=8
    )


    # =====================================================
    # FORGOT PASSWORD
    # =====================================================

    tk.Label(
        panel,
        text="Forgot Password?",
        bg="white",
        fg="#087FF5",
        font=("Segoe UI", 8)
    ).pack()


    # =====================================================
    # FOOTER
    # =====================================================

    tk.Label(
        panel,
        text="Manage tourism records efficiently and securely.",
        bg="white",
        fg="#9AA7B5",
        font=("Segoe UI", 8)
    ).pack(
        pady=(15, 2)
    )


    # =====================================================
    # ENTER KEY LOGIN
    # =====================================================

    root.bind(
        "<Return>",
        lambda event: login()
    )


    # Put cursor in username field
    user.focus_set()


    # =====================================================
    # START LOGIN WINDOW
    # =====================================================

    root.mainloop()