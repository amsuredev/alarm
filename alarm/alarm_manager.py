from datetime import datetime
from alarm import Alarm
from alarm_db import AlarmDatabase

class AlarmManager:
    def __init__(self, alarm_db=AlarmDatabase()):
        self.__alarm_db = alarm_db
        self.renew_play_alarms()#define __alarm_list

    @property
    def alarm_db(self):
        return self.__alarm_db

    @alarm_db.setter
    def alarm_db(self):
        return self.__alarm_db

    @property
    def alarm_list(self):
        return self.__alarm_list

    @alarm_list.setter
    def alarm_list(self, alarm_list):
        self.__alarm_list = alarm_list

    def add_alarm(self, alarm):#add to datebase; renew list alarms
        self.__alarm_db.insert_alarm(alarm)
        self.renew_play_alarms()

    def run(self):
        while len(self.__alarm_list) != 0:
            current_time = datetime.now()
            self.renew_play_alarms()
            for alarm in self.__alarm_list:
                if alarm == current_time:
                    remove_answer = alarm.play()
                    if remove_answer:
                        self.__alarm_db.mark_alarm_as_inactive(alarm.id)#alarm remove in next step cycle
                    else:
                        self.__alarm_db.update_alarm_min(id=alarm.id, min=alarm.min)#alarm active; time, changed

    def renew_play_alarms(self):
        self.__alarm_list = self.alarm_db.get_active_alarms()
        current_time = datetime.now()
        self.__alarm_list = [alarm for alarm in self.__alarm_list if alarm.active and alarm >= current_time]




if __name__ == "__main__":
    my_alarm_manager = AlarmManager()
    alarm1 = Alarm(17, 18, 23, 1, 2021)
    my_alarm_manager.add_alarm(alarm1)
    '''
    alarm1 = Alarm(38, 17, 23, 1, 2021)  # min, hour, day, month, year
    alarm2 = Alarm(40, 17, 23, 1, 2021)
    alarm2 = Alarm(40, 17, 23, 1, 2021)
    alarm2 = Alarm(41, 17, 23, 1, 2021)
    '''
    my_alarm_manager.run()
