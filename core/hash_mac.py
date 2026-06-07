import hashlib
import hmac
from typing import Dict, Any, List

class HashMACVisualizer:
    """Hash (SHA-256) ve MAC (HMAC) Algoritmalarının eğitimsel simülasyonunu sağlayan modül."""

    @staticmethod
    def simulate_sha256(text: str) -> Dict[str, Any]:
        """
        SHA-256 prensibini açıklayıcı metinle adım adım simüle eder.
        
        Args:
            text (str): Özetlenecek mesaj.
            
        Returns:
            Dict[str, Any]: Hash sonucu ve eğitimsel adımlar.
        """
        hash_obj = hashlib.sha256(text.encode('utf-8'))
        final_hash = hash_obj.hexdigest()
        
        explanation: List[str] = [
            "SHA-256 (Secure Hash Algorithm 256-bit)",
            f"1. Girdi Metni: '{text}'",
            "2. Padding (Dolgu) Adımı: Mesajın uzunluğu 512 bitin katı olacak şekilde ayarlanır. Önce '1' biti eklenir, ardından kalan kısım '0' ile doldurulur ve en sona orijinal mesaj uzunluğu eklenir.",
            "3. Başlangıç Değerleri (H0-H7): İlk 8 asal sayının kareköklerinin kesirli kısımlarından alınan sabit değerlerle başlar.",
            "4. Mesaj Blokları (W0-W63): Mesaj 512 bitlik bloklara bölünür ve Message Schedule (W) matrisi oluşturulur.",
            "5. Kompresyon Fonksiyonu: 64 round boyunca her bloğa bit düzeyinde mantıksal işlemler (AND, XOR, sağa döndürme, sağa kaydırma) ve modüler toplama uygulanır.",
            f"6. Nihai Hash Değeri: {final_hash}"
        ]
        
        return {
            "hash": final_hash,
            "explanation": explanation
        }

    @staticmethod
    def simulate_hmac(key: str, message: str) -> Dict[str, Any]:
        """
        HMAC prensibini açıklayıcı metinle simüle eder.
        
        Args:
            key (str): Paylaşılan gizli anahtar.
            message (str): Doğrulanacak mesaj.
            
        Returns:
            Dict[str, Any]: HMAC sonucu ve eğitimsel adımlar.
        """
        h = hmac.new(key.encode('utf-8'), message.encode('utf-8'), hashlib.sha256)
        final_hmac = h.hexdigest()
        
        explanation: List[str] = [
            "HMAC (Hash-based Message Authentication Code)",
            f"Girdi Mesajı: '{message}'",
            f"Gizli Anahtar: '{key}'",
            "1. Anahtar Düzenleme (Key Formatting): Eğer anahtar blok boyutundan (genelde 64 byte) uzunsa hashlenerek küçültülür. Kısaysa sıfırlarla doldurularak K' adı verilen 64 bytelık anahtar oluşturulur.",
            "2. Inner Pad (ipad): K' anahtarı 0x36 sabiti ile XOR'lanır.",
            "3. Outer Pad (opad): K' anahtarı 0x5C sabiti ile XOR'lanır.",
            "4. İç Hash İşlemi: İlk olarak Hash( (K' XOR ipad) || mesaj ) hesaplanır.",
            "5. Dış Hash İşlemi: Nihai MAC üretmek için Hash( (K' XOR opad) || İç_Hash_Sonucu ) hesaplanır.",
            f"Nihai MAC Değeri: {final_hmac}",
            "Pedagojik Not: Bu süreç, mesajın bütünlüğünü korurken aynı zamanda gizli anahtarı bilen doğru kişi tarafından gönderildiğini matematiksel olarak garanti eder."
        ]
        
        return {
            "hmac": final_hmac,
            "explanation": explanation
        }
