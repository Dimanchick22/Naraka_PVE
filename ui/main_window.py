# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Главное окно приложения "Калькулятор урона".
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os

from config import WINDOW_TITLE, WINDOW_SIZE, DEFAULT_HERO_LEVEL
from models.jade import JadeConfig
from models.damage_calculator import DamageCalculatorModel
from ui.main_tab import MainTab
from ui.details_tab import DetailsTab
from ui.theme import apply_theme
from utils.focus_handlers import add_focus_handler


class DamageCalculatorWindow(tk.Tk):
    """Главное окно приложения."""

    def __init__(self):
        """Инициализация главного окна приложения."""
        super().__init__()

        # Настройка окна
        self.title(WINDOW_TITLE)
        self.geometry(WINDOW_SIZE)
        self.resizable(True, True)

        # Установка иконки
        self._set_icon()

        # Применяем современную тему
        self.theme = apply_theme(self)

        # Создаем конфигурации нефритов
        self.jade_configs = []
        for i in range(6):
            self.jade_configs.append(JadeConfig(i))

        # Создаем модель для расчетов
        self.model = DamageCalculatorModel(self.jade_configs)

        # Создаем интерфейс
        self._create_widgets()

    def _set_icon(self):
        """Устанавливает иконку приложения."""
        try:
            icon_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'icon.ico')
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except Exception:
            # Если не удалось установить иконку, просто пропускаем
            pass

    def _create_widgets(self):
        """Создает основные виджеты интерфейса."""
        # Создаем главный контейнер с отступами
        main_container = ttk.Frame(self, padding=self.theme.PADDING)
        main_container.pack(fill=tk.BOTH, expand=True)

        # Добавляем обработчик клика для снятия фокуса
        add_focus_handler(main_container)

        # Создаем notebook (вкладки)
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Добавляем обработчик клика для вкладок
        add_focus_handler(self.notebook)

        # Вкладка основных настроек
        self.main_tab = MainTab(self.notebook, self.model, self.jade_configs, self.theme)
        self.notebook.add(self.main_tab, text="Основные настройки")

        # Вкладка детали расчетов
        self.details_tab = DetailsTab(self.notebook, self.theme)
        self.notebook.add(self.details_tab, text="Детали расчетов")

        # Привязываем обработчик расчета
        self.main_tab.set_calculate_callback(self._on_calculate)

        # Добавляем строку состояния
        self._create_statusbar(main_container)

    def _create_statusbar(self, parent):
        """
        Создает строку состояния в нижней части окна.

        Args:
            parent: Родительский виджет
        """
        statusbar = ttk.Frame(parent, relief=tk.SUNKEN)
        statusbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Создаем специальный стиль для статусбара, чтобы обеспечить читаемость текста
        style = ttk.Style()
        style.configure("Status.TLabel",
                        foreground=self.theme.TEXT_COLOR,
                        background=self.theme.BG_COLOR)

        self.status_var = tk.StringVar(value="Готов к расчетам")
        status_label = ttk.Label(
            statusbar,
            textvariable=self.status_var,
            anchor=tk.W,
            style="Status.TLabel",
            padding=(self.theme.SMALL_PADDING, 2)
        )
        status_label.pack(side=tk.LEFT, fill=tk.X)

        # Версия приложения
        version_label = ttk.Label(
            statusbar,
            text="Версия: 2.0.0",
            anchor=tk.E,
            style="Status.TLabel",
            padding=(self.theme.SMALL_PADDING, 2)
        )
        version_label.pack(side=tk.RIGHT)

    def _on_calculate(self):
        """Обработчик события расчета урона."""
        try:
            # Устанавливаем статус "Расчет..."
            self.status_var.set("Идет расчет...")
            self.update_idletasks()

            # Получаем значение сознания
            consciousness = float(self.main_tab.consciousness_var.get())
            self.model.set_consciousness(consciousness)

            # Получаем уровень героя
            try:
                hero_level = int(self.main_tab.hero_level_var.get())
                self.model.set_hero_level(hero_level)
            except ValueError:
                # Если уровень героя не указан или указан неправильно, используем значение по умолчанию
                self.model.set_hero_level(DEFAULT_HERO_LEVEL)
                self.main_tab.hero_level_var.set(str(DEFAULT_HERO_LEVEL))

            # Получаем базовые параметры
            self.model.set_base_params(
                self.main_tab.untouchable_talent_var.get(),
                self.main_tab.power_var.get(),
                self.main_tab.ice_root_var.get(),
                self.main_tab.ice_flash_var.get()
            )

            # Получаем боевые параметры (включая совпадение уровня сознания)
            self.model.set_combat_params(
                self.main_tab.aroma_aura_var.get(),
                self.main_tab.frost_bloom_var.get(),
                self.main_tab.frost_seal_var.get(),
                self.main_tab.tundra_power_var.get(),
                self.main_tab.frostbound_lotus_var.get(),
                self.main_tab.tessa_f_var.get(),
                self.main_tab.consciousness_match_var.get(),  # Учитываем совпадение уровня сознания
                self.main_tab.jade_active_var.get()  # Этот параметр игнорируется в модели
            )

            # Выполняем расчет
            results = self.model.calculate()

            # Обновляем результаты
            self.main_tab.update_results(results)
            self.details_tab.update_calculation_text(results["calculation_steps"])

            # Обновляем статус
            self.status_var.set(f"Расчет выполнен.")

        except ValueError as e:
            messagebox.showerror("Ошибка", f"Пожалуйста, введите корректные числовые значения: {str(e)}")
            self.status_var.set("Ошибка при расчете. Проверьте введенные данные.")