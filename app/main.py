import sys
import datetime
import socket

from datetime import date, datetime

from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QFont





class FullScreenWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Daily Reminder")
        self.showFullScreen()
        
        #CallbackTimerfor TIME
        self.timer = QTimer(self)
        # Connect the timer's timeout signal to the update_time slot
        self.timer.timeout.connect(self.update_time)
        # Set the interval in milliseconds (e.g., 1000ms = 1 second)
        self.interval = 1000
        self.timer.start(self.interval)
        
    def keyPressEvent(self, event):
        """Handle key press events to allow exiting full screen with Escape."""
        if event.key() == Qt.Key.Key_Escape:
            self.close()
            # Or use self.showNormal() to exit full screen mode without closing the window

    def update_time(self):
        """Slot to update the label with the current time."""
        # Day of Week = Monday is 0, Sunday is 6
        days_of_week = ["Monday","Tuesday","Wednesday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        day_of_week = date.today().weekday()
        # Month
        months_of_year = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        month = date.today().month
        day_of_month = date.today().day
        year = str(date.today().year)
        if 11 <= (day_of_month % 100) <= 13:
            suffix = 'th'
        else:
            # Dictionary lookup with 'th' as default for other cases
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day_of_month % 10, 'th')

        # Get the current date and time
        current_time = datetime.now()

        # Format the time string
        # %I for hour (12-hour clock), %M for minute, %S for second, %p for AM/PM
        formatted_time = current_time.strftime("%I:%M:%S %p")
        time_string = f"{days_of_week[day_of_week]}, {months_of_year[month]} {day_of_month}{suffix} {year} {formatted_time}"
        #print(time_string)
        self.time_label.setText(f"{days_of_week[day_of_week]}, {months_of_year[month]} {day_of_month}{suffix} {year} {formatted_time}")



def max_font_size(window:FullScreenWindow,label_text:str)->int:
    current_font_size = 16
    max_font_size = 200
    window.time_label.setText(label_text)
    while current_font_size < max_font_size:
        font = QFont("Arial", current_font_size) # You can also use other fonts like "Times New Roman"
        window.time_label.setFont(font)
        window.time_label.adjustSize()
        if window.time_label.width()>window.width():
            current_font_size -=2
            #print(f"Current Font Size:{current_font_size} Label Width:{window.time_label.width()} ")
            return current_font_size
        current_font_size +=2
    return 16

def screen_layout(window:FullScreenWindow):
    window.setWindowTitle("Daily Reminder")
    window.time_label = QLabel("Current time will appear here...", window)

def error_logging(logging_on:bool,WorA:str,text:str):
    if logging_on:
        hostname = socket.gethostname()
        prefix = ""
        if hostname=="DESKTOP-D17IECP":
            prefix = "C:\\Users\\Kevin\\Dropbox\\Python Projects\\Daily Reminders\\logs\\"
        if WorA=="W":
            with open(prefix+"logfile.txt", "w") as f:
                f.write(text+"\n")
        else: 
            with open(prefix+"logfile.txt", "a") as f:
                f.write(text+"\n")

def main():
    app_logging = True
    error_logging(app_logging,"W","Started App")
    error_logging(app_logging,"a",socket.gethostname())
    app = QApplication(sys.argv)
    window = FullScreenWindow()
    window.hide()
    screen_layout(window)
    font_size = max_font_size(window,"Thursday, February 10th 2026 12:08:49 AM")
    error_logging(app_logging,"A",f"Window Width:{window.width()}")
    error_logging(app_logging,"A",f"Font Size:{font_size}")
    font = QFont("Arial", font_size)
    window.time_label.setFont(font)

    

    window.show()
    sys.exit(app.exec())



if __name__ == '__main__':
    main()