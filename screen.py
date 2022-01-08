#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import random
import math

SCREEN_DIM = (800, 600)


class Vec2d:

    def __init__(self, tupl):
        self.x = tupl[0]
        self.y = tupl[1]

    def __add__(self, other):
        """возвращает сумму двух векторов"""
        # print('add call')
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other):
        """"возвращает разность двух векторов"""
        print('sub call')
        return self.x - other.x, self.y - other.y

    def __mul__(self, other):
        """возвращает произведение вектора на число"""
        # print('mul call')
        if isinstance(other, (int, float)):
            return int(self.x * other), int(self.y * other)
        if isinstance(other, tuple):
            self.x *= other[0]
            self.y *= other[1]
            return self

    def len(self):
        """возвращает длину вектора"""
        return math.sqrt(self.x * self.x + self.y * self.y)

    def int_pair(self, other):
        """возвращает пару координат, определяющих вектор (координаты точки конца вектора),
        координаты начальной точки вектора совпадают с началом системы координат (0, 0)"""
        return int(other.x - self.x), int(other.y - self.y)


class Polyline:
    """ класс замкнутых ломаных c методами отвечающими за добавление в ломаную точки (Vec2d)
    c её скоростью, пересчёт координат точек (set_points) и отрисовку ломаной (draw_points).
    Арифметические действия с векторами должны быть реализованы
    с помощью операторов, а не через вызовы соответствующих методов."""

    def __init__(self):
        self.points = []
        self.speeds = []

    def add_base_point(self, new_vect, new_vect_speed):
        """ метод отвечающими за добавление в ломаную точки (Vec2d) c её скоростью"""
        self.points.append(new_vect)
        self.speeds.append(new_vect_speed)

    def set_points(self):
        """ метод отвечающий за пересчёт координат точек"""
        """функция перерасчета координат опорных точек"""
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]
            if self.points[p].x > SCREEN_DIM[0] or self.points[p].x < 0:
                self.speeds[p] = self.speeds[p] * (-1, 1)
            if self.points[p].y > SCREEN_DIM[1] or self.points[p].y < 0:
                self.speeds[p] = self.speeds[p] * (1, -1)

    def draw_points(self, style="points", width=3, color=(255, 255, 255)):
        """ метод отвечающими за отрисовку ломаной (draw_points)"""
        """функция отрисовки точек на экране"""
        if style == "line":
            for p_n in range(-1, len(self.points) - 1):
                pygame.draw.line(gameDisplay, color,
                                 (int(self.points[p_n].x), int(self.points[p_n].y)),
                                 (int(self.points[p_n + 1].x), int(self.points[p_n + 1].y)), width)

        elif style == "points":
            for p in self.points:
                pygame.draw.circle(gameDisplay, color,
                                   (int(p.x), int(p.y)), width)



class Knot(Polyline):
    """  в котором добавление и пересчёт координат инициируют
    вызов функции get_knot для расчёта точек кривой по добавляемым «опорным» точкам"""

    def get_knot(self):
        """ функции get_knot для расчёта точек кривой по добавляемым «опорным» точкам"""
        pass



# =======================================================================================
# Функции для работы с векторами
# =======================================================================================

def sub(x, y):
    """"возвращает разность двух векторов"""
    return x[0] - y[0], x[1] - y[1]


def add(x, y):
    """возвращает сумму двух векторов"""
    return x[0] + y[0], x[1] + y[1]


def length(x):
    """возвращает длину вектора"""
    return math.sqrt(x[0] * x[0] + x[1] * x[1])


def mul(v, k):
    """возвращает произведение вектора на число"""
    return v[0] * k, v[1] * k


def vec(x, y):
    """возвращает пару координат, определяющих вектор (координаты точки конца вектора),
    координаты начальной точки вектора совпадают с началом системы координат (0, 0)"""
    return sub(y, x)


# =======================================================================================
# Функции отрисовки
# =======================================================================================
def draw_points(points, style="points", width=3, color=(255, 255, 255)):
    """функция отрисовки точек на экране"""
    if style == "line":
        for p_n in range(-1, len(points) - 1):
            pygame.draw.line(gameDisplay, color,
                             (int(points[p_n][0]), int(points[p_n][1])),
                             (int(points[p_n + 1][0]), int(points[p_n + 1][1])), width)

    elif style == "points":
        for p in points:
            pygame.draw.circle(gameDisplay, color,
                               (int(p.x), int(p.y)), width)


def draw_help():
    """функция отрисовки экрана справки программы"""
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append(["", ""])
    data.append([str(steps), "Current points"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


# =======================================================================================
# Функции, отвечающие за расчет сглаживания ломаной
# =======================================================================================
def get_point(points, alpha, deg=None):
    if deg is None:
        deg = len(points) - 1
    if deg == 0:
        return points[0]
    # return add(mul(points[deg], alpha), mul(get_point(points, alpha, deg - 1), 1 - alpha))
    return (points[deg] * alpha) + (get_point(points, alpha, deg - 1) * (1 - alpha))


def get_points(base_points, count):
    alpha = 1 / count
    res = []
    for i in range(count):
        res.append(get_point(base_points, i * alpha))
    return res


def get_knot(points, count):
    if len(points) < 3:
        return []
    res = []
    for i in range(-2, len(points) - 2):
        ptn = []
        # print(points[i] * 2)
        # ptn.append(mul(add(points[i], points[i + 1]), 0.5))
        ptn.append((points[i] + points[i + 1]) * 0.5)
        ptn.append(points[i + 1])
        # ptn.append(mul(add(points[i + 1], points[i + 2]), 0.5))
        ptn.append((points[i + 1] + points[i + 2]) * 0.5)

        res.extend(get_points(ptn, count))
    return res


def set_points(points, speeds):
    """функция перерасчета координат опорных точек"""
    for p in range(len(points)):
        points[p] = add(points[p], speeds[p])
        if points[p][0] > SCREEN_DIM[0] or points[p][0] < 0:
            speeds[p] = (- speeds[p][0], speeds[p][1])
        if points[p][1] > SCREEN_DIM[1] or points[p][1] < 0:
            speeds[p] = (speeds[p][0], -speeds[p][1])


# =======================================================================================
# Основная программа
# =======================================================================================
if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    steps = 35
    working = True
    polyline = Polyline()
    # points = []
    # speeds = []
    show_help = False
    pause = True

    hue = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    points = []
                    speeds = []
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                point_o = Vec2d(event.pos)
                speed_o = Vec2d((random.random() * 2, random.random() * 2))
                polyline.add_base_point(point_o, speed_o)
                # polyline.speeds.append(speed_o)

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        polyline.draw_points()
        # draw_points(get_knot(points, steps), "line", 3, color)
        polyline.draw_points(style="line")
        if not pause:
            polyline.set_points()
        if show_help:
            draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
