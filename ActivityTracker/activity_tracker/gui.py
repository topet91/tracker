import tkinter as tk
from tkinter import ttk
import threading
from .tracker import track_activity, tracking
from .stats import get_stats
from .database import get_today_apps, get_notification_settings, save_notification_settings, get_total_time_today


class ActivityTrackerApp:

    def __init__(self, root):

        self.root = root
        self.root.title("Трекер активности")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f0f0")


        self.tracking_thread = threading.Thread(target=track_activity, daemon=True)
        self.tracking_thread.start()


        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)


        self.active_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.active_tab, text="Текущая активность")

        self.active_frame = ttk.LabelFrame(self.active_tab, text="Использование приложений", padding=10)
        self.active_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.active_scrollbar = ttk.Scrollbar(self.active_frame, orient="vertical")
        self.active_canvas = tk.Canvas(self.active_frame, yscrollcommand=self.active_scrollbar.set, bg="#f0f0f0")
        self.active_scrollbar.config(command=self.active_canvas.yview)
        self.active_inner_frame = ttk.Frame(self.active_canvas)

        self.active_canvas.create_window((0, 0), window=self.active_inner_frame, anchor="nw")
        self.active_inner_frame.bind("<Configure>", lambda e: self.active_canvas.configure(
            scrollregion=self.active_canvas.bbox("all")))

        self.active_canvas.pack(side="left", fill="both", expand=True)
        self.active_scrollbar.pack(side="right", fill="y")

        self.active_labels = {}
        self.update_active_time()

        # Tab 2: Statistics
        self.stats_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.stats_tab, text="Статистика")

        self.stats_frame = ttk.LabelFrame(self.stats_tab, text="Статистика использования", padding=10)
        self.stats_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.stats_btn_frame = ttk.Frame(self.stats_frame)
        self.stats_btn_frame.pack(fill="x", pady=5)

        self.today_btn = ttk.Button(self.stats_btn_frame, text="Сегодня", command=lambda: self.show_stats("today"))
        self.today_btn.pack(side="left", padx=5)

        self.week_btn = ttk.Button(self.stats_btn_frame, text="Последняя неделя",
                                   command=lambda: self.show_stats("week"))
        self.week_btn.pack(side="left", padx=5)

        self.month_btn = ttk.Button(self.stats_btn_frame, text="Последний месяц",
                                    command=lambda: self.show_stats("month"))
        self.month_btn.pack(side="left", padx=5)

        self.stats_text = tk.Text(self.stats_frame, height=10, width=50, font=("Arial", 10))
        self.stats_text.pack(fill="both", expand=True, pady=5)

        # Tab 3: Notifications
        self.notify_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.notify_tab, text="Уведомления")

        self.notify_frame = ttk.LabelFrame(self.notify_tab, text="Настройки уведомлений", padding=10)
        self.notify_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.notify_scrollbar = ttk.Scrollbar(self.notify_frame, orient="vertical")
        self.notify_canvas = tk.Canvas(self.notify_frame, yscrollcommand=self.notify_scrollbar.set, bg="#f0f0f0")
        self.notify_scrollbar.config(command=self.notify_canvas.yview)
        self.notify_inner_frame = ttk.Frame(self.notify_canvas)

        self.notify_canvas.create_window((0, 0), window=self.notify_inner_frame, anchor="nw")
        self.notify_inner_frame.bind("<Configure>", lambda e: self.notify_canvas.configure(
            scrollregion=self.notify_canvas.bbox("all")))

        self.notify_canvas.pack(side="left", fill="both", expand=True)
        self.notify_scrollbar.pack(side="right", fill="y")

        self.app_vars = {}
        self.limit_entries = {}
        self.update_notification_settings()

        self.save_btn = ttk.Button(self.notify_frame, text="Сохранить настройки", command=self.save_settings)
        self.save_btn.pack(pady=10)


        self.quit_btn = ttk.Button(self.root, text="Выход", command=self.quit)
        self.quit_btn.pack(pady=10)

    def update_active_time(self):

        times = get_total_time_today()
        current_apps = set(times.keys())
        existing_apps = set(self.active_labels.keys())


        for app in existing_apps - current_apps:
            self.active_labels[app].destroy()
            del self.active_labels[app]


        for app, duration in times.items():
            hours = duration // 3600
            minutes = (duration % 3600) // 60
            seconds = duration % 60
            time_str = f"{app}: {hours}ч {minutes}м {seconds}с"
            if app in self.active_labels:
                self.active_labels[app].config(text=time_str)
            else:
                label = ttk.Label(self.active_inner_frame, text=time_str, font=("Arial", 10))
                label.pack(anchor="w", pady=2)
                self.active_labels[app] = label


        self.root.after(1000, self.update_active_time)

    def update_notification_settings(self):

        for widget in self.notify_inner_frame.winfo_children():
            widget.destroy()

        apps = get_today_apps()
        for app in apps:
            frame = ttk.Frame(self.notify_inner_frame)
            frame.pack(fill="x", pady=2)

            var = tk.BooleanVar()
            settings = get_notification_settings(app)
            var.set(settings[1] if settings else False)
            self.app_vars[app] = var

            chk = ttk.Checkbutton(frame, text=app, variable=var)
            chk.pack(side="left")

            limit_var = tk.StringVar()
            limit_var.set(str(settings[0]) if settings and settings[0] else "60")
            entry = ttk.Entry(frame, textvariable=limit_var, width=10)
            entry.pack(side="left", padx=5)
            self.limit_entries[app] = limit_var

            ttk.Label(frame, text="минут").pack(side="left")

    def save_settings(self):

        for app, var in self.app_vars.items():
            enabled = var.get()
            try:
                time_limit = int(self.limit_entries[app].get())
            except ValueError:
                time_limit = 60
            save_notification_settings(app, time_limit, enabled)
        self.update_notification_settings()

    def show_stats(self, period):

        stats = get_stats(period)
        self.stats_text.delete(1.0, tk.END)
        if not stats:
            self.stats_text.insert(tk.END, f"Нет записей активности за {period}.")
        else:
            for app, duration in stats.items():
                hours = duration // 3600
                minutes = (duration % 3600) // 60
                seconds = duration % 60
                self.stats_text.insert(tk.END, f"{app}: {hours}ч {minutes}м {seconds}с\n")

    def quit(self):

        global tracking
        tracking = False
        self.root.quit()