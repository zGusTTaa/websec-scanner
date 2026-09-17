let targetsCache = [];

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
            return `
                <div class="card">
                    <div class="card-info">
                        <h3>Scan #${s.id} — ${escapeHtml(t?.name || 'Alvo removido')}</h3>
                        <div class="card-meta">${escapeHtml(t?.url || '')} · ${formatDate(s.started_at)}</div>
                    </div>
                    <div class="card-actions">
                        <span class="badge ${s.status === 'completed' ? 'LOW' : s.status === 'failed' ? 'CRITICAL' : 'MEDIUM'}">${escapeHtml(s.status)}</span>
                        <a href="/scans/${s.id}" class="btn btn-ghost btn-small">Ver</a>
                        <button class="btn btn-danger btn-small" onclick="deleteScanRow(${s.id})">Remover</button>
                    </div>
                </div>
            `;
        }).join('');
    } catch (e) {
        container.innerHTML = `<p class="muted">Erro: ${escapeHtml(e.message)}</p>`;
    }
}

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

document.getElementById('scan-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const targetId = parseInt(document.getElementById('scan-target').value);
    const scanner = document.getElementById('scan-scanner').value;

    closeScanModal();
    showToast('Executando scan… aguarde.', 'success');

    try {
        const result = await api.post('/api/scans/', {
            target_id: targetId,
            scanners: [scanner],
        });
        showToast(`Scan concluído! ${result.total_findings} findings encontrados.`);
        loadScans();
    } catch (e) {
        showToast('Erro: ' + e.message, 'error');
    }
});

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

loadScans();