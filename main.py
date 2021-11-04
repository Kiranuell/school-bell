import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLabel, QScrollArea
from PyQt5.QtCore import *
import calendar
from calendar_rus import rus_calend, rus_day_abbr
import datetime


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.now = datetime.datetime.now()
        print(self.now)
        self.year = self.now.year
        self.month = self.now.month
        self.days = []
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
        self.scroll_zone = QScrollArea(self)
        self.create_button = QPushButton("Создать", self)
        self.create_button.setFixedSize(100, 45)
        self.delete_button = QPushButton("удалить", self)
        self.delete_button.setFixedSize(100, 45)

        self.calendar_table.addWidget(self.prew_button, 0, 0)
        self.calendar_table.addWidget(self.calendar_label, 0, 1, 1, 5)
        self.calendar_table.addWidget(self.next_button, 0, 6)
        self.calendar_table.addWidget(self.schedule_label, 0, 7, 1, 2)
        self.calendar_table.addWidget(self.scroll_zone, 1, 7, 6, 2)
        self.calendar_table.addWidget(self.create_button, 7, 7)
        self.calendar_table.addWidget(self.delete_button, 7, 8)



        for n in range(7):
            self.calendar_table.addWidget(QLabel(rus_day_abbr[n], self), 1, n)

        for row in range(6):
            for col in range(7):
                self.butt = QPushButton(self)
                self.butt.setFixedSize(75, 45)
                # self.butt.clicked.connect(self.butt_press)
                self.calendar_table.addWidget(self.butt, row + 2, col)
                self.days.append(self.butt)

        self.fill()

    def fill(self):
        self.calendar_label.setText(rus_calend[self.month] + ', ' + str(self.year))
        month_days = calendar.monthrange(self.year, self.month)[1]
        if self.month == 1:
            prew_month_days = calendar.monthrange(self.year - 1, 12)[1]
        else:
            prew_month_days = calendar.monthrange(self.year, self.month - 1)[1]
        week_day = calendar.monthrange(self.year, self.month)[0]
        for n in range(month_days):
            self.days[n + week_day].setText(str(n + 1))
            # self.days[n + week_day]['fg'] = 'black'
            if self.year == self.now.year and self.month == self.now.month and n + 1 == self.now.day:
                self.days[n + week_day].setStyleSheet('background: rgb(0, 128, 0);')
            else:
                self.days[n + week_day].setStyleSheet('background: rgb(211, 211, 211);')
        for n in range(week_day):
            self.days[week_day - n - 1].setText(str(prew_month_days - n))
            self.days[week_day - n - 1].setStyleSheet('background: rgb(243, 243, 243);')
        #     self.days[week_day - n - 1]['fg'] = 'gray'
        #     self.days[week_day - n - 1]['background'] = '#f3f3f3'
        for n in range(6 * 7 - month_days - week_day):
            self.days[week_day + month_days + n].setText(str(n + 1))
            self.days[week_day + month_days + n].setStyleSheet('background: rgb(243, 243, 243);')
        #     self.days[week_day + month_days + n]['fg'] = 'gray'
        #     self.days[week_day + month_days + n]['background'] = '#f3f3f3'

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

    # def butt_press(self):
    #     print(self.sender().text())
    #     print(self.senderSignalIndex())
    #     self.sender().setStyleSheet('background: rgb(0, 128, 0);')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
