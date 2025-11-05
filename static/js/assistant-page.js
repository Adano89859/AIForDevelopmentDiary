// Asistente IA - JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chatMessages');
    const questionInput = document.getElementById('questionInput');
    const sendQuestion = document.getElementById('sendQuestion');
    const projectContext = document.getElementById('projectContext');
    const referencesContent = document.getElementById('referencesContent');
    const referencesCount = document.getElementById('referencesCount');
    const modeBtns = document.querySelectorAll('.mode-btn');
    const shutdownBtn = document.getElementById('shutdownBtn');

    let currentMode = 'search';
    let currentReferences = [];

    // Cargar proyectos
    loadProjects();

    // Cambiar modo
    modeBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            modeBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentMode = btn.dataset.mode;

            const modeNames = {
                'search': '🔍 Búsqueda en historial',
                'suggest': '💡 Sugerencias de solución',
                'files': '📂 Archivos relacionados',
                'analyze': '📊 Análisis de patrones'
            };

            addMessage('assistant', `**Modo cambiado:** ${modeNames[currentMode]}`);
        });
    });

    // Enviar pregunta
    sendQuestion.addEventListener('click', sendMessage);
    questionInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && e.ctrlKey) {
            sendMessage();
        }
    });

    // Detener servidor
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

    // Cargar proyectos para el selector
    async function loadProjects() {
        try {
            const response = await fetch('/api/projects');
            const result = await response.json();

            if (result.success && result.projects.length > 0) {
                result.projects.forEach(project => {
                    const option = document.createElement('option');
                    option.value = project;
                    option.textContent = project;
                    projectContext.appendChild(option);
                });
            }
        } catch (error) {
            console.error('Error cargando proyectos:', error);
        }
    }

    // Enviar mensaje
    async function sendMessage() {
        const question = questionInput.value.trim();

        if (!question) {
            alert('Por favor escribe una pregunta');
            return;
        }

        // Añadir mensaje del usuario
        addMessage('user', question);
        questionInput.value = '';

        // Mostrar loading
        const loadingMsg = addLoadingMessage();

        // Deshabilitar input
        questionInput.disabled = true;
        sendQuestion.disabled = true;

        try {
            const project = projectContext.value;

            const response = await fetch('/api/assistant', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    question: question,
                    project: project,
                    mode: currentMode
                })
            });

            const result = await response.json();

            // Remover loading
            loadingMsg.remove();

            if (result.success) {
                // Renderizar respuesta con Markdown
                const html = marked.parse(result.response);
                addMessage('assistant', html, true);

                // Mostrar archivos referenciados
                if (result.referenced_files && result.referenced_files.length > 0) {
                    currentReferences = result.referenced_files;
                    displayReferences(result.referenced_files);
                }

                // Mostrar contador de contexto
                if (result.context_used > 0) {
                    addContextInfo(result.context_used);
                }
            } else {
                addMessage('assistant', `❌ Error: ${result.message}`);
            }

        } catch (error) {
            loadingMsg.remove();
            console.error('Error:', error);
            addMessage('assistant', '❌ Error al comunicarse con el asistente. Verifica que Ollama esté corriendo.');
        } finally {
            // Rehabilitar input
            questionInput.disabled = false;
            sendQuestion.disabled = false;
            questionInput.focus();
        }
    }

    // Añadir mensaje al chat
    function addMessage(sender, content, isHtml = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${sender}`;

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';

        if (isHtml) {
            contentDiv.innerHTML = content;
        } else {
            contentDiv.textContent = content;
        }

        messageDiv.appendChild(contentDiv);
        chatMessages.appendChild(messageDiv);

        // Scroll al final
        chatMessages.scrollTop = chatMessages.scrollHeight;

        return messageDiv;
    }

    // Añadir mensaje de loading
    function addLoadingMessage() {
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'chat-message assistant';
        loadingDiv.innerHTML = '<div class="message-loading">🤔 Analizando tu historial y generando respuesta...</div>';

        chatMessages.appendChild(loadingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;

        return loadingDiv;
    }

    // Añadir info de contexto
    function addContextInfo(count) {
        const infoDiv = document.createElement('div');
        infoDiv.className = 'chat-message assistant';
        infoDiv.innerHTML = `<div class="message-content"><small>📚 Analicé <strong>${count}</strong> entrada${count > 1 ? 's' : ''} de tu historial</small></div>`;

        chatMessages.appendChild(infoDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Mostrar referencias
    function displayReferences(files) {
        referencesContent.innerHTML = '';
        referencesCount.textContent = files.length;

        if (files.length === 0) {
            referencesContent.innerHTML = `
                <div class="empty-state">
                    <div class="empty-icon">📭</div>
                    <p>No hay archivos referenciados</p>
                </div>
            `;
            return;
        }

        files.forEach(file => {
            const card = createFileCard(file);
            referencesContent.appendChild(card);
        });
    }

    // Crear tarjeta de archivo
    function createFileCard(file) {
        const card = document.createElement('div');
        card.className = 'file-card';
        card.onclick = () => openFile(file.project, file.filename);

        // Determinar relevancia visual
        let relevanceBadge = '';
        if (file.relevance > 10) {
            relevanceBadge = '<span class="relevance-badge">🔥 Alta</span>';
        } else if (file.relevance > 5) {
            relevanceBadge = '<span class="relevance-badge">⚡ Media</span>';
        } else {
            relevanceBadge = '<span class="relevance-badge">💡 Baja</span>';
        }

        card.innerHTML = `
            <div class="file-header">
                <div class="file-icon">📄</div>
                <div class="file-info">
                    <div class="file-title">${escapeHtml(file.title)}</div>
                    <div class="file-meta">
                        <div class="meta-item">
                            <span>📁</span> ${escapeHtml(file.project)}
                        </div>
                        <div class="meta-item">
                            <span>🌿</span> ${escapeHtml(file.branch)}
                        </div>
                        <div class="meta-item">
                            <span>📅</span> ${formatDate(file.date)}
                        </div>
                        <div class="meta-item">
                            ${relevanceBadge}
                        </div>
                    </div>
                </div>
            </div>
        `;

        return card;
    }

    // Abrir archivo en modal
    async function openFile(project, filename) {
        try {
            const response = await fetch(`/api/entry/${encodeURIComponent(project)}/${encodeURIComponent(filename)}`);
            const result = await response.json();

            if (result.success) {
                // Crear modal temporal
                showFileModal(filename, result.content, project);
            }
        } catch (error) {
            console.error('Error abriendo archivo:', error);
            alert('Error al abrir el archivo');
        }
    }

    // Mostrar modal con contenido del archivo (MEJORADO)
    function showFileModal(filename, content, project) {
        // Crear modal
        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.style.display = 'flex';

        const html = marked.parse(content);

        modal.innerHTML = `
            <div class="modal-content" style="max-width: 900px; background: #1e293b;">
                <div class="modal-header" style="background: rgba(15, 23, 42, 0.8); border-bottom: 2px solid rgba(168, 85, 247, 0.5);">
                    <div>
                        <h2 style="color: #ffffff;">📁 ${escapeHtml(project)} / ${escapeHtml(filename)}</h2>
                    </div>
                    <button class="modal-close" onclick="this.closest('.modal').remove()">✕</button>
                </div>
                <div class="modal-body" style="background: #0f172a; color: #f1f5f9; padding: 30px;">
                    ${html}
                </div>
            </div>
        `;

        // Cerrar al hacer click fuera
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.remove();
            }
        });

        document.body.appendChild(modal);
    }

    // Utilidades
    function formatDate(dateStr) {
        if (!dateStr || dateStr === 'N/A') return 'N/A';

        try {
            const date = new Date(dateStr.replace(' ', 'T'));
            return date.toLocaleDateString('es-ES', {
                year: 'numeric',
                month: 'short',
                day: 'numeric'
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