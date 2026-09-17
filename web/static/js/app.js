// ============ Helpers ============
const api = {
    async get(path) {
        const r = await fetch(path);
        if (!r.ok) throw new Error(await r.text());
        return r.status === 204 ? null : r.json();
    },
    async post(path, data) {
        const r = await fetch(path, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        if (!r.ok) throw new Error(await r.text());
        return r.status === 204 ? null : r.json();
    },
    async put(path, data) {
        const r = await fetch(path, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        if (!r.ok) throw new Error(await r.text());
        return r.status === 204 ? null : r.json();
    },
    async del(path) {
        const r = await fetch(path, { method: 'DELETE' });
        if (!r.ok) throw new Error(await r.text());
    },
};

function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type} show`;
    setTimeout(() => toast.classList.remove('show'), 3000);
}

function escapeHtml(str) {
    if (!str) return '';
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

function formatDate(iso) {
    if (!iso) return '—';
    const d = new Date(iso + (iso.endsWith('Z') ? '' : 'Z'));
    return d.toLocaleString('pt-BR', {
        day: '2-digit', month: '2-digit', year: 'numeric',
        hour: '2-digit', minute: '2-digit',
    });
}

function severityBadge(sev) {
    return `<span class="badge ${escapeHtml(sev)}">${escapeHtml(sev)}</span>`;
}