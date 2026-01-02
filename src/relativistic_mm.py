#!/usr/bin/env python3
"""
Релятивистский расчёт эксперимента Майкельсона-Морли
с учётом лоренцева сокращения и правильной синхронизации часов.
"""

import numpy as np
import matplotlib.pyplot as plt
from classical_mm import ClassicalMichelsonMorley


class RelativisticMichelsonMorley:
    """
    Релятивистская модель эксперимента Майкельсона-Морли.

    Учитывает:
    - Лоренцево сокращение длин
    - Относительность одновременности
    - Изотропию скорости света в собственной системе отсчёта
    """

    def __init__(self, L0=11.0, c=299792458.0, wavelength=500e-9):
        """
        Параметры:
            L0: собственная длина плеча (в покое) (метры)
            c: скорость света (м/с)
            wavelength: длина волны света (метры)
        """
        self.L0 = L0  # собственная длина
        self.c = c  # скорость света
        self.wavelength = wavelength

    def gamma(self, v):
        """
        Лоренц-фактор γ = 1/√(1 - v²/c²)
        """
        beta = v / self.c
        if abs(beta) >= 1:
            raise ValueError("Скорость v должна быть меньше c")
        return 1.0 / np.sqrt(1 - beta**2)

    def length_parallel_aether_frame(self, v):
        """
        Длина продольного плеча в системе эфира (лоренцево сокращение).

        L_∥ = L₀ / γ = L₀√(1 - v²/c²)

        Параметры:
            v: скорость движения лаборатории относительно эфира

        Возвращает:
            длина продольного плеча в системе эфира
        """
        return self.L0 / self.gamma(v)

    def length_perpendicular_aether_frame(self, v):
        """
        Длина поперечного плеча в системе эфира (не сокращается).

        L_⊥ = L₀

        Параметры:
            v: скорость движения

        Возвращает:
            длина поперечного плеча
        """
        return self.L0

    def time_parallel_aether_frame(self, v):
        """
        Время прохождения света в продольном плече (система эфира).

        С учётом лоренцева сокращения:
        L_∥ = L₀/γ
        T_∥ = 2L_∥·c/(c²-v²) = 2(L₀/γ)·c/(c²-v²)

        Упрощая:
        T_∥ = (2L₀/c)·γ³ (это неточно, давайте пересчитаем)

        Правильно:
        T_∥ = L_∥/(c-v) + L_∥/(c+v) = 2L_∥c/(c²-v²)
        где L_∥ = L₀√(1-v²/c²)

        Параметры:
            v: скорость движения

        Возвращает:
            время прохождения
        """
        L_par = self.length_parallel_aether_frame(v)
        return 2 * L_par * self.c / (self.c**2 - v**2)

    def time_perpendicular_aether_frame(self, v):
        """
        Время прохождения света в поперечном плече (система эфира).

        T_⊥ = 2L₀/√(c²-v²) = (2L₀/c)·γ

        Параметры:
            v: скорость движения

        Возвращает:
            время прохождения
        """
        L_perp = self.length_perpendicular_aether_frame(v)
        return 2 * L_perp / np.sqrt(self.c**2 - v**2)

    def time_difference_aether_frame(self, v):
        """
        Разность времён в системе эфира (с учётом лоренцева сокращения).
        """
        return self.time_parallel_aether_frame(v) - self.time_perpendicular_aether_frame(v)

    def time_lab_frame(self, v):
        """
        Время прохождения в системе лаборатории.

        В собственной системе отсчёта лаборатории:
        - Скорость света изотропна: c
        - Оба плеча имеют одинаковую собственную длину: L₀
        - Времена: T_∥ = T_⊥ = 2L₀/c

        Параметры:
            v: скорость (не используется в собственной системе!)

        Возвращает:
            время прохождения (одинаковое для обоих плеч)
        """
        # В собственной системе отсчёта скорость света изотропна!
        return 2 * self.L0 / self.c

    def fringe_shift_aether_frame(self, v):
        """
        Сдвиг полос, рассчитанный в системе эфира (с лоренцевым сокращением).
        """
        dt = self.time_difference_aether_frame(v)
        path_diff = self.c * dt
        return 2 * path_diff / self.wavelength

    def fringe_shift_lab_frame(self, v):
        """
        Сдвиг полос в системе лаборатории.

        Результат: ВСЕГДА НОЛЬ!
        Потому что T_∥ = T_⊥ = 2L₀/c
        """
        # В собственной системе времена одинаковы
        return 0.0


def compare_classical_and_relativistic():
    """
    Сравнение классического и релятивистского расчётов.
    """
    print("=" * 70)
    print("СРАВНЕНИЕ КЛАССИЧЕСКОГО И РЕЛЯТИВИСТСКОГО РАСЧЁТОВ")
    print("=" * 70)
    print()

    L0 = 11.0
    c = 299792458.0
    wavelength = 500e-9
    v_earth = 30000.0

    classical = ClassicalMichelsonMorley(L=L0, c=c, wavelength=wavelength)
    relativistic = RelativisticMichelsonMorley(L0=L0, c=c, wavelength=wavelength)

    print("Параметры:")
    print(f"  L₀ = {L0} м, c = {c:.0f} м/с, λ = {wavelength*1e9:.1f} нм")
    print(f"  v = {v_earth:.0f} м/с (скорость Земли)")
    print(f"  v/c = {v_earth/c:.2e}")
    print()

    # Классический расчёт
    print("КЛАССИЧЕСКИЙ РАСЧЁТ (без лоренцева сокращения):")
    print(f"  Длина продольного плеча: L_∥ = {L0} м")
    print(f"  Длина поперечного плеча: L_⊥ = {L0} м")
    t_par_cl = classical.time_parallel(v_earth)
    t_perp_cl = classical.time_perpendicular(v_earth)
    dt_cl = classical.time_difference(v_earth)
    shift_cl = classical.fringe_shift(v_earth)
    print(f"  Время T_∥ = {t_par_cl:.15e} с")
    print(f"  Время T_⊥ = {t_perp_cl:.15e} с")
    print(f"  Разность ΔT = {dt_cl:.15e} с")
    print(f"  Сдвиг полос: δ = {shift_cl:.6f} λ")
    print()

    # Релятивистский расчёт (система эфира)
    print("РЕЛЯТИВИСТСКИЙ РАСЧЁТ (система эфира, с лоренцевым сокращением):")
    L_par_rel = relativistic.length_parallel_aether_frame(v_earth)
    L_perp_rel = relativistic.length_perpendicular_aether_frame(v_earth)
    print(f"  Длина продольного плеча: L_∥ = {L_par_rel:.12f} м")
    print(f"  Длина поперечного плеча: L_⊥ = {L_perp_rel:.12f} м")
    print(f"  Сокращение: ΔL = {L0 - L_par_rel:.2e} м")
    t_par_rel = relativistic.time_parallel_aether_frame(v_earth)
    t_perp_rel = relativistic.time_perpendicular_aether_frame(v_earth)
    dt_rel = relativistic.time_difference_aether_frame(v_earth)
    shift_rel_aether = relativistic.fringe_shift_aether_frame(v_earth)
    print(f"  Время T_∥ = {t_par_rel:.15e} с")
    print(f"  Время T_⊥ = {t_perp_rel:.15e} с")
    print(f"  Разность ΔT = {dt_rel:.15e} с")
    print(f"  Сдвиг полос: δ = {shift_rel_aether:.6f} λ")
    print()

    # Релятивистский расчёт (система лаборатории)
    print("РЕЛЯТИВИСТСКИЙ РАСЧЁТ (система лаборатории, собственная СО):")
    print(f"  Длина продольного плеча: L_∥ = {L0} м (собственная длина)")
    print(f"  Длина поперечного плеча: L_⊥ = {L0} м (собственная длина)")
    print(f"  Скорость света: c = {c:.0f} м/с (изотропна!)")
    t_lab = relativistic.time_lab_frame(v_earth)
    print(f"  Время T_∥ = {t_lab:.15e} с")
    print(f"  Время T_⊥ = {t_lab:.15e} с")
    print(f"  Разность ΔT = 0 с (точно!)")
    shift_lab = relativistic.fringe_shift_lab_frame(v_earth)
    print(f"  Сдвиг полос: δ = {shift_lab:.6f} λ")
    print()

    print("=" * 70)
    print("ВЫВОДЫ:")
    print("=" * 70)
    print()
    print("1. КЛАССИЧЕСКИЙ расчёт предсказывает сдвиг ~{:.3f} λ".format(shift_cl))
    print("   (не согласуется с экспериментом!)")
    print()
    print("2. РЕЛЯТИВИСТСКИЙ расчёт (система эфира):")
    print("   - Учитывает лоренцево сокращение продольного плеча")
    print("   - Всё ещё предсказывает ненулевой сдвиг ~{:.3f} λ".format(shift_rel_aether))
    print("   - НО: это время измерено в системе эфира!")
    print()
    print("3. РЕЛЯТИВИСТСКИЙ расчёт (система лаборатории):")
    print("   - В собственной СО скорость света ИЗОТРОПНА (по определению!)")
    print("   - Времена прохождения ОДИНАКОВЫ")
    print("   - Сдвиг полос = 0 (точно!)")
    print("   - СОГЛАСУЕТСЯ С ЭКСПЕРИМЕНТОМ!")
    print()
    print("КЛЮЧЕВОЙ МОМЕНТ:")
    print("  Интерферометр покоится в ЛАБОРАТОРИИ.")
    print("  Мы наблюдаем интерференцию В ЛАБОРАТОРИИ.")
    print("  Поэтому нужно использовать расчёт в системе ЛАБОРАТОРИИ!")
    print()
    print("  В системе лаборатории скорость света ИЗОТРОПНА")
    print("  (это следствие определения синхронизации часов),")
    print("  поэтому сдвиг полос ВСЕГДА РАВЕН НУЛЮ!")
    print()


def plot_lorentz_contraction():
    """
    График зависимости длины от скорости (лоренцево сокращение).
    """
    rel = RelativisticMichelsonMorley(L0=11.0)

    velocities = np.linspace(0, 0.9*rel.c, 1000)

    lengths_parallel = [rel.length_parallel_aether_frame(v) for v in velocities]
    lengths_perp = [rel.length_perpendicular_aether_frame(v) for v in velocities]
    gammas = [rel.gamma(v) for v in velocities]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Левый график: длины
    ax1.plot(velocities/rel.c, lengths_parallel, 'b-', linewidth=2, label='L_∥ (продольное)')
    ax1.plot(velocities/rel.c, lengths_perp, 'r--', linewidth=2, label='L_⊥ (поперечное)')
    ax1.axvline(x=30000/rel.c, color='gray', linestyle=':', alpha=0.7, label='v_Земли')
    ax1.set_xlabel('v/c', fontsize=12)
    ax1.set_ylabel('Длина плеча (м)', fontsize=12)
    ax1.set_title('Лоренцево сокращение длин', fontsize=13, weight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=10)

    # Правый график: γ-фактор
    ax2.plot(velocities/rel.c, gammas, 'purple', linewidth=2)
    ax2.axvline(x=30000/rel.c, color='gray', linestyle=':', alpha=0.7)
    ax2.set_xlabel('v/c', fontsize=12)
    ax2.set_ylabel('γ = 1/√(1 - v²/c²)', fontsize=12)
    ax2.set_title('Лоренц-фактор', fontsize=13, weight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim([1, 3])

    plt.tight_layout()
    plt.savefig('/home/user/aether-experiment/figures/lorentz_contraction.png', dpi=150)
    print("График сохранён: figures/lorentz_contraction.png")
    plt.close()


def plot_comparison():
    """
    Сравнительный график классического и релятивистского предсказаний.
    """
    classical = ClassicalMichelsonMorley(L=11.0)
    relativistic = RelativisticMichelsonMorley(L0=11.0)

    velocities = np.linspace(0, 100000, 1000)

    shift_classical = [classical.fringe_shift(v) for v in velocities]
    shift_rel_aether = [relativistic.fringe_shift_aether_frame(v) for v in velocities]
    shift_rel_lab = [relativistic.fringe_shift_lab_frame(v) for v in velocities]

    plt.figure(figsize=(10, 6))
    plt.plot(velocities/1000, shift_classical, 'b-', linewidth=2.5,
             label='Классический (без сокращения)')
    plt.plot(velocities/1000, shift_rel_aether, 'orange', linewidth=2,
             linestyle='--', label='Релятивистский (система эфира)')
    plt.plot(velocities/1000, shift_rel_lab, 'g-', linewidth=3,
             label='Релятивистский (система лаборатории)')

    plt.axvline(x=30, color='r', linestyle=':', linewidth=2, alpha=0.7, label='v_Земли (~30 км/с)')
    plt.axhline(y=0.01, color='gray', linestyle='-.', linewidth=1, alpha=0.5, label='Предел обнаружения')
    plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)

    v_earth = 30000
    shift_cl = classical.fringe_shift(v_earth)
    plt.plot(v_earth/1000, shift_cl, 'bo', markersize=10)
    plt.text(v_earth/1000 + 2, shift_cl, f'{shift_cl:.3f} λ', fontsize=10, va='center')

    plt.xlabel('Скорость относительно эфира (км/с)', fontsize=12)
    plt.ylabel('Сдвиг интерференционных полос (λ)', fontsize=12)
    plt.title('Сравнение предсказаний: классика vs релятивизм', fontsize=14, weight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=10, loc='upper left')
    plt.ylim([-0.05, max(shift_classical)*1.1])
    plt.tight_layout()

    plt.savefig('/home/user/aether-experiment/figures/classical_vs_relativistic.png', dpi=150)
    print("График сохранён: figures/classical_vs_relativistic.png")
    plt.close()


if __name__ == "__main__":
    # Сравнительный анализ
    compare_classical_and_relativistic()

    # Графики
    print("\nГенерация графиков...")
    plot_lorentz_contraction()
    plot_comparison()
    print("\nГотово!")
