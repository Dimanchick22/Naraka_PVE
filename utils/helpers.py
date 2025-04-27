#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Вспомогательные функции для приложения "Калькулятор урона".
"""

import tkinter as tk
from tkinter import ttk
import re


def create_tooltip(widget, text):
    """
    Создает всплывающую подсказку для виджета.

    Args:
        widget: Виджет, для которого создается подсказка
        text: Текст подсказки
    """
    tooltip = None

    def enter(event):
        nonlocal tooltip
        x, y, _, _ = widget.bbox("insert")
        x += widget.winfo_rootx() + 25
        y += widget.winfo_rooty() + 25

        # Создаем окно подсказки
        tooltip = tk.Toplevel(widget)
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{x}+{y}")

        label = ttk.Label(tooltip, text=text, background="#FFFFDD", relief="solid", borderwidth=1, padding=5)
        label.pack()

    def leave(event):
        nonlocal tooltip
        if tooltip:
            tooltip.destroy()
            tooltip = None

    widget.bind("<Enter>", enter)
    widget.bind("<Leave>", leave)


def validate_float_input(value):
    """
    Проверяет, является ли ввод допустимым числом с плавающей точкой.

    Args:
        value: Проверяемое значение

    Returns:
        True, если значение является допустимым числом с плавающей точкой или пустой строкой
    """
    if value == "":
        return True

    # Разрешаем только цифры, одну десятичную точку и минус в начале
    pattern = r'^-?\d*\.?\d*$'
    if re.match(pattern, value):
        try:
            # Проверяем, что это действительно число
            float(value)
            return True
        except ValueError:
            return False

    return False


def format_percent(value):
    """
    Форматирует число как процент.

    Args:
        value: Число для форматирования (от 0 до 1)

    Returns:
        Отформатированная строка вида "0.45 (45%)"
    """
    return f"{value:.2f} ({value * 100:.0f}%)"