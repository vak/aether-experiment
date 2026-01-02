#!/usr/bin/env python3
"""
Классический расчёт эксперимента Майкельсона-Морли
(с неявным предположением об абсолютном времени)
"""

import numpy as np
import matplotlib.pyplot as plt


class ClassicalMichelsonMorley:
    """
    Классическая модель эксперимента Майкельсона-Морли.

    Предполагает:
    - Абсолютное время
    - Абсолютное пространство
    - Движение относительно эфира со скоростью v
    """

    def __init__(self, L=11.0, c=299792458.0, wavelength=500e-9):
        """
        Параметры:
            L: длина плеча интерферометра (метры)
            c: скорость света (м/с)
            wavelength: длина волны света (метры)
        """
        self.L = L  # длина плеча
        self.c = c  # скорость света
        self.wavelength = wavelength  # длина волны

    def time_parallel(self, v):
        """
        Время прохождения света в продольном плече (классический расчёт).

        T_parallel = L/(c-v) + L/(c+v) = 2Lc/(c²-v²)

        Параметры:
            v: скорость движения относительно эфира (м/с)

        Возвращает:
            время прохождения туда-обратно (секунды)
        """
        if abs(v) >= self.c:
            raise ValueError("Скорость v должна быть меньше скорости света c")

        t_forward = self.L / (self.c - v)
        t_backward = self.L / (self.c + v)
        return t_forward + t_backward

    def time_perpendicular(self, v):
        """
        Время прохождения света в поперечном плече (классический расчёт).

        T_perp = 2L/√(c²-v²)

        Параметры:
            v: скорость движения относительно эфира (м/с)

        Возвращает:
            время прохождения туда-обратно (секунды)
        """
        if abs(v) >= self.c:
            raise ValueError("Скорость v должна быть меньше скорости света c")

        c_eff = np.sqrt(self.c**2 - v**2)
        return 2 * self.L / c_eff

    def time_difference(self, v):
        """
        Разность времён прохождения.

        ΔT = T_parallel - T_perp

        Параметры:
            v: скорость движения относительно эфира (м/с)

        Возвращает:
            разность времён (секунды)
        """
        return self.time_parallel(v) - self.time_perpendicular(v)

    def path_difference(self, v):
        """
        Разность хода лучей.

        Δ = c · ΔT

        Параметры:
            v: скорость движения относительно эфира (м/с)

        Возвращает:
            разность хода (метры)
        """
        return self.c * self.time_difference(v)

    def fringe_shift(self, v):
        """
        Ожидаемый сдвиг интерференционных полос.

        При повороте интерферометра на 90°, сдвиг удваивается:
        δ = 2Δ/λ

        Параметры:
            v: скорость движения относительно эфира (м/с)

        Возвращает:
            сдвиг в единицах длины волны (безразмерный)
        """
        delta = self.path_difference(v)
        return 2 * delta / self.wavelength

    def gamma(self, v):
        """
        Лоренц-фактор γ = 1/√(1 - v²/c²)

        Параметры:
            v: скорость (м/с)

        Возвращает:
            γ (безразмерный)
        """
        beta = v / self.c
        return 1.0 / np.sqrt(1 - beta**2)


def analyze_earth_velocity():
    """
    Анализ для скорости движения Земли по орбите.
    """
    print("=" * 60)
    print("КЛАССИЧЕСКИЙ АНАЛИЗ ЭКСПЕРИМЕНТА МАЙКЕЛЬСОНА-МОРЛИ")
    print("=" * 60)
    print()

    # Параметры эксперимента
    L = 11.0  # эффективная длина плеча (с учётом многократных отражений)
    c = 299792458.0  # скорость света (м/с)
    wavelength = 500e-9  # длина волны (500 нм)
    v_earth = 30000.0  # орбитальная скорость Земли (м/с, ~30 км/с)

    mm = ClassicalMichelsonMorley(L=L, c=c, wavelength=wavelength)

    print(f"Параметры эксперимента:")
    print(f"  Длина плеча: L = {L} м")
    print(f"  Скорость света: c = {c:.0f} м/с")
    print(f"  Длина волны: λ = {wavelength*1e9:.1f} нм")
    print(f"  Скорость Земли: v = {v_earth:.0f} м/с (~{v_earth/1000:.0f} км/с)")
    print(f"  v/c = {v_earth/c:.2e}")
    print()

    # Расчёты
    t_parallel = mm.time_parallel(v_earth)
    t_perp = mm.time_perpendicular(v_earth)
    dt = mm.time_difference(v_earth)
    path_diff = mm.path_difference(v_earth)
    shift = mm.fringe_shift(v_earth)
    gamma = mm.gamma(v_earth)

    print("Результаты классического расчёта:")
    print(f"  Время прохождения (продольное): T_∥ = {t_parallel:.15e} с")
    print(f"  Время прохождения (поперечное): T_⊥ = {t_perp:.15e} с")
    print(f"  Разность времён: ΔT = {dt:.15e} с")
    print(f"  Разность хода: Δ = {path_diff:.15e} м")
    print(f"  Ожидаемый сдвиг полос: δ = {shift:.4f} λ")
    print(f"  Лоренц-фактор: γ = {gamma:.12f}")
    print()

    # Проверка формул для малых v/c
    beta = v_earth / c
    gamma_approx = 1 + beta**2 / 2
    dt_approx = (2 * L / c) * beta**2 * 1.5
    shift_approx = 2 * L * v_earth**2 / (c**2 * wavelength)

    print("Приближённые формулы (для v << c):")
    print(f"  γ ≈ 1 + v²/(2c²) = {gamma_approx:.12f}")
    print(f"  ΔT ≈ (2L/c)·(3/2)·v²/c² = {dt_approx:.15e} с")
    print(f"  δ ≈ 2Lv²/(c²λ) = {shift_approx:.4f} λ")
    print()

    print("Вывод:")
    print(f"  Классический расчёт предсказывает сдвиг ~{shift:.2f} полосы")
    print(f"  Экспериментальная точность: ~0.01 полосы")
    print(f"  ОЖИДАЕТСЯ: наблюдаемый эффект!")
    print(f"  НАБЛЮДАЕТСЯ: эффект отсутствует (< 0.01 полосы)")
    print()


def plot_velocity_dependence():
    """
    График зависимости сдвига полос от скорости.
    """
    mm = ClassicalMichelsonMorley(L=11.0, c=299792458.0, wavelength=500e-9)

    # Диапазон скоростей (от 0 до 100 км/с)
    velocities = np.linspace(0, 100000, 1000)  # м/с

    # Вычисление сдвигов
    shifts = [mm.fringe_shift(v) for v in velocities]

    # График
    plt.figure(figsize=(10, 6))
    plt.plot(velocities/1000, shifts, 'b-', linewidth=2, label='Классическое предсказание')
    plt.axvline(x=30, color='r', linestyle='--', linewidth=2, label='Скорость Земли (~30 км/с)')
    plt.axhline(y=0.01, color='g', linestyle=':', linewidth=1, label='Предел обнаружения (~0.01 λ)')

    # Точка для скорости Земли
    v_earth = 30000
    shift_earth = mm.fringe_shift(v_earth)
    plt.plot(v_earth/1000, shift_earth, 'ro', markersize=10, label=f'Ожидание: {shift_earth:.3f} λ')

    plt.xlabel('Скорость относительно эфира (км/с)', fontsize=12)
    plt.ylabel('Сдвиг интерференционных полос (λ)', fontsize=12)
    plt.title('Классическое предсказание эксперимента Майкельсона-Морли', fontsize=14, weight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=10)
    plt.tight_layout()

    # Сохранение
    plt.savefig('/home/user/aether-experiment/figures/classical_prediction.png', dpi=150)
    print("График сохранён: figures/classical_prediction.png")
    plt.close()


def plot_time_components():
    """
    График компонентов времени прохождения света.
    """
    mm = ClassicalMichelsonMorley(L=11.0, c=299792458.0, wavelength=500e-9)

    velocities = np.linspace(0, 100000, 1000)  # м/с

    t_parallel = np.array([mm.time_parallel(v) for v in velocities])
    t_perp = np.array([mm.time_perpendicular(v) for v in velocities])
    t_diff = t_parallel - t_perp

    # Нормализация к времени при v=0
    t_0 = 2 * mm.L / mm.c
    t_parallel_norm = t_parallel / t_0
    t_perp_norm = t_perp / t_0

    plt.figure(figsize=(12, 5))

    # Левый график: абсолютные времена
    plt.subplot(1, 2, 1)
    plt.plot(velocities/1000, t_parallel*1e9, 'b-', linewidth=2, label='T_∥ (продольное)')
    plt.plot(velocities/1000, t_perp*1e9, 'r-', linewidth=2, label='T_⊥ (поперечное)')
    plt.axvline(x=30, color='gray', linestyle='--', alpha=0.5)
    plt.xlabel('Скорость (км/с)', fontsize=11)
    plt.ylabel('Время прохождения (нс)', fontsize=11)
    plt.title('Времена прохождения света', fontsize=12, weight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=10)

    # Правый график: разность времён
    plt.subplot(1, 2, 2)
    plt.plot(velocities/1000, t_diff*1e15, 'purple', linewidth=2)
    plt.axvline(x=30, color='r', linestyle='--', linewidth=2, alpha=0.7)
    plt.axhline(y=0, color='gray', linestyle='-', linewidth=0.5)
    v_earth = 30000
    dt_earth = mm.time_difference(v_earth)
    plt.plot(v_earth/1000, dt_earth*1e15, 'ro', markersize=10)
    plt.xlabel('Скорость (км/с)', fontsize=11)
    plt.ylabel('Разность времён ΔT (фс)', fontsize=11)
    plt.title('Разность времён T_∥ - T_⊥', fontsize=12, weight='bold')
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('/home/user/aether-experiment/figures/time_components.png', dpi=150)
    print("График сохранён: figures/time_components.png")
    plt.close()


if __name__ == "__main__":
    # Анализ
    analyze_earth_velocity()

    # Графики
    print("\nГенерация графиков...")
    plot_velocity_dependence()
    plot_time_components()
    print("\nГотово!")
