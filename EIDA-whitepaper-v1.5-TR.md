# EIDA-whitepaper-v1.5-TR.md


# EIDA
## Geçici Kimlik Dağıtım Mimarisi
### Whitepaper v1.5 — Türkçe


---
**Versiyon 1.5 — Mayıs 2026**
## 1. Özet

Klasik Açık Anahtar Altyapısı (PKI), statik kimlik garantileri sağlar — bir açık anahtarın bir varlığa ait olduğunu kanıtlar ancak belirli bir işlemin o anda o varlıktan geldiğini garanti edemez. Bu boşluk, tekrar saldırılarına, anahtar yeniden kullanım açıklarına ve uzun vadeli uzlaşma zincirlerine yol açar.

EIDA (Ephemeral Identity Distribution Architecture — Geçici Kimlik Dağıtım Mimarisi), işlem düzeyinde bağlantısızlık ve oturum anahtarı ileri gizliliği sunarak bu boşluğu giderir. Kalıcı kimlik anahtarı (uPriv), yalnızca donanımsal izolasyon ile korunur — ele geçirilmesi gelecekteki işlemleri açığa çıkarabilir ancak geçmiş oturum anahtarlarını açığa çıkarmaz. Temel primitif olan ePriPub, kullanıcının kalıcı kimliğinden işlem başına türetilen ve donanım destekli izolasyon bölgesinden asla çıkmayan tek kullanımlık geçici bir anahtar çiftidir. Kullanıldıktan sonra ePriPub bileşenleri yok edilir ve CA yeni bir tek kullanımlık sertifika yayımlar — kalıcı durum gerekmez.

EIDA, güven modelini merkezi otorite doğrulamasından kriptografik işlem benzersizliğine kaydırarak, güvenilir aracılara ihtiyaç duymadan güvenliği kullanıcıya dağıtır.

---

## 2. Problem

Günümüzde kullanıcı kimliklerini güvence altına almakla sorumlu şirketler sürekli saldırı altındadır. Merkezi bir güvenlik sistemindeki tek bir ihlal, milyonlarca kullanıcının kişisel verilerini açığa çıkarabilir. Bu, mevcut mimarinin kaçınılmaz bir sonucudur: güvenlik merkezidir ve merkezileşme yüksek değerli hedefler yaratır.

EIDA, bu sorumluluğu kullanıcı cihazlarına dağıtmayı önerir. Merkezi olmayan bir modelde, tek bir düğümü ele geçiren bir saldırgan milyonlarca kişinin değil, yalnızca bir kişinin verilerine erişir. Büyük teknoloji şirketleri artık birincil hedef değildir. Saldırı yüzeyi tek bir kritik sistemden milyonlarca bireysel cihaza küçülür.

Klasik PKI bu merkezileşme sorununu pekiştirir. Bir açık anahtarın bir varlığa ait olduğunu garanti eder ancak belirli bir işlemin o anda o varlıktan geldiğini doğrulayamaz — tekrar saldırılarına, anahtar yeniden kullanımına ve uzun vadeli uzlaşma zincirlerine olanak tanır.

---
![EIDA Mimari Diyagramı](https://raw.githubusercontent.com/guvenacar/EIDA/main/diagrams/diagram_1.png)

## 3. Mimari

EIDA üç katmandan oluşur:

**1. Kullanıcı İzolasyon Bölgesi**

Kullanıcının kalıcı gizli anahtarı (uPriv) bir güvenlik bölgesi içinde bulunur. EIDA üç güvenlik seviyesi tanımlar:

**Seviye 1 (Maksimum - Varsayılan):** Donanım destekli izolasyon bölgesi (TPM 2.0 / TEE / ARM TrustZone). uPriv bu ortamdan asla çıkmaz. Tüm üretim dağıtımları için önerilir.

**Seviye 2 (Orta):** Kod imzalama doğrulaması ile yazılım tabanlı izolasyon (örn. güvenli yerleşim, bütünlük ölçümlü korumalı alan). Düşük riskli işlemler veya geliştirme için kabul edilebilir.

**Seviye 3 (Minimum):** Doğrulama olmaksızın korumalı bellek bölgesi. Yalnızca test veya üretim dışı kullanım için.

**Platform Notları:**
- Mobil (ARM TrustZone): Seviye 1 desteklenir
- Masaüstü (Intel SGX/TDX): Uyumlu donanımda Seviye 1 desteklenir
- Eski sistemler: Yalnızca Seviye 2 veya Seviye 3

Kuruluşlar, CA politikası aracılığıyla minimum güvenlik seviyelerini zorunlu kılabilir.

> **TEE/TPM Gereksinimleri Hakkında Önemli Açıklama:** TEE/TPM YALNIZCA kullanıcı cihazlarında gereklidir. CA sunucuları, taraf olan taraflar (bankalar, sosyal medya platformları) ve ağ aktörleri TEE/TPM gerektirmez. Güvenlik modeli, saldırı yüzeyini merkezi altyapıda yoğunlaştırmak yerine milyonlarca kullanıcı cihazına dağıtır. Bir kullanıcı birden fazla cihaza sahipse, HER cihaz kendi bağımsız uPriv/uPub çiftini korur. Cihazlar arası anahtar senkronizasyonu bu standardın kapsamı dışındadır.

**2. ePriPub Türetme Katmanı**

Her işlem için, izolasyon bölgesi içinde tek kullanımlık geçici bir anahtar çifti türetilir:

```
uPriv + nonce + timestamp → HKDF → seed → Ed25519 → (ePriv, ePub)
```

Nonce her işlem için rastgele üretilir ve bir zaman damgası ile birleştirilir, böylece hiçbir iki türetme aynı anahtar çiftini üretmez. İşlem benzersizliği (ePub, nonce, timestamp) kombinasyonu ile sağlanır — harici bir token koordinatörü gerekmez.

**3. Durumsuz CA Katmanı**

CA reaktif bir imzalayıcı olarak çalışır — önceki istekleri taramaz, saklamaz veya izlemez. Gelen her istek kendi kendine yeten, atomik bir birim olarak ele alınır:

```
Al:      (ePub + nonce + timestamp + imza)
Doğrula: imza geçerli mi? → evet
         timestamp TTL içinde mi? → evet
Üret:    yeni (sPriv, sPub) anahtar çifti
Yayımla: sCert = {sPub + son_kullanma + üstveri}, CA anahtarı ile imzalı
Gönder:  (sCert + imzalı belge) kullanıcı izolasyon bölgesine
Unut:    sPriv yok edildi, durum saklanmadı
```

CA, işlenmiş isteklerin bir kara liste veya kalıcı kaydını tutmaz. Tekrar koruması, zaman damgasındaki kısa TTL penceresi ve sCert'in doğal tek kullanımlık yapısı ile sağlanır. Bu durumsuz tasarım sınırsız yatay ölçeklenebilirlik sağlar — her CA düğümü veritabanı senkronizasyonu olmadan bağımsız çalışır.

---

## 3.5 Ölçeklenebilirlik Modeli: Durumsuz Doğrulama ve İptal Listelerinin Sonu

### Eski Darboğaz

Geleneksel PKI ve kimlik sistemleri, *Durum Tükenmesi Problemi* olarak adlandırılabilecek bir sorundan muzdariptir. Bir token veya anahtarın yeniden kullanılmadığından veya tehlikeye girmediğinden emin olmak için, bir Sertifika Otoritesi büyük, sürekli büyüyen Sertifika İptal Listeleri (CRL) tutmalı veya gerçek zamanlı durum sorgularına (OCSP) yanıt vermelidir. Bu, tek bir gecikme noktası ve kullanıcı nüfusları yüz milyonlara ulaştığında kötü ölçeklenen bir veritabanı yükü yaratır.

### EIDA Modeli: Sıfır-Durum Ölçeklenebilirliği

EIDA, doğrulama sırasında bir kara liste veya herhangi bir merkezi veritabanı sorgulama ihtiyacını ortadan kaldırır. CA'nın durum yönetimi kapasitesini ölçeklendirmek yerine, EIDA güvenlik yükünü CA'dan zamana ve donanıma taşır:

**1. Donanımla Zorlanan Geçicilik**

ePriPub çifti, donanım destekli bir izolasyon bölgesi (TPM/TEE) içinde üretilir ve kesinlikle tek bir işlem bağlamına bağlıdır. Anahtar çifti, imzalamadan hemen sonra istemci tarafında yok olur — politika gereği değil, tasarım gereği. İptal edilecek bir şey yoktur çünkü kalıcı olan hiçbir şey yoktur.

**2. Zamansal Otomatik Geçersizleştirme**

Her EIDA token'ı, yüksek hassasiyetli bir zaman damgasına kriptografik olarak bağlıdır. CA anahtarları iptal etmez; sadece `Şimdiki_Zaman − Zaman_Damgası > TTL` olan istekleri reddeder. Geçersizleştirme, bir veritabanı işlemi değil, zamanın matematiksel bir sonucudur.

**3. O(1) Doğrulama Karmaşıklığı**

CA tamamen matematiksel bir doğrulama gerçekleştirir: imzayı ve saati kontrol eder. Hiçbir veritabanı sorgulanmaz, hiçbir liste kontrol edilmez. Doğrulama karmaşıklığı, veritabanı sorgulamaları açısından O(1)'dir — durum sorgulaması gerekmez.

Ancak pratik ölçeklenebilirlik hala şunlara bağlıdır:
- Ağ bant genişliği ve gecikme
- CA'nın imzalama verimi (saniye başına kriptografik işlem)
- Durumsuz CA düğümleri arasında yük dengeleme

**Gerçek Performans Özellikleri:**
- Matematiksel doğrulama: İstek başına O(1)
- Yatay ölçeklenme: Doğrusal (N düğüm = N× verim)
- Veritabanı darboğazı yok: Durumsuz tasarım merkezi çekişmeyi ortadan kaldırır

EIDA, durumsuz tasarım sayesinde doğrusal ölçeklenme sağlar ancak donanım kapasitesi ve ağ kısıtları bağlayıcı faktörler olarak kalır.

> **Mimari Not:** EIDA'da güvenlik, bir veritabanında tutulan bir kayıt değil — matematiğin ve donanımın bir özelliğidir. CA, durumsuz bir kapı bekçisi olarak çalışır ve sistemi modern PKI dağıtımlarını kısıtlayan ölçeklenebilirlik darboğazlarına karşı yapısal olarak bağışık hale getirir.

---

### 3.6 Tekrar Koruması İyileştirmesi

EIDA'nın temel TTL tabanlı tekrar koruması çoğu dağıtım için yeterlidir. Ancak yüksek verimli ortamlar için isteğe bağlı bir nonce mekanizması mevcuttur:

**İstemci Tarafı (Kullanıcı İzolasyon Bölgesi):**
```
nonce ← TRNG(32 bayt)  // Donanımsal rastgele değer
istek = {ePub, nonce, timestamp, imza}
```

**CA Tarafı (Yumuşak Durum Önbelleği):**
- CA, son (nonce, timestamp) çiftlerinin isteğe bağlı, geçici bir önbelleğini tutar
- Önbellek boyutu: yapılandırılabilir (varsayılan: son 10.000 benzersiz nonce)
- Önbellek zaman aşımı: 2 × TTL (varsayılan: 10 saniye)
- **Bu kalıcı durum değildir** — önbellek kaybı yalnızca TTL penceresi içindeki potansiyel tekrarlara izin verir

**Doğrulama Mantığı:**
```
if (nonce, timestamp) önbellekte varsa:
    reddet("Tekrar saldırısı tespit edildi")
else:
    önbellek.ekle(nonce, timestamp)
    doğrulamaya devam et
```

**Not:** Bu iyileştirme İSTEĞE BAĞLIDIR. Saf durumsuzluğu önceliklendiren dağıtımlar yalnızca TTL tabanlı korumaya güvenebilir.

---

### 3.7 Kimlik Başlangıcı (İlk Kullanımda Güven)

EIDA, önceden var olan güven ilişkilerini varsaymaz. Bir kullanıcının kalıcı açık anahtarının (uPub) CA'ya ilk kaydı, fiziksel veya biyometrik kimlik kanıtı gerektirir.

#### Yöntem 1: Fiziksel Kayıt (Önerilen)
1. Kullanıcı, bir devlet tesisinde (örn. PTT şubesi, nüfus müdürlüğü) TEE/TPM içinde (uPriv, uPub) üretir
2. Görevli, resmi kimliği doğrular ve uPub'ı kullanıcının kimliğiyle ilişkilendirir
3. CA, uPub'ı kullanıcıya bağlayan ilk sertifikayı yayımlar
4. Sertifika kullanıcının TEE/TPM'sinde saklanır

#### Yöntem 2: Uzaktan Biyometrik Kayıt
1. Kullanıcı, TEE/TPM içinde (uPriv, uPub) üretir
2. Devlet mobil uygulaması, canlılık tespiti ve biyometrik doğrulama gerçekleştirir
3. Uygulama, kullanıcının kimlik talebini dijital olarak imzalar ve CA'ya iletir
4. CA, devlet imzasını doğruladıktan sonra sertifika yayımlar

#### Güvenlik Garantisi
Bu başlangıç adımı olmadan, bir saldırgan sahte kimlikler altında rastgele uPub değerleri kaydedebilir.

#### Gizlilik Notu
CA, normal işlemler sırasında kişisel olarak tanımlanabilir bilgi (PII) almaz — yalnızca bu tek seferlik kayıt sırasında alır.

---

## 4. ePriPub — Geçici Birincil Açık Anahtar Primitifi

ePriPub, EIDA'nın temel primitifidir. Bir protokol değil — tam olarak bir işlem için hem imzalama hem doğrulama yeteneği taşıyan tek kullanımlık bir kriptografik kimlik birimidir.

### 4.1 Tanım

ePriPub, (ePriv, ePub) geçici bir anahtar çiftidir:
- **ePriv** — geçici gizli bileşen, onay token'ını imzalamak için bir kez kullanılır, hemen ardından yok edilir
- **ePub** — geçici açık bileşen, imza doğrulaması için CA'ya gönderilir, kullanımdan sonra atılır

İşlem tamamlandıktan sonra hiçbir bileşen hiçbir yerde saklanmaz.

### 4.2 Türetme

```
Girdiler:
  uPriv     — kalıcı kullanıcı gizli anahtarı (izolasyon bölgesinden asla çıkmaz)
  nonce     — 32 bayt kriptografik rastgele değer (işlem başına üretilir)
  timestamp — milisaniye cinsinden Unix zaman damgası (işlem başına üretilir)

İşlem:
  seed = HKDF(uPriv + nonce + timestamp)
  (ePriv, ePub) = Ed25519_turet(seed)

Çıktı:
  (ePriv, ePub) — yalnızca bu işlem için geçerli

**Zaman Damgası Güvenlik Notu:**
Zaman damgası, HKDF girdisine (uPriv + nonce + timestamp) dahil edilir ve kriptografik türetmenin bir parçası haline gelir. Ancak doğrulama için, zaman damgası AYRICA açık metin olarak iletilmeli ve imza kapsamına dahil edilmelidir. Bu, saldırganların türetme sonrasında zaman damgasını değiştirmesini engeller.

**Önerilen zaman damgası doğrulaması:**
1. İmzalı istekten zaman damgasını çıkar
2. |şimdiki_zaman - timestamp| ≤ TTL olduğunu doğrula
3. Pencere dışındaysa reddet (tekrarı önler)
4. Doğru zaman için çoklu kaynaklı NTP veya donanım RTC kullan

**TTL yapılandırması:** Varsayılan 5 saniye. Önerilen aralık: LAN/dahili dağıtımlar için 1-5 saniye, internet odaklı dağıtımlar için 5-30 saniye. Daha kısa TTL değerleri daha güçlü tekrar koruması sağlar ancak daha sıkı saat senkronizasyonu gerektirir.

**NTP güvenliği:** Yüksek güvenlikli dağıtımlar için kimlik doğrulamalı NTP (RFC 5905) veya GPS zaman kaynakları değerlendirilmelidir.
```

### 4.3 Yaşam Döngüsü

```
 1. TÜRET    — (ePriv, ePub) izolasyon bölgesinde üretilir
 2. İMZALA   — onay token'ı (ePub + nonce + timestamp) ePriv ile imzalanır
 3. İLET      — (ePub + nonce + timestamp + imza) CA'ya gönderilir
 4. DOĞRULA  — CA imzayı ve timestamp TTL'sini doğrular
 5. YOK ET   — ePriv izolasyon bölgesinde yok edilir
 6. ÜRET     — CA yeni oturum anahtar çifti (sPriv, sPub) üretir
 7. İMZALA-D — CA belgeyi sPriv ile imzalar, sCert yayımlar
 8. YANITLA  — (sCert + imzalı belge) kullanıcı izolasyon bölgesine gönderilir
 9. İLET     — izolasyon bölgesi talep eden kuruma iletir
10. TEMİZLE  — sPriv CA tarafından yok edilir
```

### 4.4 Güvenlik Özellikleri

- **Tek kullanımlık** — sCert TTL'den sonra geçersiz olur, tekrar saldırıları zaman damgası ile engellenir
- **Kimliğe bağlı** — türetme zinciri ePriPub'ı uPriv'e maruz bırakmadan bağlar
- **İleri gizlilik** — herhangi bir ePriPub'ın ele geçirilmesi uPriv hakkında hiçbir şey açığa çıkarmaz. Ancak uPriv'in ele geçirilmesi tüm geçmiş ePriPub türetme zincirlerini (ama oturum anahtarlarının kendilerini değil, onlar yok edilmiştir) açığa çıkarır. Gerçek kimlik düzeyinde ileri gizlilik için uPriv asla ele geçirilmemelidir — bu donanımsal izolasyon ile zorlanır.
- **Durumsuz CA** — CA istekler arasında durum tutmaz, sınırsız yatay ölçeklenebilirlik sağlar

### 4.5 ePriPub Kullanıcı Onay Kanıtı Olarak

Klasik e-imza modellerinde, kullanıcı belgeyi doğrudan kendi gizli anahtarı ile imzalar. EIDA bunu iki ayrı sorumluluğa ayırır:

```
Kullanıcı → onayı kanıtlar    (ePriPub)
CA         → belgeyi imzalar    (sPriv)
```

Bu ayrım bilinçlidir. CA, işlem başına bir kez oturum anahtar çifti (sPriv, sPub) üretir ve gerçek belge imzasını gerçekleştirir. Ancak CA, yalnızca istekte geçerli, kullanılmamış bir ePriPub varsa imzalamaya devam eder.

Dolayısıyla ePriPub bir **kriptografik onay token'ı** olarak hizmet eder:

```
Geçerli ePriPub alındı → kullanıcı onayladı → CA imzalar ve sCert yayımlar
ePriPub yok            → onay kanıtı yok      → CA reddeder
Zaman damgası geçmiş   → TTL penceresi doldu  → CA reddeder
```

**İnkar edilemezlik garantisi:**

Kullanıcı işlemi başlattığını daha sonra inkar edemez çünkü:
- ePriPub uPriv'den türetilir — yalnızca kullanıcı üretebilir
- ePriPub tek kullanımlıktır — yakalanıp tekrar oynatılamaz
- (ePub + nonce + timestamp) kombinasyonu benzersizdir — başka bir bağlamda yeniden kullanılamaz

CA kullanıcı onayını taklit edemez çünkü:
- CA, uPriv'e erişim olmadan geçerli bir ePriPub üretemez
- uPriv kullanıcının izolasyon bölgesinden asla çıkmaz

---

## 5. Güvenlik Analizi

### 5.1 Tehdit Modeli

EIDA aşağıdaki saldırganları dikkate alır:

- **Ağ saldırganı** — iletilen verileri yakalar
- **CA saldırganı** — sertifika otoritesini ele geçirir
- **Cihaz saldırganı** — kullanıcının cihazına erişir
- **Tekrar saldırganı** — yakalanan işlemleri yeniden kullanmaya çalışır

### 5.2 Saldırı Senaryoları

**Ağ dinleme**
```
Saldırgan şunu yakalar: (ePub + nonce + timestamp + imza)
timestamp TTL → zaten geçmiş (kısa pencere)
Tekrar denemesi → CA reddeder: timestamp TTL dışında
uPriv → asla iletilmez → açığa çıkmaz
Sonuç: saldırı başarısız
```

**CA ele geçirme**
```
Saldırgan CA'ya erişir
CA depolar: kalıcı kullanıcı verisi yok, kara liste yok
sPriv anahtarları → her işlemden sonra yok edilir → kurtarılamaz
uPriv → CA'ya asla ulaşmaz → açığa çıkmaz
CA_priv → saldırgan sahte sertifikalar yayımlayabilir
          (CA gizli anahtarı için donanım güvenlik modülü — HSM — ile azaltılır)
Sonuç: saldırgan kullanıcı kimlik materyali bulamaz; HSM'deki CA_priv hasarı sınırlar
```

**Cihaz ele geçirme**
```
Saldırgan kullanıcı cihazına erişir
uPriv → TPM/TEE içinde → çıkarılamaz
Geçmiş ePriPub çiftleri → yok edilmiş → kurtarılamaz
Sonuç: saldırgan yalnızca fiziksel cihaz elinde olduğu sürece
        gelecekteki işlemlerle sınırlıdır
```

**Tekrar saldırısı**
```
Saldırgan geçerli (ePub + nonce + timestamp + imza) yakalar
CA timestamp'i kontrol eder → TTL penceresi geçmiş → reddedilir
TTL içinde bile: sCert zaten teslim edilmiş ve kurum tarafından kullanılmış
Kurum sCert geçerliliğini doğrular → reddedilir
Sonuç: saldırı başarısız
```

### 5.3 EIDA'nın İddia Etmedikleri

- EIDA, TPM'nin donanım düzeyinde atlatıldığı fiziksel cihaz ele geçirmeye karşı koruma sağlamaz
- EIDA anonimlik sağlamaz — uPriv kalıcı olarak kullanıcı kimliğine bağlıdır
- EIDA CA erişilebilirliğini ele almaz — çöken bir CA işlemleri engeller

### 5.4 Anahtar İptali ve Uzlaşma Yanıtı

EIDA'nın durumsuz tasarımı bir iptal zorluğu yaratır. Üç strateji desteklenir:

#### Strateji 1: Kısa TTL + Yeniden Kimlik Doğrulama (Varsayılan)
- TTL penceresi: 5-30 saniye (önerilen: internet için 10s, LAN için 5s)
- Açık iptal yok — anahtarlar doğal olarak geçersiz olur
- Ele geçirilen uPriv, kullanıcının yeni anahtar çiftiyle yeniden kaydolmasını gerektirir

#### Strateji 2: Harici CRL Hizmeti (İsteğe Bağlı)
- CA harici Sertifika İptal Listesi'ni tutar veya sorgular
- CRL, ele geçirilen anahtarların uPub değerlerini içerir
- CA her işlemden önce CRL'yi kontrol eder (ağ gecikmesi ekler)

#### Strateji 3: Kısa Ömürlü Sertifikalar (Hibrit)
- Kullanıcı CA'dan her 24 saatte bir yeni sertifika alır
- Sertifika kısa geçerlilik süresi içerir
- Ele geçirilen uPriv CA'ya bildirilir, CA yeni sertifika vermeyi durdurur

#### Önerilen Dağıtım
- Düşük güvenlikli uygulamalar: Strateji 1
- Kurumsal/düzenlenmiş ortamlar: Strateji 2 + Strateji 1 birleşimi
- Devlet sistemleri: Strateji 3

#### İptal Süreci (Tüm Stratejiler)
1. Kullanıcı, tehlikeye giren cihazı bant dışı kanal ile CA'ya bildirir
2. CA, uPub'ı iptal edildi olarak işaretler (Strateji 2) veya engelleme listesine ekler (Strateji 3)
3. Kullanıcı güvenli cihazda yeni (uPriv, uPub) çifti üretir
4. Kullanıcı Kimlik Başlangıcı sürecini (Bölüm 3.7) kullanarak yeniden kaydolur

---

## 6. Mevcut Yaklaşımlarla Karşılaştırma

### 6.1 Klasik PKI

| Özellik | Klasik PKI | EIDA |
|---|---|---|
| Kimlik garantisi | Statik | İşlem başına |
| Anahtar yeniden kullanımı | Evet | Asla |
| uPriv maruziyet riski | Yüksek | Yok |
| Tekrar koruması | Harici | Yerleşik |
| CA ihlal etkisi | Kritik | Minimal |
| İleri gizlilik | Oturum düzeyi | İşlem düzeyi |
| Merkezileşme | Yüksek | Yok |

### 6.2 TLS Geçici (TLS 1.3)

TLS 1.3, ileri gizlilik için geçici oturum anahtarları sunar. Ancak:
- Geçici anahtarlar **oturum katmanına** uygulanır, kimlik katmanına değil
- Sunucu sertifikası statik kalır ve tüm oturumlarda yeniden kullanılır
- Sunucu sertifikasının ele geçirilmesi tüm geçmiş ve gelecek oturumları etkiler

EIDA, geçici ilkesini TLS'nin asla dokunmadığı **kimlik katmanının kendisine** uygular.

### 6.3 Tek Kullanımlık İmza Şemaları (Lamport, WOTS)

Tek kullanımlık imza şemaları, tek kullanımlık özelliğini ePriPub ile paylaşır. Ancak:
- **Kuantum sonrası direnç** için tasarlanmışlardır, kimlik izolasyonu için değil
- Merkezileşme sorununu ele almazlar
- İzolasyon bölgesi modeli veya durumsuz CA mekanizmaları yoktur

ePriPub mimari olarak farklıdır — amacı kuantum direnci değil, kimlik düzeyinde ileri gizliliktir.

### 6.4 Merkeziyetsiz Kimlik (DID, W3C)

W3C DID standardı, kimliği merkezi kayıtlardan uzaklaştırır. Ancak:
- DID, işlem başına anahtar izolasyonunu ele almaz
- DID anahtarları işlemler arasında yeniden kullanılır
- DID modelinde tek kullanımlık onay token'ı primitifi yoktur

EIDA, DID ile tamamlayıcıdır — ePriPub, bir DID çerçevesi içinde imzalama primitifi olarak hizmet edebilir.

### 6.5 GKDP (Güvenli Kimlik Doğrulama Protokolü)

GKDP, Türkiye kamu gereksinimlerine göre uyarlanmış bir EIDA türevidir. Temel farklar:

| Özellik | EIDA | GKDP |
|----------|------|------|
| İmza algoritması | Ed25519 | Dilithium3 (FIPS 204) |
| Kuantum direnci | Hayır | Evet |
| Şifreleme katmanı | Yok (CA doğrudan imzalar) | Kyber-768 KEM + AES-256-GCM |
| CA durumluluğu | Durumsuz | Durumlu (nonce önbelleği, token hash, Merkle kayıtları) |
| Bağlantısızlık | Tam (işlem başına ePub) | Sınırlı (BTK uPub'ı görür, korelasyon riskini kabul eder) |
| Başlangıç kaydı | Örtük | Açık (PTT'de fiziksel kayıt) |
| Anahtar türetme | HKDF ile uPriv'den türetilir | Oturum başına bağımsız Dilithium3.KeyGen() |
| Adli süreç | Tanımlanmamış | Tanımlı: mahkeme → BTK → eDevlet zinciri |
| Çift kayıt garantisi | Tanımlanmamış | eDevlet'e Merkle ağaç kökü |

EIDA ve GKDP farklı güven modellerine hizmet eder: EIDA matematiksel gizliliği, durumsuzluğu ve minimalizmi önceliklendirir; GKDP düzenleyici uyumu, kuantum direncini ve mahkeme kararlı kimlik tespitini önceliklendirir.

---

## 7. Sonuç

Mevcut internet güvenlik mimarisinin temel açığı merkezileşmedir. Kimlik doğrulama merkezi sistemlere bağlı olduğunda, bu sistemler yüksek değerli hedefler haline gelir. Tek bir başarılı saldırı milyonları açığa çıkarır. Bu bir uygulama başarısızlığı değil — mimari bir başarısızlıktır.

EIDA, klasik PKI'nın eşzamanlı olarak sağlamadığı üç özelliği tanıtarak bunu mimari düzeyde ele alır:

- **İşlem düzeyinde ileri gizlilik** — her işlem, kullanımdan sonra yok edilen benzersiz, türetilmiş bir anahtar çifti kullanır
- **Sıfır uPriv maruziyeti** — kalıcı gizli anahtar donanım destekli izolasyon bölgesinden asla çıkmaz
- **Dağıtılmış saldırı yüzeyi** — saldırmaya değer merkezi bir kullanıcı kimlik materyali deposu yoktur

Temel primitif ePriPub, bu özellikleri iyi bilinen kriptografik standartları — HKDF (RFC 5869) ve Ed25519 — yeni bir mimari desende birleştirerek elde eder. Yeni kriptografik varsayımlar gerekmez.

EIDA mevcut altyapıyı değiştirmez. Onu genişletir. CA sistemleri, PKI zincirleri ve mevcut kimlik çerçeveleri geçerli kalır — EIDA bunların üzerine işlem başına bir izolasyon katmanı ekler.

EIDA'nın önerdiği değişim teknik olduğu kadar kavramsaldır: güvenlik, merkezi otoriteler tarafından kullanıcılara yapılan bir şey olmamalıdır. Kullanıcıyla birlikte, kullanıcının cihazında, kullanıcının kontrolünde yaşayan bir şey olmalıdır.

---

## 8. Referanslar

1. RFC 5869 - HMAC-based Extract-and-Expand Key Derivation Function (HKDF)
2. RFC 8032 - Ed25519 and Ed448 Digital Signature Algorithms
3. Bernstein, D.J. et al. (2012). High-speed high-security signatures. *Journal of Cryptographic Engineering*
4. W3C (2022). Decentralized Identifiers (DIDs) v1.0
5. Rescorla, E. (2018). The Transport Layer Security (TLS) Protocol Version 1.3, RFC 8446

---

*EIDA Whitepaper v1.5-TR — Mayıs 2026*  
*https://github.com/guvenacar/EIDA*