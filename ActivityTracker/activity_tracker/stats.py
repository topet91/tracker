import sqlite3
import datetime
from collections import defaultdict
from datetime import timedelta


def get_stats(period):

    conn = sqlite3.connect("activity_log.db")
    c = conn.cursor()
    today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    if period == "today":
        start_time = today
    elif period == "week":
        start_time = today - timedelta(days=7)
    elif period == "month":
        start_time = today - timedelta(days=30)

    c.execute("SELECT app_name, SUM(duration) FROM activity WHERE timestamp >= ? GROUP BY app_name",
              (start_time,))
    results = c.fetchall()
    conn.close()

    stats = defaultdict(int)
    for app, duration in results:
        stats[app] += duration
    return stats