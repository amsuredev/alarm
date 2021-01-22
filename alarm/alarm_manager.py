from datetime import datetime
from alarm import Alarm


class AlarmManager:
    def __init__(self, alarm_list=[], alarm_notes_path="alarm_notes.txt"):
        self.__alarm_list = alarm_list
        self.__alarm_notes_path=alarm_notes_path

    @property
    def alarm_list(self):
        return self.__alarm_list

    @alarm_list.setter
    def alarm_list(self, alarm_list):
        self.__alarm_list = alarm_list

    def add_alarm(self, alarm):
        self.__alarm_list.append(alarm)

    def run(self):
        while len(self.__alarm_list) != 0:
            current_time = datetime.now()
            self.__alarm_list = [alarm for alarm in self.__alarm_list if alarm.active and alarm >= current_time]
            for alarm in self.__alarm_list:
                if alarm == current_time:
                    alarm.play()

    def write_alarms(self):
        for alarm in self.__alarm_list:
            alarm.write_file(self.__alarm_notes_path)


    @staticmethod
    def create_from_file(alarm_notes_path="alarm_notes.txt"):
        alarm_note_file = open(alarm_notes_path, 'r')
        alarm_list = []
        for line in alarm_note_file.readlines():
            alarm_list.append(Alarm.createFromFileNotation(line))
        return AlarmManager(alarm_list)



if __name__ == "__main__":
    #alarm1 = Alarm(2, 22, 22, 1, 2021)  # min, hour, day, month, year
    #alarm2 = Alarm(1, 22, 22, 1, 2021)
    #listAlarm = []
    #listAlarm.append(alarm1)
    #listAlarm.append(alarm2)
    #alarm_manager = AlarmManager(listAlarm)
    #alarm_manager.write_alarms()
    #alarm_manager.run()
    my_alarm_manager = AlarmManager.create_from_file()
    my_alarm_manager.run()
