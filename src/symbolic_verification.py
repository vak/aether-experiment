#!/usr/bin/env python3
"""
Символическая верификация расчётов ММ через sympy.

Цель: получить тождества аналитически, не численно.
Численные тесты проверяют с погрешностью ~10⁻¹².
Символьный результат — точное тождество (0 без погрешности).

Проверяем:
1. T_∥ = (2L/c)·γ при L_∥ = L/γ  (корректный расчёт)
2. T_⊥ = (2L/c)·γ                 (поперечное плечо)
3. T_∥ - T_⊥ = 0                  (главный результат)
4. T_∥ ≠ T_⊥ при L_∥ = L          (классическая ошибка — ненулевая разность)
5. Лоренцевский буст: события в S и S' самосогласованы
"""

from sympy import (
    symbols, sqrt, simplify, factor, expand, cancel,
    Rational, Symbol, Function, latex, pretty
)


def run_symbolic():
    # ── Символы ───────────────────────────────────────────────────
    L, v, c = symbols('L v c', positive=True)
    gamma = 1 / sqrt(1 - v**2/c**2)

    print("=" * 60)
    print("СИМВОЛИЧЕСКАЯ ВЕРИФИКАЦИЯ (sympy)")
    print("=" * 60)
    print()

    # ── Тест 1: T_∥ с лоренцевым сокращением ─────────────────────
    L_par = L / gamma          # L/γ — сокращённая длина
    T_par_raw = L_par/(c - v) + L_par/(c + v)
    T_par = simplify(T_par_raw)

    expected_par = 2*L/c * gamma
    diff_par = simplify(T_par - expected_par)

    print("Тест 1: T_∥ с лоренцевым сокращением (L_∥ = L/γ)")
    print(f"  T_∥ = L/γ·(c-v)⁻¹ + L/γ·(c+v)⁻¹")
    print(f"  T_∥ = {T_par}")
    print(f"  T_∥ - (2L/c)·γ = {diff_par}")
    assert diff_par == 0, f"FAIL: diff = {diff_par}"
    print("  PASS: T_∥ = (2L/c)·γ  (точное тождество)\n")

    # ── Тест 2: T_⊥ ───────────────────────────────────────────────
    T_perp_raw = 2*L / sqrt(c**2 - v**2)
    T_perp = simplify(T_perp_raw)

    diff_perp = simplify(T_perp - expected_par)

    print("Тест 2: T_⊥ (поперечное плечо)")
    print(f"  T_⊥ = 2L/√(c²-v²)")
    print(f"  T_⊥ = {T_perp}")
    print(f"  T_⊥ - (2L/c)·γ = {diff_perp}")
    assert diff_perp == 0, f"FAIL: diff = {diff_perp}"
    print("  PASS: T_⊥ = (2L/c)·γ  (точное тождество)\n")

    # ── Тест 3: T_∥ = T_⊥ (главный результат) ────────────────────
    delta_T_correct = simplify(T_par - T_perp)

    print("Тест 3: ΔT с лоренцевым сокращением")
    print(f"  ΔT = T_∥ - T_⊥ = {delta_T_correct}")
    assert delta_T_correct == 0, f"FAIL: ΔT = {delta_T_correct}"
    print("  PASS: ΔT = 0  (точный нуль)\n")

    # ── Тест 4: классическая ошибка — L_∥ = L (без сокращения) ───
    T_par_classical = L/(c - v) + L/(c + v)   # L вместо L/γ
    T_par_classical_simplified = simplify(T_par_classical)

    delta_T_classical = simplify(T_par_classical - T_perp)
    delta_T_classical_factored = factor(delta_T_classical)

    print("Тест 4: ΔT без лоренцева сокращения (классическая ошибка, L_∥ = L)")
    print(f"  T_∥^(классика) = L/(c-v) + L/(c+v) = {T_par_classical_simplified}")
    print(f"  ΔT^(классика)  = {delta_T_classical_factored}")
    assert delta_T_classical_factored != 0, "FAIL: classical ΔT should be nonzero"
    print("  PASS: ΔT ≠ 0  (классика предсказывает ненулевой сдвиг)\n")

    # ── Тест 5: T_∥^(классика) = (2L/c)·γ² ──────────────────────
    expected_classical = 2*L/c * gamma**2
    diff_classical = simplify(T_par_classical - expected_classical)

    print("Тест 5: Классическая формула даёт γ², не γ")
    print(f"  T_∥^(классика) - (2L/c)·γ² = {diff_classical}")
    assert diff_classical == 0, f"FAIL: diff = {diff_classical}"
    print("  PASS: T_∥^(классика) = (2L/c)·γ²  (подтверждает ошибку)\n")

    # ── Тест 6: замедление времени — пересчёт в S' ───────────────
    # T^(S') = T^(S) / γ
    T_par_lab  = simplify(T_par  / gamma)
    T_perp_lab = simplify(T_perp / gamma)
    expected_lab = 2*L/c

    diff_lab_par  = simplify(T_par_lab  - expected_lab)
    diff_lab_perp = simplify(T_perp_lab - expected_lab)

    print("Тест 6: Пересчёт в лабораторную систему T^(S') = T^(S)/γ")
    print(f"  T_∥^(S') = (2L/c)·γ / γ = {T_par_lab}")
    print(f"  T_⊥^(S') = (2L/c)·γ / γ = {T_perp_lab}")
    print(f"  T_∥^(S') - 2L/c = {diff_lab_par}")
    print(f"  T_⊥^(S') - 2L/c = {diff_lab_perp}")
    assert diff_lab_par  == 0, f"FAIL: T_par_lab wrong"
    assert diff_lab_perp == 0, f"FAIL: T_perp_lab wrong"
    print("  PASS: T_∥^(S') = T_⊥^(S') = 2L/c  (точное тождество)\n")

    # ── Тест 7: ΔT^(классика) в лидирующем порядке по v/c ────────
    # ΔT_classical ≈ L·v²/c³ для малых v
    # Это то, что ожидал Майкельсон в 1887
    from sympy import series, O, symbols as sym

    beta = symbols('beta', positive=True)   # β = v/c
    L_s, c_s = symbols('L c', positive=True)

    T_par_cl_beta  = L_s / (c_s*(1 - beta)) + L_s / (c_s*(1 + beta))
    T_perp_beta = 2*L_s / (c_s * sqrt(1 - beta**2))

    dT_beta = simplify(T_par_cl_beta - T_perp_beta)
    dT_series = series(dT_beta, beta, 0, 4)

    print("Тест 7: ΔT^(классика) в малом порядке по β = v/c")
    print(f"  ΔT = {dT_series}")
    # Ведущий член должен быть ~ β²
    coeff_beta2 = dT_series.coeff(beta, 2)
    print(f"  Коэффициент при β²: {coeff_beta2}  (= L/c, ожидается L/c)")
    assert simplify(coeff_beta2 - L_s/c_s) == 0, "FAIL: leading term"
    print(f"  PASS: ΔT^(классика) = (L/c)·β² + O(β⁴)  ≡  Lv²/c³ + ...\n")

    # ── Итог ──────────────────────────────────────────────────────
    print("=" * 60)
    print("ИТОГ: все 7 символических тестов — точные тождества.")
    print()
    print("  Корректный расчёт (L_∥ = L/γ):")
    print("    T_∥ = T_⊥ = (2L/c)·γ  →  ΔT = 0  (точный нуль)")
    print()
    print("  Классический расчёт (L_∥ = L):")
    print("    T_∥ = (2L/c)·γ²,  T_⊥ = (2L/c)·γ")
    print("    ΔT = (2L/c)·γ(γ-1) ≠ 0")
    print()
    print("  Разница: γ² vs γ в продольном плече.")
    print("  Причина: отсутствие лоренцева сокращения в классическом расчёте.")
    print("=" * 60)


if __name__ == "__main__":
    run_symbolic()
