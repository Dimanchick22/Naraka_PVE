#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Панель настройки нефритов в приложении "Калькулятор урона".
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from typing import List, Dict, Any, Callable

from models.jade import JadeConfig, calculate_jade_bonuses
from config import JADE_STAT_TYPES, FUSION_VALUES
from utils.helpers import format_percent, create_tooltip
from utils.focus_handlers import add_focus_handler
from ui.theme import create_modern_button


class JadePanel(ttk.Frame):
    """Панель для настройки нефритов."""

    def __init__(self, parent, jade_configs: List[JadeConfig], theme):
        """
        Инициализация панели настройки нефритов.

        Args:
            parent: Родительский виджет
            jade_configs: Список конфигураций нефритов
            theme: Тема оформления
        """
        super().__init__(parent)
        self.jade_configs = jade_configs
        self.theme = theme
        self.update_callback = None

        # Переменные для отображения итоговых бонусов - убираем, так как перенесли в блок статов
        # self.jade_attack_bonus_var = tk.StringVar(value="0.00 (0%)")
        # self.jade_ice_blast_bonus_var = tk.StringVar(value="0.00 (0%)")
        # self.jade_other_bonus_var = tk.StringVar(value="Нет")

        self._create_widgets()

    def set_update_callback(self, callback: Callable):
        """
        Устанавливает функцию обратного вызова для обновления статов.

        Args:
            callback: Функция для вызова при изменении нефритов
        """
        self.update_callback = callback

    def _create_widgets(self):
        """Создает виджеты панели настройки нефритов."""
        # Заголовок
        ttk.Label(self, text="Настройка нефритов", style="Title.TLabel").pack(
            fill=tk.X, pady=(0, self.theme.LARGE_PADDING))

        # Контейнер для настройки нефритов и кнопки
        jade_outer_container = ttk.Frame(self)
        jade_outer_container.pack(fill=tk.BOTH, expand=False)

        # Добавляем обработчик клика для снятия фокуса
        add_focus_handler(jade_outer_container)

        # Создаем контейнер для сетки нефритов
        jade_grid_container = ttk.Frame(jade_outer_container)
        jade_grid_container.pack(fill=tk.BOTH, expand=False)

        # Добавляем обработчик клика для снятия фокуса
        add_focus_handler(jade_grid_container)

        # Настраиваем сетку 2x3 для нефритов
        for i in range(2):
            jade_grid_container.rowconfigure(i, weight=1)
        for j in range(3):
            jade_grid_container.columnconfigure(j, weight=1)

        # Создаем и размещаем нефриты в сетке
        for i, jade_config in enumerate(self.jade_configs):
            row = i // 3  # Первые 3 в первой строке, следующие 3 во второй
            col = i % 3  # Распределяем по колонкам (0, 1, 2)

            self._create_jade_config_frame(jade_grid_container, jade_config, row, col)

        # Создаем контейнер для размещения кнопки по центру
        button_container = ttk.Frame(jade_outer_container)
        button_container.pack(fill=tk.X, pady=self.theme.SMALL_PADDING)

        # Кнопка "Применить настройки нефритов" - центрируем её
        apply_button = create_modern_button(
            button_container,
            "Применить настройки нефритов",
            command=self._apply_jade_settings,
            accent=False,
            width=self.theme.BUTTON_WIDTH
        )
        apply_button.pack(pady=self.theme.SMALL_PADDING, anchor=tk.CENTER)

        # Удаляем создание информационной панели с результатами, т.к. перенесли в блок статов

    def _create_jade_config_frame(self, parent, jade_config: JadeConfig, row: int, col: int):
        """
        Создает фрейм для настройки одного нефрита.

        Args:
            parent: Родительский виджет
            jade_config: Конфигурация нефрита
            row: Номер строки
            col: Номер колонки
        """
        # Создаем рамку для нефрита
        jade_frame = ttk.LabelFrame(
            parent,
            text=f"Нефрит {jade_config.index + 1}",
            padding=self.theme.PADDING
        )
        jade_frame.grid(
            row=row,
            column=col,
            sticky=tk.NSEW,
            padx=self.theme.SMALL_PADDING,
            pady=self.theme.SMALL_PADDING
        )

        # Добавляем обработчик клика для снятия фокуса
        add_focus_handler(jade_frame)

        # Устанавливаем минимальный размер
        jade_frame.columnconfigure(0, minsize=100)
        jade_frame.columnconfigure(1, minsize=100)

        # Удаляем чекбокс активации нефрита - теперь нефриты всегда активны

        # Создаем заголовки для столбцов
        ttk.Label(jade_frame, text="Тип стата").grid(
            row=0, column=0, sticky=tk.W, padx=(0, self.theme.SMALL_PADDING))
        ttk.Label(jade_frame, text="Значение (%)").grid(
            row=0, column=1, sticky=tk.W)

        # Добавляем статы
        for i, stat in enumerate(jade_config.stats):
            row_idx = i + 1  # Начинаем с 2-й строки (индекс 1), т.к. чекбокса больше нет

            # Выпадающий список типов статов
            stat_type_combo = ttk.Combobox(
                jade_frame,
                textvariable=stat.type,
                values=JADE_STAT_TYPES,
                width=10,
                state="readonly"
            )
            stat_type_combo.grid(
                row=row_idx,
                column=0,
                pady=self.theme.SMALL_PADDING,
                padx=(0, self.theme.SMALL_PADDING),
                sticky=tk.W
            )

            # Виджеты для ввода значений

            # 1. Entry для обычных статов
            value_entry = ttk.Entry(jade_frame, textvariable=stat.value, width=8)

            # 2. Combobox для слияния
            fusion_combo = ttk.Combobox(
                jade_frame,
                textvariable=stat.value,
                values=FUSION_VALUES,
                width=7,
                state="readonly"
            )

            # 3. Label для "Пусто"
            empty_label = ttk.Label(jade_frame, text="0", width=8)

            # Функция для обновления виджета значения при изменении типа
            def update_value_widget(event=None, stat_obj=stat, entry=value_entry,
                                    combo=fusion_combo, label=empty_label, row_num=row_idx):
                # Удаляем все виджеты
                entry.grid_forget()
                combo.grid_forget()
                label.grid_forget()

                selected_type = stat_obj.type.get()

                # Показываем нужный виджет в зависимости от типа
                if selected_type == "Пусто":
                    stat_obj.value.set("0")
                    label.grid(row=row_num, column=1, pady=self.theme.SMALL_PADDING, sticky=tk.W)
                elif selected_type == "Слияние":
                    if stat_obj.value.get() not in FUSION_VALUES:
                        stat_obj.value.set(FUSION_VALUES[0])
                    combo.grid(row=row_num, column=1, pady=self.theme.SMALL_PADDING, sticky=tk.W)
                else:
                    if stat_obj.value.get() == "0":
                        stat_obj.value.set("")
                    entry.grid(row=row_num, column=1, pady=self.theme.SMALL_PADDING, sticky=tk.W)

                # Убираем фокус, чтобы убрать синее выделение
                jade_frame.focus_set()

                # Вызываем обновление бонусов нефритов при изменении типа
                self._update_jade_bonuses()

            # Привязываем функцию обновления к событию выбора
            stat_type_combo.bind("<<ComboboxSelected>>", update_value_widget)

            # Добавляем отслеживание изменений значения для обновления бонусов
            def update_on_value_change(*args, stat_obj=stat):
                # Проверяем валидность значения
                try:
                    if stat_obj.type.get() != "Пусто" and stat_obj.type.get() != "Слияние":
                        value = stat_obj.value.get()
                        if value:
                            float(value)  # Проверка на числовое значение
                    # Обновляем бонусы нефритов
                    self._update_jade_bonuses()
                except ValueError:
                    pass  # Игнорируем некорректные значения

            # Привязываем отслеживание изменений к переменной значения
            stat.value.trace_add("write", update_on_value_change)

            # Привязываем отслеживание изменений для Combobox слияния
            def update_on_fusion_change(*args, stat_obj=stat):
                if stat_obj.type.get() == "Слияние":
                    self._update_jade_bonuses()

            # Привязываем к событию выбора значения слияния
            fusion_combo.bind("<<ComboboxSelected>>", lambda event, stat_obj=stat:
            self._update_jade_bonuses())

            # Вызываем функцию проверки сразу для инициализации состояния
            update_value_widget()

            # Добавляем подсказки
            if i == 0:
                create_tooltip(stat_type_combo, "Выберите тип стата для этой ячейки")
                create_tooltip(value_entry, "Введите значение стата в процентах")
                create_tooltip(fusion_combo, "Выберите процент слияния")

    def _update_jade_bonuses(self):
        """Обновляет отображение бонусов от нефритов и вызывает callback для обновления блока статов."""
        # Вызываем callback для обновления отображения в блоке статов
        if self.update_callback:
            self.update_callback()

    def _apply_jade_settings(self):
        """Применяет настройки нефритов и обновляет итоговые бонусы."""
        # Обновляем отображение бонусов
        self._update_jade_bonuses()

        # Создаем красивое сообщение для пользователя
        total_bonuses = calculate_jade_bonuses(self.jade_configs)
        message = f"Бонусы от нефритов успешно применены:\n\n"

        # Отображаем все бонусы четко и понятно
        if "Атака" in total_bonuses and total_bonuses["Атака"] > 0:
            message += f"• Атака: +{format_percent(total_bonuses['Атака'])}\n"

        if "Лед. взрыв" in total_bonuses and total_bonuses["Лед. взрыв"] > 0:
            message += f"• % ледяного взрыва: +{format_percent(total_bonuses['Лед. взрыв'])}\n"

        if "Атака по боссу" in total_bonuses and total_bonuses["Атака по боссу"] > 0:
            message += f"• Атака по боссам: +{format_percent(total_bonuses['Атака по боссу'])}\n"

        if "Атака по монстрам" in total_bonuses and total_bonuses["Атака по монстрам"] > 0:
            message += f"• Атака по монстрам: +{format_percent(total_bonuses['Атака по монстрам'])}\n"

        # Проверяем другие возможные бонусы
        other_bonuses = {k: v for k, v in total_bonuses.items()
                         if k not in ["Атака", "Лед. взрыв", "Атака по боссу", "Атака по монстрам"] and v > 0}

        if other_bonuses:
            for stat_type, value in other_bonuses.items():
                message += f"• {stat_type}: +{format_percent(value)}\n"

        if not any(value > 0 for value in total_bonuses.values()):
            message += "• Нет активных бонусов"

        messagebox.showinfo("Настройки применены", message)

        # Убираем фокус с любого активного виджета
        self.focus_set()