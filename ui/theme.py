#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Темы оформления для приложения "Калькулятор урона".
Содержит стили, цвета и шрифты для современного интерфейса.
"""

import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
import os


class ModernTheme:
    """Современная тема оформления приложения."""

    # Основные цвета
    PRIMARY_COLOR = "#3498db"  # Синий
    SECONDARY_COLOR = "#2ecc71"  # Зеленый
    ACCENT_COLOR = "#e74c3c"  # Красный
    BG_COLOR = "#f5f5f5"  # Светло-серый
    DARK_BG_COLOR = "#2c3e50"  # Темно-синий

    # Цвета текста
    TEXT_COLOR = "#2c3e50"  # Темно-синий
    LIGHT_TEXT_COLOR = "#1a1a1a" # Тёмный цвет для текста кнопок
    SECONDARY_TEXT_COLOR = "#7f8c8d"  # Серый
    BUTTON_TEXT_COLOR = "#1a1a1a"  # Тёмный цвет для текста кнопок

    # Цвета рамок и границ
    BORDER_COLOR = "#bdc3c7"  # Светло-серый

    # Цвета для результатов
    RESULT_BG_COLOR = "#dff0d8"  # Светло-зеленый
    WARNING_COLOR = "#fcf8e3"  # Светло-желтый
    ERROR_COLOR = "#f2dede"  # Светло-красный

    # Параметры шрифтов - ОПТИМИЗИРОВАНЫ
    LARGE_FONT_SIZE = 12  # Уменьшено с 14
    NORMAL_FONT_SIZE = 9  # Уменьшено с 10
    SMALL_FONT_SIZE = 8  # Уменьшено с 9

    # Отступы и размеры - ОПТИМИЗИРОВАНЫ
    PADDING = 8  # Уменьшено с 10
    LARGE_PADDING = 12  # Уменьшено с 15
    SMALL_PADDING = 4  # Уменьшено с 5

    # Радиус скругления для элементов
    CORNER_RADIUS = 4

    # Ширина кнопок и полей ввода - ОПТИМИЗИРОВАНЫ
    BUTTON_WIDTH = 18  # Уменьшено с 20
    ENTRY_WIDTH = 12  # Уменьшено с 15

    def __init__(self, root):
        """
        Инициализация темы и применение стилей к приложению.

        Args:
            root: Корневой виджет приложения
        """
        self.root = root

        # Настройка базовых свойств окна
        root.configure(bg=self.BG_COLOR)

        # Глобальное отключение фокусной обводки
        root.option_add('*TCombobox*Listbox.takeFocus', 0)
        root.option_add('*TButton.takeFocus', 0)
        root.option_add('*TCheckbutton.takeFocus', 0)
        root.option_add('*TNotebook.takeFocus', 0)
        root.option_add('*TNotebook.Tab.takeFocus', 0)
        root.option_add('*highlight.thickness', 0)

        # Создание и настройка стилей
        self._create_styles()

        # Установка шрифтов
        self._configure_fonts()

        # Создаем пользовательские стили кнопок с изображениями (если доступно)
        self._create_custom_buttons()

    def _create_styles(self):
        """Создает и настраивает стили для различных виджетов."""
        style = ttk.Style()

        style.layout("Tab", [('Notebook.tab', {'sticky': 'nswe', 'children':
            [('Notebook.padding', {'side': 'top', 'sticky': 'nswe', 'children':
                [('Notebook.label', {'sticky': 'nswe'})]
                                   })],
                                               })])

        # Общие настройки
        style.configure(".",
                        background=self.BG_COLOR,
                        foreground=self.TEXT_COLOR,
                        font=("Segoe UI", self.NORMAL_FONT_SIZE),
                        highlightthickness=0)

        # Кнопки - Используем DARK_BG_COLOR (тёмно-синий) для текста на кнопках
        style.configure("TButton",
                        background=self.PRIMARY_COLOR,
                        foreground=self.DARK_BG_COLOR,  # Тёмно-синий цвет текста на синем фоне
                        padding=self.PADDING,
                        relief="flat",
                        borderwidth=0,
                        highlightthickness=0,
                        font=("Segoe UI", self.NORMAL_FONT_SIZE, "bold"))

        style.map("TButton",
                  background=[("active", self.SECONDARY_COLOR),
                              ("pressed", self.SECONDARY_COLOR),
                              ("disabled", self.SECONDARY_TEXT_COLOR)],
                  foreground=[("active", self.DARK_BG_COLOR),  # Тёмно-синий цвет при наведении
                              ("disabled", self.LIGHT_TEXT_COLOR)],  # Светлый цвет для отключенных кнопок
                  relief=[("pressed", "flat"), ("active", "flat")])

        # Кнопка расчета (акцентированная) - тоже тёмный текст
        style.configure("Accent.TButton",
                        background=self.ACCENT_COLOR,
                        foreground=self.DARK_BG_COLOR,  # Тёмно-синий цвет текста на красном фоне
                        padding=self.PADDING,
                        relief="flat",
                        borderwidth=0,
                        highlightthickness=0,
                        font=("Segoe UI", self.LARGE_FONT_SIZE, "bold"))

        style.map("Accent.TButton",
                  background=[("active", "#c0392b"),
                              ("pressed", "#c0392b"),
                              ("disabled", self.SECONDARY_TEXT_COLOR)],
                  foreground=[("active", self.DARK_BG_COLOR),
                              ("disabled", self.LIGHT_TEXT_COLOR)],
                  relief=[("pressed", "flat"), ("active", "flat")])

        # Метки
        style.configure("TLabel",
                        background=self.BG_COLOR,
                        foreground=self.TEXT_COLOR,
                        font=("Segoe UI", self.NORMAL_FONT_SIZE))

        # Заголовки
        style.configure("Title.TLabel",
                        font=("Segoe UI", self.LARGE_FONT_SIZE, "bold"),
                        foreground=self.DARK_BG_COLOR,
                        background=self.BG_COLOR,
                        padding=(0, self.LARGE_PADDING))

        # Поля ввода
        style.configure("TEntry",
                        fieldbackground="white",
                        foreground=self.TEXT_COLOR,
                        padding=self.SMALL_PADDING,
                        highlightthickness=0)

        # Рамки
        style.configure("TFrame",
                        background=self.BG_COLOR)

        # Флажки
        style.configure("TCheckbutton",
                        background=self.BG_COLOR,
                        foreground=self.TEXT_COLOR,
                        highlightthickness=0,
                        borderwidth=0,
                        font=("Segoe UI", self.NORMAL_FONT_SIZE))

        style.map("TCheckbutton",
                  background=[("active", self.BG_COLOR)],
                  foreground=[("active", self.TEXT_COLOR)])

        # LabelFrame
        style.configure("TLabelframe",
                        background=self.BG_COLOR,
                        foreground=self.TEXT_COLOR,
                        font=("Segoe UI", self.NORMAL_FONT_SIZE, "bold"))

        style.configure("TLabelframe.Label",
                        background=self.BG_COLOR,
                        foreground=self.PRIMARY_COLOR,
                        font=("Segoe UI", self.NORMAL_FONT_SIZE, "bold"))

        # Combobox
        style.configure("TCombobox",
                        foreground=self.TEXT_COLOR,
                        background="white",
                        fieldbackground="white",
                        padding=self.SMALL_PADDING,
                        highlightthickness=0)

        # Notebook (вкладки)
        style.configure("TNotebook",
                        background=self.BG_COLOR,
                        tabmargins=[2, 5, 2, 0],
                        highlightthickness=0)

        style.configure("TNotebook.Tab",
                        background="#d3d3d3",
                        foreground=self.TEXT_COLOR,
                        padding=[self.PADDING, self.SMALL_PADDING],
                        highlightthickness=0,
                        font=("Segoe UI", self.NORMAL_FONT_SIZE))

        style.map("TNotebook.Tab",
                  background=[("selected", self.PRIMARY_COLOR)],
                  foreground=[("selected", self.LIGHT_TEXT_COLOR)])

        # Полосы прокрутки
        style.configure("TScrollbar",
                        background=self.BG_COLOR,
                        troughcolor=self.BG_COLOR,
                        bordercolor=self.BORDER_COLOR,
                        arrowcolor=self.TEXT_COLOR,
                        highlightthickness=0)

        # Рамки для результатов
        style.configure("Result.TLabelframe",
                        background=self.RESULT_BG_COLOR,
                        foreground=self.TEXT_COLOR)

        style.configure("Result.TLabelframe.Label",
                        background=self.RESULT_BG_COLOR,
                        foreground=self.PRIMARY_COLOR,
                        font=("Segoe UI", self.NORMAL_FONT_SIZE, "bold"))

        # Результаты
        style.configure("Result.TLabel",
                        background=self.RESULT_BG_COLOR,
                        foreground=self.TEXT_COLOR,
                        font=("Segoe UI", self.NORMAL_FONT_SIZE, "bold"))

        style.configure("ResultValue.TLabel",
                        background=self.RESULT_BG_COLOR,
                        foreground=self.PRIMARY_COLOR,
                        font=("Segoe UI", self.LARGE_FONT_SIZE, "bold"))

        # Информационные метки
        style.configure("Info.TLabel",
                        background=self.BG_COLOR,
                        foreground=self.PRIMARY_COLOR,
                        font=("Segoe UI", self.NORMAL_FONT_SIZE, "bold"))

    def _configure_fonts(self):
        """Настраивает шрифты для приложения."""
        default_font = tkfont.nametofont("TkDefaultFont")
        default_font.configure(family="Segoe UI", size=self.NORMAL_FONT_SIZE)

        text_font = tkfont.nametofont("TkTextFont")
        text_font.configure(family="Segoe UI", size=self.NORMAL_FONT_SIZE)

        fixed_font = tkfont.nametofont("TkFixedFont")
        fixed_font.configure(family="Consolas", size=self.NORMAL_FONT_SIZE)

        # Применяем шрифт для всех виджетов по умолчанию
        self.root.option_add("*Font", default_font)

    def _create_custom_buttons(self):
        """
        Создает пользовательские стили для кнопок с помощью Canvas.
        Это обход ограничений ttk, который позволяет создать красивые кнопки.
        """

        # Определяем классы кнопок с Canvas
        class PrimaryButton(tk.Frame):
            def __init__(self, parent, text, command=None, width=None, **kwargs):
                super().__init__(parent, highlightthickness=0, bd=0, bg=self.BG_COLOR)

                if width:
                    self.width = width
                else:
                    self.width = 200 if text else 100

                self.height = 40
                self.canvas = tk.Canvas(self, width=self.width, height=self.height,
                                        highlightthickness=0, bg=self.BG_COLOR)
                self.canvas.pack()

                self.text = text
                self.command = command
                self.state = "normal"

                self._draw()

                self.canvas.bind("<ButtonPress-1>", self._on_press)
                self.canvas.bind("<ButtonRelease-1>", self._on_release)
                self.canvas.bind("<Enter>", self._on_enter)
                self.canvas.bind("<Leave>", self._on_leave)

            def _draw(self):
                self.canvas.delete("all")

                # Определяем цвета в зависимости от состояния
                if self.state == "disabled":
                    fill_color = "#bdc3c7"  # Светло-серый для отключенной кнопки
                    text_color = "#7f8c8d"  # Серый для текста отключенной кнопки
                elif self.state == "pressed":
                    fill_color = "#2980b9"  # Темно-синий для нажатой кнопки
                    text_color = "#2c3e50"  # Темно-синий текст
                elif self.state == "hover":
                    fill_color = "#2ecc71"  # Зеленый для кнопки при наведении
                    text_color = "#2c3e50"  # Темно-синий текст
                else:
                    fill_color = "#3498db"  # Синий для обычного состояния
                    text_color = "#2c3e50"  # Темно-синий текст

                # Рисуем прямоугольник с скругленными углами
                self.canvas.create_rectangle(
                    0, 0, self.width, self.height,
                    fill=fill_color, outline=fill_color, width=0
                )

                # Добавляем текст
                if self.text:
                    self.canvas.create_text(
                        self.width / 2, self.height / 2,
                        text=self.text, fill=text_color,
                        font=("Segoe UI", 11, "bold")
                    )

            def _on_press(self, event):
                if self.state != "disabled":
                    self.state = "pressed"
                    self._draw()

            def _on_release(self, event):
                if self.state != "disabled":
                    x, y = event.x, event.y
                    if 0 <= x <= self.width and 0 <= y <= self.height:
                        # Клик внутри кнопки
                        if self.command:
                            self.command()
                        self.state = "hover"
                    else:
                        # Клик за пределами кнопки
                        self.state = "normal"
                    self._draw()

            def _on_enter(self, event):
                if self.state != "disabled":
                    self.state = "hover"
                    self._draw()

            def _on_leave(self, event):
                if self.state != "disabled":
                    self.state = "normal"
                    self._draw()

            def configure(self, **kwargs):
                if "state" in kwargs:
                    self.state = kwargs["state"]
                    self._draw()
                if "command" in kwargs:
                    self.command = kwargs["command"]
                if "text" in kwargs:
                    self.text = kwargs["text"]
                    self._draw()

        # Регистрируем классы кнопок
        PrimaryButton.BG_COLOR = self.BG_COLOR

        # Сохраняем классы кнопок как атрибуты темы
        self.PrimaryButton = PrimaryButton


def apply_theme(root):
    """
    Применяет современную тему к приложению.

    Args:
        root: Корневой виджет приложения

    Returns:
        Экземпляр класса ModernTheme
    """
    return ModernTheme(root)


def create_modern_button(parent, text, command=None, accent=False, width=None):
    """
    Создает современную кнопку с красивым дизайном.
    """
    # Создаем обычную кнопку tk.Button вместо ttk.Button для лучшего контроля
    if accent:
        bg_color = "#e74c3c"  # Красный для акцентной кнопки
        hover_color = "#c0392b"  # Тёмно-красный при наведении
        fg_color = "#ffffff"  # Белый текст
        font_size = 12
    else:
        bg_color = "#3498db"  # Синий для обычной кнопки
        hover_color = "#2980b9"  # Тёмно-синий при наведении
        fg_color = "#ffffff"  # Белый текст
        font_size = 9

    # Если width не указан, сделаем кнопку шире
    if width is None:
        width = 25  # Увеличено с стандартного значения

    button = tk.Button(
        parent,
        text=text,
        command=command,
        bg=bg_color,
        fg=fg_color,
        activebackground=hover_color,
        activeforeground=fg_color,
        relief="flat",
        borderwidth=0,
        highlightthickness=0,  # Обязательно отключаем обводку
        font=("Segoe UI", font_size, "bold"),
        padx=15,  # Увеличиваем горизонтальный отступ
        pady=7,  # Увеличиваем вертикальный отступ
        width=width
    )

    # Явно отключаем фокусную обводку для кнопки
    button.config(takefocus=0)

    return button