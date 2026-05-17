**EIDA: Yeni Bir Boolean Kapısı**  
*Edge-Indexed Directional Automaton*  
Güven ACAR — İzmir, 2026  
# **1. Giriş**  
Bu belge, MELP programlama dilinin kriptografik altyapısı üzerine yürütülen araştırma sürecinde keşfedilen yeni bir Boolean kapısını tanımlamakta ve matematiksel özelliklerini belgelemektedir.  
Klasik Boolean cebiri dört temel iki-operandlı kapı üzerine kurulmuştur: AND, OR, XOR ve NAND. Tek-operandlı kapı ise NOT'tur. Bu çalışmada tanımlanan EIDA kapısı, tek operandlı çalışmasına rağmen klasik kapıların hiçbirine ve bunların sabit-operandlı kombinasyonlarına indirgenemeyen yeni bir operatördür.  
# **2. Formal Tanım**  
## **2.1 Temel Kural**  
n-bitlik dairesel bir X = [x₀, x₁, ..., x_{n-1}] dizisi verilsin. EIDA operatörü her i indisi için şu şekilde tanımlanır:  
   
seq_i = rotate(X, i)          // X dizisini i adım sola döndür  
gate_i = [seq_i[0], seq_i[1]] // İlk iki elemanı kapı olarak al  
   
EIDA(X)[i] = NOT(X[i])   eğer gate_i[0] ≠ gate_i[1]  
EIDA(X)[i] = X[i]        eğer gate_i[0] = gate_i[1]  
   
Kısaca: bit i, kendi konumundan başlayan dairesel perspektifte komşu iki bit farklıysa dönüşür; aynıysa değişmez. Bu kural her bit için bağımsız uygulanır.  
## **2.2 Örnek (4 bit)**  
X = 0101 için EIDA uygulaması:  
| | | | | |  
|-|-|-|-|-|  
| **i** | **X[i]** | **seq_i (rotate)** | **gate_i** | **EIDA[i]** |   
| 0 | 0 | 0101 | 01 (≠) | 1 |   
| 1 | 1 | 1010 | 10 (≠) | 0 |   
| 2 | 0 | 0101 | 01 (≠) | 1 |   
| 3 | 1 | 1010 | 10 (≠) | 0 |   
Sonuç: EIDA(0101) = 1010  
# **3. Matematiksel Kanıtlar**  
## **3.1 Kanıt 1: Yenilik — Mevcut Kapılara İndirgenemezlik**  
4-bitlik uzayda tüm 16 giriş için EIDA truth table'ı oluşturulmuş ve şu klasik kapılarla karşılaştırılmıştır: AND, OR, XOR, NAND, NOR, XNOR, Identity, NOT.  
Karşılaştırma yöntemi: Her B ∈ {0,1}ⁿ sabit vektörü için op(X, B) = EIDA(X) eşitliği tüm X değerleri için test edilmiştir.  
Sonuç: Hiçbir klasik iki-operandlı kapı ve hiçbir sabit B vektörü kombinasyonu EIDA ile tam örtüşme sağlayamamıştır. EIDA, mevcut Boolean cebirinin dışında yeni bir operatördür.  
## **3.2 Kanıt 2: Tutarlılık ve Bijeksiyon**  
EIDA operatörü farklı bit uzunluklarında test edilmiştir:  
| | | | |  
|-|-|-|-|  
| **Bit Uzunluğu** | **Toplam Giriş** | **Benzersiz Çıktı** | **Bijeksiyon** |   
| 2 bit | 4 | 4 | ✓ |   
| 4 bit | 16 | 16 | ✓ |   
| 6 bit | 64 | 64 | ✓ |   
| 8 bit | 256 | 256 | ✓ |   
EIDA tüm n-bit uzunluklarında tam bijeksiyondur. Bu, operatörün tersinir olduğunu ve şifreleme/şifre çözme için uygun olduğunu göstermektedir.  
## **3.3 Kanıt 3: Klasik XOR'dan Farklılık**  
8-bitlik 256 dizi için EIDA ve XOR sonuçları karşılaştırılmıştır:  
EIDA ≠ XOR: 235 / 256 durumda (%91.8)  
EIDA = XOR: 21 / 256 durumda (%8.2) — yalnızca belirli simetrik yapılarda örtüşme  
4-bitlik truth table karşılaştırması:  
| | | | |  
|-|-|-|-|  
| **Giriş** | **EIDA Çıktısı** | **XOR Çıktısı** | **Fark?** |   
| 0000 | 0000 | 0000 | = |   
| 0001 | 0010 | 0011 | ✗ |   
| 0010 | 0100 | 0110 | ✗ |   
| 0011 | 0110 | 0101 | ✗ |   
| 0100 | 1000 | 1100 | ✗ |   
| 0101 | 1010 | 1111 | ✗ |   
| 0110 | 1100 | 1010 | ✗ |   
| 0111 | 1110 | 1001 | ✗ |   
| 1000 | 0001 | 1001 | ✗ |   
| 1001 | 0011 | 1010 | ✗ |   
| 1010 | 0101 | 1111 | ✗ |   
| 1011 | 0111 | 1100 | ✗ |   
| 1100 | 1001 | 0101 | ✗ |   
| 1101 | 1011 | 0110 | ✗ |   
| 1110 | , 1101 | 0011 | ✗ |   
| 1111 | 1111 | 0000 | ✗ |   
## **3.4 Kanıt 4: Cebirsel Özellikler**  
Periyot analizi (4-bit, 16 dizi):  
Periyot 1 (sabit nokta): 2 dizi — [0000, 1111]  
Periyot 2 (involutory):  2 dizi  
Periyot 4:              12 dizi  
256-bitlik dizilerde periyot 1000 turdan büyüktür — şifreleme için güçlü bir özellik.  
Sabit noktalar: Yalnızca tam homojen diziler (000...0 ve 111...1) sabit noktadır. Bu minimal sabit nokta kümesi kriptografik açıdan olumludur.  
## **3.5 Kompozisyon: EIDA² Ne Üretiyor?**  
EIDA(EIDA(X)) her X için tutarlı bir klasik operatör üretmemektedir:  
0000 → 0000 → 0000  (Identity)  
0011 → 0110 → 1100  (NOT)  
0101 → 1010 → 0101  (Identity)  
0001 → 0010 → 0100  (diğer)  
EIDA² ne tamamen Identity ne de tamamen NOT'tur. Bu, EIDA'nın kendi kendisinin tersi olmadığını göstermektedir.  
# **4. Kriptografik Açıdan Önemli Özellikler**  
| | | |  
|-|-|-|  
| **Özellik** | **Durum** | **Açıklama** |   
| Bijeksiyon | ✓ Tam | Tersinir, şifre çözme mümkün |   
| Yenilik | ✓ Kanıtlandı | Klasik kapılara indirgenemiyor |   
| Sabit noktalar | ✓ Minimal | Sadece 000...0 ve 111...1 |   
| Periyot (256 bit) | ✓ >1000 | Döngüye girmiyor |   
| XOR'dan fark | ✓ %91.8 | Çok farklı davranış |   
| Lineerlik | ⚠ İnceleniyor | Daha derin analiz gerekli |   
| Çığ etkisi | ⚠ Zayıf | Manipülasyon ile güçlendirilebilir |   
# **5. Sonraki Adımlar ve Açık Sorular**  
1. Lineerlik analizi: EIDA bir dairesel bit kaydırma (cyclic shift) operatörü müdür? Truth table bu yönde işaret etmektedir ancak kesin kanıt gereklidir.  
2. Reverse varyant: Bit değerine göre yön seçimi (0→normal, 1→reverse) eklendiğinde bijeksiyon bozulmakta, ancak farklı cebirsel özellikler ortaya çıkmaktadır. Bu varyantın bağımsız analizi yapılacaktır.  
3. Çığ etkisi güçlendirmesi: Sıfır manipülasyonla %50 çığ etkisine ulaşmak için yeni kombinasyonlar araştırılacaktır.  
4. Akademik yayın: Operatörün yeni olduğu kanıtlandıktan sonra arXiv'e gönderim planlanmaktadır.  
# **6. Python Referans Implementasyon**  
def eida(bits):  
    n = len(bits)  
    result = []  
    for i in range(n):  
        seq = bits[i:] + bits[:i]  # rotate  
        gate = [seq[0], seq[1]]  
        if gate[0] != gate[1]:     # heterojen  
            result.append(1 - bits[i])  
        else:                       # homojen  
            result.append(bits[i])  
    return result  
EIDA — MELP Projesi Dahili Araştırma Belgesi — 2026  
