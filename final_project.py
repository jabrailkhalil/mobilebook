import tkinter as tk
from tkinter import ttk
import sqlite3
import os
import tkinter.messagebox as messagebox

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()

    def init_main(self):
        # Создаем верхнюю панель инструментов с кнопками
        messagebox.showinfo("Предупреждение", "Программа выполняет обновление при пустом поиске.")
        toolbar = tk.Frame(bg='#d7d7d7', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Определяем текущий каталог, в котором находится скрипт
        current_dir = os.path.dirname(__file__)

        # Создаем пути к изображениям
        image_path_add = os.path.join(current_dir, 'img', 'add.png')
        image_path_edit = os.path.join(current_dir, 'img', 'edit.png')
        image_path_trash = os.path.join(current_dir, 'img', 'trash.png')
        image_path_search = os.path.join(current_dir, 'img', 'search.png')

        # Создаем изображения для кнопок
        self.add_img = tk.PhotoImage(file=image_path_add)
        self.edit_img = tk.PhotoImage(file=image_path_edit)
        self.trash_img = tk.PhotoImage(file=image_path_trash)
        self.search_img = tk.PhotoImage(file=image_path_search)

        # Создаем кнопки на панели инструментов
        btn_add = tk.Button(toolbar, text='Добавить', image=self.add_img, bg='#d7d7d7', bd=0, command=self.open_child)
        btn_add.pack(side=tk.LEFT)

        btn_edit = tk.Button(toolbar, text='Изменить', image=self.edit_img, bg='#d7d7d7', bd=0, command=self.edit_contact)
        btn_edit.pack(side=tk.LEFT)

        btn_delete = tk.Button(toolbar, text='Удалить', image=self.trash_img, bg='#d7d7d7', bd=0, command=self.delete_contact)
        btn_delete.pack(side=tk.LEFT)

        btn_search = tk.Button(toolbar, text='Поиск', image=self.search_img, bg='#d7d7d7', bd=0, command=self.search_contact)
        btn_search.pack(side=tk.LEFT)

        # Создаем таблицу для отображения данных
        self.tree = ttk.Treeview(self, columns=('ID', 'name', 'phone', 'email'), show='headings')
        self.tree.column('ID', width=45, anchor=tk.CENTER)
        self.tree.column('name', width=300, anchor=tk.CENTER)
        self.tree.column('phone', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='Имя')
        self.tree.heading('phone', text='Телефон')
        self.tree.heading('email', text='Email')

        self.tree.pack()

    def open_child(self):
        # Открывает окно для добавления нового сотрудника
        Child(self, self.tree)

    def edit_contact(self):
        # Открывает окно для редактирования выбранного сотрудника
        selected_item = self.tree.selection()

        if selected_item:
            EditChild(self, self.tree, selected_item[0])

    def delete_contact(self):
        # Удаляет выбранного сотрудника
        selected_item = self.tree.selection()

        if selected_item:
            contact_id = self.tree.item(selected_item, 'values')[0]

            db = Db()
            db.delete_contact(contact_id)
            db.conn.commit()

            self.tree.delete(selected_item)

    def search_contact(self):
        # Открывает окно для поиска сотрудника по имени
        SearchChild(self, self.tree)

class Child(tk.Toplevel):
    def __init__(self, master, tree):
        super().__init__(master)
        self.master = master
        self.tree = tree
        self.init_child()

    def init_child(self):
        # Инициализирует окно для добавления нового сотрудника
        self.title('Добавить сотрудника')
        self.geometry('400x200')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        label_name = tk.Label(self, text='Имя')
        label_phone = tk.Label(self, text='Телефон')
        label_email = tk.Label(self, text='Email')
        label_name.place(x=60, y=50)
        label_phone.place(x=60, y=80)
        label_email.place(x=60, y=110)

        self.entry_name = tk.Entry(self)
        self.entry_phone = tk.Entry(self)
        self.entry_email = tk.Entry(self)
        self.entry_name.place(x=220, y=50)
        self.entry_phone.place(x=220, y=80)
        self.entry_email.place(x=220, y=110)

        btn_close = tk.Button(self, text='Закрыть', command=self.destroy)
        btn_close.place(x=240, y=160)

        btn_ok = tk.Button(self, text='Добавить', command=self.add_contact)
        btn_ok.place(x=290, y=160)

    def add_contact(self):
        # Добавляет нового сотрудника в базу данных и отображает его в таблице
        name = self.entry_name.get()
        phone = self.entry_phone.get()
        email = self.entry_email.get()

        db = Db()
        contact_id = db.insert_contact(name, phone, email)
        self.tree.insert('', 'end', values=(contact_id, name, phone, email))
        self.destroy()

class EditChild(tk.Toplevel):
    def __init__(self, master, tree, selected_item):
        super().__init__(master)
        self.master = master
        self.tree = tree
        self.selected_item = selected_item
        self.init_child()

    def init_child(self):
        # Инициализирует окно для редактирования выбранного сотрудника
        self.title('Изменить данные сотрудника')
        self.geometry('400x200')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        selected_contact = self.tree.item(self.selected_item, 'values')
        if selected_contact:
            contact_id, name, phone, email = selected_contact

            label_name = tk.Label(self, text='Имя')
            label_phone = tk.Label(self, text='Телефон')
            label_email = tk.Label(self, text='Email')
            label_name.place(x=60, y=50)
            label_phone.place(x=60, y=80)
            label_email.place(x=60, y=110)

            self.entry_name = tk.Entry(self)
            self.entry_phone = tk.Entry(self)
            self.entry_email = tk.Entry(self)
            self.entry_name.insert(0, name)
            self.entry_phone.insert(0, phone)
            self.entry_email.insert(0, email)
            self.entry_name.place(x=220, y=50)
            self.entry_phone.place(x=220, y=80)
            self.entry_email.place(x=220, y=110)

            btn_close = tk.Button(self, text='Закрыть', command=self.destroy)
            btn_close.place(x=240, y=160)

            btn_save = tk.Button(self, text='Сохранить', command=self.edit_contact)
            btn_save.place(x=290, y=160)

    def edit_contact(self):
        # Сохраняет отредактированного сотрудника в базе данных и обновляет его в таблице
        new_name = self.entry_name.get()
        new_phone = self.entry_phone.get()
        new_email = self.entry_email.get()

        db = Db()
        contact_id = self.tree.item(self.selected_item, 'values')[0]
        db.update_contact(contact_id, new_name, new_phone, new_email)
        db.conn.commit()

        self.tree.item(self.selected_item, values=(contact_id, new_name, new_phone, new_email))
        self.destroy()

class SearchChild(tk.Toplevel):
    def __init__(self, master, tree):
        super().__init__(master)
        self.master = master
        self.tree = tree
        self.init_child()

    def init_child(self):
        # Инициализирует окно для поиска сотрудника по имени
        self.title('Поиск сотрудника')
        self.geometry('400x100')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        label_search = tk.Label(self, text='Введите имя для поиска')
        label_search.place(x=60, y=20)

        self.entry_search = tk.Entry(self)
        self.entry_search.place(x=220, y=20)

        btn_search = tk.Button(self, text='Поиск', command=self.search_contact)
        btn_search.place(x=290, y=60)

    def search_contact(self):
        # Выполняет поиск сотрудника по имени и обновляет таблицу с результатами
        name = self.entry_search.get()

        db = Db()
        results = db.search_contacts(name)
        self.tree.delete(*self.tree.get_children())

        for row in results:
            self.tree.insert('', 'end', values=row)

class Db:
    def __init__(self):
        # Инициализирует подключение к базе данных и создает таблицу, если она не существует
        self.conn = sqlite3.connect('contacts.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY,
                name TEXT,
                phone TEXT,
                email TEXT
            )
        ''')
        self.conn.commit()

    def insert_contact(self, name, phone, email):
        # Вставляет сотрудника в базу данных
        self.cursor.execute('INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)', (name, phone, email))
        self.conn.commit()
        return self.cursor.lastrowid

    def update_contact(self, contact_id, name, phone, email):
        # Обновляет сотрудников в базе данных
        self.cursor.execute('UPDATE contacts SET name = ?, phone = ?, email = ? WHERE id = ?', (name, phone, email, contact_id))
        self.conn.commit()

    def delete_contact(self, contact_id):
        # Удаляет сотрудника из базы данных
        self.cursor.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
        self.conn.commit()

    def search_contacts(self, name):
        # Выполняет поиск сотрудников по имени и возвращает результаты
        self.cursor.execute('SELECT * FROM contacts WHERE name LIKE ?', ('%' + name + '%',))
        return self.cursor.fetchall()

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Список сотрудников компании')
    app = Main(root)
    app.pack()
    root.geometry('700x400')
    root.resizable(False, False)
    root.mainloop()
