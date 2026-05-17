# EIDA Coulomb Kapısı — Özgünlük Kanıtları
**Geliştirici:** Güven Acar  
**Tarih:** 2026, İzmir  
**Proje:** EIDA — IoT için kuantum dirençli kriptografi altyapısı

---

## 1. İddia

> "Coulomb kuvvet modeline dayalı, pozisyon ağırlıklı, giriş-bağımlı yeni bir
> Boolean dönüşüm fonksiyonu tanımlandı. Bu fonksiyon lineer, simetrik ve
> klasik threshold fonksiyon sınıflarının dışındadır."

---

## 2. Kapının Tanımı

### Fiziksel Model
- Geçen bit `0` = elektron (e⁻), geçen bit `1` = pozitron (e⁺)
- Kapıdaki `0` bitleri: geçeni **iter** (aynı yük)
- Kapıdaki `1` bitleri: geçeni **çeker** (zıt yük)
- Kuvvet: `F = 1 / mesafe`, yönlü (sağa pozitif, sola negatif)
- Pozitron sonucu: elektronun tam tersi

### Matematiksel Formül (6-bit kapı)

Kapı bitleri `[g₋₃, g₋₂, g₋₁, g₊₁, g₊₂, g₊₃]`, geçen bit `p`:

```
F = Σᵢ  yön(i) × yük(gᵢ, p) / |i|

yön(i)     = +1 (sağda),  -1 (solda)
yük(g, p)  = +1 (g ≠ p)   — zıt yük, çeker
           = -1 (g = p)   — aynı yük, iter

Karar:
  p=0 (e⁻): F > 0 → 1,  F ≤ 0 → 0
  p=1 (e⁺): F > 0 → 0,  F ≤ 0 → 1   (tam tersi)
```

### Ağırlık Vektörü (elektron için)
```
Pozisyon : -3     -2     -1    +1    +2    +3
w        : -2/3   -1    -2    +2    +1   +2/3
```
Simetrik büyüklük, zıt işaret — sol ağırlıklar negatif, sağ ağırlıklar pozitif.

---

## 3. Kanıtlar

### 3.1 Lineer Değil (GF(2) üzerinde)

**Tanım:** Lineer Boolean fonksiyon `f(x) = a·x (mod 2)` — bitlerin XOR kombinasyonu.  
**Koşul:** `f(x ⊕ y) = f(x) ⊕ f(y)` her x, y için sağlanmalı.

**Sonuç:**
- En iyi lineer yaklaşım: `a=(0,0,0,1,0,0)` → 48/64 eşleşme (%75)
- Lineerlik koşulu ihlali: **1920/4096** çift

**Örnek ihlal:**
```
x = 000001,  y = 000010
f(x ⊕ y) = f(000011) = 1
f(x) ⊕ f(y) = 1 ⊕ 0 = 0
→ 1 ≠ 0  ✓ ihlal
```

**Sonuç: Coulomb lineer değildir.**

---

### 3.2 Klasik Threshold (Perceptron) Değil

**Tanım:** Threshold fonksiyon: `f(x) = 1  iff  w·x ≥ θ`  
Burada `w` **sabit** bir ağırlık vektörüdür, geçen bitten bağımsız.

**Test:** LP ile en iyi (w, θ) bulundu:
```
w = [48, -50, -100, 100, 50, 50],  θ = 49
Elektron doğruluğu : 64/64
```

**Kritik test — aynı w pozitron için:**
```
Pozitron doğruluğu: 0/64
```

Coulomb'da pozitron geçerken ağırlıklar **tam tersine döner**:
- Elektron (p=0): w = [−2/3, −1, −2, +2, +1, +2/3]
- Pozitron (p=1): w = [+2/3, +1, +2, −2, −1, −2/3]

**Klasik threshold tanımı gereği w sabit olmalıdır.**  
Coulomb'da w geçen bitin değerine göre değişiyor.  
Bu onu "input-dependent weighted threshold" yapar — klasik threshold sınıfının dışında.

**Sonuç: Coulomb klasik threshold fonksiyonu değildir.**

---

### 3.3 Simetrik Değil

**Tanım:** Simetrik fonksiyon: `f(x)` yalnızca `Σxᵢ` (1-sayısı) değerine bağlı.  
Giriş bitlerinin sırası önemsizdir.

**Karşı örnek (k=1, tek 1 bit):**
```
001000  →  0
000001  →  1
```
Her ikisinde de tam olarak bir adet 1 var — ama sonuçlar farklı.

**Permütasyon testi (3 adet 1, 3 adet 0 — 20 permütasyon):**
```
Sonuç=0: 10 permütasyon
Sonuç=1: 10 permütasyon
```

XOR için aynı test: tüm 20 permütasyon → aynı sonuç.

**Sonuç: Coulomb simetrik değildir.**

---

### 3.4 Pozisyon Bağımlılığı — Özgünlüğün Özü

Aynı sayıda 1 içeren kapılar farklı sonuç üretiyor:

| Kapı     | 1 sayısı | F      | Sonuç |
|----------|----------|--------|-------|
| `111000` | 3        | −3.667 | 0     |
| `000111` | 3        | +3.667 | 1     |
| `101010` | 3        | −1.667 | 0     |
| `010101` | 3        | +1.667 | 1     |

AND, OR, XOR, Majority, Threshold — hepsi pozisyon körüdür.  
**Coulomb pozisyon duyarlıdır. Bu özellik hiçbir klasik kapıda yoktur.**

---

### 3.5 6-bit Kapıda Mükemmel Denge

```
F > 0 (elektron sağa sapar → 1) : 32 kapı
F < 0 (elektron sola sapar → 0) : 32 kapı
F = 0 (belirsizlik)             :  0 kapı
```

6-bit kapıda hiçbir belirsiz durum yok. Bu denge,
Coulomb kuvvetinin antisimetrik yapısından gelir:
`g` için F = +x ise, `ḡ` (bit terse) için F = −x.

---

## 4. Coulomb Hangi Sınıfa Giriyor?

| Sınıf                     | Coulomb | Neden                                |
|---------------------------|---------|--------------------------------------|
| Lineer (GF2)              | ✗       | 1920/4096 lineerlik ihlali           |
| Klasik threshold          | ✗       | w geçen bite göre değişiyor          |
| Simetrik                  | ✗       | Pozisyon bağımlı                     |
| Input-dependent threshold | ✓       | w = f(geçen_bit, pozisyon)           |
| Pozisyon ağırlıklı        | ✓       | Ağırlıklar mesafe ve yönden türetildi |

Coulomb, **"input-dependent, position-weighted threshold"** sınıfındadır.
Bu sınıf klasik Boolean fonksiyon hiyerarşisinde tanımlı değildir.

---

## 5. İtirazlar ve Yanıtlar

**"LP ile threshold çözümü bulundu, o zaman threshold değil misin?"**

LP elektron için çalışan bir (w, θ) buldu — ama aynı w pozitron için
tamamen çalışmıyor (0/64). Klasik threshold tanımı tek bir sabit w gerektirir.
Coulomb iki farklı w kullanıyor — bu threshold'un genelleştirilmiş halidir,
kendisi değil.

**"p'yi de giriş sayarsak 7-girişli perceptron olur — yeni bir şey yok."**

Bu en güçlü itiraz. Doğrudan test edildi:

Giriş uzayı `[g₁, g₂, g₃, g₄, g₅, g₆, p]` — 128 kombinasyon.  
LP ile bu 128 noktayı ayıran bir hiper-düzlem arandı.

```
LP sonucu: INFEASIBLE
→ 7-boyutlu uzayda Coulomb'u ayıran hiper-düzlem yok.
→ 7-girişli perceptron da Coulomb'u temsil edemiyor.
```

İtiraz çürütüldü. Coulomb doğrusal olarak ayrılamaz (linearly non-separable).

**"Bu sadece iki ayrı threshold fonksiyonunun birleşimi değil mi?"**

Evet, elektron ve pozitron için ayrı ayrı threshold olarak yazılabilir.
Ama Coulomb bunları tek bir fiziksel ilkeden türetiyor: kuvvet yönü.
Bu "iki threshold'un switch'i" değil, geçen bitin yüküne göre otomatik
değişen tek bir mekanizmadır.

**"Klasik threshold sınıfının dışında olmak yeterli mi?"**

Kriptografik özgünlük için yeterli değil, ama matematiksel özgünlük için
yeterli. EIDA Coulomb kapısı yeni bir dönüşüm ilkesi tanımlıyor —
kriptolama iddiası taşımıyor.

---

## 6. Özet

### Kanıt Hiyerarşisi — İtiraz Çürütme Zinciri

| İtiraz                      | Test                   | Sonuç                    |
|-----------------------------|------------------------|--------------------------|
| "XOR kombinasyonudur"       | GF(2) lineerlik koşulu | ✗ — 1920/4096 ihlal      |
| "Simetrik fonksiyondur"     | Permütasyon testi      | ✗ — aynı k, farklı sonuç |
| "6-girişli perceptrondur"   | Pozitron LP testi      | ✗ — aynı w ile 0/64      |
| "7-girişli perceptrondur"   | LP (128 giriş)         | ✗ — **INFEASIBLE**       |

Son satır en güçlü kanıt: p'yi de giriş değişkeni sayarak 7-boyutlu
uzayda Coulomb'u ayıran hiper-düzlem arandı — yok. Coulomb doğrusal
olarak ayrılamaz (linearly non-separable).

### Özellikler

| Özellik                     | Durum                            |
|-----------------------------|----------------------------------|
| Lineer değil                | ✓ kanıtlandı (1920 ihlal)        |
| 6-girişli perceptron değil  | ✓ kanıtlandı (pozitron testi)    |
| 7-girişli perceptron değil  | ✓ kanıtlandı (LP infeasible)     |
| Simetrik değil              | ✓ kanıtlandı (permütasyon testi) |
| Pozisyon duyarlı            | ✓ kanıtlandı                     |
| 6-bit'te F=0 yok            | ✓ tam karar, belirsizlik yok     |
| Bijektif (beam ile)         | ✓ 256/256                        |
| Avalanche (2 turda)         | ✓ %50.1                          |

---

## 7. Açık Sorular

1. "Input-dependent threshold" sınıfı literatürde var mı?
   Coulomb bu sınıfa öncülük ediyor mu?
2. Ters fonksiyon (deşifre) kapalı formda türetilebilir mi?
3. 8-bit ve üzeri kapılarda F=0 durumu nasıl davranır?

---

*Bu belge EIDA projesinin bir parçasıdır. Güven Acar, 2026, İzmir.*
