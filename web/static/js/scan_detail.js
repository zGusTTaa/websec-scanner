async function loadScanDetail() {
    const id = window.SCAN_ID;
    try {
        const [scan, targets] = await Promise.all([
            api.get(`/api/scans/${id}`),
            api.get('/api/targets/'),
        ]);
        const target = targets.find(t => t.id === scan.target_id);

        document.getElementById('scan-id-label').textContent = scan.id;
        document.getElementById('scan-meta').textContent =
            `${target?.name || 'Alvo removido'} · ${target?.url || ''} · ${formatDate(scan.started_at)} · status: ${scan.status}`;

        const findings = scan.findings || [];
        const counts = { CRITICAL: 0, HIGH: 0, MEDIUM: 0, LOW: 0, INFO: 0 };
        findings.forEach(f => { counts[f.severity] = (counts[f.severity] || 0) + 1; });

        document.getElementById('detail-total').textContent = findings.length;
        document.getElementById('detail-critical').textContent = counts.CRITICAL;
        document.getElementById('detail-high').textContent = counts.HIGH;
        document.getElementById('detail-medium').textContent = counts.MEDIUM;

        const container = document.getElementById('findings-list');
        if (!findings.length) {
            container.innerHTML = `<div class="empty-state"><p>Nenhum finding neste scan.</p></div>`;
            return;
        }

        const order = { CRITICAL: 0, HIGH: 1, MEDIUM: 2, LOW: 3, INFO: 4 };
        findings.sort((a, b) => order[a.severity] - order[b.severity]);

        container.innerHTML = findings.map(f => `
            <div class="finding sev-${f.severity}">
                <div class="finding-header">
                    <span class="finding-title">${escapeHtml(f.scanner)}</span>
                    ${severityBadge(f.severity)}
                </div>
                <div class="finding-url">${escapeHtml(f.url)}</div>
                <div class="finding-desc">${escapeHtml(f.description)}</div>
                ${f.recommendation ? `<div class="finding-rec"><strong>Recomendação:</strong> ${escapeHtml(f.recommendation)}</div>` : ''}
            </div>
        `).join('');
    } catch (e) {
        showToast('Erro: ' + e.message, 'error');
    }
}

async function deleteScan() {
    if (!confirm('Remover este scan e todos os seus findings?')) return;
    try {
        await api.del(`/api/scans/${window.SCAN_ID}`);
        showToast('Scan removido.');
        setTimeout(() => window.location.href = '/scans', 800);
    } catch (e) {
        showToast('Erro: ' + e.message, 'error');
    }
}

loadScanDetail();