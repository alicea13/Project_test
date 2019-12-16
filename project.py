from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QLineEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import pygame, os, random
import sys
import sqlite3


class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.con = sqlite3.connect("one_little_worm.db")
        self.cur = self.con.cursor()

        self.setGeometry(500, 300, 700, 600)
        self.setWindowTitle("Welcome :)")

        self.lbl1 = QLabel(self)
        self.lbl1.setText("Добро пожаловать в")
        self.lbl1.setFont(QFont('Serif', 17, QFont.Light))
        self.lbl1.resize(self.lbl1.sizeHint())
        self.lbl1.move(40, 60)

        self.name_game = QLabel(self)
        self.name_game.setText("One little worm !")
        self.name_game.setFont(QFont('Serif', 20, QFont.Bold))
        self.name_game.resize(self.name_game.sizeHint())
        self.name_game.move(325, 100)

        self.to_start = QLabel(self)
        self.to_start.setText("Для начала игры введите логин")
        self.to_start.setFont(QFont('Serif', 12, QFont.AllLowercase))
        self.to_start.resize(self.to_start.sizeHint())
        self.to_start.move(45, 230)

        self.login = QLineEdit(self)
        self.login.resize(220, 30)
        self.login.move(380, 227)

        self.to_check = QLabel(self)
        self.to_check.setText("Для проверки логина нажмите")
        self.to_check.setFont(QFont("Serif", 14))
        self.to_check.resize(self.to_check.sizeHint())
        self.to_check.move(65, 300)

        self.ctrl_alt = QLabel(self)
        self.ctrl_alt.setText("Ctrl + Alt")
        self.ctrl_alt.setFont(QFont('Serif', 10, QFont.Bold))
        self.ctrl_alt.move(425, 300)

        self.or_push = QLabel(self)
        self.or_push.setText("или нажмите кнопку ")
        self.or_push.setFont(QFont("Serif", 14))
        self.or_push.resize(self.or_push.sizeHint())
        self.or_push.move(120, 350)

        self.btn_check = QPushButton(self)
        self.btn_check.setText("Проверить")
        self.btn_check.setFont(QFont('Serif', 10, QFont.Bold))
        self.btn_check.resize(self.btn_check.sizeHint())
        self.btn_check.move(410, 350)

        self.btn_check.clicked.connect(self.check_login)

    def keyPressEvent(self, event):
        if int(event.modifiers()) == (Qt.AltModifier + Qt.ControlModifier):
            if self.login != "":
                self.open()

    def check_login(self):
        if self.login != "":
            self.open()

    def open(self):
        self.id_login = self.cur.execute("""SELECT id FROM logins 
                            WHERE login == ?""", (self.login.text(),)).fetchall()

        if self.id_login != []:
            self.l, = self.log_id[0]

            self.have_login = HaveLogin(self.login.text())
            self.have_login.show()
        else:
            self.no_login = NoLogin(self.login.text())
            self.no_login.show()
            self.close()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    paint = StartWindow()
    paint.show()
    sys.exit(app.exec_())
