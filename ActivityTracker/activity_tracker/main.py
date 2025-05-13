import tkinter as tk

try:
    from .database import init_db
    from .gui import ActivityTrackerApp
except ImportError:

    from ActivityTracker.activity_tracker.database import init_db
    from ActivityTracker.activity_tracker.gui import ActivityTrackerApp


def main():

    init_db()
    root = tk.Tk()
    app = ActivityTrackerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()