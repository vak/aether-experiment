#!/usr/bin/env python3
"""
Главный скрипт для запуска полного анализа эксперимента Майкельсона-Морли.
"""

import sys
import os

# Добавляем текущую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from classical_mm import analyze_earth_velocity as classical_analysis
from classical_mm import plot_velocity_dependence, plot_time_components
from relativistic_mm import compare_classical_and_relativistic
from relativistic_mm import plot_lorentz_contraction, plot_comparison


def create_figures_directory():
    """
    Создание директории для графиков, если она не существует.
    """
    figures_dir = '/home/user/aether-experiment/figures'
    if not os.path.exists(figures_dir):
        os.makedirs(figures_dir)
        print(f"Создана директория: {figures_dir}\n")


def main():
    """
    Главная функция.
    """
    print("\n" + "="*70)
    print(" " * 15 + "АНАЛИЗ ЭКСПЕРИМЕНТА МАЙКЕЛЬСОНА-МОРЛИ")
    print(" " * 10 + "Критика классической интерпретации")
    print("="*70 + "\n")

    # Создаём директорию для графиков
    create_figures_directory()

    # Часть 1: Классический анализ
    print("\n" + "─"*70)
    print("ЧАСТЬ 1: КЛАССИЧЕСКИЙ АНАЛИЗ")
    print("─"*70 + "\n")
    classical_analysis()

    input("\nНажмите Enter для продолжения...")

    # Часть 2: Сравнение с релятивистским подходом
    print("\n" + "─"*70)
    print("ЧАСТЬ 2: РЕЛЯТИВИСТСКИЙ АНАЛИЗ")
    print("─"*70 + "\n")
    compare_classical_and_relativistic()

    input("\nНажмите Enter для генерации графиков...")

    # Часть 3: Генерация графиков
    print("\n" + "─"*70)
    print("ЧАСТЬ 3: ГЕНЕРАЦИЯ ГРАФИКОВ")
    print("─"*70 + "\n")

    print("Генерация графиков классического анализа...")
    plot_velocity_dependence()
    plot_time_components()

    print("\nГенерация релятивистских графиков...")
    plot_lorentz_contraction()
    plot_comparison()

    print("\n" + "="*70)
    print("АНАЛИЗ ЗАВЕРШЁН")
    print("="*70)
    print()
    print("Результаты:")
    print("  📄 Теоретические документы: docs/")
    print("  📊 Графики: figures/")
    print("  🐍 Код: src/")
    print()
    print("Основные выводы:")
    print()
    print("  1. Классический расчёт предсказывает сдвиг ~0.4 полосы")
    print("     (не согласуется с наблюдениями)")
    print()
    print("  2. Классический расчёт ОШИБОЧЕН, потому что:")
    print("     - Использует понятие 'абсолютного времени'")
    print("     - Смешивает величины из разных систем отсчёта")
    print("     - Игнорирует конечность скорости передачи информации")
    print()
    print("  3. Релятивистский расчёт (с лоренцевым сокращением):")
    print("     - В системе эфира: всё ещё есть эффект")
    print("     - В системе лаборатории: эффект = 0 (точно!)")
    print()
    print("  4. ГЛАВНЫЙ ВЫВОД:")
    print("     Эксперимент ММ НЕ МОГ дать положительного результата")
    print("     по ЛОГИЧЕСКИМ причинам (конечность скорости света)!")
    print()
    print("  5. Отрицательный результат ММ:")
    print("     - НЕ доказывает отсутствие эфира")
    print("     - Показывает логическую некорректность вопроса")
    print("       об 'абсолютном движении'")
    print()
    print("Подробности см. в документах docs/01-introduction.md и далее.")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nПрервано пользователем.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nОШИБКА: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
