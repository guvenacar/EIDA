# EIDA Coulomb Kapısı — Özgünlük Kanıtları
**Geliştirici:** Güven Acar  
**Tarih:** 2026, İzmir  
**Proje:** EIDA — IoT için kuantum dirençli kriptografi altyapısı

---

## 1. İddia

> "Coulomb kuvvet modeline dayalı, pozisyon ağırlıklı yeni bir Boolean dönüşüm kapısı tanımlandı."

Bu belge bu iddiayı destekleyen kanıtları ve itiraz edilebilecek noktaları içerir.

---

## 2. Kapının Tanımı

### Fiziksel Model
- Geçen bit **0** = elektron (e⁻)
- Geçen bit **1** = pozitron (e⁺)
- Kapıdaki **0** bitleri = elektron → geçeni **iter** (aynı yük)
- Kapıdaki **1** bitleri = pozitron → geçeni **çeker** (zıt yük)
- Kuvvet büyüklüğü: `F = 1 / mesafe` (Coulomb yasası)
- Kuvvet **yönlü**: sağdaki bit sola, soldaki bit sağa etki eder

### Matematiksel Formül (6-bit kapı)
Kapı bitleri `[g₋₃, g₋₂, g₋₁, g₊₁, g₊₂, g₊₃]`, geçen bit `p`:

```
F = Σ yön(i) × yük(gᵢ, p) / |i|

yön(i)    = +1 (sağda), -1 (solda)
yük(g, p) = +1 (g ≠ p, zıt yük → çeker)
           = -1 (g = p, aynı yük → iter)
```

### Karar Kuralı
```
Elektron (p=0): F > 0 → 1,  F ≤ 0 → 0 kalır
Pozitron (p=1): tam tersi — elektronun ayna görüntüsü
```

---

## 3. Kanıtlar

### 3.1 Klasik Kapılarla Örtüşme Yok

6-bit uzayda (64 kapı kombinasyonu) Coulomb kapısının truth table'ı
tüm klasik kapılarla karşılaştırıldı:

| Klasik Kapı  | Eşleşme | Oran  |
|--------------|---------|-------|
| AND          | 33/64   | %51.6 |
| OR           | 33/64   | %51.6 |
| XOR          | 32/64   | %50.0 |
| Majority(3)  | 34/64   | %53.1 |
| Threshold(2) | 33/64   | %51.6 |
| Threshold(4) | 34/64   | %53.1 |
| Threshold(5) | 33/64   | %51.6 |

**Sonuç:** Hiçbir klasik kapıyla %50'nin üzerinde anlamlı örtüşme yok.
Rastgele iki Boolean fonksiyonu zaten ortalama %50 örtüşür —
yani Coulomb hiçbir klasik kapıyla **istatistiksel olarak anlamlı benzerlik** göstermiyor.

---

### 3.2 Pozisyon Bağımlılığı — En Güçlü Kanıt

**Klasik kapılar pozisyon körüdür:** AND, OR, XOR, Majority —
hepsi giriş bitlerinin *hangi sırada geldiğine* bakmaz.

```
XOR(1,1,1,0,0,0) = XOR(0,0,0,1,1,1) = XOR(1,0,1,0,1,0) = 1
```
Aynı içerik, farklı sıra → XOR'da hep aynı sonuç.

**Coulomb pozisyon duyarlıdır:**

| Kapı     | 1 sayısı | Bileşke F | Sonuç |
|----------|----------|-----------|-------|
| `111000` | 3        | −3.667    | 0     |
| `000111` | 3        | +3.667    | 1     |
| `101010` | 3        | −1.667    | 0     |
| `010101` | 3        | +1.667    | 1     |
| `011100` | 3        | −1.000    | 0     |
| `001110` | 3        | +1.000    | 1     |

Aynı sayıda 1 içeren 20 permütasyonun 10'u → 0, 10'u → 1 üretiyor.

**Bu özellik hiçbir klasik kapıda yoktur.**

---

### 3.3 Dengeli Truth Table

6-bit kapı uzayında:
- F > 0 (elektron sağa sapar → 1): **32 kapı**
- F < 0 (elektron sola sapar → 0): **32 kapı**
- F = 0 (belirsizlik): **0 kapı**

Truth table'da 1'ler: **32/64 = %50.0**

Bu denge rastlantı değil — Coulomb kuvvetinin antisimetrik yapısından kaynaklanıyor.
`g` kapısı için F = +x ise, `ḡ` (tersi) kapısı için F = −x.

---

### 3.4 Bijeksiyon (Dinamik Beam ile)

Dinamik beam sisteminde (kapı ve geçen bit güncel diziden):
- 8-bit uzayda 256 giriş → **256 benzersiz çıkış** ✓
- Tüm beam_size değerleri (1–7) için geçerli
- 2 turda avalanche ortalaması: **%50.1** ✓

---

## 4. İtiraz Edilebilecek Noktalar

### İtiraz 1: "Bu sadece ağırlıklı threshold fonksiyonu"
**Yanıt:** Threshold fonksiyonları pozisyon körüdür — ağırlıklar *bitlere* değil,
*pozisyonlara* atanır. Coulomb'da ağırlık sabit değil, hem pozisyona hem de
geçen bitin yüküne göre dinamik olarak belirlenir. Pozisyon bağımlılığı kanıtı
(bkz. 3.2) bu itirazı çürütür.

### İtiraz 2: "Fiziksel analoji keyfi — matematiksel temeli yok"
**Yanıt:** Analoji türetim aracı, tanım değil. Matematiksel tanım §2'de
bağımsız olarak verilmiştir. Fiziksel analoji olmadan da aynı fonksiyon
tanımlanabilir: "pozisyon ağırlıklı, yönlü, ters-simetrik Boolean fonksiyonu."

### İtiraz 3: "6-bit kapı büyük — bu sadece bir lookup table"
**Yanıt:** Tüm Boolean fonksiyonları lookup table ile ifade edilebilir.
Önemli olan türetim ilkesinin tutarlılığı ve ölçeklenebilirliği.
Coulomb formülü 2, 4, 6, 8... bit için aynı ilkeyle çalışır.

### İtiraz 4: "Yeni kapı mı, yoksa bilinen bir kapının özel durumu mu?"
**Yanıt:** Bu açık soru — tam olarak yanıtlamak için:
- Tüm 6-girişli Boolean fonksiyonları uzayı: 2^(2^6) = 2^64 ≈ 1.8 × 10¹⁹
- Coulomb'un truth table vektörü bu uzayda benzersiz bir nokta
- Sistemik tarama yapılamaz — ama bilinen sınıflı fonksiyonlarla (lineer,
  eşik, simetrik) örtüşme gösterilemedi

---

## 5. Sonuç

Coulomb kapısı aşağıdaki özelliklere sahip özgün bir dönüşüm kapısıdır:

| Özellik              | Durum |
|----------------------|-------|
| Pozisyon duyarlı     | ✓     |
| Klasik kapılardan farklı | ✓ |
| Dengeli truth table  | ✓     |
| Fiziksel analogu var | ✓     |
| Bijektif (beam ile)  | ✓     |
| Ölçeklenebilir       | ✓     |

**Kriptolama için değil, dönüşüm/difüzyon katmanı için önerilir.**
Şifreleme güvenliği için ek katmanlar (key mixing, çok tur) gerekir.

---

## 6. Açık Sorular

1. Coulomb, bilinen herhangi bir fonksiyon sınıfının (lineer, kuadratik,
   eşik) özel durumu mudur? — Formal kanıt gerekli
2. 8-bit ve üzeri kapılarda bijeksiyon tek başına (beam olmadan) sağlanabilir mi?
3. Ters fonksiyon (deşifre) kapalı formda türetilebilir mi?

---

*Bu belge EIDA projesinin bir parçasıdır. Güven Acar, 2026, İzmir.*
