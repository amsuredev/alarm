import pyaudio
import wave
from datetime import datetime
from tkinter import messagebox, Tk


class Alarm:
    MIN_MOVE_ALARM = 1

    def __init__(self, min, hour, day, month, year, melody_path="default_alarm.wav", id=None, active=True):
        self.__id = id
        self.__active = active
        self.__month = month
        self.__day = day
        self.__hour = hour
        self.__min = min
        self.__melody_path = melody_path
        self.__year = year

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id

    @property
    def month(self):
        return self.__month

    @property
    def day(self):
        return self.__day

    @property
    def hour(self):
        return self.__hour

    @property
    def min(self):
        return self.__min

    @property
    def year(self):
        return self.__year

    @property
    def melody_path(self):
        return self.__melody_path

    @property
    def active(self):
        return self.__active

    @active.setter
    def active(self, active):
        self.__active = active

    @month.setter
    def month(self, month):
        if month in range(1, 12):
            self.__month = month

    def play(self):
        wf = wave.open(self.__melody_path, 'rb')
        p = pyaudio.PyAudio()
        def callback(in_data, frame_count, time_info, status):
            data = wf.readframes(frame_count)
            return (data, pyaudio.paContinue)

        # open stream using callback
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True,
                        stream_callback=callback)
        while stream.is_active():
            root = Tk()
            root.withdraw()  # hide obligatory root window
            answer_positive = messagebox.askyesno("Budzik {hour}:{min}".format(hour=self.hour, min=self.min), "Usuń budzik?")
            if answer_positive:
                #usun budzik
                stream.stop_stream()
                self.__active = False
            else:
                #przenies budzik
                self.__min += self.MIN_MOVE_ALARM
                stream.stop_stream()
        stream.close()
        p.terminate()
        wf.close()
        return answer_positive

    def __str__(self):
        return '{year} {month} {day} {hour} {min} {melody_path}'.format(year=self.year, month=self.month, day=self.day, hour=self.hour, min=self.min, melody_path=self.melody_path)

    def __eq__(self, other):
        return self.min == other.minute and self.hour == other.hour and self.day == other.day and self.month == other.month and self.year == other.year

    def __ge__(self, other):
        return (self.year, self.month, self.day, self.hour, self.min) >= (
        other.year, other.month, other.day, other.hour, other.minute)
    @classmethod
    def createFromTumple(cls, tumple):#necesary for db
        return Alarm(min=tumple[2], hour=tumple[3], day=tumple[4], month=tumple[5], year=tumple[6], melody_path=tumple[7], id=tumple[0], active=tumple[1])

if __name__ == "__main__":
    alarm1 = Alarm(10, 19, 22, 1, 2021)#min, hour, day, month, year
    alarm2 = Alarm(9, 19, 22, 1, 2021)
    listAlarm = []
    listAlarm.append(alarm1)
    listAlarm.append(alarm2)

    while len(listAlarm) != 0:
        current_time = datetime.now()
        listAlarm = [alarm for alarm in listAlarm if alarm.active]
        for alarm in listAlarm:
            if alarm == current_time:
                alarm.play()
