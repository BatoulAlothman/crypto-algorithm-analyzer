"""
GF(2^8) Galois Alanı İşlemlerinin Adım Adım Görselleştirme Modülü.

İndirgenemez (irreducible) polinom: m(x) = x^8 + x^4 + x^3 + x + 1  (0x11B)
Bu polinom AES (FIPS-197) standardında tanımlıdır.
"""
from typing import Dict, Any, List


class GaloisFieldVisualizer:
    """GF(2^8) üzerinde toplama, çarpma ve ters alma işlemlerini
    pedagojik açıklamalarla birlikte adım adım hesaplar."""

    # --- Yardımcı Fonksiyonlar -------------------------------------------

    @staticmethod
    def _multiply(a: int, b: int) -> int:
        """GF(2^8) çarpma (Russian Peasant / Shift-and-XOR)."""
        p = 0
        for _ in range(8):
            if b & 1:
                p ^= a
            hi = a & 0x80
            a = (a << 1) & 0xFF
            if hi:
                a ^= 0x1B          # 0x11B'nin alt 8 biti
            b >>= 1
        return p

    @staticmethod
    def to_poly(val: int) -> str:
        """Byte değerini polinom gösterimine çevirir (örn: x^6 + x^4 + 1)."""
        if val == 0:
            return "0"
        terms: List[str] = []
        for i in range(7, -1, -1):
            if val & (1 << i):
                if i == 0:
                    terms.append("1")
                elif i == 1:
                    terms.append("x")
                else:
                    terms.append(f"x^{i}")
        return " + ".join(terms)

    @staticmethod
    def to_bin(val: int) -> str:
        """8-bit binary gösterim."""
        return format(val, '08b')

    @staticmethod
    def to_hex(val: int) -> str:
        """Hexadecimal gösterim."""
        return f"0x{val:02X}"

    # --- Ana İşlemler (trace üretir) -------------------------------------

    @classmethod
    def trace_addition(cls, a: int, b: int) -> Dict[str, Any]:
        """GF(2^8) Toplama = XOR. Adım adım trace üretir."""
        result = a ^ b

        steps: List[str] = [
            "GF(2^8) Toplama = Bitwise XOR İşlemi",
            "",
            f"a = {cls.to_hex(a)}  =  {cls.to_bin(a)}  =  {cls.to_poly(a)}",
            f"b = {cls.to_hex(b)}  =  {cls.to_bin(b)}  =  {cls.to_poly(b)}",
            "",
            f"    {cls.to_bin(a)}   ← a",
            f"XOR {cls.to_bin(b)}   ← b",
            f"─────────────────",
            f"    {cls.to_bin(result)}   =  {cls.to_hex(result)}",
            "",
            f"Sonuç Polinom: {cls.to_poly(result)}",
            "",
            "Not: GF(2^8)'de toplama ve çıkarma aynı işlemdir (a ⊕ b).",
            "Her bit pozisyonu bağımsız olarak XOR'lanır, elde (carry) olmaz."
        ]

        return {
            "operation": "Toplama (⊕)",
            "a": a, "b": b,
            "result": result,
            "result_hex": cls.to_hex(result),
            "result_poly": cls.to_poly(result),
            "steps": steps
        }

    @classmethod
    def trace_multiplication(cls, a: int, b: int) -> Dict[str, Any]:
        """GF(2^8) Çarpma. Peasant Multiplication ile adım adım trace üretir."""
        steps: List[str] = [
            "GF(2^8) Çarpma — Polinom çarpma mod m(x)",
            f"m(x) = x^8 + x^4 + x^3 + x + 1   (AES indirgenemez polinomu)",
            "",
            f"a = {cls.to_hex(a)}  =  {cls.to_bin(a)}  =  {cls.to_poly(a)}",
            f"b = {cls.to_hex(b)}  =  {cls.to_bin(b)}  =  {cls.to_poly(b)}",
            "",
            "Algoritma: Peasant Multiplication (Shift-and-XOR)",
            "Her adımda: b'nin son biti 1 ise p ⊕= a  |  a sola kaydır, taşma varsa ⊕ 0x1B  |  b sağa kaydır",
            "──────────────────────────────────────────────────────",
        ]

        p = 0
        cur_a = a
        cur_b = b

        for i in range(8):
            parts: List[str] = []

            # --- p güncellemesi ---
            if cur_b & 1:
                old_p = p
                p ^= cur_a
                parts.append(
                    f"b₀=1 → p = {cls.to_hex(old_p)} ⊕ {cls.to_hex(cur_a)} = {cls.to_hex(p)}")
            else:
                parts.append(f"b₀=0 → p değişmez ({cls.to_hex(p)})")

            # --- a güncellemesi ---
            hi = cur_a & 0x80
            shifted = (cur_a << 1) & 0xFF
            if hi:
                cur_a = shifted ^ 0x1B
                parts.append(
                    f"a₇=1 → a = {cls.to_hex(shifted)} ⊕ 0x1B = {cls.to_hex(cur_a)}")
            else:
                cur_a = shifted
                parts.append(f"a₇=0 → a = a≪1 = {cls.to_hex(cur_a)}")

            cur_b >>= 1
            steps.append(f"Adım {i + 1}:  {parts[0]}   |   {parts[1]}")

        result = p
        steps.extend([
            "",
            f"Sonuç: {cls.to_hex(a)} ⊗ {cls.to_hex(b)} = {cls.to_hex(result)}",
            f"({cls.to_poly(a)}) × ({cls.to_poly(b)})  ≡  {cls.to_poly(result)}  (mod m(x))",
            "",
            "AES'te MixColumns adımı bu çarpmayı sabit MDS matris katsayılarıyla",
            "(0x02, 0x03, 0x01, 0x01) her sütuna uygulayarak difüzyon sağlar."
        ])

        return {
            "operation": "Çarpma (⊗)",
            "a": a, "b": b,
            "result": result,
            "result_hex": cls.to_hex(result),
            "result_poly": cls.to_poly(result),
            "steps": steps
        }

    @classmethod
    def trace_inverse(cls, a: int) -> Dict[str, Any]:
        """GF(2^8)'de çarpımsal ters alma. Fermat'ın Küçük Teoremi ile hesaplar."""
        if a == 0:
            return {
                "operation": "Ters Alma (a⁻¹)",
                "a": 0, "result": None,
                "result_hex": "yok",
                "result_poly": "tanımsız",
                "steps": [
                    "0 elemanının GF(2^8)'de çarpımsal tersi yoktur.",
                    "Çünkü: 0 × (herhangi eleman) = 0 ≠ 1"
                ]
            }

        steps: List[str] = [
            "GF(2^8)'de Çarpımsal Ters Alma",
            f"a = {cls.to_hex(a)}  =  {cls.to_bin(a)}  =  {cls.to_poly(a)}",
            "",
            "Fermat'ın Küçük Teoremi:",
            "  GF(2^n) alanında sıfır olmayan her eleman için  a^(2^n − 1) = 1",
            "  Dolayısıyla:  a⁻¹ = a^(2^8 − 2) = a^254",
            "",
            "254₁₀ = 11111110₂  →  Tekrarlı kare alma (repeated squaring) ile hesaplama:",
            "",
        ]

        result = 1
        base = a
        exp = 254
        bit_pos = 0
        power_label = 1       # 2^bit_pos değeri

        while exp > 0:
            if exp & 1:
                result = cls._multiply(result, base)
                steps.append(
                    f"  Bit {bit_pos} = 1 → sonuç = sonuç × a^{power_label} = {cls.to_hex(result)}")
            else:
                steps.append(
                    f"  Bit {bit_pos} = 0 → sonuç değişmez  ({cls.to_hex(result)})")
            base = cls._multiply(base, base)
            exp >>= 1
            bit_pos += 1
            power_label <<= 1

        # Doğrulama
        check = cls._multiply(a, result)

        steps.extend([
            "",
            f"Sonuç: {cls.to_hex(a)}⁻¹  =  {cls.to_hex(result)}  =  {cls.to_poly(result)}",
            f"Doğrulama: {cls.to_hex(a)} × {cls.to_hex(result)} = {cls.to_hex(check)}"
            f"  {'✓ Doğru!' if check == 1 else '✗ Hata!'}",
            "",
            "AES'te SubBytes adımında her byte'ın GF(2^8) çarpımsal tersi alınır,",
            "ardından afin dönüşüm uygulanarak S-Box tablosundaki değer elde edilir."
        ])

        return {
            "operation": "Ters Alma (a⁻¹)",
            "a": a,
            "result": result,
            "result_hex": cls.to_hex(result),
            "result_poly": cls.to_poly(result),
            "steps": steps
        }
