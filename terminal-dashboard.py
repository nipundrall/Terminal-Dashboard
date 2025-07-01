import sys
import psutil
import time
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout
)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt, QTimer

#For Sucessful run on Fedora 
# sudo dnf install python3 python3-pip
# pip3 install --user PyQt5 psutil
# python3 /path/to/terminal-dashboard.py
# For Debian or Arch or Any other just install the same packages.

# === USER CONFIG START Change this to the style of your liking. ===
CLOCK_COLOR = "#4f7bc2"   # For Date Color
DATE_COLOR = "#c46ab1"    # For Time Color
SYSTEM_COLOR = "#398c2a"  # For System Status Color
BG_COLOR = "#000000"      # For Background Color
FONT_FAMILY = "Helvetica" # Font Can be Changed here
# === USER CONFIG END ===


class Wallboard(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Wallboard Clock")
        self.showFullScreen()

        # Set background color
        self.setAutoFillBackground(True)
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(BG_COLOR))
        self.setPalette(palette)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(0)

        # --- Center Time/Date Layout ---
        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignCenter)
        center_layout.setContentsMargins(125, 125, 125, 125)
        center_layout.setSpacing(90)

        self.time_label = QLabel()
        self.time_label.setFont(QFont(FONT_FAMILY, 195, QFont.Bold))
        self.time_label.setStyleSheet(f"color: {CLOCK_COLOR}")
        self.time_label.setAlignment(Qt.AlignCenter)

        date_row = QHBoxLayout()
        date_row.setAlignment(Qt.AlignCenter)

        self.day_month_label = QLabel()
        self.day_month_label.setFont(QFont(FONT_FAMILY, 40))
        self.day_month_label.setStyleSheet(f"color: {DATE_COLOR}")
        self.day_month_label.setAlignment(Qt.AlignRight | Qt.AlignTop)

        self.day_label = QLabel()
        self.day_label.setFont(QFont(FONT_FAMILY, 195, QFont.Bold))
        self.day_label.setStyleSheet(f"color: {DATE_COLOR}")
        self.day_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        date_row.addWidget(self.day_month_label)
        date_row.addSpacing(30)
        date_row.addWidget(self.day_label)

        center_layout.addWidget(self.time_label)
        center_layout.addSpacing(10)
        center_layout.addLayout(date_row)

        # --- Bottom Row Layout ---
        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(20, 20, 20, 20)

        # Bottom-left (CPU + Memory)
        self.sys_label = QLabel()
        self.sys_label.setFont(QFont(FONT_FAMILY, 18))
        self.sys_label.setStyleSheet(f"color: {SYSTEM_COLOR}")
        self.sys_label.setAlignment(Qt.AlignLeft | Qt.AlignBottom)

        # Bottom-right (Battery + Uptime)
        self.battery_label = QLabel()
        self.battery_label.setFont(QFont(FONT_FAMILY, 18))
        self.battery_label.setStyleSheet(f"color: {SYSTEM_COLOR}")
        self.battery_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)

        bottom_layout.addWidget(self.sys_label)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.battery_label)

        # Final layout
        main_layout.addLayout(center_layout)
        main_layout.addStretch()
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

        # Update timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_content)
        self.timer.start(1000) # Adjust update timer here
        self.update_content()

    def update_content(self):
        now = datetime.now()
        self.time_label.setText(now.strftime("%H:%M"))
        self.day_label.setText(now.strftime("%d"))
        self.day_month_label.setText(now.strftime("%a %b"))

        # System stats
        cpu = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory().percent
        self.sys_label.setText(f"🖥️ Silicon Usage: {cpu:.1f}%    🧠 Capacitors Usage: {mem:.1f}%")  # "Silicon" For CPU. "Capacitor" For RAM

        # Battery info # For battery in Laptops.In Desktop Use "bat text" after else will be shown. {uptime is also a part of battery}
        battery = psutil.sensors_battery()
        uptime = timedelta(seconds=int(time.time() - psutil.boot_time()))
        if battery:
            status = "Got AC Juice" if battery.power_plugged else "Your Time Is Limited"
            bat_text = f"🔋 {battery.percent:.0f}% ({status})"
        else:
            bat_text = " Nice Desktop You Got Here "

        self.battery_label.setText(f"{bat_text}   ⏳  Unwinded Before: {str(uptime).split('.')[0]}") # Used to Show Uptime. Change "unwinded before" To your desired Words.

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    wb = Wallboard()
    sys.exit(app.exec_())

