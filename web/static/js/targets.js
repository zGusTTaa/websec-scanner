async function loadTargets() {
    const container = document.getElementById('targets-list');
    try {
        const targets = await api.get('/api/targets/');
        if (!targets.length) {
            container.innerHTML = `
                <div class="empty-state">
                    <p>Nenhum alvo cadastrado ainda.</p>
                    <p class="muted" style="margin-top:.5rem">Clique em "+ Novo Alvo" para começar.</p>
                </div>`;
            return;
        }
        container.innerHTML = targets.map(t => `
            <div class="card">
                <div class="card-info">
                    <h3>${escapeHtml(t.name)}</h3>
                    <div class="card-meta">${escapeHtml(t.url)}</div>
                    ${t.notes ? `<div class="card-meta" style="margin-top:.3rem">${escapeHtml(t.notes)}</div>` : ''}
                </div>
                <div class="card-actions">
                    <button class="btn btn-ghost btn-small" onclick='editTarget(${JSON.stringify(t)})'>Editar</button>
                    <button class="btn btn-danger btn-small" onclick="deleteTarget(${t.id})">Remover</button>
                </div>
            </div>
        `).join('');
    } catch (e) {
        container.innerHTML = `<p class="muted">Erro: ${escapeHtml(e.message)}</p>`;
    }
}

function openTargetModal() {
    document.getElementById('modal-title').textContent = 'Novo Alvo';
    document.getElementById('target-form').reset();
    document.getElementById('target-id').value = '';
    document.getElementById('target-modal').hidden = false;
}

function closeTargetModal() {
    document.getElementById('target-modal').hidden = true;
}

function editTarget(t) {
    document.getElementById('modal-title').textContent = 'Editar Alvo';
    document.getElementById('target-id').value = t.id;
    document.getElementById('target-name').value = t.name;
    document.getElementById('target-url').value = t.url;
    document.getElementById('target-notes').value = t.notes || '';
    document.getElementById('target-modal').hidden = false;
}

document.getElementById('target-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const id = document.getElementById('target-id').value;
    const payload = {
        name: document.getElementById('target-name').value.trim(),
        url: document.getElementById('target-url').value.trim(),
        notes: document.getElementById('target-notes').value.trim() || null,
    };

    try {
        if (id) {
            await api.put(`/api/targets/${id}`, payload);
            showToast('Alvo atualizado!');
        } else {
            await api.post('/api/targets/', payload);
            showToast('Alvo criado!');
        }
        closeTargetModal();
        loadTargets();
    } catch (e) {
        showToast('Erro: ' + e.message, 'error');
    }
});

async function deleteTarget(id) {
    if (!confirm('Remover este alvo? Todos os scans e findings dele serão apagados.')) return;
    try {
        await api.del(`/api/targets/${id}`);
        showToast('Alvo removido.');
        loadTargets();
    } catch (e) {
        showToast('Erro: ' + e.message, 'error');
    }
}

loadTargets();