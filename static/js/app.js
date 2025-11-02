// Development Diary - JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const saveBtn = document.getElementById('saveBtn');
    const successMessage = document.getElementById('successMessage');
    const recordBtn = document.getElementById('recordBtn');
    const shutdownBtn = document.getElementById('shutdownBtn');
    const projectInput = document.getElementById('project');
    const branchInput = document.getElementById('branch');

    let isRecording = false;

    // Cargar proyectos existentes al iniciar
    loadProjects();

    // Cargar ramas cuando cambia el proyecto
    projectInput.addEventListener('input', function() {
        if (this.value.trim()) {
            loadBranches(this.value);
        }
    });

    // Función para cargar proyectos
    async function loadProjects() {
        try {
            const response = await fetch('/api/projects');
            const result = await response.json();

            if (result.success && result.projects.length > 0) {
                const datalist = document.getElementById('projectsList');
                datalist.innerHTML = '';

                result.projects.forEach(project => {
                    const option = document.createElement('option');
                    option.value = project;
                    datalist.appendChild(option);
                });
            }
        } catch (error) {
            console.error('Error cargando proyectos:', error);
        }
    }

    // Función para cargar ramas de un proyecto
    async function loadBranches(project) {
        try {
            const response = await fetch(`/api/branches/${encodeURIComponent(project)}`);
            const result = await response.json();

            if (result.success && result.branches.length > 0) {
                const datalist = document.getElementById('branchesList');
                datalist.innerHTML = '';

                result.branches.forEach(branch => {
                    const option = document.createElement('option');
                    option.value = branch;
                    datalist.appendChild(option);
                });
            }
        } catch (error) {
            console.error('Error cargando ramas:', error);
        }
    }

    // Guardar entrada
    saveBtn.addEventListener('click', async function() {
        const author = document.getElementById('author').value;
        const project = document.getElementById('project').value;
        const branch = document.getElementById('branch').value;
        const commit = document.getElementById('commit').value;
        const notes = document.getElementById('notes').value;
        const useAI = document.getElementById('aiEnabled').checked;

        if (!notes.trim()) {
            alert('Por favor, escribe algo en las notas');
            return;
        }

        // Cambiar estado del botón
        saveBtn.textContent = '⏳ Guardando...';
        saveBtn.classList.add('saving');
        saveBtn.disabled = true;

        try {
            const response = await fetch('/api/save', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    author: author,
                    project: project || 'Sin_Proyecto',
                    branch: branch,
                    commit_problem: commit,
                    notes: notes,
                    use_ai: useAI
                })
            });

            const result = await response.json();

            if (result.success) {
                // Éxito
                saveBtn.textContent = '✅ ¡Guardado!';
                saveBtn.classList.remove('saving');
                saveBtn.classList.add('success');

                // Mostrar mensaje
                successMessage.classList.remove('hidden');

                // Limpiar formulario
                document.getElementById('notes').value = '';
                document.getElementById('commit').value = '';

                // Recargar proyectos y ramas
                loadProjects();
                if (project) {
                    loadBranches(project);
                }

                // Restaurar después de 2 segundos
                setTimeout(() => {
                    saveBtn.textContent = '💾 Guardar Entrada';
                    saveBtn.classList.remove('success');
                    saveBtn.disabled = false;
                    successMessage.classList.add('hidden');
                }, 2000);
            } else {
                throw new Error(result.message);
            }

        } catch (error) {
            console.error('Error:', error);
            alert('Error al guardar: ' + error.message);
            saveBtn.textContent = '💾 Guardar Entrada';
            saveBtn.classList.remove('saving');
            saveBtn.disabled = false;
        }
    });

    // Detener aplicación
    shutdownBtn.addEventListener('click', async function() {
        if (confirm('¿Seguro que quieres detener la aplicación?')) {
            try {
                await fetch('/api/shutdown', { method: 'POST' });
                document.body.innerHTML = '<div style="display: flex; align-items: center; justify-content: center; height: 100vh; color: white; font-size: 24px; text-align: center;">✅ Aplicación detenida<br><small style="font-size: 16px; margin-top: 10px;">Puedes cerrar esta ventana</small></div>';
            } catch (error) {
                // El servidor se detendrá, así que el error es esperado
                setTimeout(() => {
                    document.body.innerHTML = '<div style="display: flex; align-items: center; justify-content: center; height: 100vh; color: white; font-size: 24px; text-align: center;">✅ Aplicación detenida<br><small style="font-size: 16px; margin-top: 10px;">Puedes cerrar esta ventana</small></div>';
                }, 500);
            }
        }
    });

    // Grabar voz (placeholder por ahora)
    recordBtn.addEventListener('click', function() {
        if (!isRecording) {
            isRecording = true;
            recordBtn.textContent = '🔴 Grabando...';
            recordBtn.classList.add('recording');

            // Simular grabación (implementar Vosk más adelante)
            alert('Función de voz en desarrollo. Usa el modelo de Vosk para activarla.');

            setTimeout(() => {
                isRecording = false;
                recordBtn.textContent = '🎤 Grabar';
                recordBtn.classList.remove('recording');
            }, 1000);
        }
    });

    // Efectos de focus en inputs
    const inputs = document.querySelectorAll('input, textarea');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.style.borderColor = '#a855f7';
        });

        input.addEventListener('blur', function() {
            this.style.borderColor = 'rgba(148, 163, 184, 0.2)';
        });
    });
});