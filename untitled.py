import tkinter as tk
import random
import string
import json
import os

# Функция для генерации пароля
def generate_password():
    length = password_length.get()
    all_characters = ''
    
    if include_digits.get():
        all_characters += string.digits
    if include_letters.get():
        all_characters += string.ascii_letters
    if include_specials.get():
        all_characters += string.punctuation

    if all_characters == '':
        return  # Ничего не выбрано, ничего не генерируем

    password = ''.join(random.choice(all_characters) for _ in range(length))
    password_history.append(password)
    update_history_table()

# Функция для обновления таблицы истории
def update_history_table():
    for row in history_table.get_children():
        history_table.delete(row)
    
    for password in password_history:
        history_table.insert('', 'end', values=(password,))

# Функция для сохранения в JSON
def save_history():
    with open('password_history.json', 'w') as file:
        json.dump(password_history, file)

# Функция для загрузки из JSON
def load_history():
    if os.path.exists('password_history.json'):
        with open('password_history.json', 'r') as file:
            return json.load(file)
    return []

# Инициализация
root = tk.Tk()
root.title("Random Password Generator")

password_length = tk.IntVar(value=8)
include_digits = tk.BooleanVar(value=True)
include_letters = tk.BooleanVar(value=True)
include_specials = tk.BooleanVar(value=True)
password_history = load_history()

# Элементы интерфейса
tk.Label(root, text="Длина пароля (от 1 до 20):").pack()

length_slider = tk.Scale(root, from_=1, to=20, orient='horizontal', variable=password_length)
length_slider.pack()

tk.Checkbutton(root, text="Цифры", variable=include_digits).pack()
tk.Checkbutton(root, text="Буквы", variable=include_letters).pack()
tk.Checkbutton(root, text="Спецсимволы", variable=include_specials).pack()

generate_button = tk.Button(root, text="Сгенерировать пароль", command=generate_password)
generate_button.pack()

# Таблица истории паролей
columns = ('Пароль',)
history_table = tk.ttk.Treeview(root, columns=columns, show='headings')
history_table.heading('Пароль', text='Пароль')
history_table.pack()

# Кнопка сохранения истории
save_button = tk.Button(root, text="Сохранить историю", command=save_history)
save_button.pack()

# Загружаем историю
update_history_table()

# Запускаем приложение
root.mainloop()