import numpy as np

# Harrison (1989) evrensel parametreleri — boyutsuz katsayılar
# V_ij = η_ij * (ħ²/m₀d²)   burada d = en yakın komşu mesafesi = a₀√3/4
HARRISON_ETA = {
    'Vss':  -1.40,   # s-s sigma
    'Vxx':   0.00,   # p-p pi (genellikle ihmal edilir)
    'Vxy':   2.16,   # p-p sigma
    'Vsapc': 1.84,   # s_a - p_c sigma
    'Vscpa': 1.84,   # s_c - p_a sigma
}

# ħ²/m₀ = 7.6199 eV·Å²
HBAR2_M0 = 7.6199

def harrison_tb_params(a0_angstrom):
    """
    a₀ (Angstrom cinsinden örgü sabiti) verilen sp3s* için
    Harrison evrensel TB parametrelerini hesapla.
    
    Döndürür: dict, 5 temel TB parametresi
    """
    d  = a0_angstrom * np.sqrt(3) / 4   # en yakın komşu mesafesi
    V0 = HBAR2_M0 / d**2                # ölçek enerjisi
    
    return {
        'Vss':   HARRISON_ETA['Vss']  * V0,
        'Vxx':   HARRISON_ETA['Vxx']  * V0,
        'Vxy':   HARRISON_ETA['Vxy']  * V0,
        'Vsapc': HARRISON_ETA['Vsapc'] * V0,
        'Vscpa': HARRISON_ETA['Vscpa'] * V0,
    }

def compute_harrison_baseline(a0_dict):
    """
    Tüm malzemeler için Harrison taban vektörlerini döndür.
    
    Girdi:  a0_dict = {'GaAs': 5.666, 'AlAs': 5.660, ...}
    Çıktı: dict[mat_name] -> numpy array (5,)
    """
    result = {}
    for name, a0 in a0_dict.items():
        h = harrison_tb_params(a0)
        result[name] = np.array(list(h.values()))
    return result


if __name__ == '__main__':
    # Basit test
    a0s = {'GaAs': 5.666, 'AlAs': 5.660}
    print("Harrison baseline:")
    for name, v in compute_harrison_baseline(a0s).items():
        print(name, v)