from typing import List, Dict, Any
import secrets

class RBGVisualizer:
    """Rastgele Bit Üretimi (RBG) Eğitim ve Analiz Modülü."""
    
    @staticmethod
    def _runs_test(bits: List[int]) -> Dict[str, Any]:
        """
        İleri Düzey İstatistiksel Test: Seriler (Runs) Testi.
        Birbirini ardışık olarak takip eden aynı bit gruplarının uzunluğunu ve sayısını analiz eder.
        
        Args:
            bits (List[int]): Analiz edilecek bit dizisi.
            
        Returns:
            Dict[str, Any]: Seri testi istatistikleri.
        """
        if not bits:
            return {"total_runs": 0, "max_run_0": 0, "max_run_1": 0}
            
        runs = 1
        max_run_0 = 1 if bits[0] == 0 else 0
        max_run_1 = 1 if bits[0] == 1 else 0
        current_run = 1
        
        for i in range(1, len(bits)):
            if bits[i] == bits[i-1]:
                current_run += 1
                if bits[i] == 0 and current_run > max_run_0:
                    max_run_0 = current_run
                elif bits[i] == 1 and current_run > max_run_1:
                    max_run_1 = current_run
            else:
                runs += 1
                current_run = 1
                if bits[i] == 0 and max_run_0 == 0:
                    max_run_0 = 1
                elif bits[i] == 1 and max_run_1 == 0:
                    max_run_1 = 1
                    
        return {
            "total_runs": runs,
            "max_run_0": max_run_0,
            "max_run_1": max_run_1
        }

    @staticmethod
    def lfsr_pseudo_random(seed: List[int], taps: List[int], length: int) -> Dict[str, Any]:
        """
        Linear Feedback Shift Register (LFSR) tabanlı eğitimsel PRNG simülatörü.
        
        Args:
            seed (List[int]): Başlangıç durumu (örn: [1, 0, 1, 1]).
            taps (List[int]): XOR alınacak bit indeksleri (örn: [0, 3]).
            length (int): Üretilecek bit sayısı.
            
        Returns:
            Dict[str, Any]: Üretilen bitler, loglar ve test sonuçları.
        """
        state = list(seed)
        generated_bits = []
        trace = []
        
        for i in range(length):
            feedback = 0
            for t in taps:
                feedback ^= state[t]
            
            output_bit = state[-1]
            generated_bits.append(output_bit)
            
            trace.append({
                "step": i+1,
                "state": "".join(str(b) for b in state),
                "feedback": feedback,
                "output": output_bit
            })
            
            state = [feedback] + state[:-1]
            
        count_0 = generated_bits.count(0)
        count_1 = generated_bits.count(1)
        runs_data = RBGVisualizer._runs_test(generated_bits)
        
        return {
            "generated_bits": generated_bits,
            "trace": trace,
            "stats": {
                "test_name": "Monobit & Runs (Seri) Testi",
                "count_0": count_0,
                "count_1": count_1,
                "ratio_1": round(count_1 / length, 2) if length > 0 else 0,
                "runs_data": runs_data
            }
        }
    
    @staticmethod
    def secure_random(length_bytes: int) -> Dict[str, Any]:
        """
        Kriptografik olarak güvenli PRNG simülasyonu.
        
        Args:
            length_bytes (int): Üretilecek byte uzunluğu.
            
        Returns:
            Dict[str, Any]: Güvenli bitler ve istatistiksel test sonuçları.
        """
        rand_bytes = secrets.token_bytes(length_bytes)
        hex_str = rand_bytes.hex()
        bits_str = bin(int.from_bytes(rand_bytes, 'big'))[2:].zfill(length_bytes * 8)
        
        bit_list = [int(b) for b in bits_str]
        count_1 = bit_list.count(1)
        count_0 = bit_list.count(0)
        total = len(bit_list)
        
        runs_data = RBGVisualizer._runs_test(bit_list)
        
        return {
            "hex": hex_str,
            "bits": bits_str,
            "stats": {
                "test_name": "Monobit & Runs (Seri) İleri Düzey Testleri",
                "count_0": count_0,
                "count_1": count_1,
                "ratio_1": round(count_1 / total, 2) if total > 0 else 0,
                "runs_data": runs_data
            }
        }
