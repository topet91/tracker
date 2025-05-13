import sqlite3
import datetime


def init_db():

    conn = sqlite3.connect("activity_log.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS activity (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 app_name TEXT,
                 timestamp DATETIME,
                 duration INTEGER
                 )""")
    c.execute("""CREATE TABLE IF NOT EXISTS settings (
                 app_name TEXT PRIMARY KEY,
                 time_limit INTEGER,
                 enabled INTEGER
                 )""")
    conn.commit()
    conn.close()


def log_activity(app_name, timestamp, duration):

    if duration <= 0:
        return  # Skip logging if duration is invalid
    conn = sqlite3.connect("activity_log.db")
    c = conn.cursor()
    c.execute("INSERT INTO activity (app_name, timestamp, duration) VALUES (?, ?, ?)",
              (app_name, timestamp, duration))
    conn.commit()
    conn.close()


def get_total_time_today(app_name=None):

    conn = sqlite3.connect("activity_log.db")
    c = conn.cursor()
    today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    if app_name:
        c.execute("SELECT SUM(duration) FROM activity WHERE app_name = ? AND timestamp >= ?",
                  (app_name, today))
        result = c.fetchone()[0]
        conn.close()
        return result if result else 0
    else:
        c.execute("SELECT app_name, SUM(duration) FROM activity WHERE timestamp >= ? GROUP BY app_name",
                  (today,))
        results = c.fetchall()
        conn.close()
        return {app: duration if duration else 0 for app, duration in results}


def get_notification_settings(app_name):

    conn = sqlite3.connect("activity_log.db")
    c = conn.cursor()
    c.execute("SELECT time_limit, enabled FROM settings WHERE app_name = ?", (app_name,))
    result = c.fetchone()
    conn.close()
    return result


def save_notification_settings(app_name, time_limit, enabled):

    conn = sqlite3.connect("activity_log.db")
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO settings (app_name, time_limit, enabled) VALUES (?, ?, ?)",
              (app_name, time_limit, enabled))
    conn.commit()
    conn.close()


def get_today_apps():

    conn = sqlite3.connect("activity_log.db")
    c = conn.cursor()
    today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    c.execute("SELECT DISTINCT app_name FROM activity WHERE timestamp >= ?", (today,))
    apps = [row[0] for row in c.fetchall()]
    conn.close()
    return apps