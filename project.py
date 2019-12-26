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

        login = InputText(width // 2 - 70, height // 5 * 3 - 32, 140, 32)

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
        self.id_login = self.cur.execute("""SELECT id FROM logins
                                            WHERE login == ?""",
                                         (login_t,)).fetchall()
        print(self.id_login)
        if self.id_login != []:
            self.l, = self.id_login[0]

            self.have_login = HaveLogin(login_t)
        else:
            self.no_login = NoLogin(login_t)

    def update(self):
        width = max(200, self.text_surf.get_width() + 8)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.text_surf, (self.rect.x + 5, self.rect.y + 5))

        pygame.draw.rect(screen, pygame.Color("lightblue"), self.rect, 4)


class HaveLogin:
    def __init__(self, login):
        super().__init__()
        pygame.init()

        size = width, height = 600, 500
        screen = pygame.display.set_mode(size)

        titl = pygame.font.SysFont('arial', 36)
        self.text1 = titl.render("Добро ожаловать,", 1, pygame.Color("blue"))

        log = pygame.font.SysFont('colibri', 50)
        self.text2 = log.render(login, 1, pygame.Color('lightblue'))   # login.rjust((width - 435) % 8, " ")


        act_open = pygame.font.SysFont("arial", 25)
        self.text3 = act_open.render(f"Начать игру", 1, pygame.Color("lightblue"))

        act_chg = pygame.font.SysFont("arial", 25)
        self.text4 = act_chg.render("Выбрать персонажа", 1, pygame.Color("lightblue"))

        act_exit = pygame.font.SysFont("arial", 25)
        self.text5 = act_exit.render("Сменить пользователя", 1,
                                    pygame.Color("lightblue"))

        run = True

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    '''if 160 <= event.pos[0] <= 450 and 160 <= event.pos[1] <= 213:
                        # открытие окна с полем'''
                    if 160 <= event.pos[0] <= 450 and 160 <= event.pos[1] <= 283:
                        char = Character()
                    if 160 <= event.pos[0] <= 450 and 160 <= event.pos[1] <= 353:
                        run = False
                        # выход к стартовому окну
            screen.fill((30, 30, 30))
            for i in range(3):
                pygame.draw.rect(screen, pygame.Color("blue"),
                                 (160, 160 + i * 70, 290, 53), 3)

            screen.blit(self.text1, (100, 60))
            screen.blit(self.text2, (435, 65))
            screen.blit(self.text3, (230, 170))
            screen.blit(self.text4, (180, 240))
            screen.blit(self.text5, (175, 310))
            pygame.display.flip()


class Character:
    def __init__(self):
        super().__init__()
        pygame.init()

        size = width, height = 600, 500
        screen = pygame.display.set_mode(size)

        self.all_sprites = pygame.sprite.Group()

        snake = AnimatedSprite(self.load_image("snake_sm.png"), 4, 2, 50, 150, self.all_sprites)
        clock = pygame.time.Clock()

        run_spr = True

        while run_spr:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_spr = False
            screen.fill((0, 0, 0))
            self.all_sprites.draw(screen)  # говорим прорисовывать sprites
            self.all_sprites.update()
            pygame.display.flip()
            clock.tick(15)  # для того чтобы не тормозить программу в целом, можно создать счетчик в классе AnimatedSprite

    def load_image(self, name, color_key=None):
        fullname = os.path.join("data", name)
        image = pygame.image.load(fullname).convert()
        if color_key is not None:
            if color_key == -1:
                color_key = image.get_at((0, 0))
            image.set_colorkey(color_key)
        else:
            image = image.convert_alpha()
        return image


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, group):
        super().__init__(group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class NoLogin:
    def __init__(self, login):
        super().__init__()
        pygame.init()

        self.con = sqlite3.connect("one_little_worm.db")
        self.cur = self.con.cursor()

        '''self.log_app = self.cur.execute("INSERT INTO logins VALUES(login)").fetchall()
        self.con.commit()'''

        size = width, height = 600, 500
        screen = pygame.display.set_mode(size)

        titl = pygame.font.SysFont('arial', 36)
        self.text1 = titl.render("Новый игрок,", 1, pygame.Color("blue"))

        log = pygame.font.SysFont('colibri', 50)
        self.text2 = log.render(login, 1, pygame.Color('lightblue'))   # login.rjust((width - 435) % 8, " ")

        act_open = pygame.font.SysFont("arial", 25)
        self.text3 = act_open.render(f"Начать игру", 1, pygame.Color("lightblue"))

        act_chg = pygame.font.SysFont("arial", 25)
        self.text4 = act_chg.render("Выбрать персонажа", 1, pygame.Color("lightblue"))

        act_exit = pygame.font.SysFont("arial", 25)
        self.text5 = act_exit.render("Сменить пользователя", 1, pygame.Color("lightblue"))

        run = True

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    '''if 160 <= event.pos[0] <= 450 and 160 <= event.pos[1] <= 213:
                        # открытие окна с полем'''
                    if 160 <= event.pos[0] <= 450 and 160 <= event.pos[1] <= 283:
                        char = Character()
                    if 160 <= event.pos[0] <= 450 and 160 <= event.pos[1] <= 353:
                        run = False
                        # выход к стартовому окну
            screen.fill((30, 30, 30))
            for i in range(3):
                pygame.draw.rect(screen, pygame.Color("blue"),
                                 (160, 160 + i * 70, 290, 53), 3)
            screen.blit(self.text1, (100, 60))
            screen.blit(self.text2, (435, 65))
            screen.blit(self.text3, (230, 170))
            screen.blit(self.text4, (180, 240))
            screen.blit(self.text5, (175, 310))
            pygame.display.flip()




start = StartWindow()


# меню с настройками
# карта для перехода между режимами игры