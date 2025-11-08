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

    // ========== RECONOCIMIENTO DE VOZ CON VOSK ==========

    let mediaRecorder = null;
    let audioChunks = [];
    let audioStream = null;

    recordBtn.addEventListener('click', async function() {
        if (!isRecording) {
            await startRecording();
        } else {
            await stopRecording();
        }
    });

    async function startRecording() {
        try {
            // Solicitar permiso para el micrófono
            audioStream = await navigator.mediaDevices.getUserMedia({
                audio: {
                    channelCount: 1,  // Mono
                    sampleRate: 16000, // 16kHz
                    echoCancellation: true,
                    noiseSuppression: true
                }
            });

            // Crear MediaRecorder
            const options = { mimeType: 'audio/webm' };
            mediaRecorder = new MediaRecorder(audioStream, options);

            audioChunks = [];

            mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    audioChunks.push(event.data);
                }
            };

            mediaRecorder.onstop = async () => {
                await processRecording();
            };

            // Iniciar grabación
            mediaRecorder.start();
            isRecording = true;

            // Actualizar UI
            recordBtn.textContent = '🔴 Grabando...';
            recordBtn.classList.add('recording');

            console.log('🎤 Grabación iniciada');

        } catch (error) {
            console.error('❌ Error al acceder al micrófono:', error);

            if (error.name === 'NotAllowedError') {
                alert('⚠️ Permiso de micrófono denegado.\nPor favor, permite el acceso al micrófono en la configuración del navegador.');
            } else {
                alert('❌ Error al acceder al micrófono: ' + error.message);
            }
        }
    }

    async function stopRecording() {
        if (mediaRecorder && mediaRecorder.state === 'recording') {
            mediaRecorder.stop();

            // Detener el stream
            if (audioStream) {
                audioStream.getTracks().forEach(track => track.stop());
            }

            isRecording = false;

            // Actualizar UI
            recordBtn.textContent = '⏳ Transcribiendo...';
            recordBtn.disabled = true;

            console.log('🛑 Grabación detenida, procesando...');
        }
    }

    async function processRecording() {
        try {
            // Crear blob de audio
            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });

            // Convertir webm a wav usando Web Audio API
            const arrayBuffer = await audioBlob.arrayBuffer();
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);

            // Convertir a WAV mono 16kHz
            const wavBlob = await audioBufferToWav(audioBuffer);

            // Enviar al servidor para transcripción
            const formData = new FormData();
            formData.append('audio', wavBlob, 'recording.wav');

            console.log('📤 Enviando audio al servidor...');

            const response = await fetch('/api/transcribe', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.success) {
                const transcription = result.transcription;

                if (transcription) {
                    // Añadir transcripción al textarea
                    const notesTextarea = document.getElementById('notes');
                    const currentText = notesTextarea.value;

                    if (currentText.trim()) {
                        notesTextarea.value = currentText + '\n\n' + transcription;
                    } else {
                        notesTextarea.value = transcription;
                    }

                    console.log('✅ Transcripción completada:', transcription);

                    // Mostrar notificación visual
                    showTranscriptionSuccess(transcription);
                } else {
                    alert('⚠️ No se detectó voz en la grabación');
                }
            } else {
                throw new Error(result.message || 'Error al transcribir');
            }

        } catch (error) {
            console.error('❌ Error procesando audio:', error);
            alert('❌ Error al transcribir el audio: ' + error.message);
        } finally {
            // Restaurar botón
            recordBtn.textContent = '🎤 Grabar';
            recordBtn.classList.remove('recording');
            recordBtn.disabled = false;

            // Limpiar
            audioChunks = [];
        }
    }

    async function audioBufferToWav(audioBuffer) {
        /**
         * Convierte AudioBuffer a WAV mono 16kHz
         */
        const numberOfChannels = 1; // Mono
        const sampleRate = 16000;   // 16kHz
        const format = 1;            // PCM
        const bitDepth = 16;

        // Resamplear si es necesario
        let buffer = audioBuffer;
        if (audioBuffer.sampleRate !== sampleRate) {
            const offlineContext = new OfflineAudioContext(
                numberOfChannels,
                audioBuffer.duration * sampleRate,
                sampleRate
            );
            const source = offlineContext.createBufferSource();
            source.buffer = audioBuffer;
            source.connect(offlineContext.destination);
            source.start();
            buffer = await offlineContext.startRendering();
        }

        // Obtener datos de audio (mezclar a mono si es necesario)
        let audioData;
        if (buffer.numberOfChannels === 1) {
            audioData = buffer.getChannelData(0);
        } else {
            // Mezclar canales a mono
            const left = buffer.getChannelData(0);
            const right = buffer.getChannelData(1);
            audioData = new Float32Array(left.length);
            for (let i = 0; i < left.length; i++) {
                audioData[i] = (left[i] + right[i]) / 2;
            }
        }

        // Convertir a 16-bit PCM
        const samples = new Int16Array(audioData.length);
        for (let i = 0; i < audioData.length; i++) {
            const s = Math.max(-1, Math.min(1, audioData[i]));
            samples[i] = s < 0 ? s * 0x8000 : s * 0x7FFF;
        }

        // Crear WAV header
        const dataLength = samples.length * 2;
        const buffer_wav = new ArrayBuffer(44 + dataLength);
        const view = new DataView(buffer_wav);

        // RIFF header
        writeString(view, 0, 'RIFF');
        view.setUint32(4, 36 + dataLength, true);
        writeString(view, 8, 'WAVE');

        // fmt chunk
        writeString(view, 12, 'fmt ');
        view.setUint32(16, 16, true);              // Chunk size
        view.setUint16(20, format, true);          // Audio format (PCM)
        view.setUint16(22, numberOfChannels, true);// Channels
        view.setUint32(24, sampleRate, true);      // Sample rate
        view.setUint32(28, sampleRate * numberOfChannels * bitDepth / 8, true); // Byte rate
        view.setUint16(32, numberOfChannels * bitDepth / 8, true); // Block align
        view.setUint16(34, bitDepth, true);        // Bits per sample

        // data chunk
        writeString(view, 36, 'data');
        view.setUint32(40, dataLength, true);

        // Write PCM samples
        const offset = 44;
        for (let i = 0; i < samples.length; i++) {
            view.setInt16(offset + i * 2, samples[i], true);
        }

        return new Blob([buffer_wav], { type: 'audio/wav' });
    }

    function writeString(view, offset, string) {
        for (let i = 0; i < string.length; i++) {
            view.setUint8(offset + i, string.charCodeAt(i));
        }
    }

    function showTranscriptionSuccess(text) {
        // Crear notificación temporal
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: linear-gradient(135deg, #22c55e, #16a34a);
            color: white;
            padding: 16px 24px;
            border-radius: 12px;
            box-shadow: 0 8px 20px rgba(34, 197, 94, 0.4);
            z-index: 10000;
            max-width: 400px;
            animation: slideIn 0.3s ease-out;
        `;

        notification.innerHTML = `
            <div style="font-weight: bold; margin-bottom: 8px;">✅ Transcripción completada</div>
            <div style="font-size: 14px; opacity: 0.9;">${text.substring(0, 80)}${text.length > 80 ? '...' : ''}</div>
        `;

        document.body.appendChild(notification);

        // Eliminar después de 3 segundos
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease-out';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }

    // Añadir animaciones CSS
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from {
                transform: translateX(400px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        @keyframes slideOut {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(400px);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);

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