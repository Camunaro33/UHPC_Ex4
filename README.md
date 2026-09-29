# BFUP armé – fatigue : applet de l'exemple 4 (Application 7)

Applet Streamlit qui reproduit l'application 7 (p. 45-47) du cours « Structures existantes : chapitres choisis » : vérification de la sécurité structurale à l'état limite de fatigue (type 4), par rapport à la limite de fatigue, de la dalle de roulement d'un caisson de pont d'autoroute renforcée par une couche de BFUP armé.

- **Étape 1 – élément** : m_d(Q_fat) ≤ m_R,D = 0.5·m_Rd ; limites de fatigue des matériaux σ_U,D = 0.3 (f_Ute + f_Utu), Δσ_sd,D, σ_cd,D = 0.5 f_cd.
- **Étape 2 – analyse en section** : ε_Ut,D = σ_U,D / E_U,app imposée, axe neutre par équilibre (avec les itérations du corrigé), contraintes dans l'acier et le béton, moment résistant à la fatigue m_R,D, taux d'utilisation.
- **Rigidité apparente E_U,app** : effet de l'endommagement du BFUP (rigidité apparente réduite) sur m_R,D et sur les contraintes de l'acier et du béton ; plage de E_U,app pour laquelle toutes les vérifications sont satisfaites.
- **Étude paramétrique** : m_R,D en fonction de A_sU, A_sc, h_U, f_Utu ou E_c, avec export CSV.
- **Notes** : démarche, hypothèses et écarts relevés dans le corrigé.

Toutes les entrées sont modifiables dans la barre latérale ; les valeurs par défaut sont celles de l'énoncé.

## Lancer localement

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Déployer sur Streamlit Community Cloud

1. Pousser ce dossier dans un dépôt GitHub.
2. Sur [share.streamlit.io](https://share.streamlit.io) : **Create app**, puis indiquer l'URL du fichier, au format
   `https://github.com/<utilisateur>/<depot>/blob/main/app.py`.
3. **Deploy**. L'applet est redéployée à chaque `git push`.

## Structure

| Fichier | Rôle |
|---|---|
| `app.py` | Interface Streamlit |
| `bfup_ex4.py` | Calculs et fonctions de tracé ; utilisable seul dans Spyder |
| `test_app.py` | Tests : valeurs du corrigé et exécution de l'applet (`pytest`) |
| `requirements.txt` | Dépendances |
| `.streamlit/config.toml` | Thème |

## Écarts relevés dans le corrigé du cours

- ε_Ut,D est imposée au centre de la couche de BFUP (y = 200 mm) et non à sa fibre supérieure ; à la fibre supérieure, m_R,D = 50.0 kNm/m (option « Niveau où ε_Ut,D est imposé »).
- Le béton est vérifié avec σ à x/3 (5.5 MPa) ; la contrainte maximale à la fibre inférieure vaut 8.4 MPa, toujours < 10 MPa.
- Le moment de l'étape 2 (53.5 kNm/m) est inférieur à m_d(Q_fat) = 59 kNm/m. Le corrigé suggère E_U,app = 10 GPa. Avec les données par défaut, m_R,D ≥ 59 kNm/m exige E_U,app ≤ 11.7 GPa, et σ_c,max ≤ 10 MPa exige E_U,app ≥ 11.4 GPa : la fenêtre admissible est étroite. À 10 GPa, la contrainte maximale du béton (11.0 MPa) dépasse σ_cd,D, alors que la valeur à x/3 (7.3 MPa) la respecte.

Unités internes : N, mm, MPa ; résultats en kN/m et kNm/m.
