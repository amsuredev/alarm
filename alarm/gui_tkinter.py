import tkinter
from tkinter import ttk, filedialog
from alarm_manager import AlarmManager
from tkcalendar import Calendar
import os
from alarm import Alarm


class UI:
   def __init__(self, alarm_manager=AlarmManager()):
      self.__alarm_manager = alarm_manager

   def gui(self):
      def renew():
         self.__alarm_manager.renew_play_alarms()
         list_alarms.delete(0, tkinter.END)
         for alarm in self.__alarm_manager.alarm_list:
            list_alarms.insert(tkinter.END, alarm)

      def delete_selected_item():
         sel = list_alarms.curselection()
         for index in sel[::-1]:
            id = int(str(list_alarms.get(index)).split("-")[-1])#parse string to get id
            self.__alarm_manager.alarm_db.mark_alarm_as_inactive(id)#mark as inactive alarm with setted id
            list_alarms.delete(index)#remove from representation

      def add_alarm():
         if str(inputted_date['text']) != "RRRR-MM-DD" and str(inputted_hour.get()) != "" and str(inputted_min.get()) != "":
            #values were inputted
            date_in_integers = [int(date_num) for date_num in str(inputted_date['text']).split("-")]
            self.__alarm_manager.add_alarm(Alarm(int(inputted_min.get()), int(inputted_hour.get()), date_in_integers[2], date_in_integers[1], date_in_integers[0], melody_path=str(label_melody_path['text'])))
            renew()


      def open_file():
         my_filetypes = [('text files', '.wav')]
         file_path_ask = filedialog.askopenfilename(parent=root, initialdir=os.getcwd(), title="Please select a file:",
                                                    filetypes=my_filetypes)
         if file_path_ask != "":
            label_melody_path["text"] = file_path_ask


      def show_calendar():
         def set_text_date_label():
            inputted_date['text'] = cal.selection_get()
         top = tkinter.Toplevel(root)
         import datetime
         today = datetime.date.today()
         mindate = today
         maxdate = today + datetime.timedelta(days=365)
         print(mindate, maxdate)
         cal = Calendar(top, font="Arial 14", selectmode='day', locale='en_US',
                        mindate=mindate, maxdate=maxdate, disabledforeground='red',
                        cursor="hand1", year=2018, month=2, day=5)
         cal.pack(fill="both", expand=True)
         ttk.Button(top, text="ok", command=set_text_date_label).pack()


      root = tkinter.Tk()
      label_alarms = tkinter.Label(text="Alarms")
      label_alarms.grid(row=0, column=0)

      label_actual_alarms = tkinter.Label(text="Actual alarms:")
      label_actual_alarms.grid(row=1, column=0)

      button_renew = tkinter.Button(text="Renew", command=renew)
      button_renew.grid(row=1, column=1)

      button_delete = tkinter.Button(text="Delete", command=delete_selected_item)
      button_delete.grid(row=1, column=2)

      scrollbar = tkinter.Scrollbar(root)
      scrollbar.grid(row=2, column=1)

      list_alarms = tkinter.Listbox(root, yscrollcommand=scrollbar.set)
      list_alarms.grid(row=2, column=0)
      #refresh lines before insert
      self.__alarm_manager.renew_play_alarms()
      for alarm in self.__alarm_manager.alarm_list:
         list_alarms.insert(tkinter.END, alarm)

      scrollbar.config(command=list_alarms.yview)

      label_new_alarm = tkinter.Label(text="New Alarm:")
      label_new_alarm.grid(row=3, column=0, columnspan=3)

      date_label = tkinter.Label(text="Choose date")
      date_label.grid(row=4, column=0)

      date_button = tkinter.Button(text="Date", command=show_calendar)
      date_button.grid(row=4, column=1)

      inputted_date = tkinter.Label(text="RRRR-MM-DD")
      inputted_date.grid(row=4, column=2)

      label_choose_hour = tkinter.Label(text="Choose hour")
      label_choose_hour.grid(row=5, column=0)

      inputted_hour = ttk.Combobox(root, values=[x for x in range(24)])
      inputted_hour.grid(row=5, column=1)

      label_choose_min = tkinter.Label(text="Choose min")
      label_choose_min.grid(row=6, column=0)

      inputted_min = ttk.Combobox(root, values=[x for x in range(60)])
      inputted_min.grid(row=6, column=1)

      choose_melody = tkinter.Label(text="Choose melody")
      choose_melody.grid(row=7, column=0)

      button_get_melody = tkinter.Button(text="Melody", command=open_file)
      button_get_melody.grid(row=7, column=1)

      label_melody_path = tkinter.Label(text=r"C:\Users\User\PycharmProjects\Clock\alarm\default_alarm.wav")
      label_melody_path.grid(row=8, column=0, columnspan=2)

      button_add_alarm = tkinter.Button(text="Add alarm", command=add_alarm)
      button_add_alarm.grid(row=9, column=1)


      root.mainloop()
      print("end")



ui = UI()
ui.gui()
