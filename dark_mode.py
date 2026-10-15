def enable(app):
    """Turn on real application-wide dark mode."""
    if not app.dark:
        app.dark = True
        app.rebuild()

def disable(app):
    """Turn off dark mode and return to light mode."""
    if app.dark:
        app.dark = False
        app.rebuild()

def toggle(app):
    app.dark = not app.dark
    app.rebuild()
