# -*- coding: utf-8 -*-
"""
Applet Streamlit – Exemple 4 (Application 7)
Renforcement à la fatigue d'une dalle de roulement d'un pont-route au moyen du BFUP armé

Lancer localement :  streamlit run app.py
"""
import io

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

import bfup_ex4 as core

st.set_page_config(page_title="BFUP armé – fatigue | Ex. 4", layout="wide")
D = core.ex4_inputs()

# ----------------------------------------------------------------------------
# Entrées
# ----------------------------------------------------------------------------
with st.sidebar:
    st.header("Données d'entrée")
    st.caption("Valeurs par défaut : énoncé du cours (p. 45).")

    st.subheader("Actions et résistance")
    m_fat = st.number_input("m_d(Q_fat) [kNm/m]", 0.0, 500.0, D["m_fat"], 1.0)
    m_Rd = st.number_input("m_Rd – ELU type 2 [kNm/m]", 1.0, 1000.0, D["m_Rd"], 1.0)

    st.subheader("Géométrie (b = 1 m)")
    h_c = st.number_input("h_c – dalle existante [mm]", 100.0, 400.0, D["h_c"], 5.0)
    h_U = st.number_input("h_U – couche de BFUP [mm]", 20.0, 120.0, D["h_U"], 5.0)
    d_sU = st.number_input("d_sU – armature du BFUP [mm]", 50.0, 520.0, D["d_sU"], 1.0)
    d_sc = st.number_input("d_sc – armature de la dalle [mm]", 50.0, 400.0, D["d_sc"], 1.0)
    A_sU = st.number_input("A_sU [mm²/m]", 0.0, 5000.0, D["A_sU"], 5.0)
    A_sc = st.number_input("A_sc [mm²/m]", 0.0, 5000.0, D["A_sc"], 5.0)

    st.subheader("BFUP")
    f_Ute = st.number_input("f_Ute [MPa]", 1.0, 20.0, D["f_Ute"], 0.5)
    f_Utu = st.number_input("f_Utu [MPa]", 1.0, 20.0, D["f_Utu"], 0.5)
    E_U = st.number_input("E_U [MPa]", 20000.0, 70000.0, D["E_U"], 1000.0)
    E_U_app = st.number_input("E_U,app – module apparent écrouissant [MPa]", 2000.0, 50000.0, D["E_U_app"], 500.0,
                              help="Le cours suggère 10 GPa pour tenir compte de l'endommagement du BFUP en fatigue.")
    level = st.radio("Niveau où ε_Ut,D est imposé", core.LEVELS)

    st.subheader("Béton et acier")
    E_c = st.number_input("E_c [MPa]", 15000.0, 50000.0, D["E_c"], 1000.0)
    f_cd = st.number_input("f_cd [MPa]", 5.0, 80.0, D["f_cd"], 1.0)
    E_s = st.number_input("E_s [MPa]", 180000.0, 220000.0, D["E_s"], 1000.0)
    dsig_sD = st.number_input("Δσ_sd,D – limite de fatigue de l'acier [MPa]", 20.0, 300.0, D["dsig_sD"], 1.0)

    with st.expander("Limites de fatigue (coefficients)"):
        k_elem = st.number_input("m_R,D = k · m_Rd (étape 1)", 0.1, 1.0, D["k_elem"], 0.05)
        k_UD = st.number_input("σ_U,D = k · (f_Ute + f_Utu)", 0.1, 1.0, D["k_UD"], 0.05)
        k_cD = st.number_input("σ_cd,D = k · f_cd", 0.1, 1.0, D["k_cD"], 0.05)

p = dict(m_fat=m_fat, m_Rd=m_Rd, h_c=h_c, h_U=h_U, d_sU=d_sU, d_sc=d_sc, A_sU=A_sU, A_sc=A_sc,
         f_Ute=f_Ute, f_Utu=f_Utu, E_U=E_U, E_U_app=E_U_app, level=level, E_c=E_c, f_cd=f_cd, E_s=E_s,
         dsig_sD=dsig_sD, k_elem=k_elem, k_UD=k_UD, k_cD=k_cD)

try:
    r = core.ex4_compute(p)
except ValueError:
    st.error("Pas d'équilibre trouvé pour l'axe neutre avec ces données : vérifier la géométrie "
             "(d_sc < h_c < d_sU < h_c + h_U).")
    st.stop()
p, s = r["p"], r["st"]
h_top = p["h_c"] + p["h_U"]

# ----------------------------------------------------------------------------
# En-tête et indicateurs
# ----------------------------------------------------------------------------
st.title("Renforcement à la fatigue d'une dalle de roulement – BFUP armé")
st.markdown("Sécurité structurale à l'état limite de fatigue (type 4) par rapport à la limite de fatigue · "
            "*Cours « Structures existantes : chapitres choisis », Application 7, p. 45-47*")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Étape 1 – m_R,D = 0.5·m_Rd", f"{r['mRD1']:.1f} kNm/m",
          f"m_fat/m_R,D = {p['m_fat']/r['mRD1']:.2f} – {'OK' if r['ok1'] else 'NON'}",
          delta_color="normal" if r["ok1"] else "inverse", delta_arrow="off")
c2.metric("Étape 2 – m_R,D (analyse en section)", f"{s['m']:.1f} kNm/m",
          f"m_fat/m_R,D = {p['m_fat']/s['m']:.2f} – {'OK' if r['ok2'] else 'NON'}",
          delta_color="normal" if r["ok2"] else "inverse", delta_arrow="off")
c3.metric("Axe neutre x", f"{r['x']:.1f} mm", f"ε_Ut,D = {s['eD']*1e3:.2f}‰", delta_color="off", delta_arrow="off")
c4.metric("Matériaux à la limite de fatigue", "OK" if r["ok_mat"] else "NON",
          f"Δσ_sU = {r['s_sU']:.0f} ; σ_c,max = {abs(s['s_cmax']):.1f} MPa",
          delta_color="normal" if r["ok_mat"] else "inverse", delta_arrow="off")

if not r["ok2"]:
    E_req = core.E_app_required(p)
    msg = (f"À l'étape 2, le moment qui porte le BFUP à σ_U,D ({s['m']:.1f} kNm/m) est inférieur à "
           f"m_d(Q_fat) = {p['m_fat']:.0f} kNm/m : sous Q_fat, le BFUP dépasserait sa limite de fatigue avec "
           f"E_U,app = {p['E_U_app']/1e3:g} GPa.")
    if E_req:
        msg += (f" En admettant un endommagement du BFUP (rigidité apparente réduite), m_R,D ≥ m_d(Q_fat) pour "
                f"E_U,app ≤ {E_req/1e3:.1f} GPa ; voir l'onglet « Rigidité apparente » pour les limites du béton et de l'acier.")
    st.info(msg)


def fmt_table(df, fmts):
    out = df.copy().astype(object)
    for c, f in fmts.items():
        out[c] = [("" if (v is None or (isinstance(v, float) and np.isnan(v))) else f.format(round(v, 6) + 0.0))
                  for v in df[c]]
    return out


def show(fig, name):
    st.pyplot(fig, width="stretch")
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=160)
    plt.close(fig)
    st.download_button("Télécharger la figure (PNG)", buf.getvalue(), file_name=name, mime="image/png", key=name)


LE = lambda ok: r"\leq" if ok else ">"

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Étape 1 – élément", "Étape 2 – analyse en section",
                                        "Rigidité apparente E_U,app", "Étude paramétrique", "Notes"])

# ----------------------------------------------------------------------------
with tab1:
    st.markdown("**Vérification au niveau de l'élément de structure**")
    st.latex(rf"m_{{R,D}} = {p['k_elem']:g}\cdot m_{{Rd}} = {p['k_elem']:g}\cdot{p['m_Rd']:g} = {r['mRD1']:.1f}"
             rf"\ \mathrm{{kNm/m}}")
    st.latex(rf"m_d(Q_{{fat}}) = {p['m_fat']:g}\ {LE(r['ok1'])}\ m_{{R,D}} = {r['mRD1']:.1f}\ \mathrm{{kNm/m}}")
    (st.success if r["ok1"] else st.error)("Étape 1 vérifiée." if r["ok1"] else "Étape 1 NON vérifiée.")
    st.markdown("**Limites de fatigue des matériaux (étape 2)**")
    st.latex(rf"\sigma_{{U,D}} = {p['k_UD']:g}\,(f_{{Ute}} + f_{{Utu}}) = {p['k_UD']:g}\,({p['f_Ute']:g} + "
             rf"{p['f_Utu']:g}) = {s['sUD']:.2f}\ \mathrm{{MPa}}")
    st.latex(rf"\Delta\sigma_{{sd,D}} = {p['dsig_sD']:g}\ \mathrm{{MPa}},\qquad \sigma_{{cd,D}} = {p['k_cD']:g}"
             rf"\,f_{{cd}} = {r['scD']:.1f}\ \mathrm{{MPa}}")

# ----------------------------------------------------------------------------
with tab2:
    fig, ax = plt.subplots(1, 4, figsize=(17, 5.2), gridspec_kw=dict(wspace=0.3))
    bars = [(p["d_sU"], f"A_sU = {p['A_sU']:.0f} mm²/m"), (p["d_sc"], f"A_sc = {p['A_sc']:.0f} mm²/m")]
    core.draw_layered_section(ax[0], p["h_c"], p["h_U"], bars, r["x"])
    core.draw_strain(ax[1], s["y_ref"], s["eD"] * 1e3, r["x"], h_top,
                     [(s["y_ref"], "ε_Ut,D"), (p["d_sU"], "ε_sU"), (p["d_sc"], "ε_sc"), (0, "ε_c,max")],
                     title=f"Déformations (ε_Ut,D à y = {s['y_ref']:.0f} mm)")
    core.draw_stress(ax[2], [(np.array([p["h_c"], h_top]), np.array([s["sUD"]] * 2), core.C_TENS, "σ_U,D"),
                             (np.array([0, r["x"]]), np.array([s["s_cmax"], 0]), core.C_COMP, "σ_c,max")],
                     [(p["d_sU"], f"σ_sU={r['s_sU']:.0f}"), (p["d_sc"], f"σ_sc={r['s_sc']:.0f}")],
                     r["x"], h_top, title="Contraintes à la limite de fatigue")
    core.draw_forces(ax[3], [(row[0], row[4], row[5]) for row in s["rows"]], h_top)
    fig.subplots_adjust(left=0.05, right=0.98, top=0.9, bottom=0.12)
    show(fig, "ex4_section.png")

    left, right = st.columns([1.15, 1])
    with left:
        st.markdown(f"**Analyse en section : ε_Ut,D = σ_U,D / E_U,app = {s['sUD']:.2f} / {p['E_U_app']:.0f} = "
                    f"{s['eD']*1e3:.2f}‰**")
        rows = [list(row) for row in s["rows"]]
        rows.append(["Σ", np.nan, np.nan, np.nan, s["sumF"], np.nan, s["m"]])
        df = pd.DataFrame(rows, columns=["", "ε [‰]", "A [mm²]", "σ [MPa]", "F [kN/m]", "d [mm]", "m [kNm/m]"])
        st.dataframe(fmt_table(df, {"ε [‰]": "{:.3f}", "A [mm²]": "{:.0f}", "σ [MPa]": "{:.2f}",
                                    "F [kN/m]": "{:.1f}", "d [mm]": "{:.1f}", "m [kNm/m]": "{:.2f}"}),
                     hide_index=True, width="stretch")
        st.caption(f"Béton : σ à x/3 = {abs(s['rows'][3][3]):.2f} MPa (valeur du corrigé, force = σ(x/3)·0.75x) ; "
                   f"σ maximale à la fibre inférieure = {abs(s['s_cmax']):.2f} MPa.")
    with right:
        fig, ax = plt.subplots(figsize=(6, 3.6))
        core.draw_checks(ax, r)
        fig.tight_layout()
        st.pyplot(fig, width="stretch")
        plt.close(fig)
        fig, ax = plt.subplots(figsize=(6, 2.8))
        xs = np.linspace(max(10, r["x"] - 40), min(p["h_c"] - 1, r["x"] + 40), 120)
        ax.plot(xs, [core.ex4_state(p, xx)["sumF"] for xx in xs], color="0.3")
        ax.plot(p["x_iter"], [it["sumF"] for it in r["iters"]], "o", color=core.C_COMP, label="itérations du corrigé")
        ax.plot(r["x"], 0, "o", color=core.C_TENS, label=f"solution x = {r['x']:.1f} mm")
        ax.axhline(0, color="k", lw=0.5)
        ax.set_xlabel("x [mm]")
        ax.set_ylabel("ΣF [kN/m]")
        ax.legend(frameon=False, fontsize=7.5)
        ax.set_title("Itération sur l'axe neutre")
        fig.tight_layout()
        st.pyplot(fig, width="stretch")
        plt.close(fig)

# ----------------------------------------------------------------------------
with tab3:
    st.markdown("L'étape 2 admet un BFUP non endommagé. En fatigue, le BFUP s'endommage : sa rigidité apparente "
                "diminue et les barres reprennent davantage de contraintes, ce qui est acceptable tant que "
                "Δσ_s reste sous Δσ_sd,D. Le graphique montre l'effet de E_U,app sur le moment résistant à la fatigue.")
    Es = np.linspace(4000, 40000, 73)
    o = core.sweep_E_app(p, Es)
    E_req = core.E_app_required(p)
    E_c_lim = core.E_app_concrete_limit(p)
    E_s_lim = core.E_app_steel_limit(p)
    E_low = max([v for v in (E_c_lim, E_s_lim) if v] or [Es[0]])
    E_high = E_req if E_req else (Es[-1] if r["ok2"] else None)
    fig, ax = plt.subplots(1, 2, figsize=(14, 4.2))
    if E_high and E_low < E_high:
        for axx in ax:
            axx.axvspan(E_low / 1e3, E_high / 1e3, color="#d1e5f0", zorder=0, label="_nolegend_")
    ax[0].plot(o[:, 0] / 1e3, o[:, 1], color=core.C_TENS, lw=2, label="m_R,D (étape 2)")
    ax[0].axhline(p["m_fat"], color=core.C_COMP, ls="--", label="m_d(Q_fat)")
    ax[0].axhline(r["mRD1"], color="0.5", ls=":", label="m_R,D (étape 1)")
    ax[0].axvline(p["E_U_app"] / 1e3, color="0.6", ls=":", lw=0.9)
    if E_req:
        ax[0].plot(E_req / 1e3, p["m_fat"], "o", color=core.C_COMP)
        ax[0].text(E_req / 1e3, p["m_fat"], f"  {E_req/1e3:.1f} GPa", va="bottom", fontsize=8)
    ax[0].set_xlabel("E_U,app [GPa]")
    ax[0].set_ylabel("[kNm/m]")
    ax[0].legend(frameon=False, fontsize=8)
    ax[0].set_title("Moment résistant à la fatigue")
    ax[1].plot(o[:, 0] / 1e3, o[:, 2], color=core.C_TENS, label="Δσ_sU")
    ax[1].plot(o[:, 0] / 1e3, o[:, 3], color=core.C_COMP, label="σ_c,max")
    ax[1].axhline(p["dsig_sD"], color=core.C_TENS, ls="--", lw=0.8, label="Δσ_sd,D")
    ax[1].axhline(r["scD"], color=core.C_COMP, ls="--", lw=0.8, label="σ_cd,D")
    ax[1].axvline(p["E_U_app"] / 1e3, color="0.6", ls=":", lw=0.9)
    ax[1].set_yscale("log")
    ax[1].set_xlabel("E_U,app [GPa]")
    ax[1].set_ylabel("σ [MPa]")
    ax[1].legend(frameon=False, fontsize=8, ncol=2)
    ax[1].set_title("Contraintes dans l'acier et le béton")
    fig.tight_layout()
    show(fig, "ex4_E_app.png")
    r10 = core.ex4_compute({**p, "E_U_app": 10000.0})
    lines = [f"- Moment : m_R,D ≥ m_d(Q_fat) pour E_U,app ≤ **{E_req/1e3:.1f} GPa**." if E_req else
             f"- Moment : m_R,D {'≥' if r['ok2'] else '<'} m_d(Q_fat) sur toute la plage."]
    if E_c_lim:
        lines.append(f"- Béton : σ_c,max (fibre inférieure) ≤ σ_cd,D pour E_U,app ≥ **{E_c_lim/1e3:.1f} GPa**.")
    if E_s_lim:
        lines.append(f"- Acier : Δσ_sU ≤ Δσ_sd,D pour E_U,app ≥ **{E_s_lim/1e3:.1f} GPa**.")
    if E_high and E_low < E_high:
        lines.append(f"- Toutes les vérifications sont satisfaites pour E_U,app ∈ [{E_low/1e3:.1f} ; {E_high/1e3:.1f}] GPa "
                     "(zone bleue).")
    elif E_req:
        lines.append("- Aucune valeur de E_U,app ne satisfait simultanément toutes les vérifications.")
    lines.append(f"- Avec E_U,app = 10 GPa (suggestion du cours) : m_R,D = {r10['st']['m']:.1f} kNm/m, "
                 f"Δσ_sU = {r10['s_sU']:.0f} MPa, σ_c,max = {abs(r10['st']['s_cmax']):.1f} MPa "
                 f"(σ à x/3 = {abs(r10['st']['rows'][3][3]):.1f} MPa, convention du corrigé).")
    st.markdown("\n".join(lines))

# ----------------------------------------------------------------------------
with tab4:
    PARAMS = {
        "A_sU – armature du BFUP [mm²/m]": ("A_sU", 300.0, 2500.0),
        "A_sc – armature de la dalle [mm²/m]": ("A_sc", 500.0, 3000.0),
        "h_U – épaisseur BFUP [mm]": ("h_U", 25.0, 80.0),
        "f_Utu – BFUP [MPa]": ("f_Utu", 7.5, 14.0),
        "E_c – béton [MPa]": ("E_c", 20000.0, 45000.0),
    }
    a, b = st.columns([1, 2.2])
    with a:
        lab = st.selectbox("Paramètre", list(PARAMS))
        key, lo, hi = PARAMS[lab]
        rng = st.slider("Plage", lo, hi, (lo, hi))
        st.caption("Pour h_U, la position de A_sU est gardée à la même distance de la fibre supérieure.")
    vals = np.linspace(rng[0], rng[1], 41)
    rows = []
    for v in vals:
        q = dict(p)
        q[key] = v
        if key == "h_U":
            q["d_sU"] = p["d_sU"] + (v - p["h_U"])
        try:
            rr = core.ex4_compute(q)
            rows.append((v, rr["st"]["m"], rr["mRD1"], rr["s_sU"], abs(rr["st"]["s_cmax"])))
        except ValueError:
            rows.append((v, np.nan, np.nan, np.nan, np.nan))
    o = np.array(rows, dtype=float)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(o[:, 0], o[:, 1], color=core.C_TENS, lw=2, label="m_R,D (étape 2)")
    ax.axhline(p["m_fat"], color=core.C_COMP, ls="--", label="m_d(Q_fat)")
    ax.axvline(p[key], color="0.6", ls=":", lw=0.9)
    ax.set_xlabel(lab)
    ax.set_ylabel("[kNm/m]")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    with b:
        st.pyplot(fig, width="stretch")
    plt.close(fig)
    st.download_button("Télécharger les résultats (CSV)",
                       pd.DataFrame(o, columns=[key, "m_RD_etape2", "m_RD_etape1", "dsig_sU", "sig_c_max"]).to_csv(index=False),
                       file_name=f"ex4_parametrique_{key}.csv", mime="text/csv")

# ----------------------------------------------------------------------------
with tab5:
    rc = core.ex4_compute({**p, "level": core.LEVELS[1]}) if p["level"] == core.LEVELS[0] else None
    st.markdown(f"""
**Démarche du cours**
- Étape 1 : vérification globale, m_d(Q_fat) ≤ m_R,D = 0.5·m_Rd.
- Étape 2 : analyse en section avec le BFUP écrouissant représenté par un module apparent E_U,app. La déformation
  ε_Ut,D = σ_U,D / E_U,app est imposée pour ne pas dépasser σ_U,D ; l'axe neutre est trouvé par équilibre ; les
  contraintes dans l'acier et le béton sont comparées à leurs limites de fatigue.

**Hypothèses**
- BFUP à σ_U,D uniforme sur toute l'épaisseur ; aciers et béton élastiques ; traction du béton négligée.
- Force de béton : σ(x/3)·0.75·x, identique à ½·σ_c,max·x (distribution triangulaire).
- La contrainte de l'acier sous Q_fat (actions permanentes incluses) est comparée à Δσ_sd,D : approche prudente.

**Écarts relevés dans le corrigé du cours**
- ε_Ut,D est imposée au centre de la couche de BFUP (y = 200 mm), pas à sa fibre supérieure.""" +
                (f" À la fibre supérieure : x = {rc['x']:.1f} mm, m_R,D = {rc['st']['m']:.1f} kNm/m." if rc else "") + """
- Le béton est vérifié avec σ à x/3 (5.5 MPa) ; la contrainte maximale à la fibre inférieure est de 8.4 MPa,
  toujours inférieure à σ_cd,D = 10 MPa.
- Le moment de l'étape 2 (53.5 kNm/m) est inférieur à m_d(Q_fat) = 59 kNm/m ; le corrigé l'attribue à la prudence
  de l'hypothèse « BFUP non endommagé » et suggère E_U,app = 10 GPa. Avec les données par défaut, m_R,D ≥ 59 kNm/m
  exige E_U,app ≤ 11.7 GPa, mais σ_c,max ≤ 10 MPa exige E_U,app ≥ 11.4 GPa : la fenêtre admissible est étroite.
  À 10 GPa, le béton est vérifié avec σ à x/3 (7.3 MPa) mais la contrainte maximale (11.0 MPa) dépasse σ_cd,D.
""")
