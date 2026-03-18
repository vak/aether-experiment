#!/usr/bin/env python3
"""
Независимая верификация расчётов эксперимента Майкельсона-Морли.

Проверяет:
1. Алгебраические тождества (аналитические формулы vs прямой расчёт)
2. Самосогласованность (S_lab vs S_aether дают одинаковые наблюдаемые)
3. Предельные случаи (v→0, v→c)
4. Классический расчёт даёт ненулевой результат (для сравнения)

Использует assert вместо print-driven "самопроверки".
"""

import sys
import numpy as np

# Вычисляем всё из первых принципов, НЕ импортируя наши классы.
# Это гарантирует, что мы не проверяем код самим собой.

c = 299792458.0  # м/с


def gamma(v):
    return 1.0 / np.sqrt(1 - (v/c)**2)


# ─── Тест 1: Алгебраическое тождество ──────────────────────────

def test_parallel_time_equals_gamma():
    """
    Проверяем тождество:
      2(L/γ)c/(c²-v²) = (2L/c)·γ

    Это ключевое тождество: время прохождения в продольном плече
    (с лоренцевым сокращением) равно (2L/c)·γ.
    """
    L = 11.0
    for v in [100, 1000, 10000, 30000, 100000, 1e7, 0.5*c, 0.9*c, 0.99*c]:
        g = gamma(v)
        L_par = L / g

        # Прямой расчёт: t_forward + t_backward
        lhs = L_par/(c - v) + L_par/(c + v)

        # Аналитическая формула
        rhs = (2*L/c) * g

        rel_err = abs(lhs - rhs) / rhs
        assert rel_err < 1e-12, \
            f"FAIL at v={v}: lhs={lhs}, rhs={rhs}, rel_err={rel_err}"

    print("PASS: T_∥^(aether) = (2L/c)·γ  для всех v")


# ─── Тест 2: Перпендикулярное время тоже = (2L/c)·γ ────────────

def test_perp_time_equals_gamma():
    """
    Проверяем:
      2L/√(c²-v²) = (2L/c)·γ
    """
    L = 11.0
    for v in [100, 30000, 1e7, 0.5*c, 0.9*c, 0.99*c]:
        lhs = 2*L / np.sqrt(c**2 - v**2)
        rhs = (2*L/c) * gamma(v)

        rel_err = abs(lhs - rhs) / rhs
        assert rel_err < 1e-12, \
            f"FAIL at v={v}: lhs={lhs}, rhs={rhs}, rel_err={rel_err}"

    print("PASS: T_⊥^(aether) = (2L/c)·γ  для всех v")


# ─── Тест 3: T_∥ = T_⊥ в системе эфира ────────────────────────

def test_aether_times_equal():
    """
    Главный тест: с лоренцевым сокращением T_∥ = T_⊥ в системе эфира.
    """
    L = 11.0
    for v in [100, 30000, 1e7, 0.5*c, 0.9*c, 0.99*c]:
        g = gamma(v)
        L_par = L / g

        T_par = L_par/(c-v) + L_par/(c+v)
        T_perp = 2*L / np.sqrt(c**2 - v**2)

        rel_err = abs(T_par - T_perp) / T_perp
        assert rel_err < 1e-12, \
            f"FAIL at v={v}: T_par={T_par}, T_perp={T_perp}, rel_err={rel_err}"

    print("PASS: T_∥ = T_⊥ в S_aether (с лоренцевым сокращением)")


# ─── Тест 4: Классический расчёт даёт НЕНУЛЕВОЙ результат ──────

def test_classical_nonzero():
    """
    Без лоренцева сокращения разность времён ≠ 0.
    Это подтверждает, что классический расчёт действительно отличается.
    """
    L = 11.0
    v = 30000.0

    # Классический: L_∥ = L (без сокращения)
    T_par_classical = L/(c-v) + L/(c+v)
    T_perp = 2*L / np.sqrt(c**2 - v**2)

    dT = T_par_classical - T_perp
    assert dT > 1e-17, \
        f"FAIL: classical ΔT should be > 0, got {dT}"

    # Проверим порядок величины: ΔT ≈ Lv²/c³
    dT_approx = L * v**2 / c**3
    assert abs(dT - dT_approx) / dT < 0.5, \
        f"FAIL: ΔT={dT} not close to Lv²/c³={dT_approx}"

    print(f"PASS: Классический ΔT = {dT:.4e} с ≠ 0 (подтверждает наличие ошибки)")


# ─── Тест 5: Пересчёт в лабораторное время ─────────────────────

def test_lab_time_conversion():
    """
    T^(lab) = T^(aether) / γ = 2L/c для обоих плеч.
    """
    L = 11.0
    expected = 2 * L / c

    for v in [100, 30000, 1e7, 0.5*c, 0.9*c]:
        g = gamma(v)
        L_par = L / g

        T_par_aether = L_par/(c-v) + L_par/(c+v)
        T_perp_aether = 2*L / np.sqrt(c**2 - v**2)

        T_par_lab = T_par_aether / g
        T_perp_lab = T_perp_aether / g

        assert abs(T_par_lab - expected) / expected < 1e-12, \
            f"FAIL T_par_lab at v={v}: {T_par_lab} != {expected}"
        assert abs(T_perp_lab - expected) / expected < 1e-12, \
            f"FAIL T_perp_lab at v={v}: {T_perp_lab} != {expected}"

    print("PASS: T^(lab) = T^(aether)/γ = 2L/c")


# ─── Тест 6: Предельный случай v → 0 ──────────────────────────

def test_limit_v_zero():
    """
    При v → 0: γ → 1, все времена → 2L/c.
    """
    L = 11.0
    v = 1e-10  # почти ноль
    g = gamma(v)
    T0 = 2 * L / c

    assert abs(g - 1.0) < 1e-20, f"γ should be ≈1, got {g}"

    L_par = L / g
    T_par = L_par/(c-v) + L_par/(c+v)
    T_perp = 2*L / np.sqrt(c**2 - v**2)

    assert abs(T_par - T0) / T0 < 1e-15, f"T_par should ≈ 2L/c at v→0"
    assert abs(T_perp - T0) / T0 < 1e-15, f"T_perp should ≈ 2L/c at v→0"

    print("PASS: v → 0 предел корректен")


# ─── Тест 7: Инвариантность наблюдаемого ───────────────────────

def test_observable_frame_independent():
    """
    Разность фаз (наблюдаемая) не зависит от выбора системы отсчёта.

    В S_aether: ΔT = 0 (координатное время)
    В S_lab:    ΔT = 0 (собственное время)

    Разность фаз Δφ = ω·ΔT = 0 в обоих случаях.
    """
    L = 11.0
    for v in [30000, 1e7, 0.5*c, 0.9*c]:
        g = gamma(v)
        L_par = L / g

        # S_aether
        T_par_ae = L_par/(c-v) + L_par/(c+v)
        T_perp_ae = 2*L / np.sqrt(c**2 - v**2)
        dT_ae = T_par_ae - T_perp_ae

        # S_lab (через пересчёт)
        dT_lab = dT_ae / g  # разность тоже делится на γ

        # Оба должны быть ≈0
        assert abs(dT_ae) < 1e-20 or abs(dT_ae)/T_par_ae < 1e-12, \
            f"ΔT_aether not ≈ 0 at v={v}"
        assert abs(dT_lab) < 1e-20 or abs(dT_lab)/(T_par_ae/g) < 1e-12, \
            f"ΔT_lab not ≈ 0 at v={v}"

    print("PASS: Наблюдаемая (Δφ = 0) одинакова в обеих СО")


# ─── Тест 8: Алгебраическая ошибка γ³ ──────────────────────────

def test_gamma_cubed_is_wrong():
    """
    Проверяем, что формула с γ³ (из ошибочной версии документа) НЕВЕРНА.

    Ошибочная формула:     T_∥ = (2L/c)·γ³
    Правильная формула:    T_∥ = (2L/c)·γ

    Если γ³ была бы верна, разность T_∥ - T_⊥ была бы ненулевой.
    """
    L = 11.0
    v = 30000.0
    g = gamma(v)

    T_wrong = (2*L/c) * g**3
    T_correct = (2*L/c) * g
    T_perp = (2*L/c) * g

    # Прямой расчёт
    L_par = L / g
    T_direct = L_par/(c-v) + L_par/(c+v)

    # Правильная формула совпадает с прямым расчётом
    assert abs(T_correct - T_direct) / T_direct < 1e-12, \
        f"Correct formula doesn't match direct: {T_correct} vs {T_direct}"

    # Ошибочная формула НЕ совпадает
    assert abs(T_wrong - T_direct) / T_direct > 1e-8, \
        f"Wrong formula shouldn't match direct: {T_wrong} vs {T_direct}"

    # Ошибочная разность
    dT_wrong = T_wrong - T_perp
    assert abs(dT_wrong) > 1e-20, \
        f"Wrong formula should give ΔT ≠ 0"

    print(f"PASS: γ³ формула неверна (даёт ΔT = {dT_wrong:.4e} с вместо 0)")


# ─── Главная функция ───────────────────────────────────────────

def main():
    print("=" * 60)
    print("ВЕРИФИКАЦИЯ РАСЧЁТОВ")
    print("Все вычисления из первых принципов, без импорта классов")
    print("=" * 60)
    print()

    tests = [
        test_parallel_time_equals_gamma,
        test_perp_time_equals_gamma,
        test_aether_times_equal,
        test_classical_nonzero,
        test_lab_time_conversion,
        test_limit_v_zero,
        test_observable_frame_independent,
        test_gamma_cubed_is_wrong,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"FAIL: {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"ERROR: {test.__name__}: {e}")
            failed += 1

    print()
    print(f"Результат: {passed}/{passed+failed} тестов пройдено")

    if failed > 0:
        print(f"ОШИБКИ: {failed} тест(ов) не пройдено!")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
