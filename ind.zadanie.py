#!/usr/bin/env python3
# -*- config: utf-8 -*-


from tkinter import *
from tkinter import messagebox as mb
import modul
import sqlite3


def add_window():
    def add():
        time = en3.get()
        name = en1.get()
        num = en2.get()

        staff.add(name, num, time)

    add_w = Toplevel()
    add_w.title('Добавить')
    add_w.resizable(False, False)
    add_w.geometry('225x100')
    en1 = Entry(add_w)
    en2 = Entry(add_w)
    en3 = Entry(add_w)
    lb1 = Label(add_w, text="Название пункта назначения")
    lb2 = Label(add_w, text="Номер поезда")
    lb3 = Label(add_w, text="Время отправления")
    bt1 = Button(add_w, text="Добавить", command=add)

    lb1.grid(row=0, column=0)
    lb2.grid(row=1, column=0)
    lb3.grid(row=2, column=0)
    en1.grid(row=0, column=1)
    en2.grid(row=1, column=1)
    en3.grid(row=2, column=1)
    bt1.grid(row=3, column=0, columnspan=2)


def update_window():
    def upd():
        row = en1.get()
        value = str(en2.get())
        col = ''
        if var.get() == 0:
            col = 'name'
        elif var.get() == 1:
            col = 'num'
        elif var.get() == 2:
            col = 'time'
        print(type(col))
        cur.execute(f'''UPDATE trains SET {col} = {value} WHERE rowid = {row}''')
        db.commit()

    upd_w = Toplevel()
    upd_w.title('Обновление')
    upd_w.resizable(False, False)
    upd_w.geometry('650x100')
    var = IntVar()
    var.set(0)
    rb1 = Radiobutton(upd_w, text="Пункт назначения", indicatoron=0, variable=var, value=0)
    rb2 = Radiobutton(upd_w, text="Номер поезда", indicatoron=0, variable=var, value=1)
    rb3 = Radiobutton(upd_w, text="Время отправления",  variable=var, indicatoron=0, value=2)
    lb1 = Label(upd_w, text='Выберите столбец таблицы для обновления:')
    lb2 = Label(upd_w, text='Введите номер строки, в которой будут обновлены данные:')
    lb3 = Label(upd_w, text='Введите новые данные:')
    en1 = Entry(upd_w, width=40)
    en2 = Entry(upd_w, width=40)
    bt = Button(upd_w, text='Обновить', command=upd)
    rb1.grid(row=0, column=1)
    rb2.grid(row=0, column=2)
    rb3.grid(row=0, column=3)
    lb1.grid(row=0, column=0, sticky=E)
    lb2.grid(row=2, column=0, sticky=E)
    lb3.grid(row=4, column=0, sticky=E)
    en1.grid(row=2, column=1, columnspan=5, sticky=W+E)
    en2.grid(row=4, column=1, columnspan=5, sticky=W+E)
    bt.grid(row=5, column=0, columnspan=4, sticky=E)


def del_window():
    def row_del():
        row = int(en1.get())
        print(row)
        cur.execute(f'''DELETE FROM trains WHERE rowid = {row}''')
        db.commit()

    del_w = Toplevel()
    del_w.title('Удаление')
    lb1 = Label(del_w, text='Введите строку:')
    en1 = Entry(del_w)
    bt = Button(del_w, text='УДАЛИТЬ', command=row_del)
    lb1.pack(padx=2, pady=2)
    en1.pack(padx=2, pady=2)
    bt.pack(padx=2, pady=2)


def select_window():
    def choice():
        try:
            choice_en = en4.get()
            res = staff.select(choice_en)
            if res:
                for idx, train in enumerate(res, 1):
                    text.delete(0.0, END)
                    text.insert(0.0, '| {:>4} | {:<10} | {:<30} |'.format(idx, train.num, train.name))
            else:
                text.delete(0.0, END)
                text.insert(0.0, 'Таких поездов нет!')
        except(ValueError, TypeError):
            mb.showinfo("Выбор поезда",
                        "Введите время отправления")

    sel_w = Toplevel()
    sel_w.title('Выбрать')
    sel_w.resizable(False, False)
    sel_w.geometry('225x100')
    lb4 = Label(sel_w, text="Введите время отправления")
    en4 = Entry(sel_w)
    bt3 = Button(sel_w, text="Подтвердить", command=choice)
    lb4.pack(padx=2, pady=2)
    en4.pack(padx=2, pady=2)
    bt3.pack(padx=2, pady=2)


def show():
    text.delete(0.0, END)
    text.insert(0.0, staff)


if __name__ == '__main__':
    db = sqlite3.connect('ind.sqlite')
    cur = db.cursor()
    staff = modul.Staff()
    staff.load()

    root = Tk()
    root.geometry('800x450')
    root.title('Главное окно')
    root.resizable(False, False)

    main_menu = Menu(root)
    root.config(menu=main_menu)

    file_menu = Menu(main_menu, tearoff=0)
    file_menu.add_command(label="Загрузить", command=lambda: staff.load())
    file_menu.add_command(label="Сохранить", command=lambda: staff.save())
    file_menu.add_command(label="Обновить", command=update_window)
    file_menu.add_command(label="Удалить", command=del_window)

    main_menu.add_cascade(label="База данных", menu=file_menu)
    main_menu.add_command(label="Добавить", command=add_window)
    main_menu.add_command(label="Показать", command=show)
    main_menu.add_command(label="Выбрать", command=select_window)
    main_menu.add_command(label="Выход", command=lambda: root.destroy())

    text = Text(bg='white', width=97, height=100)
    text.pack(side=LEFT)
    scroll = Scrollbar(command=text.yview)
    scroll.pack(side=LEFT, fill=Y)
    text.config(yscrollcommand=scroll.set)

    root.mainloop()
