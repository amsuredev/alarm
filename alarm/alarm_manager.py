from datetime import datetime

from alarm import Alarm


class AlarmManager:
    def __init__(self, alarm_list=[]):
        self.__alarm_list = alarm_list

    @property
    def alarm_list(self):
        return self.__alarm_list

    @alarm_list.setter
    def alarm_list(self, alarm_list):
        self.__alarm_list = alarm_list

    def add_allarm(self, alarm):
        self.__alarm_list.append(alarm)

    def run(self):
        while len(self.__alarm_list) != 0:
            current_time = datetime.now()
            self.__alarm_list = [alarm for alarm in self.__alarm_list if alarm.active and alarm >= current_time]
            for alarm in self.__alarm_list:
                if alarm == current_time:
                    alarm.play()


if __name__ == "__main__":
    alarm1 = Alarm(36, 20, 22, 1, 2021)  # min, hour, day, month, year
    alarm2 = Alarm(37, 20, 22, 1, 2021)
    listAlarm = []
    listAlarm.append(alarm1)
    listAlarm.append(alarm2)
    alarm_manager = AlarmManager(listAlarm)
    alarm_manager.run()
