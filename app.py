from flask import Flask, render_template, request, jsonify
import sys
import os

# core klasörünü yola ekleyelim
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

from aes_core import AESVisualizer
from des_core import SDES, TripleSDES
from hash_mac import HashMACVisualizer
from rbg_core import RBGVisualizer

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/aes', methods=['POST'])
def run_aes():
    try:
        data = request.json
        
        # PKCS#7 tarzı Eğitimsel Dolgu (Sadece ilk 16 byte'lık blok için)
        raw_text = data.get('text', '').encode('utf-8')
        if len(raw_text) < 16:
            pad_len = 16 - len(raw_text)
            text = raw_text + bytes([pad_len] * pad_len)
        else:
            text = raw_text[:16] # Sadece 1 blok görselleştiriyoruz
            
        raw_key = data.get('key', '').encode('utf-8')
        if len(raw_key) < 16:
            pad_len = 16 - len(raw_key)
            key = raw_key + bytes([pad_len] * pad_len)
        else:
            key = raw_key[:16]
        
        visualizer = AESVisualizer(key)
        result = visualizer.encrypt_block(text)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"AES İşlem Hatası: {str(e)}"}), 400

@app.route('/api/des', methods=['POST'])
def run_des():
    try:
        data = request.json
        algo_type = data.get('type', 'sdes')
        
        # Sadece 0 ve 1 kontrolü
        raw_text = data.get('text', '10101010')
        raw_key = data.get('key', '1010101010')
        
        if not all(c in '01' for c in raw_text) or not all(c in '01' for c in raw_key):
            return jsonify({"error": "DES girdileri sadece 0 ve 1'lerden (binary) oluşmalıdır."}), 400
            
        text_bits = [int(b) for b in raw_text]
        key_bits = [int(b) for b in raw_key]
        
        if algo_type == '3sdes':
            raw_key2 = data.get('key2', '0101010101')
            if not all(c in '01' for c in raw_key2):
                return jsonify({"error": "3-DES 2. Anahtar sadece 0 ve 1'lerden oluşmalıdır."}), 400
            key2_bits = [int(b) for b in raw_key2]
            ciphertext, trace = TripleSDES.encrypt(text_bits, key_bits, key2_bits)
        else:
            ciphertext, trace = SDES.encrypt(text_bits, key_bits)
            
        return jsonify({
            "ciphertext": ciphertext,
            "trace": trace
        })
    except Exception as e:
        return jsonify({"error": f"DES İşlem Hatası: {str(e)}"}), 400

@app.route('/api/hash_mac', methods=['POST'])
def run_hash_mac():
    try:
        data = request.json
        action = data.get('action', 'hash')
        text = data.get('text', 'merhaba')
        key = data.get('key', 'gizlianahtar')
        
        if action == 'hash':
            result = HashMACVisualizer.simulate_sha256(text)
        else:
            if not key:
                return jsonify({"error": "HMAC için gizli anahtar boş olamaz."}), 400
            result = HashMACVisualizer.simulate_hmac(key, text)
            
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"Hash/MAC İşlem Hatası: {str(e)}"}), 400

@app.route('/api/rbg', methods=['POST'])
def run_rbg():
    try:
        data = request.json
        method = data.get('method', 'lfsr')
        length_val = data.get('length', 16)
        
        try:
            length = int(length_val)
            if length <= 0 or length > 10000:
                raise ValueError()
        except:
            return jsonify({"error": "Lütfen geçerli bir uzunluk (1-10000) giriniz."}), 400
            
        if method == 'lfsr':
            seed = [1, 0, 1, 1]
            taps = [0, 3]
            result = RBGVisualizer.lfsr_pseudo_random(seed, taps, length)
        else:
            # byte olarak uzunluk isteniyor, bit sayısı için 8'e böl
            bytes_len = max(1, length // 8)
            result = RBGVisualizer.secure_random(bytes_len)
            
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"RBG İşlem Hatası: {str(e)}"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
