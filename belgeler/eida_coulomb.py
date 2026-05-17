def coulomb_gate(bit, gate):
    """
    Coulomb kuvvet kapısı.
    bit: geçen bit (0 veya 1)
    gate: [sol_n, ..., sol_1, sağ_1, ..., sağ_n] kapı bitleri
    
    Kuvvet = k/mesafe
    Aynı kutup (bit==gate[i]) → iter (negatif)
    Zıt kutup (bit!=gate[i]) → çeker (pozitif)
    
    Bileşke > 0 → bit dönüşür
    Bileşke < 0 → bit kalır
    Bileşke = 0 → bit kalır (denge)
    """
    n = len(gate) // 2  # kanat uzunluğu
    force = 0.0
    
    # Sol kanat: mesafe n'den 1'e
    for i in range(n):
        distance = n - i  # sol2=2, sol1=1
        g = gate[i]
        if g != bit:  # zıt → çeker → pozitif
            force += 1.0 / distance
        else:         # aynı → iter → negatif
            force -= 1.0 / distance
    
    # Sağ kanat: mesafe 1'den n'e
    for i in range(n):
        distance = i + 1  # sağ1=1, sağ2=2
        g = gate[n + i]
        if g != bit:  # zıt → çeker → pozitif
            force += 1.0 / distance
        else:         # aynı → iter → negatif
            force -= 1.0 / distance
    
    if force > 0:
        return 1 - bit  # dönüşür
    else:
        return bit      # kalır (0 veya negatif)

def eida_coulomb(bits, wing=1):
    """
    Coulomb EIDA: her bit için wing genişliğinde kapı kullanır.
    wing=1: 2 bitlik kapı (1 sol, 1 sağ)
    wing=2: 4 bitlik kapı (2 sol, 2 sağ)
    """
    n = len(bits)
    result = []
    for i in range(n):
        # Kapıyı oluştur: sol kanat + sağ kanat
        gate = []
        for j in range(wing, 0, -1):  # sol: uzaktan yakına
            gate.append(bits[(i - j) % n])
        for j in range(1, wing + 1):  # sağ: yakından uzağa
            gate.append(bits[(i + j) % n])
        result.append(coulomb_gate(bits[i], gate))
    return result

def bits_to_str(bits):
    return ''.join(map(str, bits))

def int_to_bits(n, length):
    return [(n >> (length-1-i)) & 1 for i in range(length)]

# === 2 bitlik kapı (wing=1) için tüm 4 bitlik diziler ===
print("=== 2 bitlik Coulomb kapısı (4 bit dizi) ===")
print(f"{'Giriş':8} {'Çıktı':8} {'Fark?'}")
print("-" * 30)
for i in range(16):
    bits = int_to_bits(i, 4)
    out = eida_coulomb(bits, wing=1)
    fark = bits != out
    print(f"{bits_to_str(bits):8} {bits_to_str(out):8} {'✗' if fark else '='}")

# === 4 bitlik kapı (wing=2) için tüm 4 bitlik diziler ===
print("\n=== 4 bitlik Coulomb kapısı (8 bit dizi) ===")
from collections import Counter
results = Counter()
for i in range(256):
    bits = int_to_bits(i, 8)
    out = eida_coulomb(bits, wing=2)
    results[bits_to_str(out)] += 1

unique = len(results)
print(f"Benzersiz çıktı: {unique}/256")

# Bijeksiyon kontrolü
print(f"Bijeksiyon: {'✓' if unique == 256 else '✗'}")

# === Kuvvet tablosu: 4 bitlik kapı için geçen 0 ===
print("\n=== 4 bitlik kapı kuvvet tablosu (geçen bit = 0) ===")
print(f"{'Kapı':10} {'Sol2':6} {'Sol1':6} {'Sağ1':6} {'Sağ2':6} {'Bileşke':8} {'Sonuç'}")
print("-" * 55)
for i in range(16):
    gate = int_to_bits(i, 4)
    s2 = -0.5 if gate[0]==0 else 0.5
    s1 = -1.0 if gate[1]==0 else 1.0
    r1 = -1.0 if gate[2]==0 else 1.0
    r2 = -0.5 if gate[3]==0 else 0.5
    total = s2 + s1 + r1 + r2
    result = 1 if total > 0 else 0
    print(f"{bits_to_str(gate):10} {s2:+.1f}   {s1:+.1f}   {r1:+.1f}   {r2:+.1f}   {total:+.1f}     {result}")

# Dağılım kontrolü
forces = []
for i in range(16):
    gate = int_to_bits(i, 4)
    s2 = -0.5 if gate[0]==0 else 0.5
    s1 = -1.0 if gate[1]==0 else 1.0
    r1 = -1.0 if gate[2]==0 else 1.0
    r2 = -0.5 if gate[3]==0 else 0.5
    forces.append(s2+s1+r1+r2)

neg = sum(1 for f in forces if f < 0)
zer = sum(1 for f in forces if f == 0)
pos = sum(1 for f in forces if f > 0)
print(f"\nNegatif: {neg}, Sıfır: {zer}, Pozitif: {pos}")
print(f"Simetri: {'✓' if neg == pos else '✗'}")

# === Farklı boyutlarda bijeksiyon testi ===
print("\n=== Farklı boyutlarda bijeksiyon (wing=1) ===")
for n in [2, 4, 6, 8]:
    unique = len(set(bits_to_str(eida_coulomb(int_to_bits(i,n), 1)) for i in range(2**n)))
    print(f"  {n} bit: {unique}/{2**n} {'✓' if unique==2**n else '✗'}")
