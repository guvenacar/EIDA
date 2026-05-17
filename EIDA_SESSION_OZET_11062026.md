# EIDA Projesi — Oturum Özeti
**Tarih:** 2026, İzmir  
**Geliştirici:** Güven Acar  
**Amaç:** IoT cihazlar için düşük kaynaklı, kuantum dirençli kriptografi sistemi

---

## 1. Temel Kavramlar

### Dairesel Dizi
- Dizinin son elemanı ile ilk elemanı birbirine bağlı (dairesel)
- İlk bit `0` → saat yönünde hareket
- İlk bit `1` → saat yönünün tersine (veya reverse + ilgili index başa al)

### Kapı Oluşturma Kuralı
Her eleman için:
- Bit `0` ise: o index'i başa al → ikilileri/üçlüleri oluştur
- Bit `1` ise: diziyi reverse et → o index'i başa al → ikilileri/üçlüleri oluştur

### Dönüşüm Kuralı (EIDA v1 — XOR Tabanlı)
- Kapı **homojen** (`00` veya `11`) → geçen bit **değişmez**
- Kapı **heterojen** (`01` veya `10`) → geçen bit **dönüşür**
- Bu klasik XOR ile eşdeğer ama pozisyon bağımlı olduğu için farklı sonuçlar üretir

---

## 2. Kapı Sistemi Katmanları (8 bitlik dizi için)

| Adım | Kapı Genişliği | Kapı Sayısı | Üretilen Bit |
|------|---------------|-------------|--------------|
| 1 adımlık | 2 bit | 8 | 8 bit |
| 2 adımlık | 4 bit | 4 | 4 bit |
| 3 adımlık | 6 bit | 8 | 8 bit |
| 4 adımlık | 8 bit | 2 | 2 bit |
| 5 adımlık | 10 bit | 8 | 8 bit |
| 6 adımlık | 12 bit | 4 | 4 bit (ilk 2 alınır) |
| 7 adımlık | 14 bit | 8 | 8 bit |

**n adımlık sistemde kapı sayısı:** `8 / gcd(8, n)`

---

## 3. 128 Bitlik Sistem (En İyi Sonuç)

```
1 adımlık → 8 bit
2 adımlık → 4 bit  (simetri kontrolü var)
3 adımlık → 2 bit  (ilk 2 kapı)
4 adımlık → 2 bit  (ilk 2 kapı)
Toplam: 16 bit/eleman × 8 eleman = 128 bit
```

**Sonuçlar:**
- Benzersiz çıktı: 256/256 ✓
- Çakışma yok ✓
- 1 bit fark: %25.1
- Genel ortalama: %50.2 ✓

**Python kodu:** `eida128.py`

---

## 4. EIDA v1 — Matematiksel Kanıtlar

### Yenilik Kanıtı
- 4-bit uzayda tüm klasik kapılarla (AND, OR, XOR, NAND, NOR, XNOR, NOT, Identity) karşılaştırıldı
- Hiçbir sabit B vektörü ile örtüşme sağlanamadı
- **EIDA yeni bir Boolean kapısıdır** ✓

### Bijeksiyon
- 2, 4, 6, 8 bit için tam bijeksiyon ✓
- Tersinir → şifreleme için uygun

### XOR'dan Fark
- 8-bit: 235/256 durumda farklı (%91.8)
- Sadece eşit sayıda 0 ve 1 içeren simetrik dizilerde XOR ile örtüşüyor

### Sabit Noktalar
- Sadece `000...0` ve `111...1` (homojen diziler)

### Periyot
- 8-bit: maksimum 8 tur
- 256-bit: >1000 tur (şifreleme için güçlü) ✓

### Lineerlik
- **Açık soru:** EIDA bir cyclic shift (dairesel bit kaydırma) operatörü mü?
- Truth table bu yönde işaret ediyor, kesin kanıt gerekli

---

## 5. EIDA v2 — Coulomb Kuvvet Kapısı

### Fiziksel Analoji
Her bit elektrik yükü gibi davranır:
- Geçen bit `0`: kapıdaki `0`'lar **iter** (−), `1`'ler **çeker** (+)
- Geçen bit `1`: kapıdaki `1`'ler **iter** (−), `0`'lar **çeker** (+)
- Kuvvet: `F = k / mesafe` (Coulomb yasası)
- Bileşke > 0 → dönüşür, ≤ 0 → kalır

### 4 Bitlik Kapı Kuvvet Tablosu (geçen bit = 0)
```
Kapı    Sol2   Sol1   Sağ1   Sağ2   Bileşke  Sonuç
0000    -0.5   -1.0   -1.0   -0.5   -3.0     0 kalır
0001    -0.5   -1.0   -1.0   +0.5   -2.0     0 kalır
0010    -0.5   -1.0   +1.0   -0.5   -1.0     0 kalır
0011    -0.5   -1.0   +1.0   +0.5    0.0     0 kalır
0100    -0.5   +1.0   -1.0   -0.5   -1.0     0 kalır
0101    -0.5   +1.0   -1.0   +0.5    0.0     0 kalır
0110    -0.5   +1.0   +1.0   -0.5   +1.0     1 olur  ← Çoğunluktan FARKLI!
0111    -0.5   +1.0   +1.0   +0.5   +2.0     1 olur
1000    +0.5   -1.0   -1.0   -0.5   -2.0     0 kalır
1001    +0.5   -1.0   -1.0   +0.5   -1.0     0 kalır
1010    +0.5   -1.0   +1.0   -0.5    0.0     0 kalır
1011    +0.5   -1.0   +1.0   +0.5   +1.0     1 olur
1100    +0.5   +1.0   -1.0   -0.5    0.0     0 kalır
1101    +0.5   +1.0   -1.0   +0.5   +1.0     1 olur
1110    +0.5   +1.0   +1.0   -0.5   +2.0     1 olur
1111    +0.5   +1.0   +1.0   +0.5   +3.0     1 olur
```
**Simetri:** Negatif=6, Sıfır=4, Pozitif=6 ✓  
**Geçen bit = 1 için tam ayna simetri geçerli** ✓

### Coulomb ≠ Çoğunluk Kuralı
`0110` kapısı için:
- Çoğunluk: 2 adet 0, 2 adet 1 → eşitlik → değişmez
- Coulomb: bileşke = +1 → **1 olur** ← FARKLI!
Coulomb **pozisyona duyarlı**, çoğunluk değil.

### Özellikler
- Bijeksiyon: YOK (birden-çoka)
- Kullanım: **Difüzyon** (hash, karıştırma)
- Kanat genişliği: ayarlanabilir (2, 4, 6, 8... bit)

**Python kodu:** `eida_coulomb.py`

---

## 6. Işın Demeti (Beam) Sistemi

### Kavram
Tek tanecik yerine çok tanecikli (demet) geçiş:
- Her tanecik bağımsız kapıdan geçer
- Demet çıktısı da çok bitli
- Kriptografi için uygun (bijektif olabilir)

### Mekanizma (8 bit, 3 bitlik demet)
```
Orijinal dizi: 10001100 (indexler 0-7)

1. adım: demet=result[0,1,2], kapı=original[0,1,2,3,4,5]
2. adım: demet=result[3,4,5], kapı=original[3,4,5,6,7,0]
3. adım: demet=result[6,7,0], kapı=original[6,7,0,1,2,3]
4. adım: demet=result[1,2,3], kapı=original[1,2,3,4,5,6]
...
```

**Kural:**
- Kapılar **orijinal diziden** belirlenir (değişmez)
- Demetler **güncel diziden** alınır (her adım güncellenir)
- Her adımda `beam_size` kadar ilerler
- `gcd(8, 3) = 1` → 8 adımda tüm dizi işlenir

**Kapı indexleri (beam_size=3):**
```
1. kapı: 0,1,2,3,4,5
2. kapı: 3,4,5,6,7,0
3. kapı: 6,7,0,1,2,3
4. kapı: 1,2,3,4,5,6
5. kapı: 4,5,6,7,0,1
6. kapı: 7,0,1,2,3,4
7. kapı: 2,3,4,5,6,7
8. kapı: 5,6,7,0,1,2
```

**Python kodu:** `eida_beam.py`

**Test sonucu (10001100):**
```
Giriş:  10001100
Çıkış:  00111000
Fark:   4/8 bit (%50)
```

**Açık sorular:**
- İstatistiksel kalite analizi henüz yapılmadı
- Bijeksiyon kontrolü yapılmadı
- Farklı beam_size değerleri denenmedi

---

## 7. Karıştırma Sistemi (256 bit)

### Genel Hedef
- 256 bitlik IoT mesajını karıştır
- %50 avalanche etkisi
- Private key ile şifreleme

### Denenen Yöntemler
1. **32 byte → 8 bit/byte → 256 bit maske:** Genel ort. %50, 1-bit fark %1.7 (zayıf)
2. **f(msg) XOR f(key):** 1-bit key fark %0.6 (çok zayıf)
3. **Dairesel zincirleme:** 4 blok, tam dairesel XOR → %11.2 dengeli ✓

### En İyi Sonuç
32 byte, her byte 8 bit üretir, dairesel difüzyon:
- Genel ort: %50.0 ✓
- Her blok eşit katkı: ~%11.2 ✓

**Ana sorun:** Avalanche etkisi zayıf (%11 civarı, hedef %50)
**Çözüm yolu:** EIDA beam sistemi ile difüzyon güçlendirme

---

## 8. Sonraki Adımlar

1. **Beam sistemi istatistiksel analizi** — bijeksiyon, avalanche, dağılım
2. **EIDA lineerlik kanıtı** — cyclic shift mi, gerçekten yeni mi?
3. **Beam + 256 bit entegrasyonu** — karıştırma kalitesi testi
4. **Private key entegrasyonu** — EIDA mimarisine bağlama
5. **EIDA v1 belgesini güncelle** — Güven Acar (Yılmaz değil!)

---

## 9. Python Dosyaları

| Dosya | İçerik |
|-------|--------|
| `eida128.py` | 8→128 bit sistemi, en iyi istatistiksel sonuç |
| `eida_coulomb.py` | Coulomb kuvvet kapısı (v2) |
| `eida_beam.py` | Işın demeti sistemi |
| `eida_mix.py` | 256 bit karıştırma denemeleri |
| `eida_vs_xor.py` | EIDA vs klasik kapılar karşılaştırması |
| `eida_proof.py` | Matematiksel kanıtlar |

---

*Bu belge bir sonraki oturumda bağlamı korumak için oluşturulmuştur.*
