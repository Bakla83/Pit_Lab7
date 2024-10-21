import tkinter as tk
from tkinter import messagebox
import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('store.db')
cursor = conn.cursor()

# Создание таблицы товаров
cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    price REAL,
                    category TEXT)''')

# Создание таблицы пользователей
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    email TEXT UNIQUE,
                    password TEXT)''')

# Добавление товаров в базу данных (3-4 группы по 8-10 товаров)
products = [
    (1, 'Наушники', 1500, 'Аудио'),
    (2, 'Колонки', 3000, 'Аудио'),
    (3, 'Микрофон', 2000, 'Аудио'),
    (4, 'MP3-плеер', 2500, 'Аудио'),
    (5, 'Усилитель звука', 8000, 'Аудио'),
    (6, 'Виниловый проигрыватель', 12000, 'Аудио'),
    (7, 'Цифровое пианино', 25000, 'Аудио'),
    (8, 'Звуковая карта', 4000, 'Аудио'),
    (9, 'Телевизор', 20000, 'Видео'),
    (10, 'Проектор', 25000, 'Видео'),
    (11, 'Видеокамера', 15000, 'Видео'),
    (12, 'DVD-проигрыватель', 3500, 'Видео'),
    (13, 'Blu-Ray проигрыватель', 5000, 'Видео'),
    (14, '4K монитор', 10000, 'Видео'),
    (15, 'Потоковый медиаплеер', 4500, 'Видео'),
    (16, 'Видео конвертер', 2500, 'Видео'),
    (17, 'Цифровая камера', 10000, 'Фототехника'),
    (18, 'Объектив', 15000, 'Фототехника'),
    (19, 'Трипод', 3000, 'Фототехника'),
    (20, 'Свет для съемки', 4000, 'Фототехника'),
    (21, 'Фотобокс', 2500, 'Фототехника'),
    (22, 'Аналоговая камера', 6000, 'Фототехника'),
    (23, 'Пленка', 1000, 'Фототехника'),
    (24, 'Штатив', 2000, 'Фототехника'),
    (25, 'Смартфон', 25000, 'Гаджеты'),
    (26, 'Смарт-часы', 8000, 'Гаджеты'),
    (27, 'Фитнес-браслет', 4000, 'Гаджеты'),
    (28, 'Планшет', 15000, 'Гаджеты'),
    (29, 'Электронная книга', 5000, 'Гаджеты'),
    (30, 'Умная колонка', 7000, 'Гаджеты'),
    (31, 'Портативный аккумулятор', 2000, 'Гаджеты'),
    (32, 'Виртуальные очки', 10000, 'Гаджеты')
]

# Вставка данных о товарах в таблицу, игнорируя дубликаты по id
cursor.executemany('INSERT OR IGNORE INTO products VALUES (?, ?, ?, ?)', products)
conn.commit()

# Основной класс приложения
class StoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Интернет-магазин")
        self.root.geometry("600x600")

        self.user = None

        # Создаем окно авторизации
        self.frame_login = tk.Frame(root)
        self.frame_login.pack()

        self.label_email = tk.Label(self.frame_login, text="Электронная почта:")
        self.label_email.pack()
        self.entry_email = tk.Entry(self.frame_login)
        self.entry_email.pack()

        self.label_password = tk.Label(self.frame_login, text="Пароль:")
        self.label_password.pack()
        self.entry_password = tk.Entry(self.frame_login, show='*')
        self.entry_password.pack()

        self.button_login = tk.Button(self.frame_login, text="Войти", command=self.login_user)
        self.button_login.pack()

        self.button_register = tk.Button(self.frame_login, text="Регистрация", command=self.show_registration)
        self.button_register.pack()

    def show_registration(self):
        # Форма для регистрации
        self.frame_login.pack_forget()
        self.frame_register = tk.Frame(self.root)
        self.frame_register.pack()

        self.label_new_email = tk.Label(self.frame_register, text="Электронная почта:")
        self.label_new_email.pack()
        self.entry_new_email = tk.Entry(self.frame_register)
        self.entry_new_email.pack()

        self.label_new_password = tk.Label(self.frame_register, text="Пароль:")
        self.label_new_password.pack()
        self.entry_new_password = tk.Entry(self.frame_register, show='*')
        self.entry_new_password.pack()

        self.button_create_account = tk.Button(self.frame_register, text="Создать аккаунт", command=self.register_user)
        self.button_create_account.pack()

        self.button_back = tk.Button(self.frame_register, text="Назад", command=self.show_login)
        self.button_back.pack()

    def register_user(self):
        email = self.entry_new_email.get()
        password = self.entry_new_password.get()

        if not email or not password:
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля")
            return

        try:
            cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
            conn.commit()
            messagebox.showinfo("Успех", "Аккаунт успешно создан")
            self.show_login()
        except sqlite3.IntegrityError:
            messagebox.showerror("Ошибка", "Пользователь с таким email уже существует")

    def show_login(self):
        self.frame_register.pack_forget()
        self.frame_login.pack()

    def login_user(self):
        email = self.entry_email.get()
        password = self.entry_password.get()

        cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = cursor.fetchone()

        if user:
            self.user = user
            self.frame_login.pack_forget()
            self.show_product_selection()
        else:
            messagebox.showerror("Ошибка", "Неверные учетные данные")

    def show_product_selection(self):
        self.frame_selection = tk.Frame(self.root)
        self.frame_selection.pack()

        tk.Label(self.frame_selection, text="Выберите категорию:").pack()

        self.category_var = tk.StringVar()
        self.category_var.set("Аудио")

        categories = ["Аудио", "Видео", "Фототехника", "Гаджеты"]
        self.option_menu = tk.OptionMenu(self.frame_selection, self.category_var, *categories)
        self.option_menu.pack()

        self.button_select = tk.Button(self.frame_selection, text="Показать товары", command=self.show_products)
        self.button_select.pack()

        self.button_exit = tk.Button(self.frame_selection, text="Выход", command=self.root.quit)
        self.button_exit.pack()

    def show_products(self):
        category = self.category_var.get()
        cursor.execute("SELECT * FROM products WHERE category=?", (category,))
        products = cursor.fetchall()

        self.frame_selection.pack_forget()
        self.frame_products = tk.Frame(self.root)
        self.frame_products.pack()

        self.selected_products = {}
        for product in products:
            product_id, name, price, _ = product
            var = tk.IntVar()

            check = tk.Checkbutton(self.frame_products, text=f"{name} - {price} руб.", variable=var)
            check.pack()

            quantity_entry = tk.Entry(self.frame_products)
            quantity_entry.insert(0, "1")
            quantity_entry.pack()
            quantity_entry.config(state=tk.DISABLED)  # По умолчанию отключаем поле ввода

            # Сохраняем переменные и виджеты
            self.selected_products[product_id] = (var, quantity_entry)

            # Функция для включения/выключения поля ввода количества
            def toggle_quantity_entry(var=var, entry=quantity_entry):
                if var.get():
                    entry.config(state=tk.NORMAL)
                else:
                    entry.config(state=tk.DISABLED)

            # Привязываем событие изменения переменной `var` к функции
            var.trace_add("write", lambda *args, var=var, entry=quantity_entry: toggle_quantity_entry(var, entry))

        self.button_buy = tk.Button(self.frame_products, text="Купить", command=self.purchase_products)
        self.button_buy.pack()

        self.button_buy_again = tk.Button(self.frame_products, text="Купить еще", command=self.buy_again)
        self.button_buy_again.pack()

        self.button_exit = tk.Button(self.frame_products, text="Выход", command=self.root.quit)
        self.button_exit.pack()

    def purchase_products(self):
        total_sum = 0
        purchase_details = ""

        for product_id, (var, quantity_entry) in self.selected_products.items():
            if var.get():
                try:
                    quantity = int(quantity_entry.get())
                except ValueError:
                    messagebox.showerror("Ошибка", "Некорректное количество")
                    return

                cursor.execute("SELECT name, price FROM products WHERE id=?", (product_id,))
                name, price = cursor.fetchone()
                total_price = price * quantity
                total_sum += total_price
                purchase_details += f"{name} ({quantity} шт.) - {total_price} руб.\n"

        if total_sum > 0:
            messagebox.showinfo("Покупка", f"Вы купили:\n{purchase_details}\nИтоговая сумма: {total_sum} руб.")
        else:
            messagebox.showerror("Ошибка", "Выберите хотя бы один товар")

    def buy_again(self):
        self.frame_products.pack_forget()
        self.show_product_selection()


if __name__ == "__main__":
    root = tk.Tk()
    app = StoreApp(root)
    root.mainloop()

    conn.close()
