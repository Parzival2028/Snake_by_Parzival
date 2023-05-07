from tkinter import Tk, Canvas
import random

# ширина экрана
WIDTH = 800
# высота экрана
HEIGHT = 600
# Размер сегмента змейки
SEG_SIZE = 20
# Переменная отвечающая за состояние игры
IN_GAME = True

# Вспомогательные функции
def create_block():
    # Создаём яблоки
    global BLOCK
    posx = SEG_SIZE * random.randint(1, (WIDTH-SEG_SIZE) / SEG_SIZE)
    posy = SEG_SIZE * random.randint(1, (HEIGHT-SEG_SIZE) / SEG_SIZE)
    BLOCK = c.create_oval(posx, posy,
                          posx+SEG_SIZE, posy+SEG_SIZE,
                          fill="red")


def main():
    global IN_GAME
    if IN_GAME:
    # Двигаем змейку
        s.move()
        # Определяем координаты головы
        head_coords = c.coords(s.segments[-1].instance)
        x1, y1, x2, y2 = head_coords
        # Столкновение с границами экрана
        if x2 > WIDTH or x1 < 0 or y1 < 0 or y2 > HEIGHT:
            IN_GAME = False
        # Поедание яблок
        elif head_coords == c.coords(BLOCK):
            s.add_segment()
            c.delete(BLOCK)
            create_block()
        # Самопоедание
        else:
            for index in range(len(s.segments)-1):
                if head_coords == c.coords(s.segments[index].instance):
                    IN_GAME = False
        root.after(100, main)
    else:
        set_state(restart_text, 'normal')
        set_state(game_over_text, 'normal')


class Segment(object):
    def __init__(self, x, y):
        self.instance = c.create_rectangle(x, y,
                                           x+SEG_SIZE, y+SEG_SIZE,
                                           fill="white")


class Snake(object):
    def __init__(self, segments):
        self.segments = segments
         
        # список доступных направлений движения змейки
        self.mapping = {"Down": (0, 1), "Up": (0, -1),
                                "Left": (-1, 0), "Right": (1, 0) }
        # изначально змейка двигается вправо
        self.vector = self.mapping["Right"]

    def move(self):
        # перебираем все сегменты кроме первого
        for index in range(len(self.segments)-1):
            segment = self.segments[index].instance
            x1, y1, x2, y2 = c.coords(self.segments[index+1].instance)
            # задаем каждому сегменту позицию сегмента стоящего после него
            c.coords(segment, x1, y1, x2, y2)
        # получаем координаты сегмента перед "головой"
        x1, y1, x2, y2 = c.coords(self.segments[-2].instance)
        # помещаем "голову" в направлении указанном в векторе движения
        c.coords(self.segments[-1].instance,
                 x1+self.vector[0]*SEG_SIZE, y1+self.vector[1]*SEG_SIZE,
                 x2+self.vector[0]*SEG_SIZE, y2+self.vector[1]*SEG_SIZE)

    def add_segment(self):
        # Добавляем сегменты
        # определяем последний сегмент
        last_seg = c.coords(self.segments[0].instance)
        # определяем координаты куда поставить следующий сегмент
        x = last_seg[2] - SEG_SIZE
        y = last_seg[3] - SEG_SIZE
        # добавляем змейке еще один сегмент в заданных координатах
        self.segments.insert(0, Segment(x, y))

    def change_direction(self, event):
        # event передаст нам символ нажатой клавиши
        # и если эта клавиша в доступных направлениях 
        # изменяем направление
        if event.keysym in self.mapping:
            self.vector = self.mapping[event.keysym]

    def reset_snake(self):
        for segment in self.segments:
            c.delete(segment.instance)


def set_state(item, state):
    c.itemconfigure(item, state=state)


def clicked(event):
    global IN_GAME
    s.reset_snake()
    IN_GAME = True
    c.delete(BLOCK)
    c.itemconfigure(restart_text, state='hidden')
    c.itemconfigure(game_over_text, state='hidden')
    start_game()


def start_game():
    global s
    create_block()
    s = create_snake()
    # Реакция на нажатую кнопку
    c.bind("<KeyPress>", s.change_direction)
    main()


def create_snake():
    # Создаем змеку из 3 сегментов вначале
    segments = [Segment(SEG_SIZE, SEG_SIZE),
                Segment(SEG_SIZE*2, SEG_SIZE),
                Segment(SEG_SIZE*3, SEG_SIZE)]
    return Snake(segments)


# Настройки окна
root = Tk()
root.title("Snake")


c = Canvas(root, width=WIDTH, height=HEIGHT, bg="#003300")
c.grid()
c.focus_set()
#Конец игры
game_over_text = c.create_text(WIDTH/2, HEIGHT/2, text="Конец игры!",
                               font='Arial 20', fill='red',
                               state='hidden')
#Кнопка для перезапуска
restart_text = c.create_text(WIDTH/2, HEIGHT-HEIGHT/3,
                             font='Arial 30',
                             fill='white',
                             text="Заново",
                             state='hidden')
c.tag_bind(restart_text, "<Button-1>", clicked)
start_game()
root.mainloop()
