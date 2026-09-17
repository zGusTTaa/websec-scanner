async function loadDashboard() {
    try {
        const [targets, scans, findings] = await Promise.all([
            api.get('/api/targets/'),
            api.get('/api/scans/'),
            api.get('/api/findings/'),
        ]);

        document.getElementById('stat-targets').textContent = targets.length;
        document.getElementById('stat-scans').textContent = scans.length;
        document.getElementById('stat-findings').textContent = findings.length;

        const critical = findings.filter(f => f.severity === 'CRITICAL').length;
        document.getElementById('stat-critical').textContent = critical;

        renderSeverityChart(findings);
        renderRecentScans(scans, targets);
    } catch (e) {
        showToast('Erro ao carregar dashboard: ' + e.message, 'error');
    }
}

function renderSeverityChart(findings) {
    const container = document.getElementById('severity-chart');
    if (!findings.length) {
        container.innerHTML = '<p class="muted">Nenhum finding registrado ainda.</p>';
        return;
    }

    const order = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO'];
    const counts = {};
    order.forEach(s => counts[s] = 0);
    findings.forEach(f => { counts[f.severity] = (counts[f.severity] || 0) + 1; });

    const total = findings.length;
    const segments = order.map(s => {
        const pct = (counts[s] / total) * 100;
        return counts[s] > 0
            ? `<div class="seg-${s.toLowerCase()}" style="width: ${pct}%"></div>`
            : '';
    }).join('');

    const legend = order
        .filter(s => counts[s] > 0)
        .map(s => `<span class="legend-${s.toLowerCase()}">${s}: ${counts[s]}</span>`)
        .join('');

    container.innerHTML = `
        <div class="severity-bar">${segments}</div>
        <div class="severity-legend">${legend}</div>
    `;
}

function renderRecentScans(scans, targets) {
    const container = document.getElementById('recent-scans');
    if (!scans.length) {
        container.innerHTML = `
            <div class="empty-state">
                <p>Nenhum scan ainda.</p>
                <p class="muted" style="margin-top:.5rem">Vá em <a href="/scans">Scans</a> para disparar o primeiro.</p>
            </div>`;
        return;
    }

    const targetMap = Object.fromEntries(targets.map(t => [t.id, t]));
    const recent = scans.slice(0, 5);

    container.innerHTML = recent.map(s => {
        const t = targetMap[s.target_id];
        return `
            <div class="card">
                <div class="card-info">
                    <h3>${escapeHtml(t?.name || 'Alvo removido')}</h3>
                    <div class="card-meta">${escapeHtml(t?.url || '')} · ${formatDate(s.started_at)}</div>
                </div>
                <div class="card-actions">
                    <span class="badge ${s.status === 'completed' ? 'LOW' : 'MEDIUM'}">${escapeHtml(s.status)}</span>
                    <a href="/scans/${s.id}" class="btn btn-ghost btn-small">Ver</a>
                </div>
            </div>
        `;
    }).join('');
}

loadDashboard();