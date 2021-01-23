import sqlite3
from alarm import Alarm


class AlarmDatabase:
    def __init__(self):
        conn = sqlite3.connect('alarm.db')  # create file if not exist;connect if exist
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS alarms (
                _id INTEGER PRIMARY KEY AUTOINCREMENT,
                ACTIVE NUMERIC,
                MIN INTEGER,
                HOUR INTEGER,
                DAY INTEGER,
                MONTH INTEGER,
                YEAR INTEGER,
                MELODY_PATH TEXT
                )""")
        cursor.close()
        conn.commit()
        conn.close()

    def insert_alarm(self, alarm: Alarm):
        conn = sqlite3.connect('alarm.db')  # create file if not exist;connect if exist
        cursor = conn.cursor()
        params = (alarm.active, alarm.min, alarm.hour, alarm.day, alarm.month, alarm.year, alarm.melody_path)
        cursor.execute(
            "INSERT INTO alarms(ACTIVE, MIN, HOUR, DAY, MONTH, YEAR, MELODY_PATH) VALUES (?, ?, ?, ?, ?, ?, ?)", params)
        cursor.close()
        conn.commit()
        conn.close()

    def get_active_alarms(self):
        conn = sqlite3.connect('alarm.db')  # create file if not exist;connect if exist
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM alarms WHERE ACTIVE = TRUE""")
        active_alarms_tumple = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        return [Alarm.createFromTumple(alarm_tumpe) for alarm_tumpe in active_alarms_tumple]#list of alarm objects

    def mark_alarm_as_inactive(self, id):
        conn = sqlite3.connect('alarm.db')  # create file if not exist;connect if exist
        cursor = conn.cursor()
        cursor.execute("""UPDATE alarms SET ACTIVE = FALSE
                WHERE _id = :id""", {'id': id})
        cursor.close()
        conn.commit()
        conn.close()

    def update_alarm_min(self, id, min):
        conn = sqlite3.connect('alarm.db')  # create file if not exist;connect if exist
        cursor = conn.cursor()
        cursor.execute("""UPDATE alarms SET MIN = :min
                        WHERE _id = :id""", {'id': id, "min": min})
        cursor.close()
        conn.commit()
        conn.close()

    def print_all_lines(self):
        conn = sqlite3.connect('alarm.db')  # create file if not exist;connect if exist
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM alarms""")
        lines = cursor.fetchall()
        for line in lines:
            print(line)
        cursor.close()
        conn.commit()
        conn.close()


if __name__=="__main__":
    alarm_db = AlarmDatabase()
    alarm_db.print_all_lines()