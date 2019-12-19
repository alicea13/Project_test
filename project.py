<<<<<<< Updated upstream
=======
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

        self.setGeometry(500, 300, 700, 500)
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
            self.l, = self.id_login[0]

            self.have_login = HaveLogin("have", self.login.text())
            self.have_login.show()
        else:
            self.no_login = NoLogin(self.login.text())
            self.no_login.show()


class HaveLogin(QWidget):
    def __init__(self, hv_or_cr, log):
        super().__init__()

        self.log = log

        self.con = sqlite3.connect("one_little_worm.db")
        self.cur = self.con.cursor()

        self.setGeometry(600, 350, 500, 400)
        self.setWindowTitle("HaveLogin")

        self.lbl = QLabel(self)
        if hv_or_cr == "have":
            self.lbl.setText("Логин найден")
        elif hv_or_cr == "created":
            self.lbl.setText("Логин создан")
        self.lbl.setFont(QFont('Serif', 15, QFont.Bold))
        self.lbl.resize(self.lbl.sizeHint())
        self.lbl.move(158, 70)

        self.start_game = QPushButton(self)
        self.start_game.setText("Начать игру")
        self.start_game.setFont(QFont("Times", 10, QFont.AnyStyle))
        self.start_game.resize(190, 30)
        self.start_game.move(150, 160)
        self.start_game.clicked.connect(self.game_start)

        self.sh_rec = QPushButton(self)
        self.sh_rec.setText("Таблица рекордов")
        self.sh_rec.setFont(QFont("Times", 10, QFont.AnyStyle))
        self.sh_rec.resize(190, 30)
        self.sh_rec.move(150, 205)
        self.sh_rec.clicked.connect(self.record_tbl)

        self.del_acc = QPushButton(self)
        self.del_acc.setText("Удалить пользователя")
        self.del_acc.setFont(QFont("Times", 10, QFont.AnyStyle))
        self.del_acc.resize(190, 30)
        self.del_acc.move(150, 250)
        self.del_acc.clicked.connect(self.del_account)

    def del_account(self):
        print(self.log)

        #   удаляем логин пользователя из таблицв logins и Main
        self.del_the_acc_logins = self.cur.execute("""DELETE FROM logins WHERE 
                                                    login == ?""", (self.log,))
        self.del_the_acc_main = self.cur.execute("""DELETE FROM Main WHERE 
                                                    login == ?""", (self.log,))

        self.con.commit()
        self.con.close()
        self.close()

    def record_tbl(self):
        pass
        # нужно это или нет

    def game_start(self):
        pass
        #   как открыть в новом окне игру


class NoLogin(QWidget):
    def __init__(self, log):
        super().__init__()

        self.log = log
        print("here", self.log)

        self.con = sqlite3.connect("one_little_worm.db")
        self.cur = self.con.cursor()

        self.setGeometry(600, 350, 500, 400)
        self.setWindowTitle("NoLogin")

        self.titl = QLabel(self)
        self.titl.setText("Логин не найден")
        self.titl.setFont(QFont('Serif', 15, QFont.Bold))
        self.titl.resize(self.titl.sizeHint())
        self.titl.move(148, 70)

        self.cr_log = QPushButton(self)
        self.cr_log.setText("Создать логин")
        self.cr_log.setFont(QFont("Times", 10, QFont.AnyStyle))
        self.cr_log.resize(150, 30)
        self.cr_log.move(175, 160)
        self.cr_log.clicked.connect(self.create_log)

        self.exit = QPushButton(self)
        self.exit.setText("Выйти")
        self.exit.setFont(QFont("Times", 10, QFont.AnyStyle))
        self.exit.resize(150, 30)
        self.exit.move(175, 205)

    def create_log(self):
        # добавляем log в таблицы Main и logins

        self.ap_log_logins = self.cur.execute("""INSERT INTO logins(login) 
                                            VALUES(?)""", (self.log,))
        self.ap_log_main = self.cur.execute("""INSERT INTO Main(login, 
                                            record, place) VALUES(?, 0, 0)""",
                                            (self.log,))
        self.con.commit()
        print('ok')
        self.close()

        self.open_log = HaveLogin("created", self.log)
        self.open_log.show()


# class Game(QWidget):

if __name__ == '__main__':
    app = QApplication(sys.argv)
    paint = StartWindow()
    paint.show()
    sys.exit(app.exec_())
>>>>>>> Stashed changes
