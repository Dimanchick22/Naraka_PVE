#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Вкладка основных настроек в приложении "Калькулятор урона".
"""

import tkinter as tk
from tkinter import ttk
from typing import List, Dict, Any, Callable, Optional

from models.damage_calculator import DamageCalculatorModel
from models.jade import JadeConfig, calculate_jade_bonuses
from ui.jade_panel import JadePanel
from config import DEFAULT_CONSCIOUSNESS, DEFAULT_HERO_LEVEL, HERO_LEVEL_ATTACK_BONUS
from utils.helpers import validate_float_input
from utils.focus_handlers import add_focus_handler
from ui.theme import create_modern_button

class MainTab(ttk.Frame):
    """Вкладка основных настроек."""

    def __init__(self, parent, model: DamageCalculatorModel, jade_configs: List[JadeConfig], theme):
        """
        Инициализация вкладки основных настроек.

        Args:
            parent: Родительский виджет
            model: Модель расчета урона
            jade_configs: Список конфигураций нефритов
            theme: Тема оформления
        """
        super().__init__(parent, padding=theme.PADDING)
        self.model = model
        self.jade_configs = jade_configs
        self.theme = theme
        self.calculate_callback = None

        # Импортируем нужные модули
        from models.jade import calculate_jade_bonuses

        # Создаем переменные для элементов управления
        self._init_variables()

        # Создаем виджеты
        self._create_widgets()

    def _init_variables(self):
        """Инициализирует переменные для элементов управления."""
        # Сознание
        self.consciousness_var = tk.StringVar(value=str(DEFAULT_CONSCIOUSNESS))

        # Уровень героя
        self.hero_level_var = tk.StringVar(value=str(DEFAULT_HERO_LEVEL))

        # Нефрит с тремя взрывами теперь всегда активен
        self.jade_active_var = tk.BooleanVar(value=True)  # Всегда True

        # Базовые параметры (удалён атака_per_level)
        self.untouchable_talent_var = tk.BooleanVar(value=False)
        self.power_var = tk.BooleanVar(value=False)
        self.ice_root_var = tk.BooleanVar(value=False)
        self.ice_flash_var = tk.BooleanVar(value=False)

        # Боевые параметры
        self.aroma_aura_var = tk.BooleanVar(value=False)
        self.frost_bloom_var = tk.BooleanVar(value=False)
        self.frost_seal_var = tk.BooleanVar(value=False)
        self.tundra_power_var = tk.BooleanVar(value=False)
        self.frostbound_lotus_var = tk.BooleanVar(value=False)
        self.tessa_f_var = tk.BooleanVar(value=False)
        self.consciousness_match_var = tk.BooleanVar(value=False)  # Новый параметр: совпадение уровня сознания

        # Результаты расчетов базовых статов
        self.base_attack_result_var = tk.StringVar(value="0.00")
        self.base_ice_blast_result_var = tk.StringVar(value="0.00 (0%)")
        self.final_attack_result_var = tk.StringVar(value="0.00")
        self.final_ice_blast_result_var = tk.StringVar(value="0.00 (0%)")

        # Физический урон
        self.physical_damage_var = tk.StringVar(value="0.00")

        # Бонусы по боссам
        self.boss_attack_bonus_var = tk.StringVar(value="0.00 (0%)")
        self.boss_ice_blast_percent_var = tk.StringVar(value="0.00 (0%)")

        # Урон по боссам
        self.boss_damage_var = tk.StringVar(value="0.00")
        self.boss_flower_damage_var = tk.StringVar(value="0.00")

        # Результаты для нефрита с 3 взрывами по боссам
        self.jade_first_blast_boss_var = tk.StringVar(value="0")
        self.jade_second_blast_boss_var = tk.StringVar(value="0")
        self.jade_third_blast_boss_var = tk.StringVar(value="0")
        self.jade_total_damage_boss_var = tk.StringVar(value="0")

        # Бонусы по монстрам
        self.monster_attack_bonus_var = tk.StringVar(value="0.00 (0%)")
        self.monster_ice_blast_percent_var = tk.StringVar(value="0.00 (0%)")

        # Урон по монстрам
        self.monster_damage_var = tk.StringVar(value="0.00")
        self.monster_flower_damage_var = tk.StringVar(value="0.00")

        # Результаты для нефрита с 3 взрывами по монстрам
        self.jade_first_blast_monster_var = tk.StringVar(value="0")
        self.jade_second_blast_monster_var = tk.StringVar(value="0")
        self.jade_third_blast_monster_var = tk.StringVar(value="0")
        self.jade_total_damage_monster_var = tk.StringVar(value="0")

    def set_calculate_callback(self, callback: Callable):
        """
        Устанавливает функцию обратного вызова для расчета урона.

        Args:
            callback: Функция для вызова при расчете урона
        """
        self.calculate_callback = callback

    def _create_widgets(self):
        """Создает виджеты вкладки."""
        # Создаем основную рамку
        frame_container = ttk.Frame(self)
        frame_container.pack(fill=tk.BOTH, expand=True)

        # Добавляем обработчик клика для снятия фокуса
        add_focus_handler(frame_container)

        # Создаем контейнер для левой и правой панелей с фиксированными размерами
        panels_container = ttk.Frame(frame_container)
        panels_container.pack(fill=tk.BOTH, expand=True)

        # Настраиваем сетку для левой и правой панелей
        panels_container.columnconfigure(0, weight=3)  # Левая панель (больше пространства)
        panels_container.columnconfigure(1, weight=2)  # Правая панель (нефриты)

        # Левая панель для ввода
        left_panel = ttk.Frame(panels_container, padding=self.theme.PADDING)
        left_panel.grid(row=0, column=0, sticky="nsew")

        # Добавляем обработчик клика для снятия фокуса
        add_focus_handler(left_panel)

        # Правая панель для настройки нефритов
        right_panel = ttk.Frame(panels_container, padding=self.theme.PADDING)
        right_panel.grid(row=0, column=1, sticky="nsew")

        # Добавляем обработчик клика для снятия фокуса
        add_focus_handler(right_panel)

        # Создаем левую панель
        self._create_left_panel(left_panel)

        # Создаем правую панель с настройками нефритов
        self._create_right_panel(right_panel)

    def _create_left_panel(self, parent):
        """
        Создает левую панель с основными настройками.

        Args:
            parent: Родительский виджет
        """
        # Определяем уменьшенные отступы для компактного отображения
        compact_padding = max(3, self.theme.PADDING // 2)
        # Заголовок
        title_label = ttk.Label(parent, text="Калькулятор урона", style="Title.TLabel")
        title_label.pack(fill=tk.X, pady=(0, self.theme.LARGE_PADDING))

        # Создаем контейнер для параметров и статов в одном ряду
        horizontal_container = ttk.Frame(parent)
        horizontal_container.pack(fill=tk.BOTH, expand=True)

        # Панель с вводом данных и параметрами (слева)
        params_panel = ttk.Frame(horizontal_container, padding=self.theme.PADDING)
        params_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, self.theme.PADDING))

        # Устанавливаем фиксированную ширину для панели параметров
        params_panel.config(width=250)

        # Создаем рамку для основных параметров
        input_frame = ttk.Frame(params_panel, padding=self.theme.PADDING)
        input_frame.pack(fill=tk.X, expand=False)

        # Сознание
        consciousness_frame = ttk.Frame(input_frame)
        consciousness_frame.pack(fill=tk.X, pady=self.theme.SMALL_PADDING)

        ttk.Label(consciousness_frame, text="Сознание:").pack(side=tk.LEFT)

        # Создаем валидацию для ввода чисел
        validate_cmd = (self.register(validate_float_input), '%P')

        consciousness_entry = ttk.Entry(
            consciousness_frame,
            textvariable=self.consciousness_var,
            width=self.theme.ENTRY_WIDTH,
            validate="key",
            validatecommand=validate_cmd
        )
        consciousness_entry.pack(side=tk.RIGHT, padx=self.theme.SMALL_PADDING)

        # Уровень героя (новое поле)
        hero_level_frame = ttk.Frame(input_frame)
        hero_level_frame.pack(fill=tk.X, pady=self.theme.SMALL_PADDING)

        ttk.Label(hero_level_frame, text="Уровень героя:").pack(side=tk.LEFT)

        # Валидация для ввода целых чисел
        validate_int_cmd = (self.register(lambda P: P == "" or P.isdigit()), '%P')

        hero_level_entry = ttk.Entry(
            hero_level_frame,
            textvariable=self.hero_level_var,
            width=self.theme.ENTRY_WIDTH,
            validate="key",
            validatecommand=validate_int_cmd
        )
        hero_level_entry.pack(side=tk.RIGHT, padx=self.theme.SMALL_PADDING)

        # Показываем текущий бонус от уровня героя

        # Переменная для отображения бонуса от уровня
        self.level_bonus_var = tk.StringVar(value="0.00 (0%)")

        # Обновляем бонус при изменении уровня героя
        def update_level_bonus(*args):
            try:
                level = int(self.hero_level_var.get())
                bonus = 0.0
                for lvl, val in sorted(HERO_LEVEL_ATTACK_BONUS.items()):
                    if level >= lvl:
                        bonus += val
                self.level_bonus_var.set(f"{bonus:.2f} ({bonus * 100:.0f}%)")
            except ValueError:
                self.level_bonus_var.set("0.00 (0%)")

        self.hero_level_var.trace_add("write", update_level_bonus)

        # Вызываем функцию сразу для инициализации
        update_level_bonus()

        # Базовые параметры
        base_frame = ttk.LabelFrame(
            params_panel,
            text="Базовые параметры",
            padding=self.theme.PADDING
        )
        base_frame.pack(fill=tk.X, pady=self.theme.PADDING, padx=0)

        # Создаем чекбоксы для базовых параметров
        self._create_parameter_checkbox(base_frame, "Талант неприкосновенности", self.untouchable_talent_var)
        self._create_parameter_checkbox(base_frame, "Мощь", self.power_var)
        self._create_parameter_checkbox(base_frame, "Ледяной корень", self.ice_root_var)
        self._create_parameter_checkbox(base_frame, "Ледяная вспышка", self.ice_flash_var)

        # Боевые параметры
        combat_frame = ttk.LabelFrame(
            params_panel,
            text="Боевые параметры (активируются в бою)",
            padding=self.theme.PADDING
        )
        combat_frame.pack(fill=tk.X, pady=self.theme.PADDING, padx=0)

        # Создаем чекбоксы для боевых параметров
        self._create_parameter_checkbox(combat_frame, "Аура Аромата", self.aroma_aura_var)
        self._create_parameter_checkbox(combat_frame, "Морозное цветение", self.frost_bloom_var)
        self._create_parameter_checkbox(combat_frame, "Морозная печать", self.frost_seal_var)
        self._create_parameter_checkbox(combat_frame, "Мощь тундры", self.tundra_power_var)
        self._create_parameter_checkbox(combat_frame, "Морозный лотос", self.frostbound_lotus_var)
        self._create_parameter_checkbox(combat_frame, "F тессы", self.tessa_f_var)
        # Добавляем чекбокс для совпадения уровня сознания
        self._create_parameter_checkbox(combat_frame, "Уровень сознания совпадает", self.consciousness_match_var)

        # Статы панель (справа от параметров)
        stats_panel = ttk.Frame(horizontal_container, padding=self.theme.PADDING)
        stats_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Создаем блок статов
        stats_frame = ttk.LabelFrame(
            stats_panel,
            text="Статы",
            padding=compact_padding,
            style="Result.TLabelframe"
        )
        stats_frame.pack(fill=tk.BOTH, expand=True)

        # Обычные статы
        ttk.Label(stats_frame, text="Обычные:", style="Result.TLabel").grid(
            row=0, column=0, sticky=tk.W, pady=2, columnspan=2)

        ttk.Label(stats_frame, text="Атака:", style="Result.TLabel").grid(
            row=1, column=0, sticky=tk.W, pady=2, padx=(10, 0))
        ttk.Label(stats_frame, textvariable=self.base_attack_result_var,
                  style="ResultValue.TLabel").grid(row=1, column=1, pady=2)

        ttk.Label(stats_frame, text="% лед. взрыва:", style="Result.TLabel").grid(
            row=2, column=0, sticky=tk.W, pady=2, padx=(10, 0))
        ttk.Label(stats_frame, textvariable=self.base_ice_blast_result_var,
                  style="ResultValue.TLabel").grid(row=2, column=1, pady=2)

        # Боевые статы
        ttk.Label(stats_frame, text="Боевые:", style="Result.TLabel").grid(
            row=3, column=0, sticky=tk.W, pady=2, columnspan=2)

        ttk.Label(stats_frame, text="Атака:", style="Result.TLabel").grid(
            row=4, column=0, sticky=tk.W, pady=2, padx=(10, 0))
        ttk.Label(stats_frame, textvariable=self.final_attack_result_var,
                  style="ResultValue.TLabel").grid(row=4, column=1, pady=2)

        ttk.Label(stats_frame, text="% лед. взрыва:", style="Result.TLabel").grid(
            row=5, column=0, sticky=tk.W, pady=2, padx=(10, 0))
        ttk.Label(stats_frame, textvariable=self.final_ice_blast_result_var,
                  style="ResultValue.TLabel").grid(row=5, column=1, pady=2)

        ttk.Label(stats_frame, text="Физический урон:", style="Result.TLabel").grid(
            row=6, column=0, sticky=tk.W, pady=2, padx=(10, 0))
        ttk.Label(stats_frame, textvariable=self.physical_damage_var,
                  style="ResultValue.TLabel").grid(row=6, column=1, pady=2)

        # # Бонусы от нефритов (добавляем в блок статов)
        # ttk.Label(stats_frame, text="Бонусы от нефритов:", style="Result.TLabel").grid(
        #     row=7, column=0, sticky=tk.W, pady=(10, 2), columnspan=2)
        #
        # ttk.Label(stats_frame, text="Бонус атаки:", style="Result.TLabel").grid(
        #     row=8, column=0, sticky=tk.W, pady=2, padx=(10, 0))
        # # Создаем переменную для бонуса атаки от нефритов
        # self.jade_attack_bonus_display = tk.StringVar(value="0.00 (0%)")
        # ttk.Label(stats_frame, textvariable=self.jade_attack_bonus_display,
        #           style="ResultValue.TLabel").grid(row=8, column=1, pady=2)
        #
        # ttk.Label(stats_frame, text="Бонус % лед. взрыва:", style="Result.TLabel").grid(
        #     row=9, column=0, sticky=tk.W, pady=2, padx=(10, 0))
        # # Создаем переменную для бонуса лед. взрыва от нефритов
        # self.jade_ice_blast_bonus_display = tk.StringVar(value="0.00 (0%)")
        # ttk.Label(stats_frame, textvariable=self.jade_ice_blast_bonus_display,
        #           style="ResultValue.TLabel").grid(row=9, column=1, pady=2)
        #
        # ttk.Label(stats_frame, text="Бонус атаки по боссам:", style="Result.TLabel").grid(
        #     row=10, column=0, sticky=tk.W, pady=2, padx=(10, 0))
        # # Создаем переменную для бонуса атаки по боссам от нефритов
        # self.jade_boss_attack_bonus_display = tk.StringVar(value="0.00 (0%)")
        # ttk.Label(stats_frame, textvariable=self.jade_boss_attack_bonus_display,
        #           style="ResultValue.TLabel").grid(row=10, column=1, pady=2)
        #
        # ttk.Label(stats_frame, text="Бонус атаки по монстрам:", style="Result.TLabel").grid(
        #     row=11, column=0, sticky=tk.W, pady=2, padx=(10, 0))
        # # Создаем переменную для бонуса атаки по монстрам от нефритов
        # self.jade_monster_attack_bonus_display = tk.StringVar(value="0.00 (0%)")
        # ttk.Label(stats_frame, textvariable=self.jade_monster_attack_bonus_display,
        #           style="ResultValue.TLabel").grid(row=11, column=1, pady=2)

        # Кнопка расчета (с акцентным стилем) по центру внизу
        calculate_button = create_modern_button(
            parent,
            "Рассчитать урон",
            command=self._on_calculate,
            accent=True,
            width=self.theme.BUTTON_WIDTH
        )
        calculate_button.pack(pady=self.theme.LARGE_PADDING)

        # Фрейм с результатами
        self._create_results_frame(parent)

    def _create_parameter_checkbox(self, parent, text, variable):
        """
        Создает чекбокс для параметра с улучшенным стилем.

        Args:
            parent: Родительский виджет
            text: Текст чекбокса
            variable: Переменная для хранения состояния
        """
        checkbox_frame = ttk.Frame(parent)
        checkbox_frame.pack(fill=tk.X, pady=2)

        checkbox = ttk.Checkbutton(
            checkbox_frame,
            text=text,
            variable=variable
        )
        checkbox.pack(side=tk.LEFT, padx=5)

    def _create_results_frame(self, parent):
        """
        Создает реорганизованный фрейм с результатами расчетов.

        Args:
            parent: Родительский виджет
        """
        # Уменьшаем отступы в рамках
        compact_padding = max(3, self.theme.PADDING // 2)
        small_horizontal_padding = max(2, self.theme.SMALL_PADDING // 2)

        results_wrapper = ttk.Frame(parent)
        results_wrapper.pack(fill=tk.X, expand=True)

        # Создаем контейнер для результатов
        results_container = ttk.Frame(results_wrapper)
        results_container.pack(fill=tk.X, expand=True)

        # Настраиваем сетку для 3 колонок
        results_container.columnconfigure(0, minsize=200, weight=1)
        results_container.columnconfigure(1, minsize=200, weight=1)
        results_container.columnconfigure(2, minsize=200, weight=1)

        # ВТОРОЙ РЯД - урон по боссам (мы удалили первый ряд, т.к. вынесли статы отдельно)

        # 1. Блок "Урон по боссам"
        boss_damage_frame = ttk.LabelFrame(
            results_container,
            text="Урон по боссам",
            padding=compact_padding,
            style="Result.TLabelframe"
        )
        boss_damage_frame.grid(row=0, column=0, columnspan=3, sticky=tk.NSEW, pady=(0, self.theme.PADDING))

        # Настраиваем сетку для отображения результатов урона по боссам
        boss_damage_frame.columnconfigure(0, weight=1)
        boss_damage_frame.columnconfigure(1, weight=1)
        boss_damage_frame.columnconfigure(2, weight=1)
        boss_damage_frame.columnconfigure(3, weight=1)

        # Бонусы по боссам
        ttk.Label(boss_damage_frame, text="Бонус атаки:", style="Result.TLabel").grid(
            row=0, column=0, sticky=tk.W, pady=2, padx=(10, 0))
        ttk.Label(boss_damage_frame, textvariable=self.boss_attack_bonus_var,
                  style="ResultValue.TLabel").grid(row=0, column=1, pady=2)

        ttk.Label(boss_damage_frame, text="% лед. взрыва:", style="Result.TLabel").grid(
            row=0, column=2, sticky=tk.W, pady=2, padx=(10, 0))
        ttk.Label(boss_damage_frame, textvariable=self.boss_ice_blast_percent_var,
                  style="ResultValue.TLabel").grid(row=0, column=3, pady=2)

        # Урон по боссам
        ttk.Label(boss_damage_frame, text="Урон лед. взрыва:", style="Result.TLabel").grid(
            row=2, column=2, sticky=tk.W, pady=2, padx=(10, 0))
        ttk.Label(boss_damage_frame, textvariable=self.boss_damage_var,
                  style="ResultValue.TLabel").grid(row=2, column=3, pady=2)

        ttk.Label(boss_damage_frame, text="Урон цветочного взрыва:", style="Result.TLabel").grid(
            row=1, column=2, sticky=tk.W, pady=2, padx=(10, 0))
        ttk.Label(boss_damage_frame, textvariable=self.boss_flower_damage_var,
                  style="ResultValue.TLabel").grid(row=1, column=3, pady=2)

        # Нефрит x3 по боссам
        ttk.Label(boss_damage_frame, text="Первый взрыв:", style="Result.TLabel").grid(
            row=1, column=0, sticky=tk.W, pady=2, padx=(10, 0))
        ttk.Label(boss_damage_frame, textvariable=self.jade_first_blast_boss_var,
                  style="ResultValue.TLabel").grid(row=1, column=1, pady=2)

        ttk.Label(boss_damage_frame, text="Второй взрыв:", style="Result.TLabel").grid(
            row=2, column=0, sticky=tk.W, pady=2, padx=(10, 0))
        ttk.Label(boss_damage_frame, textvariable=self.jade_second_blast_boss_var,
                  style="ResultValue.TLabel").grid(row=2, column=1, pady=2)

        ttk.Label(boss_damage_frame, text="Третий взрыв:", style="Result.TLabel").grid(
            row=3, column=0, sticky=tk.W, pady=2, padx=(10, 0))
        ttk.Label(boss_damage_frame, textvariable=self.jade_third_blast_boss_var,
                  style="ResultValue.TLabel").grid(row=3, column=1, pady=2)

        ttk.Label(boss_damage_frame, text="Суммарно x3 взрыв:", style="Result.TLabel").grid(
            row=3, column=2, sticky=tk.W, pady=2, padx=(10, 0))
        ttk.Label(boss_damage_frame, textvariable=self.jade_total_damage_boss_var,
                  style="ResultValue.TLabel").grid(row=3, column=3, pady=2)

        # ТРЕТИЙ РЯД - урон по монстрам

        # 1. Блок "Урон по монстрам"
        monster_damage_frame = ttk.LabelFrame(
            results_container,
            text="Урон по обычным монстрам",
            padding=compact_padding,
            style="Result.TLabelframe"
        )
        monster_damage_frame.grid(row=1, column=0, columnspan=3, sticky=tk.NSEW)

        # Настраиваем сетку для отображения результатов урона по монстрам
        monster_damage_frame.columnconfigure(0, weight=1)
        monster_damage_frame.columnconfigure(1, weight=1)
        monster_damage_frame.columnconfigure(2, weight=1)
        monster_damage_frame.columnconfigure(3, weight=1)

        # Бонусы по монстрам
        ttk.Label(monster_damage_frame, text="Бонус атаки:", style="Result.TLabel").grid(
            row=0, column=0, sticky=tk.W, pady=2, padx=(10, 0))
        ttk.Label(monster_damage_frame, textvariable=self.monster_attack_bonus_var,
                  style="ResultValue.TLabel").grid(row=0, column=1, pady=2)

        ttk.Label(monster_damage_frame, text="% лед. взрыва:", style="Result.TLabel").grid(
            row=0, column=2, sticky=tk.W, pady=2, padx=(10, 0))
        ttk.Label(monster_damage_frame, textvariable=self.monster_ice_blast_percent_var,
                  style="ResultValue.TLabel").grid(row=0, column=3, pady=2)

        # Урон по монстрам
        ttk.Label(monster_damage_frame, text="Урон лед. взрыва:", style="Result.TLabel").grid(
            row=2, column=2, sticky=tk.W, pady=2, padx=(10, 0))
        ttk.Label(monster_damage_frame, textvariable=self.monster_damage_var,
                  style="ResultValue.TLabel").grid(row=2, column=3, pady=2)

        ttk.Label(monster_damage_frame, text="Урон цветочного взрыва:", style="Result.TLabel").grid(
            row=1, column=2, sticky=tk.W, pady=2, padx=(10, 0))
        ttk.Label(monster_damage_frame, textvariable=self.monster_flower_damage_var,
                  style="ResultValue.TLabel").grid(row=1, column=3, pady=2)

        # Нефрит x3 по монстрам
        ttk.Label(monster_damage_frame, text="Первый взрыв:", style="Result.TLabel").grid(
            row=1, column=0, sticky=tk.W, pady=2, padx=(10, 0))
        ttk.Label(monster_damage_frame, textvariable=self.jade_first_blast_monster_var,
                  style="ResultValue.TLabel").grid(row=1, column=1, pady=2)

        ttk.Label(monster_damage_frame, text="Второй взрыв:", style="Result.TLabel").grid(
            row=2, column=0, sticky=tk.W, pady=2, padx=(10, 0))
        ttk.Label(monster_damage_frame, textvariable=self.jade_second_blast_monster_var,
                  style="ResultValue.TLabel").grid(row=2, column=1, pady=2)

        ttk.Label(monster_damage_frame, text="Третий взрыв:", style="Result.TLabel").grid(
            row=3, column=0, sticky=tk.W, pady=2, padx=(10, 0))
        ttk.Label(monster_damage_frame, textvariable=self.jade_third_blast_monster_var,
                  style="ResultValue.TLabel").grid(row=3, column=1, pady=2)

        ttk.Label(monster_damage_frame, text="Суммарно x3 взрыв:", style="Result.TLabel").grid(
            row=3, column=2, sticky=tk.W, pady=2, padx=(10, 0))
        ttk.Label(monster_damage_frame, textvariable=self.jade_total_damage_monster_var,
                  style="ResultValue.TLabel").grid(row=3, column=3, pady=2)

    def _create_right_panel(self, parent):
        """
        Создает правую панель с настройками нефритов.

        Args:
            parent: Родительский виджет
        """
        # Создаем панель настройки нефритов
        jade_panel = JadePanel(parent, self.jade_configs, self.theme)
        jade_panel.pack(fill=tk.BOTH, expand=True)

    def _on_calculate(self):
        """Обработчик события нажатия на кнопку расчета урона."""
        if self.calculate_callback:
            self.calculate_callback()

    def update_results(self, results: Dict[str, Any]):
        """
        Обновляет результаты расчетов.

        Args:
            results: Словарь с результатами расчетов
        """
        # Обновляем базовые результаты
        self.base_attack_result_var.set(f"{results['base_attack']:.2f}")

        # Отображение без базовых 100%
        base_ice_blast_bonus = results['base_ice_blast_percent'] - 1.0
        self.base_ice_blast_result_var.set(
            f"{base_ice_blast_bonus:.2f} ({base_ice_blast_bonus * 100:.0f}%)")

        # Обновляем боевые результаты
        self.final_attack_result_var.set(f"{results['final_attack']:.2f}")

        # Боевой % ледяного взрыва остается с базой в 100%
        self.final_ice_blast_result_var.set(
            f"{results['final_ice_blast_percent']:.2f} ({results['final_ice_blast_percent'] * 100:.0f}%)")

        # Обновляем физический урон
        self.physical_damage_var.set(f"{results['physical_damage']:.2f}")

        # Обновляем бонусы по боссам
        self.boss_attack_bonus_var.set(
            f"{results['boss_attack_bonus']:.2f} ({results['boss_attack_bonus'] * 100:.0f}%)")
        self.boss_ice_blast_percent_var.set(
            f"{results['boss_ice_blast_percent']:.2f} ({results['boss_ice_blast_percent'] * 100:.0f}%)")

        # Обновляем урон по боссам
        self.boss_damage_var.set(f"{results['boss_damage']:.2f}")
        self.boss_flower_damage_var.set(f"{results['boss_flower_damage']:.2f}")

        # Обновляем результаты по нефриту (x3 взрыв) для боссов
        self.jade_first_blast_boss_var.set(f"{results['jade_first_blast_boss']}")
        self.jade_second_blast_boss_var.set(f"{results['jade_second_blast_boss']}")
        self.jade_third_blast_boss_var.set(f"{results['jade_third_blast_boss']}")
        self.jade_total_damage_boss_var.set(f"{results['jade_total_damage_boss']}")

        # Обновляем бонусы по монстрам
        self.monster_attack_bonus_var.set(
            f"{results['monster_attack_bonus']:.2f} ({results['monster_attack_bonus'] * 100:.0f}%)")
        self.monster_ice_blast_percent_var.set(
            f"{results['monster_ice_blast_percent']:.2f} ({results['monster_ice_blast_percent'] * 100:.0f}%)")

        # Обновляем урон по монстрам
        self.monster_damage_var.set(f"{results['monster_damage']:.2f}")
        self.monster_flower_damage_var.set(f"{results['monster_flower_damage']:.2f}")

        # Обновляем результаты по нефриту (x3 взрыв) для монстров
        self.jade_first_blast_monster_var.set(f"{results['jade_first_blast_monster']}")
        self.jade_second_blast_monster_var.set(f"{results['jade_second_blast_monster']}")
        self.jade_third_blast_monster_var.set(f"{results['jade_third_blast_monster']}")
        self.jade_total_damage_monster_var.set(f"{results['jade_total_damage_monster']}")