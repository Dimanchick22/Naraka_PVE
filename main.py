#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Точка входа для приложения "Калькулятор урона".
Инициализирует и запускает главное окно приложения с современным дизайном.
"""

import tkinter as tk
import os
import sys

# Добавляем текущую директорию в путь импорта
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from ui.main_window import DamageCalculatorWindow


def show_splash_screen():
    """
    Показывает экран загрузки перед запуском основного приложения.
    Простая анимация для улучшения UX.
    """
    # Создаем окно загрузки
    splash = tk.Tk()
    splash.overrideredirect(True)  # Убираем рамку окна

    # Размеры экрана загрузки
    width, height = 400, 200
    screen_width = splash.winfo_screenwidth()
    screen_height = splash.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # Располагаем по центру экрана
    splash.geometry(f"{width}x{height}+{x}+{y}")

    # Добавляем фон и стилизацию
    splash.configure(bg="#3498db")

    # Добавляем текст
    title_label = tk.Label(
        splash,
        text="Калькулятор урона",
        font=("Segoe UI", 24, "bold"),
        bg="#3498db",
        fg="white"
    )
    title_label.pack(pady=(40, 10))

    # Добавляем подзаголовок
    subtitle_label = tk.Label(
        splash,
        text="Загрузка приложения...",
        font=("Segoe UI", 12),
        bg="#3498db",
        fg="white"
    )
    subtitle_label.pack(pady=5)

    # Добавляем индикатор загрузки
    progress_frame = tk.Frame(splash, bg="#3498db")
    progress_frame.pack(pady=20, padx=50, fill=tk.X)

    progress_var = tk.DoubleVar()
    progress_bar = tk.Canvas(
        progress_frame,
        width=300,
        height=20,
        bg="white",
        highlightthickness=0
    )
    progress_bar.pack(fill=tk.X)

    # Функция для анимации загрузки
    def update_progress(current=0):
        if current <= 100:
            # Очищаем и рисуем прогресс-бар
            progress_bar.delete("progress")
            width = current * 3  # 300 пикселей - полная ширина
            progress_bar.create_rectangle(
                0, 0, width, 20,
                fill="#2ecc71",
                tags="progress"
            )
            subtitle_label.config(text=f"Загрузка приложения... {current}%")

            # Рекурсивно вызываем с увеличенным значением
            splash.after(30, update_progress, current + 2)
        else:
            # Закрываем экран загрузки и открываем основное приложение
            splash.destroy()
            launch_app()

    # Запускаем анимацию
    splash.after(500, update_progress)
    splash.mainloop()


def launch_app():
    """Основная функция для запуска приложения."""
    app = DamageCalculatorWindow()

    # Настраиваем отображение по центру экрана
    window_width = 1450
    window_height = 950
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # Устанавливаем позицию и размеры окна
    app.geometry(f"{window_width}x{window_height}+{x}+{y}")

    app.mainloop()


if __name__ == "__main__":
    # Запускаем с экраном загрузки для лучшего UX
    show_splash_screen()