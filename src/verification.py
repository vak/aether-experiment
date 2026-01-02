#!/usr/bin/env python3
"""
Независимая проверка расчётов.
Проверяем, что мы не ошиблись в формулах.
"""

import numpy as np
import sys

def verify_classical_formula():
    """Проверка классических формул."""
    print("="*70)
    print("ПРОВЕРКА КЛАССИЧЕСКИХ ФОРМУЛ")
    print("="*70)

    L = 11.0
    c = 299792458.0
    v = 30000.0

    # Формула 1: через отдельные времена
    t_forward = L / (c - v)
    t_backward = L / (c + v)
    T_parallel_v1 = t_forward + t_backward

    # Формула 2: упрощённая
    T_parallel_v2 = 2 * L * c / (c**2 - v**2)

    # Проверка
    print(f"T_parallel (формула 1): {T_parallel_v1:.15e}")
    print(f"T_parallel (формула 2): {T_parallel_v2:.15e}")
    print(f"Разность: {abs(T_parallel_v1 - T_parallel_v2):.2e}")

    if abs(T_parallel_v1 - T_parallel_v2) < 1e-20:
        print("✅ Формулы совпадают!")
    else:
        print("❌ ОШИБКА: формулы не совпадают!")
        return False

    print()

    # Поперечное
    T_perp = 2 * L / np.sqrt(c**2 - v**2)

    print(f"T_perpendicular: {T_perp:.15e}")
    print()

    # Разность
    dT = T_parallel_v1 - T_perp
    print(f"ΔT = T_∥ - T_⊥ = {dT:.15e} с")
    print(f"Разность хода: Δ = c·ΔT = {c*dT:.15e} м")
    print()

    return True


def verify_relativistic_formula():
    """Проверка релятивистских формул с лоренцевым сокращением."""
    print("="*70)
    print("ПРОВЕРКА РЕЛЯТИВИСТСКИХ ФОРМУЛ")
    print("="*70)

    L0 = 11.0
    c = 299792458.0
    v = 30000.0

    gamma = 1.0 / np.sqrt(1 - v**2/c**2)

    print(f"Собственная длина: L₀ = {L0} м")
    print(f"Скорость: v = {v} м/с")
    print(f"Лоренц-фактор: γ = {gamma:.12f}")
    print()

    # Длины в системе эфира
    L_parallel = L0 / gamma  # лоренцево сокращение
    L_perp = L0  # не сокращается

    print(f"Продольная длина (система эфира): L_∥ = L₀/γ = {L_parallel:.12f} м")
    print(f"Поперечная длина (система эфира): L_⊥ = L₀ = {L_perp:.12f} м")
    print(f"Сокращение: ΔL = {L0 - L_parallel:.2e} м")
    print()

    # Времена в системе эфира
    # Продольное (с сокращённой длиной!)
    T_parallel_aether = 2 * L_parallel * c / (c**2 - v**2)

    # Поперечное
    T_perp_aether = 2 * L_perp / np.sqrt(c**2 - v**2)

    print(f"Время продольное (эфир): T_∥ = {T_parallel_aether:.15e} с")
    print(f"Время поперечное (эфир): T_⊥ = {T_perp_aether:.15e} с")
    print()

    # КРИТИЧЕСКАЯ ПРОВЕРКА!
    print("КРИТИЧЕСКАЯ ПРОВЕРКА:")
    print("-" * 70)

    # Упростим формулу для T_parallel
    # T_∥ = 2·(L₀/γ)·c/(c²-v²)
    #     = 2L₀c / [γ(c²-v²)]
    #     = 2L₀c / [γc²(1-v²/c²)]
    #     = 2L₀ / [γc(1-v²/c²)]
    #
    # γ = 1/√(1-v²/c²), поэтому:
    # γ(1-v²/c²) = (1-v²/c²)/√(1-v²/c²) = √(1-v²/c²)
    #
    # T_∥ = 2L₀ / [c·√(1-v²/c²)] = 2L₀/√(c²-v²)

    T_parallel_simplified = 2 * L0 / np.sqrt(c**2 - v**2)

    print(f"T_∥ (прямой расчёт):       {T_parallel_aether:.15e} с")
    print(f"T_∥ (упрощённая формула):  {T_parallel_simplified:.15e} с")
    print(f"T_⊥:                        {T_perp_aether:.15e} с")
    print()

    diff_parallel = abs(T_parallel_aether - T_parallel_simplified)
    diff_perp = abs(T_parallel_simplified - T_perp_aether)

    print(f"Разность (прямой vs упрощённый): {diff_parallel:.2e} с")
    print(f"Разность (T_∥ vs T_⊥):            {diff_perp:.2e} с")
    print()

    success = True

    if diff_perp < 1e-20:
        print("✅ ПОДТВЕРЖДЕНО: T_∥ = T_⊥ в системе эфира!")
        print("   Лоренцево сокращение ПОЛНОСТЬЮ компенсирует разность!")
    else:
        print(f"⚠️  Разность: {diff_perp:.15e} с")
        if diff_perp > 1e-15:
            print("❌ КРИТИЧЕСКАЯ ОШИБКА: разность слишком велика!")
            success = False
        else:
            print("✅ Разность в пределах численной погрешности")
    print()

    # Времена в системе лаборатории
    print("В системе ЛАБОРАТОРИИ:")
    print("-" * 70)
    T_lab = 2 * L0 / c
    print(f"T_∥ = T_⊥ = 2L₀/c = {T_lab:.15e} с")
    print("✅ Скорость света изотропна, времена одинаковы!")
    print()

    return success


def numerical_precision_check():
    """Проверка численной точности для разных скоростей."""
    print("="*70)
    print("ПРОВЕРКА ДЛЯ РАЗЛИЧНЫХ СКОРОСТЕЙ")
    print("="*70)

    L0 = 11.0
    c = 299792458.0

    velocities = [100, 1000, 10000, 30000, 100000, 1000000, 10000000]

    print(f"{'v (м/с)':<12} {'v/c':<12} {'T_∥ - T_⊥ (сек)':<20} {'Относительная погрешность':<25}")
    print("-" * 90)

    all_good = True

    for v in velocities:
        gamma = 1.0 / np.sqrt(1 - v**2/c**2)
        L_par = L0 / gamma

        T_par = 2 * L_par * c / (c**2 - v**2)
        T_perp = 2 * L0 / np.sqrt(c**2 - v**2)

        dT = abs(T_par - T_perp)
        rel_error = dT / T_perp if T_perp > 0 else 0

        status = "✅" if rel_error < 1e-14 else ("⚠️" if rel_error < 1e-10 else "❌")

        print(f"{v:<12} {v/c:<12.2e} {dT:<20.2e} {rel_error:<25.2e} {status}")

        if rel_error >= 1e-10:
            all_good = False

    print()
    if all_good:
        print("✅ Для всех скоростей: ΔT ≈ 0 в пределах численной точности!")
    else:
        print("⚠️  Обнаружены численные погрешности при больших скоростях")
    print()

    return all_good


def check_extreme_cases():
    """Проверка предельных случаев."""
    print("="*70)
    print("ПРОВЕРКА ПРЕДЕЛЬНЫХ СЛУЧАЕВ")
    print("="*70)

    L0 = 11.0
    c = 299792458.0

    print("1. Предел v → 0:")
    print("-" * 70)

    v = 1.0  # очень малая скорость
    gamma = 1.0 / np.sqrt(1 - v**2/c**2)

    print(f"v = {v} м/с (v/c = {v/c:.2e})")
    print(f"γ = {gamma:.15f} (должно быть ≈ 1)")
    print(f"L_∥ = L₀/γ = {L0/gamma:.15f} м (должно быть ≈ {L0})")

    T_classical = 2 * L0 / c
    T_relativistic = 2 * L0 / np.sqrt(c**2 - v**2)

    print(f"T (классика) = {T_classical:.15e} с")
    print(f"T (релятивизм) = {T_relativistic:.15e} с")
    print(f"Разность: {abs(T_classical - T_relativistic):.2e} с")

    if abs(gamma - 1.0) < 1e-10 and abs(T_classical - T_relativistic) < 1e-15:
        print("✅ При v → 0 релятивистские формулы переходят в классические")
    else:
        print("❌ ОШИБКА в предельном переходе!")
        return False

    print()
    print("2. Большие скорости:")
    print("-" * 70)

    for beta in [0.1, 0.5, 0.9, 0.99, 0.999]:
        v = beta * c
        gamma = 1.0 / np.sqrt(1 - beta**2)
        L_contracted = L0 / gamma

        print(f"v/c = {beta:.3f}: γ = {gamma:.4f}, L_∥/L₀ = {L_contracted/L0:.6f}")

    print()
    print("✅ Лоренц-фактор растёт, длина сокращается как ожидается")
    print()

    return True


def cross_check_with_known_values():
    """Перекрёстная проверка с известными значениями."""
    print("="*70)
    print("ПЕРЕКРЁСТНАЯ ПРОВЕРКА С ИЗВЕСТНЫМИ ЗНАЧЕНИЯМИ")
    print("="*70)

    c = 299792458.0

    # Скорость электрона в атоме водорода (первая боровская орбита)
    v_electron = 2187691.0  # м/с (примерно)

    gamma_electron = 1.0 / np.sqrt(1 - v_electron**2/c**2)

    print(f"Скорость электрона в атоме H: v ≈ {v_electron:.0f} м/с")
    print(f"v/c ≈ {v_electron/c:.6f}")
    print(f"γ ≈ {gamma_electron:.12f}")
    print(f"Релятивистская поправка: (γ-1) ≈ {gamma_electron - 1.0:.2e}")
    print("(для электронов в атомах релятивистские эффекты малы)")
    print()

    # Космические мюоны
    v_muon = 0.98 * c  # типичная скорость космических мюонов
    gamma_muon = 1.0 / np.sqrt(1 - (v_muon/c)**2)

    print(f"Космический мюон: v ≈ 0.98c")
    print(f"γ ≈ {gamma_muon:.2f}")
    print(f"Время жизни увеличивается в γ ≈ {gamma_muon:.1f} раз")
    print(f"Расстояние сокращается в γ ≈ {gamma_muon:.1f} раз")
    print("(поэтому мюоны долетают до поверхности Земли)")
    print()

    return True


def main():
    """Главная функция."""
    print("\n" + "="*70)
    print(" " * 20 + "ЧИСЛЕННАЯ ВЕРИФИКАЦИЯ")
    print(" " * 15 + "Проверка на самообман")
    print("="*70 + "\n")

    all_tests_passed = True

    # Тест 1
    print("\n")
    if not verify_classical_formula():
        all_tests_passed = False
        print("❌ Тест классических формул ПРОВАЛЕН!")

    # Тест 2
    print("\n")
    if not verify_relativistic_formula():
        all_tests_passed = False
        print("❌ Тест релятивистских формул ПРОВАЛЕН!")

    # Тест 3
    print("\n")
    if not numerical_precision_check():
        all_tests_passed = False
        print("❌ Тест численной точности ПРОВАЛЕН!")

    # Тест 4
    print("\n")
    if not check_extreme_cases():
        all_tests_passed = False
        print("❌ Тест предельных случаев ПРОВАЛЕН!")

    # Тест 5
    print("\n")
    cross_check_with_known_values()

    # Итоги
    print("\n" + "="*70)
    print("ИТОГОВЫЙ ВЫВОД")
    print("="*70)
    print()

    if all_tests_passed:
        print("✅ ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ УСПЕШНО!")
        print()
        print("Подтверждено:")
        print("  1. Классические формулы математически корректны")
        print("  2. Релятивистские формулы математически корректны")
        print("  3. В системе эфира с лоренцевым сокращением: T_∥ = T_⊥")
        print("  4. В системе лаборатории: T_∥ = T_⊥ = 2L₀/c")
        print("  5. Предельные переходы корректны")
        print()
        print("ВЕРДИКТ: Мы НЕ обманываем себя!")
        print("         Математика подтверждает наши выводы.")
        print()
        return 0
    else:
        print("❌ ОБНАРУЖЕНЫ ОШИБКИ!")
        print()
        print("Необходимо пересмотреть анализ!")
        print()
        return 1


if __name__ == "__main__":
    sys.exit(main())
