#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль для работы с нефритами и их статами в приложении "Калькулятор урона".
"""

import tkinter as tk
from typing import List, Dict, Any, Optional


class JadeStat:
    """Класс для представления одного стата на нефрите."""

    def __init__(self, enabled: bool = True, stat_type: str = "Пусто", value: str = "0"):
        """
        Инициализация стата нефрита.

        Args:
            enabled: Активен ли стат
            stat_type: Тип стата (Атака, Лед. взрыв, Слияние, Пусто, Атака по боссу, Атака по монстрам)
            value: Значение стата в процентах
        """
        self.enabled = tk.BooleanVar(value=enabled)
        self.type = tk.StringVar(value=stat_type)
        self.value = tk.StringVar(value=value)

    def get_value_as_float(self) -> float:
        """
        Получить числовое значение стата.

        Returns:
            Значение стата как число с плавающей точкой
        """
        try:
            return float(self.value.get())
        except ValueError:
            return 0.0

    def is_empty(self) -> bool:
        """
        Проверить, является ли стат пустым.

        Returns:
            True, если стат пустой или не активен
        """
        return not self.enabled.get() or self.type.get() == "Пусто"

    def is_fusion(self) -> bool:
        """
        Проверить, является ли стат слиянием.

        Returns:
            True, если стат является слиянием
        """
        return self.type.get() == "Слияние"

    def get_fusion_multiplier(self) -> float:
        """
        Получить множитель слияния.

        Returns:
            Множитель слияния (0.3, 0.4 или 0.5) или 0, если это не слияние
        """
        if not self.is_fusion():
            return 0.0

        try:
            return float(self.value.get()) / 100.0
        except ValueError:
            return 0.0


class JadeConfig:
    """Класс для представления конфигурации нефрита со статами."""

    def __init__(self, index: int):
        """
        Инициализация конфигурации нефрита.

        Args:
            index: Индекс нефрита (от 0 до 5)
        """
        self.index = index
        # Удаляем переменную enabled, теперь нефриты всегда активны
        self.stats: List[JadeStat] = []

        # Добавляем до 4 возможных статов для нефрита
        for _ in range(4):
            self.stats.append(JadeStat())

    def get_effective_stats(self) -> Dict[str, float]:
        """
        Получить эффективные значения статов с учетом слияний.

        Returns:
            Словарь с типами статов и их значениями с учетом слияний
        """
        # Нефриты теперь всегда активны, поэтому убираем проверку enabled

        # Собираем обычные статы
        base_stats = {}
        fusion_total = 0.0

        for stat in self.stats:
            if stat.is_empty():
                continue

            stat_type = stat.type.get()
            stat_value = stat.get_value_as_float() / 100.0  # Переводим проценты в десятичную дробь

            if stat.is_fusion():
                fusion_total += stat.get_fusion_multiplier()
            else:
                if stat_type in base_stats:
                    base_stats[stat_type] += stat_value
                else:
                    base_stats[stat_type] = stat_value

        # Применяем множитель слияния ко всем статам
        fusion_multiplier = 1.0 + fusion_total
        result = {}

        for stat_type, value in base_stats.items():
            result[stat_type] = value * fusion_multiplier

        return result


def calculate_jade_bonuses(jade_configs: List[JadeConfig]) -> Dict[str, float]:
    """
    Рассчитывает общие бонусы от всех нефритов.

    Args:
        jade_configs: Список конфигураций нефритов

    Returns:
        Словарь с типами бонусов и их значениями
    """
    total_bonuses = {
        "Атака": 0.0,
        "Лед. взрыв": 0.0,
        "Атака по боссу": 0.0,  # Новый тип бонуса
        "Атака по монстрам": 0.0  # Новый тип бонуса
    }
    other_bonuses = {}

    for jade in jade_configs:
        # Удаляем проверку enabled, теперь нефриты всегда активны
        effective_stats = jade.get_effective_stats()

        for stat_type, value in effective_stats.items():
            if stat_type in total_bonuses:
                total_bonuses[stat_type] += value
            else:
                if stat_type in other_bonuses:
                    other_bonuses[stat_type] += value
                else:
                    other_bonuses[stat_type] = value

    # Добавляем другие бонусы в общий результат
    total_bonuses.update(other_bonuses)

    return total_bonuses