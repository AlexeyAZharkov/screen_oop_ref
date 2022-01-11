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
        sum = Vec2d((self.x + other.x, self.y + other.y))
        return sum

    def __sub__(self, other):
        """"возвращает разность двух векторов"""
        sub = Vec2d((self.x - other.x, self.y - other.y))
        return sub

    def __mul__(self, other):
        """возвращает произведение вектора на число"""
        if isinstance(other, Vec2d):
            mul = Vec2d((int(self.x * other.x), int(self.y * other.y)))
            return mul
        if isinstance(other, (int, float)):
            mul = Vec2d((int(self.x * other), int(self.y * other)))
            return mul
        if isinstance(other, tuple):
            mul = Vec2d((self.x * other[0], self.y * other[1]))
            return mul

    def len(self):
        """возвращает длину вектора"""
        return math.sqrt(self.x * self.x + self.y * self.y)

    def int_pair(self):
        """возвращает кортеж из двух целых чисел (текущие координаты вектора)."""
        return self.x, self.y


class Polyline:
    """ класс замкнутых ломаных c методами отвечающими за добавление в ломаную точки (Vec2d)
    c её скоростью, пересчёт координат точек (set_points) и отрисовку ломаной (draw_points).
    Арифметические действия с векторами должны быть реализованы
    с помощью операторов, а не через вызовы соответствующих методов."""

    def __init__(self):
        self.points = []
        self.speeds = []
        self.points_smooth = []

    def add_base_point(self, new_vect, new_vect_speed):
        """ метод отвечающими за добавление в ломаную точки (Vec2d) c её скоростью"""
        self.points.append(new_vect)
        self.speeds.append(new_vect_speed)

    def set_points(self):
        """ метод отвечающий за пересчёт координат точек"""
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]
            if self.points[p].x > SCREEN_DIM[0] or self.points[p].x < 0:
                self.speeds[p] = self.speeds[p] * (-1, 1)
            if self.points[p].y > SCREEN_DIM[1] or self.points[p].y < 0:
                self.speeds[p] = self.speeds[p] * (1, -1)

    def draw_points(self, style="points", width=3, color=(255, 255, 255)):
        """ метод отвечающими за отрисовку ломаной (draw_points)"""
        if style == "line":
            for p_n in range(-1, len(self.points_smooth) - 1):
                pygame.draw.line(gameDisplay, color,
                                 (int(self.points_smooth[p_n].x), int(self.points_smooth[p_n].y)),
                                 (int(self.points_smooth[p_n + 1].x), int(self.points_smooth[p_n + 1].y)), width)

        elif style == "points":
            for p in self.points:
                pygame.draw.circle(gameDisplay, color,
                                   (int(p.x), int(p.y)), width)


class Knot(Polyline):
    """ класс, в котором добавление и пересчёт координат инициируют
    вызов функции get_knot для расчёта точек кривой по добавляемым «опорным» точкам"""

    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        point = (points[deg] * alpha) + (self.get_point(points, alpha, deg - 1) * (1 - alpha))
        return point

    def get_points(self, base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def get_knot(self, count, color):
        """ функции get_knot для расчёта точек кривой по добавляемым «опорным» точкам"""
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append((self.points[i] + self.points[i + 1]) * 0.5)
            ptn.append(self.points[i + 1])
            ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)
            res.extend(self.get_points(ptn, count))
        self.points_smooth = res
        self.draw_points(style="line", color=color)


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
# Основная программа
# =======================================================================================
if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    steps = 35
    working = True
    knot = Knot()
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
                knot.add_base_point(point_o, speed_o)

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        knot.draw_points()
        knot.get_knot(steps, color)
        if not pause:
            knot.set_points()
        if show_help:
            draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
