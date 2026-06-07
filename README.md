# Etkileşimli Kriptografik Algoritma Analiz ve Görselleştirme Platformu

**Kriptografi ve Uygulamaları Dersi Final Projesi**

## Proje Hakkında
Bu platform, kriptografik algoritmaların (DES, 3-DES, AES, Hash, MAC, RBG) çalışma prensiplerini adım adım görselleştiren etkileşimli bir eğitim aracıdır. Özellikle AES'in Galois Alanları (GF(2^8)) tabanlı dönüşümleri animasyonlu olarak incelenebilir.

## Özellikler
- **AES-128**: 10 round boyunca SubBytes, ShiftRows, MixColumns, AddRoundKey adımlarını adım adım (ileri/geri) veya otomatik animasyonla izleme. Değişen hücreler mavi ile vurgulanır.
- **S-DES / 3-S-DES**: 8-bit basitleştirilmiş DES ile Feistel ağı prensibini ve 3-DES (EDE) yapısını gösteren simülasyon.
- **SHA-256 / HMAC**: Gerçek hash hesaplaması + pedagojik adım adım açıklama.
- **RBG (LFSR + CSPRNG)**: LFSR pseudo-random ve `secrets` modülü ile kriptografik güvenli bit üretimi. Monobit ve Runs (Seri) istatistiksel test sonuçları gösterilir.

## Kurulum ve Çalıştırma

### Gereksinimler
- Python 3.8+
- pip

### Adımlar
```bash
# 1. Repoyu klonla
git clone <repo-url>
cd <proje-klasörü>

# 2. Sanal ortam oluştur (önerilen)
python -m venv venv

# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Bağımlılıkları yükle
pip install -r requirements.txt

# 4. Uygulamayı başlat
python app.py
```

### 5. Tarayıcıda Aç
`http://localhost:5000` adresini ziyaret edin.

## Proje Yapısı
```
├── app.py                  # Flask uygulaması, API endpoint'leri
├── core/
│   ├── aes_core.py         # AES-128 implementasyonu (GF(2^8) dahil)
│   ├── des_core.py         # S-DES ve Triple S-DES
│   ├── hash_mac.py         # SHA-256 ve HMAC simülasyonu
│   └── rbg_core.py         # LFSR ve CSPRNG
├── static/
│   ├── style.css           # Karanlık tema CSS
│   └── main.js             # Frontend mantığı, API çağrıları
├── templates/
│   └── index.html          # Ana sayfa şablonu
└── requirements.txt
```

## Kullanılan Teknolojiler
- **Backend**: Python, Flask
- **Frontend**: HTML5, CSS3 (custom dark theme), Vanilla JavaScript
- **Kriptografi**: Sıfırdan yazılmış AES, S-DES; Python `hashlib`, `hmac`, `secrets`
