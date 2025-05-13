import time
import datetime
import pygetwindow as gw
from plyer import notification
from .database import log_activity, get_total_time_today, get_notification_settings

tracking = True


def track_activity():

    last_app = None
    start_time = None
    notified_apps = set()
    while tracking:
        try:
            active_window = gw.getActiveWindow()
            current_time = datetime.datetime.now()
            if active_window and active_window.title:
                current_app = active_window.title
                if "Telegram" in current_app:
                    current_app = "Telegram"
                else:
                    current_app = (current_app.split(" - ")[-1]
                                  if " - " in current_app else current_app)

                if last_app is None:
                    last_app = current_app
                    start_time = current_time

                if current_app != last_app:
                    duration = int((current_time - start_time).total_seconds())
                    log_activity(last_app, start_time, duration)
                    start_time = current_time
                    last_app = current_app


                if current_app not in notified_apps:
                    total_time = get_total_time_today(current_app)
                    settings = get_notification_settings(current_app)
                    if settings and settings[1] and total_time >= settings[0] * 60:
                        notification.notify(
                            title="Трекер активности",
                            message=(f"Превышен лимит времени {settings[0]} минут "
                                     f"для {current_app}!"),
                            timeout=10
                        )
                        notified_apps.add(current_app)
            else:

                if last_app and start_time:
                    duration = int((current_time - start_time).total_seconds())
                    log_activity(last_app, start_time, duration)
                last_app = None
                start_time = None

            time.sleep(1)
        except Exception:
            time.sleep(1)


    if last_app and start_time:
        duration = int((datetime.datetime.now() - start_time).total_seconds())
        log_activity(last_app, start_time, duration)