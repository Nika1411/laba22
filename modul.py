#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Вариант6
# Использовать словарь, содержащий следующие ключи: название пункта назначения; номер
# поезда; время отправления. Написать программу, выполняющую следующие действия:
# ввод с клавиатуры данных в список, состоящий из словарей заданной структуры; записи должны
# быть размещены в алфавитном порядке по названиям пунктов назначения; вывод на экран
# информации о поездах, отправляющихся после введенного с клавиатуры времени; если
# таких поездов нет, выдать на дисплей соответствующее сообщение.


from dataclasses import dataclass, field
from typing import List
import sqlite3


#   Выполнить индивидуальное задание 2 лабораторной работы 13, добавив возможность работы с
#   исключениями и логгирование.

class IllegalTimeError(Exception):

    def __init__(self, time, message="Illegal time (ЧЧ:ММ)"):
        self.time = time
        self.message = message
        super(IllegalTimeError, self).__init__(message)

    def __str__(self):
        return f"{self.time} -> {self.message}"


class UnknownCommandError(Exception):

    def __init__(self, command, message="Unknown command"):
        self.command = command
        self.message = message
        super(UnknownCommandError, self).__init__(message)

    def __str__(self):
        return f"{self.command} -> {self.message}"


@dataclass(frozen=True)
class train:
    name: str
    num: int
    time: str


@dataclass
class Staff:
    trains: List[train] = field(default_factory=lambda: [])

    db = sqlite3.connect('ind.sqlite')
    cur = db.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS trains (
            rowid INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            num INTEGER,
            time TEXT
        )''')

    db.commit()

    def add(self, name, num, time):

        if ":" not in time:
            raise IllegalTimeError(time)

        self.trains.append(
            train(
                name=name,
                num=num,
                time=time
            )
        )

        self.trains.sort(key=lambda train: train.name)

    def __str__(self):
        # Заголовок таблицы.
        table = []
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 17
        )
        table.append(line)
        table.append(
            '| {:^4} | {:^30} | {:^20} | {:^17} |'.format(
                "№",
                "Пункт назначения",
                "Номер поезда",
                "Время отправления"
            )
        )
        table.append(line)

        # Вывести данные о всех сотрудниках.
        for idx, train in enumerate(self.trains, 1):
            table.append(
                '| {:>4} | {:<30} | {:<20} | {:>17} |'.format(
                    idx,
                    train.name,
                    train.num,
                    train.time
                )
            )

        table.append(line)

        return '\n'.join(table)

    def select(self, numbers):
        result = []

        for train in self.trains:
            if numbers == train.time:
                result.append(train)

        return result

    def load(self):
        self.trains = []
        data = self.cur.execute("SELECT * FROM trains")

        for i in data:
            name = i[1]
            num = i[2]
            time = i[3]
            self.trains.append(
                train(
                    name=name,
                    num=num,
                    time=time
                )
            )

    def save(self):
        self.cur.execute('''DELETE FROM trains''')
        for train in self.trains:
            name = train.name
            num = train.num
            time = train.time

            self.cur.execute('''INSERT INTO trains (
                    name, num, time) VALUES (?, ?, ?)
                    ''', (name, num, time))
            self.db.commit()

    def kill(self) -> None:
        self.cur.execute('''DROP TABLE trains''')
        self.db.commit()
