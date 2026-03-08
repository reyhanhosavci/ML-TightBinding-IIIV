"""
AŞAMA 1 — Fizik-Bilgili Özellikler

Çekirdek kodun 6 gözlemlenebilirini (Eg, Eg_X, Eg_L, Dso, me, a0)
6 ek fizik-bilgili özellik ile 12'ye genişletir.

Kullanım:
    from features.physics_features import compute_physics_features, FEATURE_NAMES
    feat = compute_physics_features('GaAs', EXP['GaAs'], a0=5.666)
"""

import numpy as np

# Pauling elektronegativilik, atom numarası, kovalen yarıçap (Å)
ATOM_DATA = {
    'Ga': (1.81, 31, 1.22),
    'Al': (1.61, 13, 1.21),
    'In': (1.78, 49, 1.42),
    'As': (2.18, 33, 1.19),
    'P':  (2.19, 15, 1.07),
    'Sb': (2.05, 51, 1.39),
}

COMPOUND_ATOMS = {
    'GaAs': ('Ga', 'As'), 'AlAs': ('Al', 'As'), 'InAs': ('In', 'As'),
    'GaP':  ('Ga', 'P'),  'AlP':  ('Al', 'P'),  'InP':  ('In', 'P'),
    'GaSb': ('Ga', 'Sb'), 'AlSb': ('Al', 'Sb'), 'InSb': ('In', 'Sb'),
}

DIRECT_GAP = {'GaAs', 'InAs', 'InP', 'GaSb', 'InSb'}

# Özellik isimleri: 6 orijinal + 6 yeni = 12
FEATURE_NAMES = [
    'Eg', 'Eg_X', 'Eg_L', 'Dso', 'me', 'a0',
    'DEN', 'Z4_avg', 'fi', 'direct_flag', 'EgX_EgG', 'V0_harrison',
]


def compute_physics_features(mat_name, exp_dict, a0):
    """
    6 gözlemlenebiliri 12 fizik-bilgili özelliğe genişletir.

    Girdi:
        mat_name  : 'GaAs', 'InP', vb.
        exp_dict  : {'Eg': ..., 'Eg_X': ..., 'Eg_L': ..., 'Dso': ..., 'me': ...}
        a0        : örgü sabiti (Angstrom)

    Çıktı:
        numpy array, şekil (12,)
    """
    cat, an = COMPOUND_ATOMS[mat_name]
    en_cat, z_cat, _ = ATOM_DATA[cat]
    en_an,  z_an,  _ = ATOM_DATA[an]

    Eg   = exp_dict['Eg']
    Eg_X = exp_dict.get('Eg_X', Eg)
    Eg_L = exp_dict.get('Eg_L', Eg)
    Dso  = exp_dict['Dso']
    me   = exp_dict['me']

    # ── Orijinal 6 özellik (generate_training_data ile uyumlu) ────
    f1 = Eg
    f2 = Eg_X
    f3 = Eg_L
    f4 = Dso
    f5 = me
    f6 = a0

    # ── Yeni fizik-bilgili özellikler ─────────────────────────────
    f7  = en_an - en_cat                              # ΔEN
    f8  = np.log1p((z_an**4 + z_cat**4) / 2)   # ~10-16 aralığına düşer
    f9  = 1.0 - np.exp(-0.25 * (en_an - en_cat)**2)   # Phillips iyonisite fᵢ
    f10 = 1.0 if mat_name in DIRECT_GAP else 0.0       # Direkt/indirekt bayrak
    f11 = np.clip(Eg_X / max(Eg, 0.01), 0, 5)  # uç değerleri kır                        # Eg(X)/Eg(Γ)
    f12 = 7.62 / (a0**2)                               # Harrison V₀

    return np.array([f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12])


if __name__ == '__main__':
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from tb_ml_optim import EXP, LIT_PARAMS, MAT_NAMES

    print("Fizik-bilgili özellik testi")
    print("=" * 80)
    header = f"  {'Malzeme':<8}"
    for fn in FEATURE_NAMES:
        header += f" {fn:>10}"
    print(header)
    print("  " + "-" * 78)

    for name in MAT_NAMES:
        a0 = LIT_PARAMS[name].a0
        feat = compute_physics_features(name, EXP[name], a0)
        row = f"  {name:<8}"
        for v in feat:
            row += f" {v:>10.4f}"
        print(row)
    print("=" * 80)
