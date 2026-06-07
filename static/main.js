// UI Navigation
document.querySelectorAll('.nav-links li').forEach(item => {
    item.addEventListener('click', () => {
        document.querySelectorAll('.nav-links li').forEach(nav => nav.classList.remove('active'));
        item.classList.add('active');
        
        document.querySelectorAll('.algo-section').forEach(sec => sec.classList.remove('active'));
        const targetId = item.getAttribute('data-target');
        document.getElementById(targetId).classList.add('active');
    });
});

// Hash/MAC Type Switcher
document.getElementById('hash-type').addEventListener('change', (e) => {
    const keyGroup = document.getElementById('mac-key-group');
    keyGroup.style.display = (e.target.value === 'mac') ? 'block' : 'none';
});

// DES Type Switcher
document.getElementById('des-type').addEventListener('change', (e) => {
    const key2Group = document.getElementById('des-key2-group');
    key2Group.style.display = (e.target.value === '3sdes') ? 'block' : 'none';
});

// =====================
// AES Visualization
// =====================
let aesTrace = [];
let currentAesStep = 0;
let aesAutoPlayInterval = null;
let prevState = null; // previous state for highlighting changed cells

async function runAES() {
    const text = document.getElementById('aes-text').value;
    const key = document.getElementById('aes-key').value;

    try {
        const response = await fetch('/api/aes', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({text, key})
        });
        const data = await response.json();

        if (!response.ok || data.error) {
            alert(data.error || "AES şifreleme sırasında bir hata oluştu.");
            return;
        }

        aesTrace = data.trace;
        currentAesStep = 0;
        prevState = null;

        document.getElementById('aes-visualizer').classList.remove('hidden');
        renderAesStep();
    } catch (e) {
        console.error("AES Error", e);
        alert("AES şifreleme sırasında bir hata oluştu.");
    }
}

function renderAesStep() {
    if (aesTrace.length === 0) return;

    const stepData = aesTrace[currentAesStep];
    document.getElementById('aes-step-info').innerText =
        `Round: ${stepData.round} | Adım: ${currentAesStep + 1} / ${aesTrace.length}`;
    document.getElementById('aes-step-title').innerText = `${stepData.step} Sonrası Durum`;

    // Pedagojik açıklamalar
    const pedagogyMap = {
        "Initial State": "Başlangıç Durumu: 16 bytelık girdi metni 4x4'lük duruma (State) dönüştürüldü. Baytlar sütun-öncelikli sırada yerleştirilir.",
        "AddRoundKey": "AddRoundKey: Durum matrisindeki her byte, ilgili Round Key (Döngü Anahtarı) byte'ı ile XOR işlemine sokulur. Tek tersine çevrilebilir Galois toplama işlemidir.",
        "SubBytes": "SubBytes: Doğrusal olmayan bayt yer değiştirme adımı. Her byte, S-Box (Yerine Koyma Kutusu) üzerinden GF(2^8) alanında ters alma ile türetilmiş yeni bir değerle değiştirilir.",
        "ShiftRows": "ShiftRows: Satır kaydırma adımı. 1. satır sabit, 2. satır 1 sola, 3. satır 2 sola, 4. satır 3 sola kaydırılır. Baytları sütunlar arasına yayar.",
        "MixColumns": "MixColumns: Sütun karıştırma adımı. Her sütun, Galois Cismi GF(2^8) aritmetiği üzerinden sabit bir MDS matrisi ile çarpılır. Difüzyon sağlar."
    };
    document.getElementById('aes-pedagogy').innerText = pedagogyMap[stepData.step] || "";

    const tbody = document.createElement('tbody');
    for (let r = 0; r < 4; r++) {
        const tr = document.createElement('tr');
        for (let c = 0; c < 4; c++) {
            const td = document.createElement('td');
            let hexVal = stepData.state[r][c].toString(16).padStart(2, '0').toUpperCase();
            td.innerText = hexVal;

            // Highlight cells that changed from previous step
            if (prevState !== null && prevState[r][c] !== stepData.state[r][c]) {
                td.classList.add('cell-changed');
            }

            tr.appendChild(td);
        }
        tbody.appendChild(tr);
    }

    const table = document.getElementById('aes-matrix');
    table.innerHTML = '';
    table.appendChild(tbody);

    prevState = stepData.state.map(row => [...row]);
}

function toggleAesAutoPlay() {
    const btn = document.getElementById('aes-play-btn');
    if (aesAutoPlayInterval) {
        clearInterval(aesAutoPlayInterval);
        aesAutoPlayInterval = null;
        btn.innerHTML = '&#9654; Otomatik Oynat';
    } else {
        btn.innerHTML = '&#10074;&#10074; Durdur';
        const speed = parseInt(document.getElementById('aes-speed').value);
        aesAutoPlayInterval = setInterval(() => {
            if (currentAesStep < aesTrace.length - 1) {
                aesNextStep();
            } else {
                toggleAesAutoPlay();
            }
        }, speed);
    }
}

document.getElementById('aes-speed').addEventListener('change', () => {
    if (aesAutoPlayInterval) {
        toggleAesAutoPlay();
        toggleAesAutoPlay();
    }
});

function aesNextStep() {
    if (currentAesStep < aesTrace.length - 1) {
        currentAesStep++;
        renderAesStep();
    }
}

function aesPrevStep() {
    if (currentAesStep > 0) {
        // Recalculate prevState for going backwards
        prevState = currentAesStep > 1 ? aesTrace[currentAesStep - 2].state.map(row => [...row]) : null;
        currentAesStep--;
        renderAesStep();
    }
}

// =====================
// DES Execution
// =====================
async function runDES() {
    const type = document.getElementById('des-type').value;
    const text = document.getElementById('des-text').value;
    const key = document.getElementById('des-key').value;
    const key2 = document.getElementById('des-key2').value;

    const outPanel = document.getElementById('des-output');
    outPanel.classList.remove('hidden');
    outPanel.innerHTML = "<p>Hesaplanıyor...</p>";

    try {
        const response = await fetch('/api/des', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({type, text, key, key2})
        });
        const data = await response.json();

        if (!response.ok || data.error) {
            outPanel.innerHTML = `<p style="color: #ef4444;">Hata: ${data.error || "İşlem başarısız"}</p>`;
            return;
        }

        let html = `<h3>Şifreli Metin: <span class="highlight-text">${data.ciphertext.join('')}</span></h3><br/>`;

        if (type === '3sdes') {
            // 3-DES trace has a different structure: array of phases
            data.trace.forEach((phase, idx) => {
                html += `<div class="trace-step"><strong>Faz ${idx + 1}: ${phase.phase}</strong><br/>`;
                html += `Sonuç: <span class="highlight-text">${phase.result.join('')}</span><br/>`;
                if (phase.details) {
                    phase.details.forEach((step, sidx) => {
                        if (step.bits) {
                            html += `&nbsp;&nbsp;• ${step.step}: ${step.bits.join('')}<br/>`;
                        } else if (step.k1) {
                            html += `&nbsp;&nbsp;• ${step.step}: K1=${step.k1.join('')}<br/>`;
                        } else if (step.k2) {
                            html += `&nbsp;&nbsp;• ${step.step}: K2=${step.k2.join('')}<br/>`;
                        }
                    });
                }
                html += `</div>`;
            });
        } else {
            // S-DES trace: flat array of steps
            data.trace.forEach((step, idx) => {
                html += `<div class="trace-step">
                    <strong>Adım ${idx + 1}: ${step.step}</strong><br/>
                    ${step.bits ? 'Bits: ' + step.bits.join('') : 
                      step.k1 ? 'K1: ' + step.k1.join('') :
                      step.k2 ? 'K2: ' + step.k2.join('') : ''}
                </div>`;
            });
        }

        outPanel.innerHTML = html;

    } catch (e) {
        console.error(e);
        outPanel.innerHTML = "<p>Hata oluştu.</p>";
    }
}

// =====================
// Hash/MAC Execution
// =====================
async function runHashMAC() {
    const action = document.getElementById('hash-type').value;
    const text = document.getElementById('hash-text').value;
    const key = document.getElementById('hash-key').value;

    const outPanel = document.getElementById('hash-output');
    outPanel.classList.remove('hidden');
    outPanel.innerHTML = "<p>Hesaplanıyor...</p>";

    try {
        const response = await fetch('/api/hash_mac', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({action, text, key})
        });
        const data = await response.json();

        if (!response.ok || data.error) {
            outPanel.innerHTML = `<p style="color: #ef4444;">Hata: ${data.error || "İşlem başarısız"}</p>`;
            return;
        }

        const resultVal = data.hash || data.hmac;
        let html = `<h3>Sonuç: <span class="highlight-text" style="word-break: break-all; font-size:0.85em;">${resultVal}</span></h3><br/><h4>Çalışma Prensibi:</h4>`;
        data.explanation.forEach(line => {
            html += `<div class="trace-step">${line}</div>`;
        });
        outPanel.innerHTML = html;

    } catch (e) {
        console.error(e);
        outPanel.innerHTML = "<p>Hata oluştu.</p>";
    }
}

// =====================
// RBG Execution
// =====================
async function runRBG() {
    const method = document.getElementById('rbg-type').value;
    const length = document.getElementById('rbg-length').value;

    const outPanel = document.getElementById('rbg-output');
    outPanel.classList.remove('hidden');
    outPanel.innerHTML = "<p>Hesaplanıyor...</p>";

    try {
        const response = await fetch('/api/rbg', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({method, length})
        });
        const data = await response.json();

        if (!response.ok || data.error) {
            outPanel.innerHTML = `<p style="color: #ef4444;">Hata: ${data.error || "İşlem başarısız"}</p>`;
            return;
        }

        const ratio = data.stats.ratio_1;
        const isBalanced = ratio >= 0.4 && ratio <= 0.6;
        const ratioColor = isBalanced ? '#22c55e' : '#f59e0b';

        let html = `
        <h3>${data.stats.test_name || "İstatistikler"}</h3>
        <div class="trace-step">
            <p>Üretilen <strong>0</strong> sayısı: ${data.stats.count_0}</p>
            <p>Üretilen <strong>1</strong> sayısı: ${data.stats.count_1}</p>
            <p>Oran (1'lerin oranı): <span style="color:${ratioColor}; font-weight:bold;">${ratio} 
               ${isBalanced ? '✓ Dengeli (0.4-0.6 aralığı)' : '⚠ Dengesiz'}</span></p>
        </div>
        <div class="trace-step">
            <p><strong>Runs (Seri) Testi Sonuçları:</strong></p>
            <p>Toplam Seri Sayısı: ${data.stats.runs_data.total_runs}</p>
            <p>En Uzun Kesintisiz '0' Serisi: ${data.stats.runs_data.max_run_0}</p>
            <p>En Uzun Kesintisiz '1' Serisi: ${data.stats.runs_data.max_run_1}</p>
        </div><br/>`;

        if (method === 'lfsr') {
            const bitsStr = data.generated_bits.join('');
            html += `<h3>Üretilen Bitler: <span class="highlight-text" style="font-size:0.8em; word-break:break-all;">${bitsStr}</span></h3><br/>`;
            html += `<h4>LFSR Simülasyon Adımları (İlk 10 Adım):</h4>`;
            data.trace.slice(0, 10).forEach(step => {
                html += `<div class="trace-step">Adım ${step.step} | Durum: <strong>${step.state}</strong> | Geribildirim: ${step.feedback} | Çıktı Biti: <strong>${step.output}</strong></div>`;
            });
            if (data.trace.length > 10) {
                html += `<div class="trace-step" style="color: var(--text-muted);">... ve ${data.trace.length - 10} adım daha</div>`;
            }
        } else {
            html += `<div class="trace-step"><strong>Üretilen (Hex):</strong><br/><span class="highlight-text" style="font-size:0.85em; word-break:break-all;">${data.hex}</span></div>`;
            html += `<div class="trace-step" style="margin-top:10px;"><strong>Üretilen (Binary):</strong><br/><span style="font-family:monospace; font-size:0.75em; word-break:break-all; color:var(--text-muted);">${data.bits}</span></div>`;
        }

        outPanel.innerHTML = html;

    } catch (e) {
        console.error(e);
        outPanel.innerHTML = "<p>Hata oluştu.</p>";
    }
}
