#!/usr/bin/env python3
"""
Расчёт эксперимента Майкельсона-Морли через физические события
и преобразования Лоренца.

Подход: задаём события в системе эфира S, где геометрия прозрачна.
Затем применяем лоренцевский буст, чтобы получить координаты в S' (лаборатория).
Равенство собственных времён возврата — не постулат, а результат вычисления.

Обозначения:
  S   — система эфира (preferred frame), интерферометр движется со скоростью +v
  S'  — система лаборатории (rest frame интерферометра)
  L   — собственная длина плеча (в S')
  t, x, y — координаты в S
  t', x', y' — координаты в S'
"""

import numpy as np

c = 299792458.0  # м/с


# ─── Преобразование Лоренца ──────────────────────────────────────

def boost(event, v):
    """
    Лоренцевский буст: S → S'  (S' движется со скоростью +v относительно S).

    Параметры:
        event: (t, x, y) — координаты события в S
        v: скорость S' относительно S

    Возвращает:
        (t', x', y') — координаты события в S'
    """
    t, x, y = event
    g = 1.0 / np.sqrt(1 - (v/c)**2)
    t_prime = g * (t - v*x / c**2)
    x_prime = g * (x - v*t)
    y_prime = y
    return (t_prime, x_prime, y_prime)


def boost_inverse(event_prime, v):
    """
    Обратный буст: S' → S.
    """
    return boost(event_prime, -v)


# ─── События в системе эфира S ───────────────────────────────────

def mm_events_aether(L, v):
    """
    Вычисляем координаты событий в системе S (эфир).

    Начало координат: светоделитель в момент t=0.
    Интерферометр движется вправо со скоростью v.

    В момент t=0:
      - Светоделитель: x=0, y=0
      - Продольное зеркало: x=L/γ (сокращено!), y=0
      - Поперечное зеркало: x=0, y=L (поперечный размер не сокращается)

    Возвращает dict с событиями {имя: (t, x, y)}.
    """
    g = 1.0 / np.sqrt(1 - (v/c)**2)
    L_par = L / g   # сокращённая длина продольного плеча в S

    events = {}

    # E0: испускание фотонов из светоделителя
    events['E0'] = (0.0, 0.0, 0.0)

    # ── Продольный фотон ──────────────────────────────────────────

    # E1: отражение от продольного зеркала.
    # За время t1 фотон прошёл c·t1 вправо.
    # Зеркало за это время сдвинулось с x=L_par до x=L_par + v·t1.
    # Условие встречи: c·t1 = L_par + v·t1
    t1 = L_par / (c - v)
    x1 = c * t1          # = L_par·c/(c-v)
    events['E1_par'] = (t1, x1, 0.0)

    # E2: возврат продольного фотона к светоделителю.
    # Фотон летит влево (-c), светоделитель летит вправо (+v).
    # Условие встречи: x1 - c·(t2-t1) = v·t2
    # x1 - c·t2 + c·t1 = v·t2  →  t2 = (x1 + c·t1)/(c+v)
    t2 = (x1 + c*t1) / (c + v)
    x2 = v * t2          # светоделитель в момент t2
    events['E2_par'] = (t2, x2, 0.0)

    # ── Поперечный фотон ──────────────────────────────────────────

    # E3: отражение от поперечного зеркала.
    # Фотон летит под углом θ, чтобы попасть в зеркало на y=L.
    # Горизонтальная компонента скорости: v (в ногу со зеркалом).
    # Вертикальная компонента: c_y = √(c²-v²).
    # Время: t3 = L / c_y
    c_y = np.sqrt(c**2 - v**2)
    t3 = L / c_y
    x3 = v * t3          # зеркало и фотон движутся горизонтально синхронно
    events['E3_perp'] = (t3, x3, L)

    # E4: возврат поперечного фотона к светоделителю.
    # По симметрии t4 = 2·t3, x4 = v·t4
    t4 = 2 * t3
    x4 = v * t4
    events['E4_perp'] = (t4, x4, 0.0)

    return events


# ─── Собственное время детектора ─────────────────────────────────

def proper_time(event_a, event_b, v):
    """
    Собственное время вдоль мировой линии светоделителя
    между двумя событиями.

    Светоделитель движется в S со скоростью v.
    Его собственное время: dτ = dt/γ (замедление времени).
    """
    g = 1.0 / np.sqrt(1 - (v/c)**2)
    dt = event_b[0] - event_a[0]
    return dt / g


# ─── Основной расчёт ─────────────────────────────────────────────

def run_analysis(L=11.0, v=30000.0):
    g = 1.0 / np.sqrt(1 - (v/c)**2)

    print("=" * 65)
    print("РАСЧЁТ ЧЕРЕЗ СОБЫТИЯ И ПРЕОБРАЗОВАНИЯ ЛОРЕНЦА")
    print("=" * 65)
    print(f"\nПараметры: L = {L} м, v = {v:.0f} м/с, γ = {g:.10f}")
    print(f"L/γ = {L/g:.12f} м\n")

    # ── Система эфира S ───────────────────────────────────────────
    events_S = mm_events_aether(L, v)

    print("СОБЫТИЯ В S (система эфира):")
    print("-" * 65)
    labels = {
        'E0':       'Испускание фотонов',
        'E1_par':   'Отражение: продольное зеркало',
        'E2_par':   'Возврат: продольный фотон',
        'E3_perp':  'Отражение: поперечное зеркало',
        'E4_perp':  'Возврат: поперечный фотон',
    }
    for key, label in labels.items():
        t, x, y = events_S[key]
        print(f"  {label}:")
        print(f"    t = {t:.15e} с,  x = {x:.6f} м,  y = {y:.3f} м")

    # Времена в S
    T_par_S  = events_S['E2_par'][0]  - events_S['E0'][0]
    T_perp_S = events_S['E4_perp'][0] - events_S['E0'][0]

    print(f"\n  T_∥  (в S) = {T_par_S:.15e} с  = (2L/c)·γ = {(2*L/c)*g:.15e}")
    print(f"  T_⊥  (в S) = {T_perp_S:.15e} с  = (2L/c)·γ = {(2*L/c)*g:.15e}")
    print(f"  ΔT   (в S) = {T_par_S - T_perp_S:.4e} с")

    # ── Буст в лабораторию S' ─────────────────────────────────────
    events_Sp = {k: boost(ev, v) for k, ev in events_S.items()}

    print("\nСОБЫТИЯ В S' (система лаборатории, после буста):")
    print("-" * 65)
    for key, label in labels.items():
        t, x, y = events_Sp[key]
        print(f"  {label}:")
        print(f"    t' = {t:.15e} с,  x' = {x:.6f} м,  y' = {y:.3f} м")

    T_par_Sp  = events_Sp['E2_par'][0]  - events_Sp['E0'][0]
    T_perp_Sp = events_Sp['E4_perp'][0] - events_Sp['E0'][0]

    print(f"\n  T_∥  (в S') = {T_par_Sp:.15e} с  = 2L/c = {2*L/c:.15e}")
    print(f"  T_⊥  (в S') = {T_perp_Sp:.15e} с  = 2L/c = {2*L/c:.15e}")
    print(f"  ΔT   (в S') = {T_par_Sp - T_perp_Sp:.4e} с")

    # ── Собственное время детектора ───────────────────────────────
    tau_par  = proper_time(events_S['E0'], events_S['E2_par'],  v)
    tau_perp = proper_time(events_S['E0'], events_S['E4_perp'], v)

    print("\nСОБСТВЕННОЕ ВРЕМЯ ДЕТЕКТОРА (τ = T_S / γ):")
    print("-" * 65)
    print(f"  τ_∥  = {tau_par:.15e} с  = 2L/c = {2*L/c:.15e}")
    print(f"  τ_⊥  = {tau_perp:.15e} с  = 2L/c = {2*L/c:.15e}")
    print(f"  Δτ   = {tau_par - tau_perp:.4e} с")

    # ── Проверка позиций зеркал в S' ──────────────────────────────
    print("\nПРОВЕРКА: позиции зеркал в S' в момент t'=0")
    print("-" * 65)

    # В S' интерферометр покоится. Зеркала должны быть на расстоянии L.
    # E1 в S' имеет t'≠0 (зеркало движется в S, поэтому событие смещено).
    # Но позиция зеркала в S' при t'=0: x'_mirror = x'(E1) - v'·t'(E1)
    # v' = 0 (зеркало покоится в S'), поэтому x'_mirror = x'(E1).

    # Однако правильнее смотреть на x' в момент t'=0.
    # Продольное зеркало в S покоится при x = L/γ (в момент t=0).
    # Буст события (t=0, x=L/γ, y=0):
    mirror_par_S = (0.0, L/g, 0.0)
    mirror_par_Sp = boost(mirror_par_S, v)
    print(f"  Продольное зеркало (при t'={mirror_par_Sp[0]:.3e} с): x' = {mirror_par_Sp[1]:.9f} м")

    mirror_perp_S = (0.0, 0.0, L)
    mirror_perp_Sp = boost(mirror_perp_S, v)
    print(f"  Поперечное зеркало (при t'={mirror_perp_Sp[0]:.3e} с): y' = {mirror_perp_Sp[2]:.9f} м")
    print(f"  Собственная длина L = {L} м — оба зеркала на расстоянии L в S'")

    # ── Итог ──────────────────────────────────────────────────────
    print("\n" + "=" * 65)
    print("ИТОГ:")
    print("=" * 65)
    print()
    print("  Система S (эфир):  T_∥ = T_⊥ = (2L/c)·γ")
    print("  Система S' (лаб):  T_∥ = T_⊥ = 2L/c")
    print("  Собственное время: τ_∥ = τ_⊥ = 2L/c")
    print()
    print("  Разность фаз Δφ = 0 — получена из вычисления, не из постулата.")
    print()

    return events_S, events_Sp


# ─── Тесты ────────────────────────────────────────────────────────

def run_tests():
    """Assert-based тесты для событийного расчёта."""
    print("=" * 65)
    print("ТЕСТЫ")
    print("=" * 65)
    L = 11.0
    passed = 0

    for v in [100.0, 1e4, 3e4, 1e7, 0.5*c, 0.9*c]:
        g = 1.0 / np.sqrt(1 - (v/c)**2)
        events_S  = mm_events_aether(L, v)
        events_Sp = {k: boost(ev, v) for k, ev in events_S.items()}

        T_par_S  = events_S['E2_par'][0]
        T_perp_S = events_S['E4_perp'][0]

        T_par_Sp  = events_Sp['E2_par'][0]
        T_perp_Sp = events_Sp['E4_perp'][0]

        tau_par  = proper_time(events_S['E0'], events_S['E2_par'],  v)
        tau_perp = proper_time(events_S['E0'], events_S['E4_perp'], v)

        expected_S  = (2*L/c) * g
        expected_Sp = 2*L/c

        tol = 1e-12

        # T_∥ = T_⊥ = (2L/c)·γ в S
        assert abs(T_par_S  - expected_S) / expected_S < tol, f"T_par_S  wrong at v={v}"
        assert abs(T_perp_S - expected_S) / expected_S < tol, f"T_perp_S wrong at v={v}"

        # T_∥ = T_⊥ = 2L/c в S'
        assert abs(T_par_Sp  - expected_Sp) / expected_Sp < tol, f"T_par_Sp  wrong at v={v}"
        assert abs(T_perp_Sp - expected_Sp) / expected_Sp < tol, f"T_perp_Sp wrong at v={v}"

        # τ_∥ = τ_⊥ = 2L/c
        assert abs(tau_par  - expected_Sp) / expected_Sp < tol, f"tau_par  wrong at v={v}"
        assert abs(tau_perp - expected_Sp) / expected_Sp < tol, f"tau_perp wrong at v={v}"

        # Светоделитель возвращается в x'=0 (покоится в S')
        assert abs(events_Sp['E2_par'][1])  < 1e-6, f"beamsplitter x' nonzero at v={v}"
        assert abs(events_Sp['E4_perp'][1]) < 1e-6, f"beamsplitter x' nonzero at v={v}"

        print(f"  PASS v = {v:.2e} м/с  "
              f"(γ = {g:.6f}, T_S = {T_par_S:.6e}, T_S' = {T_par_Sp:.6e})")
        passed += 1

    # Буст и обратный буст = тождество
    ev = (1.23e-7, 5.0, 3.0)
    for v_test in [1e4, 3e4, 0.5*c]:
        ev_back = boost_inverse(boost(ev, v_test), v_test)
        for a, b in zip(ev, ev_back):
            assert abs(a - b) < 1e-10 * (abs(a) + 1e-30), "boost inverse failed"
    print("  PASS буст + обратный буст = тождество")
    passed += 1

    print(f"\nРезультат: {passed}/{passed} тестов пройдено\n")


if __name__ == "__main__":
    run_tests()
    run_analysis(L=11.0, v=30000.0)
