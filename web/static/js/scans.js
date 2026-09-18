let targetsCache = [];
let scanEmAndamento = false;

// ============================================
// Carregar lista de scans
// ============================================
async function loadScans() {
    const container = document.getElementById('scans-list');
    try {
        const [scans, targets] = await Promise.all([
            api.get('/api/scans/'),
            api.get('/api/targets/'),
        ]);
        targetsCache = targets;

        if (!scans.length) {
            container.innerHTML = `
                <div class="empty-state">
                    <p>Nenhum scan executado.</p>
                    <p class="muted" style="margin-top:.5rem">Clique em "▶ Disparar Scan" para começar.</p>
                </div>`;
            return;
        }

        const targetMap = Object.fromEntries(targets.map(t => [t.id, t]));
        container.innerHTML = scans.map(s => {
            const t = targetMap[s.target_id];
            const statusClass = s.status === 'completed' ? 'LOW'
                              : s.status === 'failed'    ? 'CRITICAL'
                              : 'MEDIUM';
            const isRunning = s.status === 'running';
            return `
                <div class="card">
                    <div class="card-info">
                        <h3>Scan #${s.id} — ${escapeHtml(t?.name || 'Alvo removido')}</h3>
                        <div class="card-meta">${escapeHtml(t?.url || '')} · ${formatDate(s.started_at)}</div>
                    </div>
                    <div class="card-actions">
                        <span class="badge ${statusClass}">${escapeHtml(s.status.toUpperCase())}</span>
                        <a href="/scans/${s.id}" class="btn btn-ghost btn-small">Ver</a>
                        <button class="btn btn-danger btn-small"
                                onclick="deleteScanRow(${s.id})"
                                ${isRunning ? 'disabled title="Aguarde o scan terminar"' : ''}>
                            Remover
                        </button>
                    </div>
                </div>
            `;
        }).join('');
    } catch (e) {
        container.innerHTML = `<p class="muted">Erro: ${escapeHtml(e.message)}</p>`;
    }
}

// ============================================
// Modal
// ============================================
function openScanModal() {
    const select = document.getElementById('scan-target');
    if (!targetsCache.length) {
        showToast('Cadastre um alvo primeiro em "Alvos".', 'error');
        return;
    }
    select.innerHTML = targetsCache.map(t =>
        `<option value="${t.id}">${escapeHtml(t.name)} — ${escapeHtml(t.url)}</option>`
    ).join('');
    document.getElementById('scan-modal').hidden = false;
}

function closeScanModal() {
    document.getElementById('scan-modal').hidden = true;
}

// ============================================
// Polling: acompanha o status do scan
// ============================================
async function pollScan(scanId, maxAttempts = 90, intervalMs = 2000) {
    for (let i = 0; i < maxAttempts; i++) {
        await new Promise(r => setTimeout(r, intervalMs));
        try {
            const scan = await api.get(`/api/scans/${scanId}`);
            if (scan.status !== 'running') {
                return scan;
            }
        } catch (e) {
            console.warn('Erro no polling:', e);
        }
    }
    return null;
}

// ============================================
// Submit: dispara scan em background
// ============================================
document.getElementById('scan-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    if (scanEmAndamento) {
        showToast('Aguarde — já existe um scan em execução.', 'error');
        return;
    }

    const targetId = parseInt(document.getElementById('scan-target').value);
    const scannerValue = document.getElementById('scan-scanner').value;
    const scanners = scannerValue === '__all__' ? null : [scannerValue];

    closeScanModal();

    scanEmAndamento = true;

    try {
        const scan = await api.post('/api/scans/', {
            target_id: targetId,
            scanners: scanners,
        });

        showToast(`Scan #${scan.id} iniciado…`);
        loadScans();

        const finished = await pollScan(scan.id);

        if (finished) {
            showToast(`✅ Scan #${finished.id} concluído: ${finished.total_findings} findings.`);
        } else {
            showToast('⏱ Scan ainda em execução. Recarregue em alguns segundos.', 'error');
        }
    } catch (e) {
        showToast('Erro: ' + e.message, 'error');
    } finally {
        scanEmAndamento = false;
        loadScans();
    }
});

// ============================================
// Deletar
// ============================================
async function deleteScanRow(id) {
    if (!confirm('Remover este scan?')) return;
    try {
        await api.del(`/api/scans/${id}`);
        showToast('Scan removido.');
        loadScans();
    } catch (e) {
        showToast('Erro: ' + e.message, 'error');
    }
}

// ============================================
// Inicialização
// ============================================
loadScans();