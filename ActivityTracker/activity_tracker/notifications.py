from plyer import notification


def notify_limit_exceeded(app_name, time_limit):

    notification.notify(
        title="Трекер активности",
        message=f"Превышен лимит времени {time_limit} минут для {app_name}!",
        timeout=10
    )