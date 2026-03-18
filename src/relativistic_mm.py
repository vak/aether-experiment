#!/usr/bin/env python3
"""
Релятивистский расчёт эксперимента Майкельсона-Морли
с учётом лоренцева сокращения.

Обозначения:
  L  — собственная длина плеча (в системе покоя интерферометра = лаборатория)
  v  — скорость лаборатории относительно эфира
  c  — скорость света

Два расчёта:
  1. В системе лаборатории (S_lab): c изотропна, L_∥ = L_⊥ = L
  2. В системе эфира (S_aether): c анизотропна, L_∥ = L/γ, L_⊥ = L
"""

import numpy as np
import matplotlib.pyplot as plt
from classical_mm import ClassicalMichelsonMorley


class RelativisticMichelsonMorley:
    """
    Релятивистская модель эксперимента Майкельсона-Морли.

    L — собственная длина плеча (в лаборатории, где интерферометр покоится).
    """

    def __init__(self, L=11.0, c=299792458.0, wavelength=500e-9):
        self.L = L            # собственная длина плеча
        self.c = c            # скорость света
        self.wavelength = wavelength

    def gamma(self, v):
        """Лоренц-фактор γ = 1/√(1 - v²/c²)"""
        beta = v / self.c
        if abs(beta) >= 1:
            raise ValueError("v must be less than c")
        return 1.0 / np.sqrt(1 - beta**2)

    # ─── Система эфира (S_aether) ───────────────────────────────

    def length_parallel_aether(self, v):
        """Длина продольного плеча в системе эфира: L/γ"""
        return self.L / self.gamma(v)

    def length_perp_aether(self, v):
        """Длина поперечного плеча в системе эфира: L (не сокращается)"""
        return self.L

    def time_parallel_aether(self, v):
        """
        Координатное время прохождения света в продольном плече (S_aether).

        T_∥ = (L/γ)/(c-v) + (L/γ)/(c+v) = 2(L/γ)c/(c²-v²) = (2L/c)·γ
        """
        L_par = self.length_parallel_aether(v)
        return L_par / (self.c - v) + L_par / (self.c + v)

    def time_perp_aether(self, v):
        """
        Координатное время прохождения света в поперечном плече (S_aether).

        T_⊥ = 2L/√(c²-v²) = (2L/c)·γ
        """
        return 2 * self.L / np.sqrt(self.c**2 - v**2)

    def time_difference_aether(self, v):
        """Разность координатных времён в S_aether. Должна быть ≈0."""
        return self.time_parallel_aether(v) - self.time_perp_aether(v)

    # ─── Система лаборатории (S_lab) ────────────────────────────

    def time_parallel_lab(self, v):
        """
        Время прохождения в продольном плече, измеренное в S_lab.

        Два эквивалентных способа получить результат:

        Способ 1 (принцип относительности):
          В S_lab скорость света изотропна, плечо имеет собственную длину L.
          T_∥ = 2L/c

        Способ 2 (пересчёт из S_aether):
          T_∥^(aether) = (2L/c)·γ  (координатное время в эфире)
          T_∥^(lab) = T_∥^(aether) / γ = 2L/c  (замедление времени)

        Оба способа дают один ответ.
        """
        # Вычисляем через пересчёт из S_aether (способ 2) для прозрачности:
        return self.time_parallel_aether(v) / self.gamma(v)

    def time_perp_lab(self, v):
        """
        Время прохождения в поперечном плече, измеренное в S_lab.

        T_⊥^(aether) = (2L/c)·γ
        T_⊥^(lab) = T_⊥^(aether) / γ = 2L/c
        """
        return self.time_perp_aether(v) / self.gamma(v)

    def time_difference_lab(self, v):
        """Разность времён в S_lab. Должна быть ≈0."""
        return self.time_parallel_lab(v) - self.time_perp_lab(v)

    def fringe_shift(self, v):
        """
        Сдвиг полос (наблюдаемая величина, не зависит от выбора СО).

        При повороте на 90° сдвиг удваивается: δ = 2·c·ΔT/λ
        """
        dt = self.time_difference_lab(v)
        return 2 * abs(self.c * dt) / self.wavelength


def compare_classical_and_relativistic():
    """Сравнение классического и релятивистского расчётов."""
    print("=" * 70)
    print("СРАВНЕНИЕ КЛАССИЧЕСКОГО И РЕЛЯТИВИСТСКОГО РАСЧЁТОВ")
    print("=" * 70)
    print()

    L = 11.0
    c = 299792458.0
    wavelength = 500e-9
    v = 30000.0

    cl = ClassicalMichelsonMorley(L=L, c=c, wavelength=wavelength)
    rel = RelativisticMichelsonMorley(L=L, c=c, wavelength=wavelength)

    print(f"Параметры: L = {L} м, c = {c:.0f} м/с, λ = {wavelength*1e9:.1f} нм")
    print(f"           v = {v:.0f} м/с (~{v/1000:.0f} км/с), v/c = {v/c:.2e}")
    print()

    # ── Классический расчёт ──
    print("КЛАССИЧЕСКИЙ РАСЧЁТ (ошибка: L_∥ = L в системе эфира)")
    print("-" * 70)
    t_par_cl = cl.time_parallel(v)
    t_perp_cl = cl.time_perpendicular(v)
    dt_cl = cl.time_difference(v)
    shift_cl = cl.fringe_shift(v)
    print(f"  L_∥^(aether) = {L} м  (неверно! должно быть L/γ)")
    print(f"  T_∥ = {t_par_cl:.15e} с = (2L/c)·γ²")
    print(f"  T_⊥ = {t_perp_cl:.15e} с = (2L/c)·γ")
    print(f"  ΔT  = {dt_cl:.4e} с")
    print(f"  Сдвиг полос: δ = {shift_cl:.4f} λ")
    print()

    # ── Релятивистский расчёт: система эфира ──
    print("РЕЛЯТИВИСТСКИЙ: система эфира (с лоренцевым сокращением)")
    print("-" * 70)
    g = rel.gamma(v)
    L_par = rel.length_parallel_aether(v)
    t_par = rel.time_parallel_aether(v)
    t_perp = rel.time_perp_aether(v)
    dt_aether = rel.time_difference_aether(v)
    print(f"  γ = {g:.12f}")
    print(f"  L_∥^(aether) = L/γ = {L_par:.12f} м")
    print(f"  L_⊥^(aether) = L   = {L} м")
    print(f"  T_∥ = {t_par:.15e} с = (2L/c)·γ")
    print(f"  T_⊥ = {t_perp:.15e} с = (2L/c)·γ")
    print(f"  ΔT  = {dt_aether:.4e} с")
    expected = 2 * L / c * g
    print(f"  Проверка: (2L/c)·γ = {expected:.15e} с")
    print()

    # ── Релятивистский расчёт: система лаборатории ──
    print("РЕЛЯТИВИСТСКИЙ: система лаборатории (пересчёт из S_aether)")
    print("-" * 70)
    t_par_lab = rel.time_parallel_lab(v)
    t_perp_lab = rel.time_perp_lab(v)
    dt_lab = rel.time_difference_lab(v)
    shift = rel.fringe_shift(v)
    print(f"  T_∥^(lab) = T_∥^(aether)/γ = {t_par_lab:.15e} с")
    print(f"  T_⊥^(lab) = T_⊥^(aether)/γ = {t_perp_lab:.15e} с")
    print(f"  Проверка: 2L/c = {2*L/c:.15e} с")
    print(f"  ΔT  = {dt_lab:.4e} с")
    print(f"  Сдвиг полос: δ = {shift:.6f} λ")
    print()

    # ── Итог ──
    print("=" * 70)
    print("ИТОГ:")
    print("=" * 70)
    print()
    print(f"  Классический расчёт:      δ = {shift_cl:.4f} λ (ошибка: L вместо L/γ)")
    print(f"  Релятивистский расчёт:    δ = {shift:.6f} λ (корректно)")
    print(f"  Эксперимент Майкельсона:  δ < 0.01 λ")
    print()
    print("  Ошибка классического расчёта: использование собственной длины L")
    print("  вместо сокращённой L/γ при вычислении в системе эфира.")
    print("  Это эквивалентно смешению величин из разных систем отсчёта.")
    print()


def plot_lorentz_contraction():
    """График лоренцева сокращения."""
    rel = RelativisticMichelsonMorley(L=11.0)

    velocities = np.linspace(0, 0.9*rel.c, 1000)

    lengths_par = [rel.length_parallel_aether(v) for v in velocities]
    lengths_perp = [rel.length_perp_aether(v) for v in velocities]
    gammas = [rel.gamma(v) for v in velocities]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    ax1.plot(velocities/rel.c, lengths_par, 'b-', linewidth=2, label='L_∥ (продольное)')
    ax1.plot(velocities/rel.c, lengths_perp, 'r--', linewidth=2, label='L_⊥ (поперечное)')
    ax1.axvline(x=30000/rel.c, color='gray', linestyle=':', alpha=0.7, label='v_Земли')
    ax1.set_xlabel('v/c', fontsize=12)
    ax1.set_ylabel('Длина плеча в S_aether (м)', fontsize=12)
    ax1.set_title('Лоренцево сокращение длин', fontsize=13, weight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=10)

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
    """Сравнительный график классического и релятивистского предсказаний."""
    cl = ClassicalMichelsonMorley(L=11.0)
    rel = RelativisticMichelsonMorley(L=11.0)

    velocities = np.linspace(1, 100000, 1000)

    shift_classical = [cl.fringe_shift(v) for v in velocities]
    shift_relativistic = [rel.fringe_shift(v) for v in velocities]

    plt.figure(figsize=(10, 6))
    plt.plot(velocities/1000, shift_classical, 'b-', linewidth=2.5,
             label='Классический (L_∥ = L, ошибочный)')
    plt.plot(velocities/1000, shift_relativistic, 'g-', linewidth=2.5,
             label='Релятивистский (L_∥ = L/γ, корректный)')

    plt.axvline(x=30, color='r', linestyle=':', linewidth=2, alpha=0.7,
                label='v_Земли (~30 км/с)')
    plt.axhline(y=0.01, color='gray', linestyle='-.', linewidth=1, alpha=0.5,
                label='Предел обнаружения')
    plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)

    v_earth = 30000
    shift_cl_earth = cl.fringe_shift(v_earth)
    plt.plot(v_earth/1000, shift_cl_earth, 'bo', markersize=10)
    plt.text(v_earth/1000 + 2, shift_cl_earth, f'{shift_cl_earth:.3f} λ',
             fontsize=10, va='center')

    plt.xlabel('Скорость относительно эфира (км/с)', fontsize=12)
    plt.ylabel('Сдвиг интерференционных полос (λ)', fontsize=12)
    plt.title('Классический vs релятивистский расчёт', fontsize=14, weight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=10, loc='upper left')
    plt.ylim([-0.05, max(shift_classical)*1.1])
    plt.tight_layout()

    plt.savefig('/home/user/aether-experiment/figures/classical_vs_relativistic.png', dpi=150)
    print("График сохранён: figures/classical_vs_relativistic.png")
    plt.close()


if __name__ == "__main__":
    compare_classical_and_relativistic()
    print("\nГенерация графиков...")
    plot_lorentz_contraction()
    plot_comparison()
    print("\nГотово!")
