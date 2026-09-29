# -*- coding: utf-8 -*-
"""
bfup_ex4.py – noyau de calcul et de tracé de l'exemple 4 (Application 7)
Renforcement à la fatigue d'une dalle de roulement d'un pont-route au moyen du BFUP armé :
vérification de la sécurité structurale à l'état limite de fatigue (type 4) par rapport à la limite de fatigue.

Cours « Structures existantes : chapitres choisis », p. 45-47.
Unités internes : N, mm, MPa ; résultats en kN/m, kNm/m.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

B = 1000.0
C_CONC, C_UHPC, C_STEEL, C_COMP, C_TENS, C_NA = "0.85", "0.55", "k", "#b2182b", "#2166ac", "#d6604d"
plt.rcParams.update({"font.size": 9, "axes.titlesize": 10, "axes.titleweight": "bold",
                     "axes.spines.top": False, "axes.spines.right": False})

LEVELS = ("centre de la couche de BFUP (corrigé)", "fibre supérieure du BFUP")


def bar_area(phi, s):
    """Aire d'armature par mètre [mm²/m] pour Ø phi [mm] tous les s [mm]."""
    return np.pi * phi**2 / 4.0 * B / s


def trap(f, y):
    return float(np.sum(0.5 * (f[1:] + f[:-1]) * np.diff(y)))


def bisect(f, a, b, tol=1e-7, nmax=300):
    fa, fb = f(a), f(b)
    if fa * fb > 0:
        raise ValueError("Pas de changement de signe dans l'intervalle")
    for _ in range(nmax):
        m = 0.5 * (a + b)
        fm = f(m)
        if abs(b - a) < tol:
            break
        if fa * fm <= 0:
            b, fb = m, fm
        else:
            a, fa = m, fm
    return 0.5 * (a + b)


def input_box(ax, items, title="Données d'entrée"):
    ax.axis("off")
    ax.set_title(title, loc="left")
    txt = "\n".join(f"{k:<14s} {v}" for k, v in items)
    ax.text(0.0, 0.98, txt, va="top", ha="left", family="monospace",
            fontsize=7.8, transform=ax.transAxes)


def table(ax, cols, rows, title, summary=None):
    ax.axis("off")
    ax.set_title(title, loc="left")
    t = ax.table(cellText=rows, colLabels=cols, loc="upper center",
                 cellLoc="center", bbox=[0, 0.38 if summary else 0.0, 1, 0.62 if summary else 1])
    t.auto_set_font_size(False)
    t.set_fontsize(7.8)
    for (r, c), cell in t.get_celld().items():
        cell.set_linewidth(0.4)
        if r == 0:
            cell.set_text_props(weight="bold")
            cell.set_facecolor("0.93")
    if summary:
        ax.text(0.0, 0.33, "\n".join(summary), va="top", ha="left", fontsize=8,
                family="monospace", transform=ax.transAxes)


def draw_layered_section(ax, h_c, h_U, bars, x_na=None, title="Section (b = 1 m)"):
    w = 1.0
    ax.add_patch(Rectangle((0, 0), w, h_c, fc=C_CONC, ec="k", hatch="///", lw=0.8))
    ax.add_patch(Rectangle((0, h_c), w, h_U, fc=C_UHPC, ec="k", lw=0.8))
    ax.text(w / 2, h_c + h_U / 2, "BFUP armé", ha="center", va="center", fontsize=8,
            color="w", weight="bold", bbox=dict(fc=C_UHPC, ec="none", pad=0.5))
    ax.text(w / 2, h_c * 0.12, "béton armé", ha="center", fontsize=8,
            bbox=dict(fc=C_CONC, ec="none", pad=0.5))
    for y, lab in bars:
        xs = np.linspace(0.08, 0.92, 7) * w
        ax.plot(xs, [y] * len(xs), "o", color=C_STEEL, ms=3.5)
        ax.text(w + 0.04, y, lab, va="center", fontsize=7.5)
    # cotes
    ax.annotate("", (-0.12, 0), (-0.12, h_c), arrowprops=dict(arrowstyle="<->", lw=0.7))
    ax.text(-0.15, h_c / 2, f"h_c={h_c:.0f}", rotation=90, ha="right", va="center", fontsize=7.5)
    ax.annotate("", (-0.12, h_c), (-0.12, h_c + h_U), arrowprops=dict(arrowstyle="<->", lw=0.7))
    ax.text(-0.15, h_c + h_U / 2, f"h_U={h_U:.0f}", rotation=90, ha="right", va="center", fontsize=7.5)
    if x_na is not None:
        ax.axhline(x_na, color=C_NA, ls="--", lw=1)
        ax.text(w / 2, x_na + 3, f"axe neutre x = {x_na:.1f} mm", color=C_NA, ha="center", fontsize=7.5,
                bbox=dict(fc="w", ec="none", pad=0.5))
    ax.set_xlim(-0.45, w + 0.75)
    ax.set_ylim(-8, h_c + h_U + 12)
    ax.set_xticks([])
    ax.spines["bottom"].set_visible(False)
    ax.set_ylabel("y depuis la fibre inférieure [mm]")
    ax.set_title(title)


def draw_strain(ax, y_ref, eps_ref, x, y_top, marks, title="Déformations"):
    """Profil linéaire : eps(y_ref) = eps_ref [‰], eps(x) = 0."""
    k = eps_ref / (y_ref - x)
    y = np.array([0.0, y_top])
    e = k * (y - x)
    ax.fill_betweenx([0, x], 0, [e[0], 0], color=C_COMP, alpha=0.25)
    ax.fill_betweenx([x, y_top], 0, [0, e[1]], color=C_TENS, alpha=0.25)
    ax.plot(e, y, "k", lw=1)
    ax.axvline(0, color="k", lw=0.6)
    ax.axhline(x, color=C_NA, ls="--", lw=1)
    for yy, lab in marks:
        ev = k * (yy - x)
        ax.plot(ev, yy, "o", color="k", ms=3)
        ax.text(ev, yy, f"  {lab} = {ev:.2f}‰", va="center",
                ha="left" if ev >= 0 else "right", fontsize=7.5)
    lim = 1.25 * max(abs(e).max(), 1e-9)
    ax.set_xlim(-lim * 1.6, lim * 1.9)
    ax.set_ylim(-8, y_top + 12)
    ax.set_xlabel("ε [‰]  (traction +)")
    ax.set_yticklabels([])
    ax.set_title(title)
    return k


def draw_stress(ax, continua, bar_notes, x, y_top, title="Contraintes (béton, BFUP)"):
    """continua : liste de (y_array, sigma_array, couleur, label)."""
    smax = 1.0
    for y, s, c, lab in continua:
        ax.fill_betweenx(y, 0, s, color=c, alpha=0.45, lw=0)
        ax.plot(s, y, color=c, lw=1)
        i = np.argmax(np.abs(s))
        ax.text(s[i], y[i], f" {lab}: {s[i]:.1f} MPa", fontsize=7.5, va="center",
                ha="left" if s[i] >= 0 else "right")
        smax = max(smax, np.abs(s).max())
    ax.axvline(0, color="k", lw=0.6)
    ax.axhline(x, color=C_NA, ls="--", lw=1)
    for yy, txt in bar_notes:
        ax.plot(0, yy, "o", color=C_STEEL, ms=3)
        ax.text(0.03 * smax, yy - 4, txt, fontsize=7, va="top")
    ax.set_xlim(-2.3 * smax, 2.3 * smax)
    ax.set_ylim(-8, y_top + 12)
    ax.set_xlabel("σ [MPa]")
    ax.set_yticklabels([])
    ax.set_title(title)


def draw_forces(ax, forces, y_top, unit="kN/m", title="Forces internes"):
    """forces : liste de (label, F, y). F>0 traction."""
    Fm = max(abs(F) for _, F, _ in forces)
    seen = {}
    for lab, F, y in forces:
        n = seen.get(round(y), 0)
        seen[round(y)] = n + 1
        c = C_TENS if F > 0 else C_COMP
        ax.annotate("", xy=(F, y), xytext=(0, y),
                    arrowprops=dict(arrowstyle="-|>", color=c, lw=1.8, shrinkA=0, shrinkB=0))
        ax.text(F, y + (9 * n if n else -9) if y > 100 else y, f" {lab} = {F:.1f}", color=c, fontsize=7.5,
                ha="left" if F > 0 else "right", va="bottom" if (n or y <= 100) else "top")
    ax.axvline(0, color="k", lw=0.6)
    ax.set_xlim(-1.9 * Fm, 1.9 * Fm)
    ax.set_ylim(-8, y_top + 12)
    ax.set_xlabel(f"F [{unit}]")
    ax.set_yticklabels([])
    ax.set_title(title)



def ex4_inputs():
    return dict(
        h_c=180.0, h_U=40.0, d_sU=190.0, d_sc=160.0,
        f_Ute=7.5, f_Utu=9.0, E_U=50000.0, eps_Utu=1.5, E_U_app=15000.0,
        E_c=40000.0, f_cd=20.0, E_s=200000.0, f_sy=500.0,
        A_sU=905.0, A_sc=1610.0,
        m_fat=59.0, m_Rd=136.0, dsig_sD=116.0,
        k_UD=0.3, k_cD=0.5, k_elem=0.5,      # σ_U,D = k_UD(f_Ute+f_Utu) ; σ_cd,D = k_cD f_cd ; m_R,D = k_elem m_Rd
        level=LEVELS[0],
        x_iter=(80.0, 75.0, 77.0),
    )


def y_ref_of(p):
    return p["h_c"] + (p["h_U"] / 2 if p["level"] == LEVELS[0] else p["h_U"])


def ex4_state(p, x):
    """État de section à la limite de fatigue : ε_Ut,D = σ_U,D / E_U,app imposé au niveau y_ref ;
    BFUP à σ_U,D uniforme sur h_U ; aciers et béton élastiques ; traction du béton négligée."""
    y_ref = y_ref_of(p)
    d_U = p["h_c"] + p["h_U"] / 2
    sUD = p["k_UD"] * (p["f_Ute"] + p["f_Utu"])
    eD = sUD / p["E_U_app"]
    k = eD / (y_ref - x)
    eps = lambda y: k * (y - x)
    rows = []
    for n, e, A, s, d in (("BFUP", eD, p["h_U"] * B, sUD, d_U),
                          ("A_sU", eps(p["d_sU"]), p["A_sU"], p["E_s"] * eps(p["d_sU"]), p["d_sU"]),
                          ("A_sc", eps(p["d_sc"]), p["A_sc"], p["E_s"] * eps(p["d_sc"]), p["d_sc"])):
        rows.append((n, e * 1e3, A, s, A * s / 1e3, d, A * s * d / 1e6))
    s_cmax = p["E_c"] * eps(0.0)
    F_c = 0.5 * s_cmax * x * B / 1e3
    rows.append(("Béton", eps(0) * 1e3, 0.75 * x * B, p["E_c"] * eps(x / 3), F_c, x / 3, F_c * x / 3 / 1e3))
    return dict(rows=rows, sumF=sum(r[4] for r in rows), m=sum(r[6] for r in rows), x=x, k=k,
                s_cmax=s_cmax, sUD=sUD, eD=eD, y_ref=y_ref, eps=eps)


def solve_x(p):
    lo, hi = 5.0, min(p["h_c"], y_ref_of(p)) - 1.0
    return bisect(lambda xx: ex4_state(p, xx)["sumF"], lo, hi)


def ex4_compute(p=None):
    p = ex4_inputs() if p is None else {**ex4_inputs(), **p}
    mRD1 = p["k_elem"] * p["m_Rd"]
    scD = p["k_cD"] * p["f_cd"]
    x = solve_x(p)
    st = ex4_state(p, x)
    iters = [ex4_state(p, xi) for xi in p["x_iter"]]
    s_sU = st["rows"][1][3]
    s_sc = st["rows"][2][3]
    checks = [("m_d(Q_fat) / m_R,D (étape 1)", p["m_fat"] / mRD1),
              ("m_d(Q_fat) / m_R,D (étape 2)", p["m_fat"] / st["m"]),
              ("σ_U / σ_U,D", 1.0),
              ("Δσ_sU / Δσ_sd,D", s_sU / p["dsig_sD"]),
              ("Δσ_sc / Δσ_sd,D", s_sc / p["dsig_sD"]),
              ("σ_c,max / σ_cd,D", abs(st["s_cmax"]) / scD)]
    return dict(p=p, mRD1=mRD1, scD=scD, x=x, st=st, iters=iters, s_sU=s_sU, s_sc=s_sc,
                ok1=p["m_fat"] <= mRD1, ok2=p["m_fat"] <= st["m"], checks=checks,
                ok_mat=(s_sU <= p["dsig_sD"] and s_sc <= p["dsig_sD"] and abs(st["s_cmax"]) <= scD))


def sweep_E_app(p, E_values):
    out = []
    for E in E_values:
        r = ex4_compute({**p, "E_U_app": E})
        out.append((E, r["st"]["m"], r["s_sU"], abs(r["st"]["s_cmax"]), r["x"]))
    return np.array(out)


def E_app_required(p):
    """E_U,app pour lequel m_R,D (étape 2) = m_d(Q_fat) ; None si hors de [2, 50] GPa."""
    f = lambda E: ex4_compute({**p, "E_U_app": E})["st"]["m"] - p["m_fat"]
    lo, hi = 2000.0, 50000.0
    if f(lo) * f(hi) > 0:
        return None
    return bisect(f, lo, hi, tol=1.0)


def E_app_concrete_limit(p):
    """E_U,app minimal pour que σ_c,max (fibre inférieure) ≤ σ_cd,D ; None si hors de [2, 50] GPa."""
    f = lambda E: abs(ex4_compute({**p, "E_U_app": E})["st"]["s_cmax"]) - p["k_cD"] * p["f_cd"]
    lo, hi = 2000.0, 50000.0
    if f(lo) * f(hi) > 0:
        return None
    return bisect(f, lo, hi, tol=1.0)


def E_app_steel_limit(p):
    """E_U,app minimal pour que Δσ_sU ≤ Δσ_sd,D ; None si hors de [2, 50] GPa."""
    f = lambda E: ex4_compute({**p, "E_U_app": E})["s_sU"] - p["dsig_sD"]
    lo, hi = 2000.0, 50000.0
    if f(lo) * f(hi) > 0:
        return None
    return bisect(f, lo, hi, tol=1.0)


def draw_checks(ax, r):
    labs = [c[0].replace(" (", "\n(").replace(" / ", " /\n") for c in r["checks"]]
    vals = [c[1] for c in r["checks"]]
    b = ax.bar(range(len(vals)), vals, color=[C_TENS if v <= 1.0 + 1e-9 else C_COMP for v in vals], width=0.6)
    ax.bar_label(b, fmt="%.2f", fontsize=8)
    ax.axhline(1, color="k", ls="--", lw=0.8)
    ax.set_xticks(range(len(vals)), labs, fontsize=7.5)
    ax.set_ylim(0, max(1.3, max(vals) * 1.15))
    ax.set_ylabel("taux d'utilisation [-]")
    ax.set_title("Vérifications à la limite de fatigue")
