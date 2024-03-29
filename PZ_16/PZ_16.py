import tkinter as tk
from tkinter import ttk
import sqlite3 as sq


class Main(tk.Frame):
    """Класс для главного окна"""

    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):
        toolbar = tk.Frame(bg='#f2d8e4', bd=4)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file="DB/11.png")
        self.btn_open_dialog = tk.Button(toolbar, text='Добавить работника', command=self.open_dialog, bg='#f5bad5',
                                         bd=0,
                                         compound=tk.TOP, image=self.add_img)
        self.btn_open_dialog.pack(side=tk.LEFT, padx=5)

        self.update_img = tk.PhotoImage(file="DB/12.png")
        btn_edit_dialog = tk.Button(toolbar, text="Редактировать", command=self.open_update_dialog, bg='#f5bad5',
                                    bd=0, compound=tk.TOP, image=self.update_img)
        btn_edit_dialog.pack(side=tk.LEFT, padx=5)

        self.delete_img = tk.PhotoImage(file="DB/13.png")
        btn_delete = tk.Button(toolbar, text="Удалить запись", command=self.delete_records, bg='#f5bad5',
                               bd=0, compound=tk.TOP, image=self.delete_img)
        btn_delete.pack(side=tk.LEFT, padx=5)

        self.search_img = tk.PhotoImage(file="DB/14.png")
        btn_search = tk.Button(toolbar, text="Поиск записи", command=self.open_search_dialog, bg='#f5bad5',
                               bd=0, compound=tk.TOP, image=self.search_img)
        btn_search.pack(side=tk.LEFT, padx=5)

        self.refresh_img = tk.PhotoImage(file="DB/15.png")
        btn_refresh = tk.Button(toolbar, text="Обновить экран", command=self.view_records, bg='#f5bad5',
                                bd=0, compound=tk.TOP, image=self.refresh_img)
        btn_refresh.pack(side=tk.LEFT, padx=5)

        self.tree = ttk.Treeview(self, columns=('id', 'name', 'add_work', 'total', 'time'), height=15, show='headings')

        self.tree.column('id', width=50, anchor=tk.CENTER)
        self.tree.column('name', width=180, anchor=tk.CENTER)
        self.tree.column('add_work', width=140, anchor=tk.CENTER)
        self.tree.column('total', width=140, anchor=tk.CENTER)
        self.tree.column('time', width=140, anchor=tk.CENTER)

        self.tree.heading('id', text='ID')
        self.tree.heading('name', text='Имя работника')
        self.tree.heading('add_work', text='Вид доп.работы')
        self.tree.heading('total', text='Сумма оплаты')
        self.tree.heading('time', text='Срок')

        self.tree.pack()

    def records(self, id, name, add_work, total, time):
        self.db.insert_data(id, name, add_work, total, time)
        self.view_records()

    def update_record(self, id, name, add_work, total, time):
        self.db.cur.execute("""UPDATE responsibility SET id=?, name=?, add_work=?, total=?, time=? WHERE id=?""",
                            (id, name, add_work, total, time, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.con.commit()
        self.view_records()

    def view_records(self):
        self.db.cur.execute("""SELECT * FROM responsibility""")
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cur.fetchall()]

    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.cur.execute("""DELETE FROM responsibility WHERE id=?""", (self.tree.set(selection_item, '#1'),))
        self.db.con.commit()
        self.view_records()

    def search_records(self, total):
        total = (total,)
        self.db.cur.execute("""SELECT * FROM responsibility WHERE total>?""", total)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cur.fetchall()]

    def open_dialog(self):
        Child(root, app)

    def open_update_dialog(self):
        Update()

    def open_search_dialog(self):
        Search()


class Child(tk.Toplevel):
    """Класс для дочернего окна"""

    def __init__(self, root, app):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добавить работника')
        self.geometry('400x220+400+300')
        self.resizable(False, False)

        label_description = tk.Label(self, text='Номер')
        label_description.place(x=50, y=25)
        self.entry_description = ttk.Entry(self)
        self.entry_description.place(x=150, y=25)

        label_name = tk.Label(self, text='ФИО')
        label_name.place(x=50, y=50)
        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=150, y=50)

        label_work = tk.Label(self, text='Вид доп.работы')
        label_work.place(x=50, y=75)
        self.entry_work = ttk.Entry(self)
        self.entry_work.place(x=150, y=75)

        label_total = tk.Label(self, text='Сумма оплаты')
        label_total.place(x=50, y=100)
        self.entry_total = ttk.Entry(self)
        self.entry_total.place(x=150, y=100)

        label_time = tk.Label(self, text='Срок')
        label_time.place(x=50, y=125)
        self.entry_time = ttk.Entry(self)
        self.entry_time.place(x=150, y=125)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=170)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=170)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_description.get(),
                                                                       self.entry_name.get(),
                                                                       self.entry_work.get(),
                                                                       self.entry_total.get(),
                                                                       self.entry_time.get()))

        self.grab_set()
        self.focus_set()


class Update(Child):
    def __init__(self):
        super().__init__(root, app)
        self.init_edit()
        self.view = app

    def init_edit(self):
        self.title("Редактировать запись")
        btn_edit = ttk.Button(self, text="Редактировать")
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_description.get(),
                                                                          self.entry_name.get(),
                                                                          self.entry_work.get(),
                                                                          self.entry_total.get(),
                                                                          self.entry_time.get()))
        self.btn_ok.destroy()


class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title("Поиск")
        self.geometry("300x100+400+300")
        self.resizable(False, False)

        label_search = tk.Label(self, text="Сумма оплаты")
        label_search.place(x=10, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text="Поиск")
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get()))
        # btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')


class DB:
    def __init__(self):
        with sq.connect('DB/responsibility.db') as self.con:
            self.cur = self.con.cursor()
            self.cur.execute("""CREATE TABLE IF NOT EXISTS responsibility (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                add_work TEXT,
                total INTEGER,
                time INTEGER
                )""")

    def insert_data(self, id, name, add_work, total, time):
        self.cur.execute("""INSERT INTO responsibility(id, name, add_work, total, time) VALUES (?, ?, ?, ?, ?)""",
                         (id, name, add_work, total, time))
        self.con.commit()


if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Распределение дополнительных обязанностей")
    root.geometry("650x450+300+200")
    root.resizable(False, False)
    root.mainloop()
