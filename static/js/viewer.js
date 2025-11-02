// Visor de entradas - JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const entriesGrid = document.getElementById('entriesGrid');
    const projectFilter = document.getElementById('projectFilter');
    const searchInput = document.getElementById('searchInput');
    const entryModal = document.getElementById('entryModal');
    const closeModal = document.getElementById('closeModal');
    const shutdownBtn = document.getElementById('shutdownBtn');

    let allEntries = [];

    // Cargar entradas al iniciar
    loadEntries();
    loadProjects();

    // Event listeners
    projectFilter.addEventListener('change', filterEntries);
    searchInput.addEventListener('input', filterEntries);
    closeModal.addEventListener('click', () => entryModal.classList.add('hidden'));
    entryModal.addEventListener('click', (e) => {
        if (e.target === entryModal) {
            entryModal.classList.add('hidden');
        }
    });

    // Detener aplicación
    shutdownBtn.addEventListener('click', async function() {
        if (confirm('¿Seguro que quieres detener la aplicación?')) {
            try {
                await fetch('/api/shutdown', { method: 'POST' });
                document.body.innerHTML = '<div style="display: flex; align-items: center; justify-content: center; height: 100vh; color: white; font-size: 24px; text-align: center;">✅ Aplicación detenida<br><small style="font-size: 16px; margin-top: 10px;">Puedes cerrar esta ventana</small></div>';
            } catch (error) {
                setTimeout(() => {
                    document.body.innerHTML = '<div style="display: flex; align-items: center; justify-content: center; height: 100vh; color: white; font-size: 24px; text-align: center;">✅ Aplicación detenida<br><small style="font-size: 16px; margin-top: 10px;">Puedes cerrar esta ventana</small></div>';
                }, 500);
            }
        }
    });

    // Cargar todas las entradas
    async function loadEntries() {
        try {
            const response = await fetch('/api/entries');
            const result = await response.json();

            if (result.success) {
                allEntries = result.entries;
                displayEntries(allEntries);
            }
        } catch (error) {
            console.error('Error cargando entradas:', error);
            entriesGrid.innerHTML = '<p style="color: white; text-align: center;">Error cargando entradas</p>';
        }
    }

    // Cargar proyectos para el filtro
    async function loadProjects() {
        try {
            const response = await fetch('/api/projects');
            const result = await response.json();

            if (result.success && result.projects.length > 0) {
                result.projects.forEach(project => {
                    const option = document.createElement('option');
                    option.value = project;
                    option.textContent = project;
                    projectFilter.appendChild(option);
                });
            }
        } catch (error) {
            console.error('Error cargando proyectos:', error);
        }
    }

    // Mostrar entradas
    function displayEntries(entries) {
        if (entries.length === 0) {
            entriesGrid.innerHTML = `
                <div style="grid-column: 1/-1; text-align: center; color: #d8b4fe; padding: 40px;">
                    <div style="font-size: 48px; margin-bottom: 16px;">📭</div>
                    <p style="font-size: 18px;">No hay entradas todavía</p>
                    <p style="font-size: 14px; opacity: 0.7;">Empieza a documentar tu desarrollo</p>
                </div>
            `;
            return;
        }

        entriesGrid.innerHTML = entries.map(entry => {
            const title = entry.commit_problema || 'Sin título';
            const author = entry.autor || 'Anónimo';
            const branch = entry.rama || 'sin-rama';
            const date = formatDate(entry.fecha);
            const preview = extractPreview(entry.content);

            return `
                <div class="entry-card" onclick="openEntry('${entry.project}', '${entry.filename}')">
                    <div class="entry-header">
                        <div class="entry-title">${escapeHtml(title)}</div>
                        <div class="entry-meta">
                            <span class="meta-tag">📁 ${escapeHtml(entry.project)}</span>
                            <span class="meta-tag">🌿 ${escapeHtml(branch)}</span>
                            <span class="meta-tag">👤 ${escapeHtml(author)}</span>
                        </div>
                        <div class="entry-date">📅 ${date}</div>
                    </div>
                    <div class="entry-preview">${escapeHtml(preview)}</div>
                </div>
            `;
        }).join('');
    }

    // Filtrar entradas
    function filterEntries() {
        const projectValue = projectFilter.value.toLowerCase();
        const searchValue = searchInput.value.toLowerCase();

        const filtered = allEntries.filter(entry => {
            const matchProject = !projectValue || entry.project.toLowerCase() === projectValue;
            const matchSearch = !searchValue ||
                (entry.commit_problema && entry.commit_problema.toLowerCase().includes(searchValue)) ||
                (entry.content && entry.content.toLowerCase().includes(searchValue));

            return matchProject && matchSearch;
        });

        displayEntries(filtered);
    }

    // Abrir modal con entrada completa
    window.openEntry = async function(project, filename) {
        try {
            const response = await fetch(`/api/entry/${encodeURIComponent(project)}/${encodeURIComponent(filename)}`);
            const result = await response.json();

            if (result.success) {
                // Renderizar markdown
                const html = marked.parse(result.content);

                document.getElementById('modalTitle').textContent = filename.replace('.md', '');
                document.getElementById('modalBody').innerHTML = html;

                entryModal.classList.remove('hidden');
            }
        } catch (error) {
            console.error('Error cargando entrada:', error);
            alert('Error al cargar la entrada');
        }
    };

    // Utilidades
    function extractPreview(content) {
        // Extraer texto después del frontmatter y primera línea
        const parts = content.split('---');
        if (parts.length >= 3) {
            const body = parts[2].trim();
            const lines = body.split('\n').filter(l => l.trim() && !l.startsWith('#'));
            return lines.slice(0, 3).join(' ').substring(0, 150) + '...';
        }
        return content.substring(0, 150) + '...';
    }

    function formatDate(dateStr) {
        if (!dateStr) return 'Fecha desconocida';

        try {
            const date = new Date(dateStr.replace(' ', 'T'));
            return date.toLocaleDateString('es-ES', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        } catch {
            return dateStr;
        }
    }

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
});