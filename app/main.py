import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer, QDateTime
from PyQt6.QtGui import QFont
import random

from weather import OpenWeatherMapResponse, get_weather

Time_Font_Size = 48
Weather_Font_Size = 36
Message_Font_Size = 18
Appointments_Font_Size = 18
Holidays_Font_Size = 18
TV_Font_Size = 18
API_KEY = "dae6a4dddbdf38e9e44e492026e18c4b"
lat = 49.2488
lon = -122.9805

class KioskClock(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Kiosk Clock")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.showFullScreen()

        self.setStyleSheet("QWidget { background-color: #121212; } QLabel { color: #FFFFFF; }")

        # Clock label
        self.clock_label = QLabel("Loading Time...")
        self.clock_label.setFont(QFont("Arial", Time_Font_Size, QFont.Weight.Bold))
        self.clock_label.setStyleSheet("""
            color: #77DD77;
            font-weight: bold;
        """)

        # Weather label
        self.weather_label = QLabel("Loading Weather...")
        self.weather_label.setFont(QFont("Arial", Weather_Font_Size))
        self.weather_label.setStyleSheet("""
            color: #77DD77;
            font-weight: bold;
        """)
        
        # Appointments label
        self.appointments_title_label = QLabel("Appointments:")
        self.appointments_title_label.setFont(QFont("Arial", Appointments_Font_Size))
        self.appointments_title_label.setStyleSheet("""
            color: #77DD77;
            font-weight: bold;
        """)
        self.appointments_label = QLabel("Loading Appointments...")
        self.appointments_label.setFont(QFont("Arial", Appointments_Font_Size))

        # Holidays label
        self.holidays_title_label = QLabel("Holidays:")
        self.holidays_title_label.setFont(QFont("Arial", Holidays_Font_Size))
        self.holidays_title_label.setStyleSheet("""
            color: #77DD77;
            font-weight: bold;
        """)
        self.holidays_label = QLabel("Loading Holidays...")
        self.holidays_label.setFont(QFont("Arial", Holidays_Font_Size))

        # TV label
        self.tv_title_label = QLabel("What's on TV:")
        self.tv_title_label.setFont(QFont("Arial", TV_Font_Size))
        self.tv_title_label.setStyleSheet("""
            color: #77DD77;
            font-weight: bold;
        """)
        self.tv_label = QLabel("Loading TV...")
        self.tv_label.setFont(QFont("Arial", TV_Font_Size))

        # Message label
        self.message_title_label = QLabel("Messages:")
        self.message_title_label.setFont(QFont("Arial", Message_Font_Size))
        self.message_title_label.setStyleSheet("""
            color: #77DD77;
            font-weight: bold;
        """)
        self.message_label = QLabel("Loading messages...")
        self.message_label.setFont(QFont("Arial", Message_Font_Size))



        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(10)
        layout.addWidget(self.clock_label, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.weather_label, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.appointments_title_label, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.appointments_label, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.holidays_title_label, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.holidays_label, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.tv_title_label, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.tv_label, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.message_title_label, alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.message_label, alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft)
        self.setLayout(layout)

        # Timers
        self.time_timer = QTimer(self)
        self.time_timer.timeout.connect(self.update_time)
        self.time_timer.start(1000)
        self.update_time()

        self.weather_timer = QTimer(self)
        self.weather_timer.timeout.connect(self.update_weather)
        self.weather_timer.start(3600000)  # 1 hour
        self.update_weather()

        self.item_timer = QTimer(self)
        self.item_timer.timeout.connect(self.update_all_items)
        self.item_timer.start(900000)  # 15 minutes
        self.update_all_items()

    def update_time(self):
        now = QDateTime.currentDateTime()
        day = now.date().day()
        suffix = self.day_suffix(day)
        formatted_time = f"{now.toString('dddd, MMMM')} {day}{suffix} {now.toString('yyyy hh:mm:ss ap')}"
        self.clock_label.setText(formatted_time)

    def update_weather(self):
        # Fetch JSON
        json_data = get_weather(
            lat=lat,
            lon=lon,
            api_key=API_KEY,
            exclude="alerts,hourly,minutely",
            units="metric"
        )

        OpenWeather = OpenWeatherMapResponse.from_dict(json_data)

        self.weather_label.setText(f"{str.title(OpenWeather.current.description)} / Now: {round(OpenWeather.current.temp_c())}°C / Low: {round(OpenWeather.daily[0].temp_min_c)}°C / High: {round(OpenWeather.daily[0].temp_max_c)}°C")
    
    def update_all_items(self):
        self.appointments_label.setText("Friday, Feb 6th - Haircut with Jennifer 10:00 AM - 12:00 PM\r\nFriday, Feb 6th - Bingo 1:00 PM - 2:00 PM\r\nFriday, Feb 6th - Grocery Shopping 3:30 PM - 5:00 PM\r\nFriday, Feb 6th - Call with Louise 6:00 PM - 7:00 PM")
        self.holidays_label.setText("Saturday,Feb 14th - Valentine's Day\r\nSunday, Feb 18th - Family Day")
        schedule= "Friday, Feb  5 -  8am - Morning News - Ch  2\r\nFriday, Feb  5 - 10am - Antiques Roadshow - Ch 12\r\nFriday, Feb  5 - 12pm - Classic Movie Matinee: Casablanca - Ch  7\r\nFriday, Feb  5 -  2pm - Gardening Tips with Martha - Ch  9\r\nFriday, Feb  5 -  4pm - The Lawrence Welk Show - Ch  5\r\nFriday, Feb  5 -  6pm - Evening News - Ch  2\r\nFriday, Feb  5 -  8pm - Masterpiece Theatre: Downton Abbey - Ch 11"
        self.tv_label.setText(schedule)  # Example placeholder
        
        self.message_label.setText("Have a wonderful day!\r\nDerrick and Louise are in Port Hardy - Returning Sunday")

    def day_suffix(self, day):
        if 11 <= day <= 13:
            return "th"
        return {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            QApplication.quit()

def main():
    app = QApplication(sys.argv)
    kiosk = KioskClock()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
