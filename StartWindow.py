from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QLineEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import pygame, os, random
import sys
import sqlite3


class StartWindow:
    def __init__(self):
        super().__init__()
        pygame.init()

        self.con = sqlite3.connect("one_little_worm.db")
        self.cur = self.con.cursor()

        size = width, height = 600, 500
        screen = pygame.display.set_mode(size)

        titl = pygame.font.SysFont('gadugi', 36)
        self.text1 = titl.render("One Little Warm", 1, pygame.Color("blue"))

        ask_input = pygame.font.SysFont('arial', 25)
        self.text2 = ask_input.render("Введите логин:", 1, pygame.Color("lightblue"))

        login = InputText(235, 230, 140, 32)

        run_st = True

        while run_st:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_st = False
                '''if event.type == pygame.MOUSEBUTTONDOWN:
                    self.get_click(event.pos)'''
                login.events(event)
            screen.fill((30, 30, 30))
            login.draw(screen)
            screen.blit(self.text1, (180, 60))
            screen.blit(self.text2, (220, 170))
            pygame.display.flip()

    def get_click(self, pos):
        print("here")


class InputText:
    def __init__(self, x, y, width, height, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.login_t = text
        self.text_surf = pygame.font.Font(None, 32).render(text, True, pygame.Color('lightblue'))
        self.run_text = False

        self.con = sqlite3.connect("one_little_worm.db")
        self.cur = self.con.cursor()

    def events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.run_text = True
            else:
                self.run_text = False

        if event.type == pygame.KEYDOWN and self.run_text:
            if event.key == pygame.K_RETURN:
                self.open(self.login_t)
                self.login_t = ""
            elif event.key == pygame.K_BACKSPACE:
                self.login_t = self.login_t[:-1]
            else:
                self.login_t += event.unicode
            self.text_surf = pygame.font.Font(None, 32).render(self.login_t, True, pygame.Color('lightblue'))

    def open(self, login_t):
        self.id_login = self.cur.execute("""SELECT id FROM Main
                                            WHERE login == ?""", (login_t,)).fetchall()
        print(self.id_login)
        if self.id_login != []:
            self.l, = self.log_id[0] ###

            self.have_login = HaveLogin(self.login.text())
            self.have_login.show()
        else:
            self.no_login = NoLogin(self.login.text())
            self.no_login.show()
            #self.close()

    def update(self):
        width = max(200, self.text_surf.get_width() + 8)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.text_surf, (self.rect.x + 5, self.rect.y + 5))

        pygame.draw.rect(screen, pygame.Color("lightblue"), self.rect, 4)



start = StartWindow()
