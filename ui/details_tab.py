#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Вкладка с деталями расчетов в приложении "Калькулятор урона".
"""
from utils.focus_handlers import add_focus_handler
import tkinter as tk
from tkinter import ttk


class DetailsTab(ttk.Frame):
    """Вкладка с деталями расчетов."""

    def __init__(self, parent, theme):
        """
        Инициализация вкладки с деталями расчетов.

        Args:
            parent: Родительский виджет
            theme: Тема оформления
        """
        super().__init__(parent, padding=theme.PADDING)
        self.theme = theme
        self._create_widgets()

    def _create_widgets(self):
        """Создает виджеты для вкладки."""
        # Заголовок
        title_label = ttk.Label(self, text="Детали расчетов урона", style="Title.TLabel")
        title_label.pack(fill=tk.X, pady=(0, self.theme.LARGE_PADDING))

        # Контейнер для расчетов
        details_container = ttk.Frame(self)
        details_container.pack(fill=tk.BOTH, expand=True)

        # Добавляем обработчик клика для снятия фокуса
        add_focus_handler(details_container)

        # Фрейм для отображения расчетов
        calculations_frame = ttk.LabelFrame(
            details_container,
            text="Подробный расчет",
            padding=self.theme.PADDING
        )
        calculations_frame.pack(fill=tk.BOTH, expand=True, padx=self.theme.PADDING, pady=self.theme.PADDING)

        # Добавляем обработчик клика для снятия фокуса
        add_focus_handler(calculations_frame)

        # Создаем текстовое поле с улучшенным форматированием
        self.calculations_text = tk.Text(
            calculations_frame,
            width=80,
            height=40,
            wrap=tk.WORD,
            bg="white",
            fg=self.theme.TEXT_COLOR,
            font=("Consolas", self.theme.NORMAL_FONT_SIZE),
            padx=self.theme.PADDING,
            pady=self.theme.PADDING,
            border=1,
            relief=tk.SOLID
        )

        # Настраиваем теги для форматирования текста
        self.calculations_text.tag_configure("heading",
                                             font=("Consolas", self.theme.NORMAL_FONT_SIZE, "bold"),
                                             foreground=self.theme.PRIMARY_COLOR)
        self.calculations_text.tag_configure("subheading",
                                             font=("Consolas", self.theme.NORMAL_FONT_SIZE, "bold"),
                                             foreground=self.theme.SECONDARY_COLOR)
        self.calculations_text.tag_configure("formula",
                                             font=("Consolas", self.theme.NORMAL_FONT_SIZE, "italic"))
        self.calculations_text.tag_configure("result",
                                             font=("Consolas", self.theme.NORMAL_FONT_SIZE, "bold"),
                                             foreground=self.theme.ACCENT_COLOR)

        # Создаем и настраиваем скролбар
        scrollbar_frame = ttk.Frame(calculations_frame)
        scrollbar_frame.pack(side=tk.RIGHT, fill=tk.Y)

        scrollbar = ttk.Scrollbar(scrollbar_frame, command=self.calculations_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.calculations_text.configure(yscrollcommand=scrollbar.set)
        self.calculations_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Запрещаем редактирование текста
        self.calculations_text.config(state=tk.DISABLED)

        # Добавляем инструкции
        self._add_instructions()

    def _add_instructions(self):
        """Добавляет инструкции по использованию вкладки."""
        # Разрешаем редактирование для вставки текста
        self.calculations_text.config(state=tk.NORMAL)

        # Очищаем текстовое поле
        self.calculations_text.delete("1.0", tk.END)

        # Добавляем инструкции
        self.calculations_text.insert(tk.END, "ДЕТАЛИ РАСЧЁТА УРОНА\n\n", "heading")
        self.calculations_text.insert(tk.END,
                                      "Эта вкладка показывает подробный расчет урона с учетом всех параметров.\n\n",
                                      "subheading")
        self.calculations_text.insert(tk.END,
                                      "Для выполнения расчета:\n"
                                      "1. Настройте параметры на вкладке \"Основные настройки\"\n"
                                      "2. Настройте нефриты, если они используются\n"
                                      "3. Нажмите кнопку \"Рассчитать урон\"\n\n")
        self.calculations_text.insert(tk.END,
                                      "После этого здесь будут отображены подробные шаги всех выполненных расчетов.\n\n")
        self.calculations_text.insert(tk.END,
                                      "Вы увидите:\n"
                                      "• Базовые параметры и их влияние на урон\n"
                                      "• Боевые бонусы и коэффициенты\n"
                                      "• Подробные вычисления для различных типов урона\n"
                                      "• Расчет для нефритов, если они активированы\n\n")
        self.calculations_text.insert(tk.END,
                                      "Результаты выполненных расчетов помогут вам понять, "
                                      "как разные параметры влияют на итоговый урон.\n")

        # Снова запрещаем редактирование
        self.calculations_text.config(state=tk.DISABLED)

    def update_calculation_text(self, text):
        """
        Обновляет текст с деталями расчетов с форматированием.

        Args:
            text: Текст с деталями расчетов
        """
        # Разрешаем редактирование для вставки текста
        self.calculations_text.config(state=tk.NORMAL)

        # Очищаем текст
        self.calculations_text.delete("1.0", tk.END)

        # Добавляем форматированный текст
        lines = text.split('\n')
        for line in lines:
            if line.isupper() and ":" in line:  # Заголовки
                self.calculations_text.insert(tk.END, line + "\n", "heading")
            elif "Формула" in line or ":" in line and not line.startswith(' '):  # Подзаголовки
                self.calculations_text.insert(tk.END, line + "\n", "subheading")
            elif "=" in line and not line.startswith(' '):  # Формулы
                self.calculations_text.insert(tk.END, line + "\n", "formula")
            elif "Итоговый" in line or "Суммарный" in line:  # Результаты
                self.calculations_text.insert(tk.END, line + "\n", "result")
            else:
                self.calculations_text.insert(tk.END, line + "\n")

        # Снова запрещаем редактирование
        self.calculations_text.config(state=tk.DISABLED)

        # Прокручиваем к началу
        self.calculations_text.see("1.0")