# Modelo financiero simplificado Rango Creative Studio - COP millones, 36 meses
# Fases: 1 (M1-6) portafolio, 2 (M7-18) traccion, 3 (M19-36) escala
LOAD = 1.5  # carga prestacional aprox sobre salario base (Colombia)

def phase(m):
    return 1 if m <= 6 else (2 if m <= 18 else 3)

def revenue(m, s):
    # s: escenario dict con proyectos/mes, ticket promedio, retainers
    p = phase(m)
    # rampa dentro de fase
    if p == 1:
        t = (m - 1) / 5
        proj = s['p1_proj'][0] + (s['p1_proj'][1]-s['p1_proj'][0]) * t
        ticket = s['p1_ticket'][0] + (s['p1_ticket'][1]-s['p1_ticket'][0]) * t
        ret = s['p1_ret'][0] + (s['p1_ret'][1]-s['p1_ret'][0]) * t
    elif p == 2:
        t = (m - 7) / 11
        proj = s['p2_proj'][0] + (s['p2_proj'][1]-s['p2_proj'][0]) * t
        ticket = s['p2_ticket'][0] + (s['p2_ticket'][1]-s['p2_ticket'][0]) * t
        ret = s['p2_ret'][0] + (s['p2_ret'][1]-s['p2_ret'][0]) * t
    else:
        t = (m - 19) / 17
        proj = s['p3_proj'][0] + (s['p3_proj'][1]-s['p3_proj'][0]) * t
        ticket = s['p3_ticket'][0] + (s['p3_ticket'][1]-s['p3_ticket'][0]) * t
        ret = s['p3_ret'][0] + (s['p3_ret'][1]-s['p3_ret'][0]) * t
    political = s['political'].get(m, 0)
    return proj * ticket + ret + political

def costs(m, rev, s):
    p = phase(m)
    cogs_ratio = {1: 0.45, 2: 0.40, 3: 0.38}[p]
    cogs = rev * cogs_ratio
    # nomina base mensual (COP M) x carga
    founders = {1: 2.0, 2: 4.0, 3: 8.0}[p] * 2
    team = {1: 0, 2: s['team2'], 3: s['team3']}[p]
    payroll = (founders + team) * LOAD
    space = {1: 1.2, 2: 3.5, 3: 9.0}[p]
    software = {1: 0.8, 2: 1.8, 3: 3.5}[p]
    admin = {1: 0.7, 2: 1.5, 3: 3.0}[p]
    marketing = max({1: 1.5, 2: 3.0, 3: 5.0}[p], rev * 0.08)
    equipment = {1: 0.8, 2: 2.5, 3: 5.0}[p]  # arriendo/leasing/depreciacion
    opex = payroll + space + software + admin + marketing + equipment
    return cogs, opex

scen = {
 'Conservador': dict(p1_proj=(1.5,2.5), p1_ticket=(3.5,5), p1_ret=(0,3),
                     p2_proj=(2.5,3.5), p2_ticket=(6,10), p2_ret=(4,12),
                     p3_proj=(3.5,4.5), p3_ticket=(12,20), p3_ret=(14,30),
                     team2=8.0, team3=28.0, political={}),
 'Base':        dict(p1_proj=(2,3), p1_ticket=(4,6), p1_ret=(0,5),
                     p2_proj=(3,4.5), p2_ticket=(8,14), p2_ret=(6,18),
                     p3_proj=(4,5.5), p3_ticket=(18,30), p3_ret=(22,45),
                     team2=12.0, team3=40.0,
                     political={9:15, 10:15, 11:20, 12:25, 13:30, 14:30, 15:30, 16:35, 17:40, 18:40, 19:45, 20:50, 21:50, 22:30}),
 'Agresivo':    dict(p1_proj=(2.5,3.5), p1_ticket=(5,8), p1_ret=(2,8),
                     p2_proj=(4,5.5), p2_ticket=(10,20), p2_ret=(10,28),
                     p3_proj=(5,7), p3_ticket=(25,45), p3_ret=(35,70),
                     team2=16.0, team3=60.0,
                     political={9:20, 10:25, 11:30, 12:40, 13:50, 14:50, 15:60, 16:60, 17:70, 18:70, 19:80, 20:90, 21:90, 22:50}),
}

for name, s in scen.items():
    cash = 0; min_cash = 0; min_m = 0; be = None; cum = 0
    years = {1: [0,0,0], 2: [0,0,0], 3: [0,0,0]}
    rows = []
    for m in range(1, 37):
        rev = revenue(m, s)
        cogs, opex = costs(m, rev, s)
        ebitda = rev - cogs - opex
        # capital de trabajo: clientes grandes pagan a 60-90 dias en fase 3 -> 15% de ingresos retenidos
        wc = rev * ({1: 0.0, 2: 0.05, 3: 0.15}[phase(m)])
        cash += ebitda - wc * 0.3
        if cash < min_cash: min_cash, min_m = cash, m
        if be is None and ebitda > 0 and m > 1: be = m
        y = (m-1)//12 + 1
        years[y][0] += rev; years[y][1] += cogs; years[y][2] += ebitda
        rows.append((m, rev, ebitda))
    print(f"\n=== {name} ===")
    for y in (1,2,3):
        r, c, e = years[y]
        print(f"Año {y}: ingresos {r:7.0f}M | margen bruto {(r-c)/r*100:4.0f}% | EBITDA {e:6.0f}M ({e/r*100:4.0f}%)")
    print(f"Break-even mensual: mes {be} | Caja mínima acumulada: {min_cash:.0f}M en mes {min_m} -> capital requerido ~{-min_cash*1.3:.0f}M (con 30% colchón)")
    for m in (1,6,12,18,24,36):
        r = rows[m-1]
        print(f"  M{m:2d}: ingresos {r[1]:6.1f}M  EBITDA {r[2]:6.1f}M")
