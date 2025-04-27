#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модель для расчета урона в приложении "Калькулятор урона".
Содержит всю логику расчета параметров и урона.
"""

import tkinter as tk
from typing import List, Dict, Any, Optional, Tuple

from config import (
    BASE_ATTACK, EXPLOSION_COEF, FLOWER_EXPLOSION_COEF,
    JADE_FIRST_BLAST_MULTIPLIER, JADE_OTHER_BLAST_MULTIPLIER,
    TALENT_VALUES, DEFAULT_HERO_LEVEL, HERO_LEVEL_ATTACK_BONUS
)
from models.jade import JadeConfig, calculate_jade_bonuses


class DamageCalculatorModel:
    """Класс для расчета урона и показателей персонажа."""

    def __init__(self, jade_configs: List[JadeConfig]):
        """
        Инициализация модели расчета урона.

        Args:
            jade_configs: Список конфигураций нефритов
        """
        self.consciousness = 0.0
        self.hero_level = DEFAULT_HERO_LEVEL  # Добавляем уровень героя
        self.jade_configs = jade_configs
        self.jade_active = True  # Нефрит с тремя взрывами теперь всегда активен

        # Базовые параметры
        self.untouchable_talent = False
        self.power = False
        self.ice_root = False
        self.ice_flash = False

        # Боевые параметры
        self.aroma_aura = False
        self.frost_bloom = False
        self.frost_seal = False
        self.tundra_power = False
        self.frostbound_lotus = False
        self.tessa_f = False
        self.consciousness_match = False  # Новый параметр: совпадение уровня сознания

        # Расчетные значения
        self.base_attack = 0.0
        self.base_ice_blast_percent = 0.0
        self.final_attack = 0.0
        self.final_ice_blast_percent = 0.0

        # Физический урон
        self.physical_damage = 0.0

        # Новые расчетные значения для боссов
        self.boss_attack_bonus = 0.0
        self.boss_ice_blast_percent = 0.0
        self.boss_damage = 0.0
        self.boss_flower_damage = 0.0

        # Новые расчетные значения для обычных монстров
        self.monster_attack_bonus = 0.0
        self.monster_ice_blast_percent = 0.0
        self.monster_damage = 0.0
        self.monster_flower_damage = 0.0

        # Значения для нефрита с 3 взрывами (для боссов и монстров)
        self.jade_first_blast_boss = 0
        self.jade_second_blast_boss = 0
        self.jade_third_blast_boss = 0
        self.jade_total_damage_boss = 0

        self.jade_first_blast_monster = 0
        self.jade_second_blast_monster = 0
        self.jade_third_blast_monster = 0
        self.jade_total_damage_monster = 0

        # Расчетные шаги для подробного вывода
        self.calculation_steps = []

    def set_consciousness(self, value: float) -> None:
        """
        Установить значение сознания персонажа.

        Args:
            value: Значение сознания
        """
        self.consciousness = value

    def set_hero_level(self, value: int) -> None:
        """
        Установить уровень героя.

        Args:
            value: Уровень героя
        """
        self.hero_level = value

    def set_base_params(self,
                        untouchable_talent: bool,
                        power: bool,
                        ice_root: bool,
                        ice_flash: bool) -> None:
        """
        Установить базовые параметры персонажа.

        Args:
            untouchable_talent: Талант неприкосновенности
            power: Мощь
            ice_root: Ледяной корень
            ice_flash: Ледяная вспышка
        """
        self.untouchable_talent = untouchable_talent
        self.power = power
        self.ice_root = ice_root
        self.ice_flash = ice_flash

    def set_combat_params(self,
                          aroma_aura: bool,
                          frost_bloom: bool,
                          frost_seal: bool,
                          tundra_power: bool,
                          frostbound_lotus: bool,
                          tessa_f: bool,
                          consciousness_match: bool,
                          jade_active: bool) -> None:
        """
        Установить боевые параметры персонажа.

        Args:
            aroma_aura: Аура Аромата
            frost_bloom: Морозное цветение
            frost_seal: Морозная печать
            tundra_power: Мощь тундры
            frostbound_lotus: Морозный лотос
            tessa_f: F тессы
            consciousness_match: Совпадение уровня сознания
            jade_active: Активен ли нефрит с 3 взрывами (параметр игнорируется, нефрит всегда активен)
        """
        self.aroma_aura = aroma_aura
        self.frost_bloom = frost_bloom
        self.frost_seal = frost_seal
        self.tundra_power = tundra_power
        self.frostbound_lotus = frostbound_lotus
        self.tessa_f = tessa_f
        self.consciousness_match = consciousness_match
        # Параметр jade_active игнорируется, нефрит всегда активен
        self.jade_active = True

    # Функция для расчета бонуса атаки по уровню героя
    def calculate_hero_level_bonus(self) -> float:
        """
        Рассчитывает бонус атаки в зависимости от уровня героя.

        Returns:
            Бонус атаки от уровня героя (от 0 до 0.12)
        """
        bonus = 0.0
        for level, value in sorted(HERO_LEVEL_ATTACK_BONUS.items()):
            if self.hero_level >= level:
                bonus += value
        return bonus

    def calculate(self) -> Dict[str, Any]:
        """
        Выполнить расчет урона и всех параметров.

        Returns:
            Словарь с результатами расчетов
        """
        self.calculation_steps = []

        # Добавляем входные данные в шаги расчета
        self._add_input_data()

        # Получаем бонусы от нефритов
        jade_bonuses = calculate_jade_bonuses(self.jade_configs)
        jade_attack_bonus = jade_bonuses.get("Атака", 0.0)
        jade_ice_blast_bonus = jade_bonuses.get("Лед. взрыв", 0.0)
        jade_boss_attack_bonus = jade_bonuses.get("Атака по боссу", 0.0)
        jade_monster_attack_bonus = jade_bonuses.get("Атака по монстрам", 0.0)

        # Расчет базовых параметров
        self._calculate_base_parameters(jade_attack_bonus, jade_ice_blast_bonus)

        # Расчет боевых параметров
        self._calculate_combat_parameters(
            jade_attack_bonus,
            jade_ice_blast_bonus,
            jade_boss_attack_bonus,
            jade_monster_attack_bonus
        )

        # Расчет урона с нефритом (3 взрыва) - для боссов и монстров
        self._calculate_jade_damage()

        # Возвращаем результаты расчетов
        return {
            "base_attack": self.base_attack,
            "base_ice_blast_percent": self.base_ice_blast_percent,
            "final_attack": self.final_attack,
            "final_ice_blast_percent": self.final_ice_blast_percent,
            "physical_damage": self.physical_damage,

            # Параметры для боссов
            "boss_attack_bonus": self.boss_attack_bonus,
            "boss_ice_blast_percent": self.boss_ice_blast_percent,
            "boss_damage": self.boss_damage,
            "boss_flower_damage": self.boss_flower_damage,
            "jade_first_blast_boss": self.jade_first_blast_boss,
            "jade_second_blast_boss": self.jade_second_blast_boss,
            "jade_third_blast_boss": self.jade_third_blast_boss,
            "jade_total_damage_boss": self.jade_total_damage_boss,

            # Параметры для монстров
            "monster_attack_bonus": self.monster_attack_bonus,
            "monster_ice_blast_percent": self.monster_ice_blast_percent,
            "monster_damage": self.monster_damage,
            "monster_flower_damage": self.monster_flower_damage,
            "jade_first_blast_monster": self.jade_first_blast_monster,
            "jade_second_blast_monster": self.jade_second_blast_monster,
            "jade_third_blast_monster": self.jade_third_blast_monster,
            "jade_total_damage_monster": self.jade_total_damage_monster,

            "calculation_steps": "\n".join(self.calculation_steps)
        }

    def _add_input_data(self) -> None:
        """Добавляет информацию о входных данных в шаги расчета."""
        self.calculation_steps.append("ВХОДНЫЕ ДАННЫЕ:")
        self.calculation_steps.append(f"Сознание: {self.consciousness}")
        self.calculation_steps.append(f"Уровень героя: {self.hero_level}")
        self.calculation_steps.append(f"База атаки: {BASE_ATTACK}")
        self.calculation_steps.append(f"Коэффициент взрыва: {EXPLOSION_COEF}")
        self.calculation_steps.append(f"Коэффициент цветочного взрыва: {FLOWER_EXPLOSION_COEF}")
        # Нефрит всегда активен, но сохраняем информацию в расчетах
        self.calculation_steps.append(f"Нефрит (3 взрыва): Активен")
        # Добавляем информацию о совпадении уровня сознания
        self.calculation_steps.append(
            f"Совпадение уровня сознания: {'Активно' if self.consciousness_match else 'Неактивно'}")

        # Получаем бонусы от нефритов для отображения
        jade_bonuses = calculate_jade_bonuses(self.jade_configs)
        jade_attack_bonus = jade_bonuses.get("Атака", 0.0)
        jade_ice_blast_bonus = jade_bonuses.get("Лед. взрыв", 0.0)
        jade_boss_attack_bonus = jade_bonuses.get("Атака по боссу", 0.0)
        jade_monster_attack_bonus = jade_bonuses.get("Атака по монстрам", 0.0)

        self.calculation_steps.append(
            f"Бонус атаки от нефритов: {jade_attack_bonus:.2f} ({jade_attack_bonus * 100:.0f}%)"
        )
        self.calculation_steps.append(
            f"Бонус лед. взрыва от нефритов: {jade_ice_blast_bonus:.2f} ({jade_ice_blast_bonus * 100:.0f}%)"
        )
        self.calculation_steps.append(
            f"Бонус атаки по боссам от нефритов: {jade_boss_attack_bonus:.2f} ({jade_boss_attack_bonus * 100:.0f}%)"
        )
        self.calculation_steps.append(
            f"Бонус атаки по монстрам от нефритов: {jade_monster_attack_bonus:.2f} ({jade_monster_attack_bonus * 100:.0f}%)"
        )
        self.calculation_steps.append("")

    def _calculate_base_parameters(self, jade_attack_bonus: float, jade_ice_blast_bonus: float) -> None:
        """
        Рассчитывает базовые параметры персонажа (без боевых бонусов).

        Args:
            jade_attack_bonus: Бонус атаки от нефритов
            jade_ice_blast_bonus: Бонус процента ледяного взрыва от нефритов
        """
        self.calculation_steps.append("РАСЧЕТ БАЗОВЫХ ПАРАМЕТРОВ:")
        self.calculation_steps.append("Формула атаки: (база атаки + (сознание/10)) * (1 + бонусы)")
        self.calculation_steps.append("")

        # Расчет базового бонуса атаки
        base_attack_bonus = 1.0
        self.calculation_steps.append("Базовый бонус атаки: 1.0")

        # Добавляем бонус от уровня героя
        hero_level_bonus = self.calculate_hero_level_bonus()
        if hero_level_bonus > 0:
            base_attack_bonus += hero_level_bonus
            self.calculation_steps.append(f"+ Бонус атаки от уровня героя ({self.hero_level}): {hero_level_bonus}")

        if self.untouchable_talent:
            base_attack_bonus += TALENT_VALUES["untouchable_talent"]
            self.calculation_steps.append(f"+ Талант неприкосновенности: {TALENT_VALUES['untouchable_talent']}")

        if self.power:
            base_attack_bonus += TALENT_VALUES["power"]
            self.calculation_steps.append(f"+ Мощь: {TALENT_VALUES['power']}")

        # Добавляем бонус атаки от нефритов
        if jade_attack_bonus > 0:
            base_attack_bonus += jade_attack_bonus
            self.calculation_steps.append(f"+ Статы атаки на нефритах: {jade_attack_bonus:.2f}")

        self.calculation_steps.append(f"Итоговый базовый бонус атаки: {base_attack_bonus:.2f}")
        self.calculation_steps.append("")

        # Расчет базовой атаки
        self.base_attack = (BASE_ATTACK + (self.consciousness / 10)) * base_attack_bonus
        self.calculation_steps.append("Расчет базовой атаки:")
        self.calculation_steps.append(
            f"({BASE_ATTACK} + ({self.consciousness}/10)) * {base_attack_bonus:.2f} = {self.base_attack:.2f}"
        )
        self.calculation_steps.append("")

        # Расчет базового % ледяного взрыва
        self.base_ice_blast_percent = 1.0
        self.calculation_steps.append("Расчет базового % ледяного взрыва:")
        self.calculation_steps.append("Базовый % ледяного взрыва: 1.0 (100%)")

        if self.ice_root:
            self.base_ice_blast_percent += TALENT_VALUES["ice_root"]
            self.calculation_steps.append(f"+ Ледяной корень: {TALENT_VALUES['ice_root']}")

        # Добавляем бонус ледяного взрыва от нефритов
        if jade_ice_blast_bonus > 0:
            self.base_ice_blast_percent += jade_ice_blast_bonus
            self.calculation_steps.append(f"+ Статы %взрыва на нефритах: {jade_ice_blast_bonus:.2f}")

        if self.ice_flash:
            self.base_ice_blast_percent += TALENT_VALUES["ice_flash"]
            self.calculation_steps.append(f"+ Ледяная вспышка: {TALENT_VALUES['ice_flash']}")

        self.calculation_steps.append(
            f"Итоговый базовый % ледяного взрыва: {self.base_ice_blast_percent:.2f} "
            f"({self.base_ice_blast_percent * 100:.0f}%)"
        )
        self.calculation_steps.append("")

    def _calculate_combat_parameters(self,
                                     jade_attack_bonus: float,
                                     jade_ice_blast_bonus: float,
                                     jade_boss_attack_bonus: float,
                                     jade_monster_attack_bonus: float) -> None:
        """
        Рассчитывает боевые параметры персонажа.

        Args:
            jade_attack_bonus: Бонус атаки от нефритов
            jade_ice_blast_bonus: Бонус процента ледяного взрыва от нефритов
            jade_boss_attack_bonus: Бонус атаки по боссам от нефритов
            jade_monster_attack_bonus: Бонус атаки по монстрам от нефритов
        """
        self.calculation_steps.append("РАСЧЕТ БОЕВЫХ ПАРАМЕТРОВ:")
        self.calculation_steps.append(
            "Формула атаки: (база атаки + (сознание/10)) * (1 + бонусы) * (1 + F тессы)"
        )
        self.calculation_steps.append("")

        # Расчет боевого бонуса атаки
        combat_attack_bonus = 1.0
        self.calculation_steps.append("Боевой бонус атаки: 1.0")

        # Добавляем бонус от уровня героя
        hero_level_bonus = self.calculate_hero_level_bonus()
        if hero_level_bonus > 0:
            combat_attack_bonus += hero_level_bonus
            self.calculation_steps.append(f"+ Бонус атаки от уровня героя ({self.hero_level}): {hero_level_bonus}")

        if self.untouchable_talent:
            combat_attack_bonus += TALENT_VALUES["untouchable_talent"]
            self.calculation_steps.append(f"+ Талант неприкосновенности: {TALENT_VALUES['untouchable_talent']}")

        if self.power:
            combat_attack_bonus += TALENT_VALUES["power"]
            self.calculation_steps.append(f"+ Мощь: {TALENT_VALUES['power']}")

        # Добавляем бонус атаки от нефритов
        if jade_attack_bonus > 0:
            combat_attack_bonus += jade_attack_bonus
            self.calculation_steps.append(f"+ Статы атаки на нефритах: {jade_attack_bonus:.2f}")

        if self.aroma_aura:
            combat_attack_bonus += TALENT_VALUES["aroma_aura"]
            self.calculation_steps.append(f"+ Аура Аромата: {TALENT_VALUES['aroma_aura']}")

        if self.frost_seal:
            combat_attack_bonus += TALENT_VALUES["frost_seal"]
            self.calculation_steps.append(f"+ Морозная печать: {TALENT_VALUES['frost_seal']}")

        if self.tundra_power:
            combat_attack_bonus += TALENT_VALUES["tundra_power"]
            self.calculation_steps.append(f"+ Мощь тундры: {TALENT_VALUES['tundra_power']}")

        if self.frostbound_lotus:
            combat_attack_bonus += TALENT_VALUES["frostbound_lotus"]
            self.calculation_steps.append(f"+ Морозный лотос: {TALENT_VALUES['frostbound_lotus']}")

        self.calculation_steps.append(f"Итоговый боевой бонус атаки: {combat_attack_bonus:.2f}")
        self.calculation_steps.append("")

        # Учитываем F тессы
        tessa_multiplier = TALENT_VALUES["tessa_f"] if self.tessa_f else 1.0
        tessa_text = "активирован" if self.tessa_f else "не активирован"
        self.calculation_steps.append(f"Множитель F тессы: {tessa_multiplier:.2f} ({tessa_text})")

        # Расчет базовой боевой атаки
        base_final_attack = (BASE_ATTACK + (self.consciousness / 10)) * combat_attack_bonus * tessa_multiplier

        # Применяем бонус от совпадения уровня сознания к атаке
        consciousness_match_multiplier = TALENT_VALUES["consciousness_match"] if self.consciousness_match else 1.0

        # Применяем бонус к АТАКЕ
        if self.consciousness_match:
            self.calculation_steps.append(
                f"Бонус атаки от совпадения уровня сознания: +{(TALENT_VALUES['consciousness_match'] - 1.0) * 100:.0f}%")

        self.final_attack = base_final_attack * consciousness_match_multiplier

        self.calculation_steps.append("Расчет боевой атаки:")
        if self.consciousness_match:
            self.calculation_steps.append(
                f"({BASE_ATTACK} + ({self.consciousness}/10)) * {combat_attack_bonus:.2f} * "
                f"{tessa_multiplier:.2f} = {base_final_attack:.2f} (базовая атака)"
            )
            self.calculation_steps.append(
                f"{base_final_attack:.2f} * {consciousness_match_multiplier:.2f} = {self.final_attack:.2f} (с учетом совпадения уровня сознания)"
            )
        else:
            self.calculation_steps.append(
                f"({BASE_ATTACK} + ({self.consciousness}/10)) * {combat_attack_bonus:.2f} * "
                f"{tessa_multiplier:.2f} = {self.final_attack:.2f}"
            )
        self.calculation_steps.append("")

        # Расчет физического урона (базовая формула, без специализации)
        self.physical_damage = self.final_attack
        self.calculation_steps.append("Расчет физического урона:")
        self.calculation_steps.append(f"Физический урон = Атака = {self.final_attack:.2f}")
        self.calculation_steps.append("")

        # Расчет итогового % ледяного взрыва
        self.final_ice_blast_percent = 1.0
        self.calculation_steps.append("Расчет боевого % ледяного взрыва:")
        self.calculation_steps.append("Базовый % ледяного взрыва: 1.0 (100%)")

        if self.ice_root:
            self.final_ice_blast_percent += TALENT_VALUES["ice_root"]
            self.calculation_steps.append(f"+ Ледяной корень: {TALENT_VALUES['ice_root']}")

        # Добавляем бонус ледяного взрыва от нефритов
        if jade_ice_blast_bonus > 0:
            self.final_ice_blast_percent += jade_ice_blast_bonus
            self.calculation_steps.append(f"+ Статы %взрыва на нефритах: {jade_ice_blast_bonus:.2f}")

        if self.ice_flash:
            self.final_ice_blast_percent += TALENT_VALUES["ice_flash"]
            self.calculation_steps.append(f"+ Ледяная вспышка: {TALENT_VALUES['ice_flash']}")

        if self.frost_bloom:
            self.final_ice_blast_percent += TALENT_VALUES["frost_bloom"]
            self.calculation_steps.append(f"+ Морозное цветение: {TALENT_VALUES['frost_bloom']}")

        self.calculation_steps.append(
            f"Итоговый боевой % ледяного взрыва: {self.final_ice_blast_percent:.2f} "
            f"({self.final_ice_blast_percent * 100:.0f}%)"
        )
        self.calculation_steps.append("")

        # =============== Расчет для боссов ================
        self.calculation_steps.append("РАСЧЕТ ПАРАМЕТРОВ ПО БОССАМ:")

        # Бонус атаки по боссам
        self.boss_attack_bonus = jade_boss_attack_bonus
        self.calculation_steps.append(
            f"Бонус атаки по боссам: {self.boss_attack_bonus:.2f} ({self.boss_attack_bonus * 100:.0f}%)")

        # Расчет физ урона по боссам
        boss_physical_damage = self.final_attack * (1 + self.boss_attack_bonus)
        self.calculation_steps.append("Расчет физического урона по боссам:")
        self.calculation_steps.append(
            f"{self.final_attack:.2f} * (1 + {self.boss_attack_bonus:.2f}) = {boss_physical_damage:.2f}")

        # Расчет % ледяного взрыва по боссам
        # Формула: (1 * (1 + %атаки_по_боссу)) + другие_бонусы
        self.boss_ice_blast_percent = (1 * (1 + self.boss_attack_bonus)) + (self.final_ice_blast_percent - 1)

        self.calculation_steps.append("Расчет % ледяного взрыва по боссам:")
        self.calculation_steps.append(
            f"(1 * (1 + {self.boss_attack_bonus:.2f})) + ({self.final_ice_blast_percent:.2f} - 1) = {self.boss_ice_blast_percent:.2f}")

        # Расчет урона ледяного взрыва по боссам
        self.boss_damage = self.final_attack * self.boss_ice_blast_percent * EXPLOSION_COEF

        self.calculation_steps.append("Расчет урона ледяного взрыва по боссам:")
        self.calculation_steps.append(
            f"{self.final_attack:.2f} * {self.boss_ice_blast_percent:.2f} * {EXPLOSION_COEF} = {self.boss_damage:.2f}")

        # Расчет урона цветочного взрыва по боссам
        self.boss_flower_damage = self.final_attack * self.boss_ice_blast_percent * FLOWER_EXPLOSION_COEF

        self.calculation_steps.append("Расчет урона цветочного взрыва по боссам:")
        self.calculation_steps.append(
            f"{self.final_attack:.2f} * {self.boss_ice_blast_percent:.2f} * {FLOWER_EXPLOSION_COEF} = {self.boss_flower_damage:.2f}")
        self.calculation_steps.append("")

        # =============== Расчет для обычных монстров ================
        self.calculation_steps.append("РАСЧЕТ ПАРАМЕТРОВ ПО ОБЫЧНЫМ МОНСТРАМ:")

        # Бонус атаки по монстрам
        self.monster_attack_bonus = jade_monster_attack_bonus
        self.calculation_steps.append(
            f"Бонус атаки по монстрам: {self.monster_attack_bonus:.2f} ({self.monster_attack_bonus * 100:.0f}%)")

        # Расчет физ урона по монстрам
        monster_physical_damage = self.final_attack * (1 + self.monster_attack_bonus)
        self.calculation_steps.append("Расчет физического урона по монстрам:")
        self.calculation_steps.append(
            f"{self.final_attack:.2f} * (1 + {self.monster_attack_bonus:.2f}) = {monster_physical_damage:.2f}")

        # Расчет % ледяного взрыва по монстрам
        # Формула: (1 * (1 + %атаки_по_монстрам)) + другие_бонусы
        self.monster_ice_blast_percent = (1 * (1 + self.monster_attack_bonus)) + (self.final_ice_blast_percent - 1)

        self.calculation_steps.append("Расчет % ледяного взрыва по монстрам:")
        self.calculation_steps.append(
            f"(1 * (1 + {self.monster_attack_bonus:.2f})) + ({self.final_ice_blast_percent:.2f} - 1) = {self.monster_ice_blast_percent:.2f}")

        # Расчет урона ледяного взрыва по монстрам
        self.monster_damage = self.final_attack * self.monster_ice_blast_percent * EXPLOSION_COEF

        self.calculation_steps.append("Расчет урона ледяного взрыва по монстрам:")
        self.calculation_steps.append(
            f"{self.final_attack:.2f} * {self.monster_ice_blast_percent:.2f} * {EXPLOSION_COEF} = {self.monster_damage:.2f}")

        # Расчет урона цветочного взрыва по монстрам
        self.monster_flower_damage = self.final_attack * self.monster_ice_blast_percent * FLOWER_EXPLOSION_COEF

        self.calculation_steps.append("Расчет урона цветочного взрыва по монстрам:")
        self.calculation_steps.append(
            f"{self.final_attack:.2f} * {self.monster_ice_blast_percent:.2f} * {FLOWER_EXPLOSION_COEF} = {self.monster_flower_damage:.2f}")
        self.calculation_steps.append("")

    def _calculate_jade_damage(self) -> None:
        """Рассчитывает урон с нефритом (3 взрыва) для боссов и монстров."""
        self.calculation_steps.append("РАСЧЕТ УРОНА С НЕФРИТОМ (3 ВЗРЫВА):")

        # Коэффициенты для взрывов с нефритом
        first_blast_coef = EXPLOSION_COEF * JADE_FIRST_BLAST_MULTIPLIER
        other_blast_coef = EXPLOSION_COEF * JADE_OTHER_BLAST_MULTIPLIER

        self.calculation_steps.append("Формула для первого взрыва:")
        self.calculation_steps.append(
            f"Округлить(Атака * %ЛедВзрыва * {EXPLOSION_COEF} * {JADE_FIRST_BLAST_MULTIPLIER})")
        self.calculation_steps.append("")

        self.calculation_steps.append("Формула для второго/третьего взрыва:")
        self.calculation_steps.append(
            f"Округлить(Атака * %ЛедВзрыва * {EXPLOSION_COEF} * {JADE_OTHER_BLAST_MULTIPLIER})")
        self.calculation_steps.append("")

        # ============ Расчет урона по боссам ============
        self.calculation_steps.append("Расчет урона с нефритом по боссам:")

        # Расчет боевого урона с нефритом по боссам
        self.jade_first_blast_boss = round(
            self.final_attack * self.boss_ice_blast_percent * EXPLOSION_COEF * JADE_FIRST_BLAST_MULTIPLIER)
        self.jade_second_blast_boss = round(
            self.final_attack * self.boss_ice_blast_percent * EXPLOSION_COEF * JADE_OTHER_BLAST_MULTIPLIER)
        self.jade_third_blast_boss = self.jade_second_blast_boss  # Третий взрыв равен второму
        self.jade_total_damage_boss = self.jade_first_blast_boss + self.jade_second_blast_boss + self.jade_third_blast_boss

        self.calculation_steps.append(
            f"Первый взрыв: округлить({self.final_attack:.2f} * {self.boss_ice_blast_percent:.2f} * "
            f"{EXPLOSION_COEF} * {JADE_FIRST_BLAST_MULTIPLIER}) = {self.jade_first_blast_boss}"
        )
        self.calculation_steps.append(
            f"Второй взрыв: округлить({self.final_attack:.2f} * {self.boss_ice_blast_percent:.2f} * "
            f"{EXPLOSION_COEF} * {JADE_OTHER_BLAST_MULTIPLIER}) = {self.jade_second_blast_boss}"
        )
        self.calculation_steps.append(
            f"Третий взрыв: округлить({self.final_attack:.2f} * {self.boss_ice_blast_percent:.2f} * "
            f"{EXPLOSION_COEF} * {JADE_OTHER_BLAST_MULTIPLIER}) = {self.jade_third_blast_boss}"
        )
        self.calculation_steps.append(f"Суммарный урон по боссам: {self.jade_total_damage_boss}")
        self.calculation_steps.append("")

        # ============ Расчет урона по монстрам ============
        self.calculation_steps.append("Расчет урона с нефритом по монстрам:")

        # Расчет боевого урона с нефритом по монстрам
        self.jade_first_blast_monster = round(
            self.final_attack * self.monster_ice_blast_percent * EXPLOSION_COEF * JADE_FIRST_BLAST_MULTIPLIER)
        self.jade_second_blast_monster = round(
            self.final_attack * self.monster_ice_blast_percent * EXPLOSION_COEF * JADE_OTHER_BLAST_MULTIPLIER)
        self.jade_third_blast_monster = self.jade_second_blast_monster  # Третий взрыв равен второму
        self.jade_total_damage_monster = self.jade_first_blast_monster + self.jade_second_blast_monster + self.jade_third_blast_monster

        self.calculation_steps.append(
            f"Первый взрыв: округлить({self.final_attack:.2f} * {self.monster_ice_blast_percent:.2f} * "
            f"{EXPLOSION_COEF} * {JADE_FIRST_BLAST_MULTIPLIER}) = {self.jade_first_blast_monster}"
        )
        self.calculation_steps.append(
            f"Второй взрыв: округлить({self.final_attack:.2f} * {self.monster_ice_blast_percent:.2f} * "
            f"{EXPLOSION_COEF} * {JADE_OTHER_BLAST_MULTIPLIER}) = {self.jade_second_blast_monster}"
        )
        self.calculation_steps.append(
            f"Третий взрыв: округлить({self.final_attack:.2f} * {self.monster_ice_blast_percent:.2f} * "
            f"{EXPLOSION_COEF} * {JADE_OTHER_BLAST_MULTIPLIER}) = {self.jade_third_blast_monster}"
        )
        self.calculation_steps.append(f"Суммарный урон по монстрам: {self.jade_total_damage_monster}")
        self.calculation_steps.append("")