import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLabel, QScrollArea, QVBoxLayout, QButtonGroup
from PyQt5.QtCore import *
import calendar
from calendar_rus import rus_calend, rus_day_abbr
import datetime

con = sqlite3.connect("schulglocke.db")
cur = con.cursor()


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.now = datetime.datetime.now()
        print(self.now)
        self.year = self.now.year
        self.month = self.now.month
        self.days = []
        self.table = [[0 for _ in range(7)] for _ in range(6)]

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Управление звонками')

        self.calendar_table = QGridLayout(self)

        self.prew_button = QPushButton("<", self)
        self.prew_button.setFixedSize(75, 45)
        self.prew_button.clicked.connect(self.prew)

        self.next_button = QPushButton(">", self)
        self.next_button.setFixedSize(75, 45)
        self.next_button.clicked.connect(self.next)

        self.calendar_label = QLabel(self)
        self.calendar_label.setAlignment(Qt.AlignCenter)

        self.schedule_label = QLabel("Расписание", self)
        self.schedule_label.setAlignment(Qt.AlignCenter)

        self.create_button = QPushButton("Создать", self)
        self.create_button.setFixedSize(100, 45)

        self.delete_button = QPushButton("удалить", self)
        self.delete_button.setFixedSize(100, 45)

        self.schedule = QScrollArea()  # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()  # Widget that contains the collection of Vertical Box
        self.vbox = QVBoxLayout()  # The Vertical Box that contains the Horizontal Boxes of  labels and buttons




        self.calendar_table.addWidget(self.prew_button, 0, 0)
        self.calendar_table.addWidget(self.calendar_label, 0, 1, 1, 5)
        self.calendar_table.addWidget(self.next_button, 0, 6)
        self.calendar_table.addWidget(self.schedule_label, 0, 7, 1, 2)
        self.calendar_table.addWidget(self.create_button, 7, 7)
        self.calendar_table.addWidget(self.delete_button, 7, 8)
        self.calendar_table.addWidget(self.schedule, 1, 7, 6, 2)

        self.fill_schedule()

        self.widget.setLayout(self.vbox)

        self.schedule.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.schedule.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.schedule.setWidgetResizable(True)
        self.schedule.setWidget(self.widget)

        for n in range(7):
            self.calendar_table.addWidget(QLabel(rus_day_abbr[n], self), 1, n)

        for row in range(6):
            for col in range(7):
                self.butt = QPushButton(self)
                self.butt.setFixedSize(75, 45)
                self.butt.clicked.connect(self.butt_press)
                self.calendar_table.addWidget(self.butt, row + 2, col)
                self.days.append(self.butt)

        self.fill()


    def fill(self):
        self.table = [[0 for _ in range(7)] for _ in range(6)]
        self.calendar_label.setText(rus_calend[self.month] + ', ' + str(self.year))
        month_days = calendar.monthrange(self.year, self.month)[1]
        if self.month == 1:
            prew_month_days = calendar.monthrange(self.year - 1, 12)[1]
            prew_year = self.year - 1
            prew_mounth = 12
        else:
            prew_month_days = calendar.monthrange(self.year, self.month - 1)[1]
            prew_year = self.year
            prew_mounth = self.month - 1
        if self.month == 12:
            next_year = self.year + 1
            next_mounth = 1
        else:
            next_year = self.year
            next_mounth = self.month + 1

        week_day = calendar.monthrange(self.year, self.month)[0]
        for n in range(week_day):
            self.days[week_day - n - 1].setText(str(prew_month_days - n))
            self.days[week_day - n - 1].setStyleSheet('background: rgb(243, 243, 243);')
            self.table[0][week_day - n - 1] = (week_day - n, prew_mounth, prew_year)

        for n in range(month_days):
            self.days[n + week_day].setText(str(n + 1))
            if self.year == self.now.year and self.month == self.now.month and n + 1 == self.now.day:
                self.days[n + week_day].setStyleSheet(
                    'border-color: rgb(0, 128, 0); background: rgb(211, 211, 211); border-width: 5px; border-style: outset;')

            else:
                self.days[n + week_day].setStyleSheet('background: rgb(211, 211, 211);')
            self.table[(n + week_day) // 7][(n + week_day) % 7] = (n + 1, self.month, self.year)

        for n in range(6 * 7 - month_days - week_day):
            self.days[week_day + month_days + n].setText(str(n + 1))
            self.days[week_day + month_days + n].setStyleSheet('background: rgb(243, 243, 243);')
            self.table[(month_days + week_day + n) // 7][(month_days + week_day + n) % 7] = (
                n + 1, next_mounth, next_year)
        for i in self.table:
            print(i)

    def fill_schedule(self):
        schedule_info = cur.execute("SELECT ID, NAME, COLOR FROM schedule")
        for i in schedule_info:
            butt = QPushButton(i[1], self)
            butt.setStyleSheet(f"background: rgb({i[2]});")
            self.vbox.addWidget(butt)

    def prew(self):
        self.month -= 1
        if self.month == 0:
            self.month = 12
            self.year -= 1
        self.fill()

    def next(self):
        self.month += 1
        if self.month == 13:
            self.month = 1
            self.year += 1
        self.fill()

    def butt_press(self):
        cord = self.calendar_table.getItemPosition(self.calendar_table.indexOf(self.sender()))
        print(self.table[cord[0] - 2][cord[1]])
        date = self.table[cord[0] - 2][cord[1]]
        if self.year == date[2] and self.month == date[1] and date[0] == self.now.day:
            self.sender().setStyleSheet(
                'border-color: rgb(0, 128, 0); background: rgb(128, 0, 0); border-width: 5px; border-style: outset;')
        else:
            self.sender().setStyleSheet('background: rgb(128, 0, 0);')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
