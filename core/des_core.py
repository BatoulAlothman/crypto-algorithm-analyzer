# Kriptografi Motoru: Basitleştirilmiş DES (S-DES) ve 3-DES Simülasyonu
# Eğitim amacıyla "Basitleştirilmiş DES" (S-DES) kullanılmıştır.
# S-DES, DES'in tüm yapısal özelliklerini taşır ancak daha küçük bit boyutlarıyla
# adım adım takip edilmesini çok kolaylaştırır.

class SDES:
    # S-DES Tabloları
    P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
    P8 = [6, 3, 7, 4, 8, 5, 10, 9]
    IP = [2, 6, 3, 1, 4, 8, 5, 7]
    EP = [4, 1, 2, 3, 2, 3, 4, 1]
    P4 = [2, 4, 3, 1]
    IP_INV = [4, 1, 3, 5, 7, 2, 8, 6]

    S0 = [
        [1, 0, 3, 2],
        [3, 2, 1, 0],
        [0, 2, 1, 3],
        [3, 1, 3, 2]
    ]

    S1 = [
        [0, 1, 2, 3],
        [2, 0, 1, 3],
        [3, 0, 1, 0],
        [2, 1, 0, 3]
    ]

    @staticmethod
    def permute(bits, mapping):
        return [bits[i - 1] for i in mapping]

    @staticmethod
    def left_shift(bits, n):
        return bits[n:] + bits[:n]

    @staticmethod
    def generate_keys(key_10bit):
        trace = []
        p10_key = SDES.permute(key_10bit, SDES.P10)
        left = p10_key[:5]
        right = p10_key[5:]
        
        ls1_left = SDES.left_shift(left, 1)
        ls1_right = SDES.left_shift(right, 1)
        k1 = SDES.permute(ls1_left + ls1_right, SDES.P8)
        trace.append({"step": "K1 Üretimi", "k1": k1})
        
        ls2_left = SDES.left_shift(ls1_left, 2)
        ls2_right = SDES.left_shift(ls1_right, 2)
        k2 = SDES.permute(ls2_left + ls2_right, SDES.P8)
        trace.append({"step": "K2 Üretimi", "k2": k2})
        
        return k1, k2, trace

    @staticmethod
    def f_k(bits, key):
        left = bits[:4]
        right = bits[4:]
        
        ep_right = SDES.permute(right, SDES.EP)
        xor_res = [e ^ k for e, k in zip(ep_right, key)]
        
        s0_input = xor_res[:4]
        s1_input = xor_res[4:]
        
        r0 = (s0_input[0] << 1) | s0_input[3]
        c0 = (s0_input[1] << 1) | s0_input[2]
        s0_val = SDES.S0[r0][c0]
        
        r1 = (s1_input[0] << 1) | s1_input[3]
        c1 = (s1_input[1] << 1) | s1_input[2]
        s1_val = SDES.S1[r1][c1]
        
        s_out = [(s0_val >> 1) & 1, s0_val & 1, (s1_val >> 1) & 1, s1_val & 1]
        p4_out = SDES.permute(s_out, SDES.P4)
        
        final_left = [l ^ p for l, p in zip(left, p4_out)]
        return final_left + right

    @staticmethod
    def encrypt(plaintext_8bit, key_10bit):
        k1, k2, trace = SDES.generate_keys(key_10bit)
        
        ip_bits = SDES.permute(plaintext_8bit, SDES.IP)
        trace.append({"step": "Initial Permutation (IP)", "bits": ip_bits})
        
        fk1_bits = SDES.f_k(ip_bits, k1)
        trace.append({"step": "Round 1 (F_K1)", "bits": fk1_bits})
        
        swapped = fk1_bits[4:] + fk1_bits[:4]
        trace.append({"step": "Switch (SW)", "bits": swapped})
        
        fk2_bits = SDES.f_k(swapped, k2)
        trace.append({"step": "Round 2 (F_K2)", "bits": fk2_bits})
        
        ciphertext = SDES.permute(fk2_bits, SDES.IP_INV)
        trace.append({"step": "Inverse IP", "bits": ciphertext})
        
        return ciphertext, trace

    @staticmethod
    def decrypt(ciphertext_8bit, key_10bit):
        k1, k2, _ = SDES.generate_keys(key_10bit)
        
        ip_bits = SDES.permute(ciphertext_8bit, SDES.IP)
        fk2_bits = SDES.f_k(ip_bits, k2)
        swapped = fk2_bits[4:] + fk2_bits[:4]
        fk1_bits = SDES.f_k(swapped, k1)
        plaintext = SDES.permute(fk1_bits, SDES.IP_INV)
        
        return plaintext

class TripleSDES:
    """3-DES prensibini S-DES üzerinden uygular (Encrypt-Decrypt-Encrypt)"""
    @staticmethod
    def encrypt(plaintext_8bit, key1_10bit, key2_10bit):
        trace = []
        # Adım 1: Key1 ile şifreleme
        c1, t1 = SDES.encrypt(plaintext_8bit, key1_10bit)
        trace.append({"phase": "Encryption (Key 1)", "details": t1, "result": c1})
        
        # Adım 2: Key2 ile deşifreleme
        p2 = SDES.decrypt(c1, key2_10bit)
        trace.append({"phase": "Decryption (Key 2)", "result": p2})
        
        # Adım 3: Key1 ile tekrar şifreleme
        c3, t3 = SDES.encrypt(p2, key1_10bit)
        trace.append({"phase": "Encryption (Key 1)", "details": t3, "result": c3})
        
        return c3, trace
