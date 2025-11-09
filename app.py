"""
Development Diary - Servidor Flask
Versión web con interfaz moderna
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime
from pathlib import Path
import requests
import os
import signal
import json
import wave
import tempfile
from vosk import Model, KaldiRecognizer
import speech_recognition as sr
from pydub import AudioSegment
import io
from diary.pdf_generator import PDFGenerator
import tempfile

app = Flask(__name__)
CORS(app)

# Configuración
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.1:8b"
BASE_PATH = Path("Development Diary")
BASE_PATH.mkdir(exist_ok=True)
VOSK_MODEL = None


@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')


@app.route('/viewer')
def viewer():
    """Página del visor de entradas"""
    return render_template('viewer.html')


@app.route('/assistant')
def assistant_page():
    """Página del asistente IA"""
    return render_template('assistant.html')


@app.route('/api/projects', methods=['GET'])
def get_projects():
    """Obtiene lista de proyectos existentes"""
    try:
        projects = []
        if BASE_PATH.exists():
            for item in BASE_PATH.iterdir():
                if item.is_dir() and item.name != '.gitkeep':
                    projects.append(item.name)

        return jsonify({
            'success': True,
            'projects': sorted(projects)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/branches/<project>', methods=['GET'])
def get_branches(project):
    """Obtiene lista de ramas de un proyecto"""
    try:
        branches = set()
        project_path = BASE_PATH / project / "entries"

        if project_path.exists():
            # Leer archivos markdown y extraer ramas del frontmatter
            for md_file in project_path.glob("*.md"):
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Buscar la rama en el frontmatter
                    for line in content.split('\n'):
                        if line.startswith('rama:'):
                            branch = line.replace('rama:', '').strip()
                            if branch and branch.lower() not in ['', 'nada']:
                                branches.add(branch)

        return jsonify({
            'success': True,
            'branches': sorted(list(branches))
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/save', methods=['POST'])
def save_entry():
    """
    Guarda una entrada del diario
    Recibe: author, project, branch, commit_problem, notes, use_ai
    """
    try:
        data = request.json

        author = data.get('author', '')
        project = data.get('project', 'Sin_Proyecto')
        branch = data.get('branch', '')
        commit_problem = data.get('commit_problem', '')
        notes = data.get('notes', '')
        use_ai = data.get('use_ai', True)

        if not notes:
            return jsonify({
                'success': False,
                'message': 'No hay contenido para guardar'
            }), 400

        # Mejorar con IA si está activado
        if use_ai:
            print("🤖 Mejorando texto con IA...")
            improved_notes = improve_with_ai(data)
        else:
            improved_notes = notes

        # Crear carpeta del proyecto
        project_path = BASE_PATH / project / "entries"
        project_path.mkdir(parents=True, exist_ok=True)

        # Generar nombre de archivo con timestamp y rama
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Limpiar nombre de rama para el archivo (sin caracteres especiales)
        branch_clean = branch.replace('/', '-').replace('\\', '-').replace(' ', '_') if branch else 'sin-rama'

        # Formato: FECHA_HORA_rama-nombre.md
        filename = f"{timestamp}_{branch_clean}.md"
        filepath = project_path / filename

        # Generar contenido Markdown
        markdown_content = generate_markdown(data, improved_notes, timestamp)

        # Guardar archivo
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        print(f"✅ Entrada guardada: {filepath}")

        return jsonify({
            'success': True,
            'message': '¡Entrada guardada exitosamente!',
            'filepath': str(filepath)
        })

    except Exception as e:
        print(f"❌ Error guardando entrada: {e}")
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500


@app.route('/api/entries', methods=['GET'])
def get_entries():
    """
    Obtiene todas las entradas del diario
    Opcionalmente filtrar por proyecto
    """
    try:
        project_filter = request.args.get('project', None)
        entries = []

        # Determinar qué proyectos buscar
        if project_filter:
            projects_to_scan = [project_filter]
        else:
            projects_to_scan = [p.name for p in BASE_PATH.iterdir() if p.is_dir()]

        # Escanear entradas
        for project_name in projects_to_scan:
            entries_path = BASE_PATH / project_name / "entries"

            if not entries_path.exists():
                continue

            for md_file in sorted(entries_path.glob("*.md"), reverse=True):
                # Leer archivo
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Parsear frontmatter
                entry_data = parse_frontmatter(content)
                entry_data['filename'] = md_file.name
                entry_data['project'] = project_name
                entry_data['content'] = content

                entries.append(entry_data)

        # Ordenar por fecha (más reciente primero)
        entries.sort(key=lambda x: x.get('fecha', ''), reverse=True)

        return jsonify({
            'success': True,
            'entries': entries,
            'total': len(entries)
        })

    except Exception as e:
        print(f"❌ Error obteniendo entradas: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/entry/<project>/<filename>', methods=['GET'])
def get_entry_content(project, filename):
    """Obtiene el contenido completo de una entrada específica"""
    try:
        filepath = BASE_PATH / project / "entries" / filename

        if not filepath.exists():
            return jsonify({
                'success': False,
                'message': 'Entrada no encontrada'
            }), 404

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extraer solo el contenido después del frontmatter
        parts = content.split('---', 2)
        if len(parts) >= 3:
            body = parts[2].strip()
        else:
            body = content

        return jsonify({
            'success': True,
            'content': body,
            'raw': content
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/assistant', methods=['POST'])
def assistant():
    """
    Asistente inteligente que ayuda con problemas
    usando el historial de entradas como contexto
    """
    try:
        data = request.json
        question = data.get('question', '')
        project = data.get('project', '')
        mode = data.get('mode', 'search')

        if not question:
            return jsonify({
                'success': False,
                'message': 'No hay pregunta'
            }), 400

        # Obtener contexto del historial
        context = get_relevant_context(question, project, mode)

        # Generar respuesta con IA
        response = generate_assistant_response(question, context, mode)

        # Extraer referencias a archivos
        referenced_files = extract_file_references(context)

        return jsonify({
            'success': True,
            'response': response,
            'context_used': len(context.get('entries', [])),
            'referenced_files': referenced_files
        })

    except Exception as e:
        print(f"❌ Error en asistente: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/shutdown', methods=['POST'])
def shutdown():
    """Detiene el servidor Flask"""
    print("🛑 Deteniendo servidor...")
    os.kill(os.getpid(), signal.SIGINT)
    return jsonify({'success': True, 'message': 'Servidor detenido'})


# ==================== FUNCIONES AUXILIARES ====================


def improve_with_ai(data):
    """Mejora el texto usando Ollama con formato visual atractivo"""
    prompt = f"""Eres un asistente que ayuda a desarrolladores a documentar su trabajo de forma clara, visual y profesional.

CONTEXTO:
- Proyecto: {data['project']}
- Rama: {data['branch']}
- Commit/Problema: {data['commit_problem']}

NOTAS DEL DESARROLLADOR:
{data['notes']}

INSTRUCCIONES PARA EL FORMATO:

1. **Resume el contenido** que el usuario proporcionó, manteniendo TODOS los detalles técnicos importantes
2. **Usa Markdown rico y visual:**
   - Headers (##, ###) para secciones
   - **Negritas** para términos clave y conceptos importantes
   - *Cursivas* para énfasis suave
   - `código inline` para nombres de archivos, funciones, variables
   - Bloques de código ```language si hay código
   - Listas (-, *) para puntos múltiples
   - > Citas para destacar conclusiones importantes
   - ⚠️ 🔧 💡 ✅ ❌ 📝 🚀 Emojis contextuales (usa con moderación, solo cuando añadan claridad)

3. **Estructura sugerida** (adapta según el contenido):
   - Resumen breve (1-2 líneas)
   - Qué se hizo / Qué problema había
   - Cómo se resolvió / Pasos realizados
   - Resultados / Estado actual
   - Notas adicionales (si aplica)

4. **IMPORTANTE:**
   - NO inventes información que no esté en las notas
   - Si las notas son breves, el resumen también debe ser breve
   - Sé literal con los detalles técnicos
   - Si el usuario menciona errores, inclúyelos textualmente

5. **Objetivo:** Crear un documento que sea:
   - Fácil de leer visualmente
   - Profesional pero accesible
   - Útil para revisar en el futuro

Responde SOLO con el texto en Markdown mejorado, sin introducciones ni meta-comentarios.

RESUMEN VISUAL:"""

    try:
        print(f"🧠 Consultando a {OLLAMA_MODEL}...")

        resp = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.5,
                    "num_predict": 1536,
                    "top_k": 30,
                    "top_p": 0.85
                }
            },
            timeout=120
        )

        if resp.status_code == 200:
            result = resp.json()
            improved = result.get("response", "").strip()

            if improved:
                print(f"✅ Texto mejorado ({len(improved)} caracteres)")
                return improved
            else:
                print("⚠️ IA devolvió respuesta vacía")
                return data['notes']
        else:
            print(f"❌ Error HTTP {resp.status_code}")
            return data['notes']

    except Exception as e:
        print(f"❌ Error con IA: {e}")
        return data['notes']


def generate_markdown(data, improved_notes, timestamp):
    """Genera el contenido Markdown"""
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    frontmatter = f"""---
autor: {data['author'] or 'Anónimo'}
proyecto: {data['project']}
rama: {data['branch']}
commit_problema: {data['commit_problem']}
fecha: {fecha}
---

"""

    body = f"""# {data['commit_problem'] or 'Entrada de desarrollo'}

{improved_notes}

---

## 📝 Notas Originales
```
{data['notes']}
```

---
*Generado por Development Diary el {fecha}*
"""

    return frontmatter + body


def parse_frontmatter(content):
    """Extrae datos del frontmatter YAML"""
    data = {}

    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 2:
            frontmatter = parts[1].strip()

            for line in frontmatter.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    data[key.strip()] = value.strip()

    return data


def get_relevant_context(question, project_filter, mode):
    """
    Obtiene entradas relevantes del historial según la pregunta
    Busca en TODOS los proyectos pero prioriza el proyecto actual
    """
    context = {
        'entries': [],
        'projects': set(),
        'branches': set(),
        'errors': []
    }

    try:
        question_lower = question.lower()
        keywords = extract_keywords(question_lower)

        # Palabras clave de errores comunes
        error_keywords = ['error', 'bug', 'fallo', 'problema', 'excepción', 'exception',
                         'crash', 'no funciona', 'roto', 'broken']

        # Buscar en TODOS los proyectos
        all_projects = [p.name for p in BASE_PATH.iterdir() if p.is_dir()]

        for project_name in all_projects:
            entries_path = BASE_PATH / project_name / "entries"

            if not entries_path.exists():
                continue

            for md_file in entries_path.glob("*.md"):
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                content_lower = content.lower()

                # Calcular relevancia
                relevance_score = 0

                # Boost si coincide con el proyecto actual
                if project_filter and project_name.lower() == project_filter.lower():
                    relevance_score += 10

                # Buscar keywords
                for keyword in keywords:
                    if keyword in content_lower:
                        relevance_score += content_lower.count(keyword) * 2

                # Detectar si contiene errores
                is_error_entry = any(err in content_lower for err in error_keywords)
                if is_error_entry and mode in ['search', 'suggest']:
                    relevance_score += 5

                # Si es relevante, incluir
                if relevance_score > 0:
                    entry_data = parse_frontmatter(content)
                    entry_data['content'] = content
                    entry_data['content_preview'] = content[:800]
                    entry_data['relevance'] = relevance_score
                    entry_data['project'] = project_name
                    entry_data['filename'] = md_file.name
                    entry_data['is_error'] = is_error_entry

                    context['entries'].append(entry_data)
                    context['projects'].add(project_name)

                    if entry_data.get('rama'):
                        context['branches'].add(entry_data['rama'])

        # Ordenar por relevancia
        context['entries'].sort(key=lambda x: x.get('relevance', 0), reverse=True)

        # Limitar según el modo
        limit = 10 if mode == 'analyze' else 5
        context['entries'] = context['entries'][:limit]

        # Convertir sets a listas
        context['projects'] = list(context['projects'])
        context['branches'] = list(context['branches'])

    except Exception as e:
        print(f"⚠️ Error obteniendo contexto: {e}")

    return context


def extract_keywords(text):
    """Extrae palabras clave de la pregunta"""
    stop_words = {'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'ser', 'se', 'no', 'haber',
                  'por', 'con', 'su', 'para', 'como', 'estar', 'tener', 'le', 'lo', 'todo',
                  'pero', 'más', 'hacer', 'o', 'poder', 'decir', 'este', 'ir', 'otro', 'ese',
                  'si', 'me', 'ya', 'ver', 'porque', 'dar', 'cuando', 'él', 'muy', 'sin',
                  'vez', 'mucho', 'saber', 'qué', 'sobre', 'mi', 'alguno', 'mismo', 'yo',
                  'también', 'hasta', 'año', 'dos', 'querer', 'entre', 'así', 'primero',
                  'desde', 'grande', 'eso', 'ni', 'nos', 'llegar', 'pasar', 'tiempo', 'ella',
                  'tengo', 'he', 'ha', 'sido', 'cómo', 'hay', 'puedo', 'puede', 'los', 'las',
                  'una', 'unos', 'unas', 'del'}

    # Extraer palabras
    words = text.lower().split()
    keywords = []

    for word in words:
        # Limpiar puntuación
        word = word.strip('.,;:!?¿¡()[]{}"\'-')

        # Filtrar
        if len(word) > 3 and word not in stop_words:
            keywords.append(word)

    return keywords


def extract_file_references(context):
    """
    Extrae referencias a archivos mencionados en las entradas del contexto
    """
    files = []

    for entry in context.get('entries', []):
        file_ref = {
            'project': entry.get('project'),
            'filename': entry.get('filename'),
            'title': entry.get('commit_problema', 'Sin título'),
            'branch': entry.get('rama', 'N/A'),
            'date': entry.get('fecha', 'N/A'),
            'relevance': entry.get('relevance', 0)
        }
        files.append(file_ref)

    return files


def generate_assistant_response(question, context, mode):
    """
    Genera respuesta del asistente usando IA con contexto del historial
    """
    # Preparar información del contexto
    context_text = ""

    if context['entries']:
        context_text = f"\n\n📚 **HISTORIAL RELEVANTE (encontradas {len(context['entries'])} entradas):**\n"
        context_text += f"📁 Proyectos: {', '.join(context['projects'])}\n"
        context_text += f"🌿 Ramas: {', '.join(context['branches']) if context['branches'] else 'N/A'}\n\n"

        for i, entry in enumerate(context['entries'], 1):
            context_text += f"**═══ Entrada {i} ═══**\n"
            context_text += f"📁 Proyecto: `{entry.get('project', 'N/A')}`\n"
            context_text += f"🌿 Rama: `{entry.get('rama', 'N/A')}`\n"
            context_text += f"💡 Problema: {entry.get('commit_problema', 'N/A')}\n"
            context_text += f"📅 Fecha: {entry.get('fecha', 'N/A')}\n"
            context_text += f"📄 Archivo: `{entry.get('filename', 'N/A')}`\n"
            context_text += f"📝 Contenido:\n{entry.get('content_preview', '')[:600]}...\n\n"
    else:
        context_text = "\n\n⚠️ No se encontraron entradas relevantes en el historial de NINGÚN proyecto.\n"

    # Prompts según el modo
    prompts = {
        'search': f"""Eres un asistente técnico experto que ayuda a desarrolladores buscando en su historial.

**PREGUNTA DEL DESARROLLADOR:**
"{question}"

{context_text}

**INSTRUCCIONES:**
1. 🔍 Busca en el historial si hay problemas SIMILARES o RELACIONADOS
2. Si encuentras algo similar:
   - Menciona ESPECÍFICAMENTE el proyecto y archivo (usa formato `Proyecto/archivo.md`)
   - Explica qué se hizo en esa ocasión
   - Indica si la situación es idéntica o solo similar
3. Si NO encuentras nada similar:
   - Indica claramente que es un problema NUEVO
   - Sugiere que documente bien la solución cuando la encuentre
4. **IMPORTANTE:** Siempre menciona los archivos referenciados con este formato: `[Proyecto/archivo]`

**FORMATO DE RESPUESTA:**
- Usa Markdown rico (##, **, `, listas, >)
- Emojis contextuales (🔍, ✅, ⚠️, 💡, 📁)
- Bloques de código ``` cuando sea apropiado
- Citas > para destacar conclusiones

**RESPUESTA:**""",

        'suggest': f"""Eres un asistente técnico que sugiere soluciones basándose en experiencia previa.

**PROBLEMA DEL DESARROLLADOR:**
"{question}"

{context_text}

**INSTRUCCIONES:**
1. 💡 Analiza el historial y sugiere soluciones CONCRETAS
2. Si hay entradas similares:
   - Explica qué funcionó antes (menciona archivos específicos)
   - Adapta la solución al contexto actual
3. Si no hay precedentes:
   - Da sugerencias generales pero útiles
   - Pregunta por más detalles si es necesario
4. 📂 Sugiere archivos/carpetas que podrían estar relacionados
5. **MENCIONA SIEMPRE** los archivos del historial con formato: `[Proyecto/archivo]`

**FORMATO DE RESPUESTA:**
- Secciones claras con ##
- Pasos numerados si es apropiado
- Código inline `código` y bloques ```
- Emojis (🔧, 💡, 📁, ⚠️, ✅)
- Referencias explícitas a archivos del historial

**RESPUESTA:**""",

        'files': f"""Eres un asistente que identifica archivos relacionados con un problema.

**CONSULTA DEL DESARROLLADOR:**
"{question}"

{context_text}

**INSTRUCCIONES:**
1. 📂 Identifica TODOS los archivos del historial relacionados con la consulta
2. Para cada archivo mencionado:
   - Proyecto y nombre: `[Proyecto/archivo]`
   - Por qué es relevante
   - Qué información contiene
3. Sugiere archivos del código que podrían estar relacionados (aunque no estén en el historial)
4. Prioriza por relevancia

**FORMATO DE RESPUESTA:**
## 📁 Archivos del Historial
- Lista de archivos con enlaces
- Descripción breve de cada uno

## 💻 Archivos del Código (sugeridos)
- Archivos que probablemente deban revisarse
- Explicación de por qué

**RESPUESTA:**""",

        'analyze': f"""Eres un asistente que analiza patrones en el desarrollo.

**CONSULTA DEL DESARROLLADOR:**
"{question}"

{context_text}

**INSTRUCCIONES:**
1. 📊 Analiza el historial completo proporcionado
2. Identifica:
   - Errores recurrentes (🔴 frecuente, 🟡 ocasional)
   - Áreas problemáticas
   - Patrones en ramas/proyectos
   - Tendencias temporales
3. Da insights ACCIONABLES
4. Menciona archivos específicos donde se repiten problemas: `[Proyecto/archivo]`

**FORMATO DE RESPUESTA:**
## 📊 Análisis de Patrones
- Estadísticas visuales (usa emojis como gráficos)
- Conclusiones clave

## 🔴 Problemas Recurrentes
- Lista con frecuencia

## 💡 Recomendaciones
- Acciones concretas para mejorar

**RESPUESTA:**"""
    }

    prompt = prompts.get(mode, prompts['search'])

    try:
        print(f"🤖 Asistente ({mode}): Procesando pregunta...")

        resp = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.6,
                    "num_predict": 2048,
                    "top_k": 40,
                    "top_p": 0.9
                }
            },
            timeout=180
        )

        if resp.status_code == 200:
            result = resp.json()
            response = result.get("response", "").strip()

            if response:
                print(f"✅ Respuesta generada ({len(response)} caracteres)")
                return response
            else:
                return "⚠️ No pude generar una respuesta. Intenta reformular tu pregunta."
        else:
            return f"❌ Error al contactar con la IA (HTTP {resp.status_code})"

    except Exception as e:
        print(f"❌ Error generando respuesta: {e}")
        return f"❌ Error: {str(e)}"


def load_vosk_model():
    """Carga el modelo de Vosk una sola vez (prioriza modelo grande)"""
    global VOSK_MODEL

    if VOSK_MODEL is None:
        # Priorizar modelo grande (mejor precisión), fallback a pequeño
        model_paths = [
            ("vosk-model-es-0.42", "Grande (1.4GB) - Alta precisión"),
            ("vosk-model-small-es-0.42", "Pequeño (50MB) - Precisión básica")
        ]

        model_path = None
        model_name = None

        for path, name in model_paths:
            if os.path.exists(path):
                model_path = path
                model_name = name
                break

        if model_path is None:
            print("=" * 60)
            print("⚠️  MODELO DE VOSK NO ENCONTRADO")
            print("=" * 60)
            print("\n💡 Descarga uno de estos modelos:")
            print("\n   Recomendado (mejor precisión):")
            print("   → https://alphacephei.com/vosk/models/vosk-model-es-0.42.zip")
            print("   → Descomprime en la raíz del proyecto")
            print("\n   Alternativa (más rápido):")
            print("   → https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip")
            print("=" * 60)
            return None

        try:
            print("=" * 60)
            print(f"📂 Cargando modelo de Vosk...")
            print(f"   Modelo: {model_name}")
            print(f"   Ruta: {model_path}")
            print("   ⏳ Esto puede tardar unos segundos...")

            VOSK_MODEL = Model(model_path)

            print(f"✅ Modelo cargado exitosamente: {model_name}")
            print("=" * 60)

        except Exception as e:
            print(f"❌ Error cargando modelo de Vosk: {e}")
            print("💡 Verifica que la carpeta del modelo esté completa")
            return None

    return VOSK_MODEL


@app.route('/api/transcribe', methods=['POST'])
def transcribe_audio():
    """
    Transcribe audio usando Vosk con optimizaciones para mejor precisión
    """
    try:
        if 'audio' not in request.files:
            return jsonify({
                'success': False,
                'message': 'No se recibió archivo de audio'
            }), 400

        audio_file = request.files['audio']

        # Cargar modelo de Vosk
        model = load_vosk_model()
        if model is None:
            return jsonify({
                'success': False,
                'message': 'Modelo de Vosk no disponible. Descarga el modelo desde la documentación.'
            }), 500

        # Guardar audio temporalmente
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio:
            audio_file.save(temp_audio.name)
            temp_audio_path = temp_audio.name

        try:
            # Abrir archivo de audio
            wf = wave.open(temp_audio_path, "rb")

            sample_rate = wf.getframerate()

            print(f"🎤 Procesando audio:")
            print(f"   - Sample Rate: {sample_rate} Hz")
            print(f"   - Canales: {wf.getnchannels()}")
            print(f"   - Duración: {wf.getnframes() / sample_rate:.1f}s")

            # Crear reconocedor con configuración mejorada
            rec = KaldiRecognizer(model, sample_rate)
            rec.SetWords(True)  # Incluir info de palabras
            rec.SetPartialWords(True)  # Mejor reconocimiento parcial

            # Procesar audio en chunks
            transcription_parts = []
            chunk_size = 8000  # Chunks más grandes = mejor contexto

            print("   ⏳ Transcribiendo...")

            while True:
                data = wf.readframes(chunk_size)
                if len(data) == 0:
                    break

                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    text = result.get('text', '').strip()

                    if text:
                        # Capitalizar primera letra de cada frase
                        text = text[0].upper() + text[1:] if text else text
                        transcription_parts.append(text)
                        print(f"   📝 Fragmento: {text[:50]}...")

            # Procesar resultado final
            final_result = json.loads(rec.FinalResult())
            final_text = final_result.get('text', '').strip()

            if final_text:
                final_text = final_text[0].upper() + final_text[1:] if final_text else final_text
                transcription_parts.append(final_text)
                print(f"   📝 Final: {final_text[:50]}...")

            # Unir frases con puntuación
            if transcription_parts:
                full_transcription = '. '.join(transcription_parts)
                # Asegurar punto final
                if not full_transcription.endswith('.'):
                    full_transcription += '.'
            else:
                full_transcription = ''

            # Limpiar archivo temporal
            wf.close()
            os.unlink(temp_audio_path)

            if full_transcription:
                print(f"✅ Transcripción completada ({len(full_transcription)} caracteres)")
                return jsonify({
                    'success': True,
                    'transcription': full_transcription,
                    'method': 'vosk'
                })
            else:
                print("⚠️ No se detectó voz en el audio")
                return jsonify({
                    'success': True,
                    'transcription': '',
                    'message': 'No se detectó voz clara en la grabación'
                })

        except Exception as e:
            # Limpiar en caso de error
            if os.path.exists(temp_audio_path):
                os.unlink(temp_audio_path)
            raise e

    except Exception as e:
        print(f"❌ Error en transcripción: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': f'Error al transcribir: {str(e)}'
        }), 500


@app.route('/api/transcribe_google', methods=['POST'])
def transcribe_google():
    """
    Transcribe audio usando Google Speech API (online)
    Mejor precisión y vocabulario actualizado
    """
    try:
        if 'audio' not in request.files:
            return jsonify({
                'success': False,
                'message': 'No se recibió archivo de audio'
            }), 400

        audio_file = request.files['audio']

        print("🌐 Transcribiendo con Google Speech API...")

        # Guardar audio temporalmente
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio:
            audio_file.save(temp_audio.name)
            temp_audio_path = temp_audio.name

        try:
            # Usar SpeechRecognition
            recognizer = sr.Recognizer()

            # Ajustar para ruido ambiental (mejora precisión)
            recognizer.energy_threshold = 4000
            recognizer.dynamic_energy_threshold = True

            with sr.AudioFile(temp_audio_path) as source:
                # Ajustar según ruido ambiental
                recognizer.adjust_for_ambient_noise(source, duration=0.5)

                # Grabar audio
                audio_data = recognizer.record(source)

                print("   ⏳ Enviando a Google Cloud Speech...")

                # Transcribir con Google (español de España)
                text = recognizer.recognize_google(
                    audio_data,
                    language='es-ES',
                    show_all=False  # Solo mejor resultado
                )

                # Capitalizar primera letra
                text = text.strip()
                if text:
                    text = text[0].upper() + text[1:]
                    # Añadir punto final si no tiene
                    if not text.endswith(('.', '!', '?')):
                        text += '.'

                print(f"✅ Google transcripción: {text[:80]}...")

                return jsonify({
                    'success': True,
                    'transcription': text,
                    'method': 'google'
                })

        finally:
            # Limpiar archivo temporal
            if os.path.exists(temp_audio_path):
                os.unlink(temp_audio_path)

    except sr.UnknownValueError:
        print("⚠️ Google no pudo entender el audio")
        return jsonify({
            'success': True,
            'transcription': '',
            'message': 'No se detectó voz clara en la grabación'
        })

    except sr.RequestError as e:
        print(f"❌ Error de Google API: {e}")
        return jsonify({
            'success': False,
            'message': f'Error de conexión con Google: {str(e)}. Verifica tu conexión a internet.'
        }), 500

    except Exception as e:
        print(f"❌ Error en transcripción Google: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': f'Error al transcribir: {str(e)}'
        }), 500


@app.route('/api/export_entry_pdf/<project>/<filename>', methods=['GET'])
def export_entry_pdf(project, filename):
    """Exporta una entrada individual a PDF"""
    try:
        filepath = BASE_PATH / project / "entries" / filename

        if not filepath.exists():
            return jsonify({
                'success': False,
                'message': 'Entrada no encontrada'
            }), 404

        # Leer entrada
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parsear datos
        entry_data = parse_frontmatter(content)
        entry_data['content'] = content

        # Generar PDF
        pdf_gen = PDFGenerator()

        # Crear PDF temporal
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_pdf:
            pdf_path = temp_pdf.name

        pdf_gen.generate_single_entry_pdf(entry_data, pdf_path)

        # Nombre del archivo PDF
        pdf_filename = filename.replace('.md', '.pdf')

        # Enviar archivo
        from flask import send_file
        return send_file(
            pdf_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=pdf_filename
        )

    except Exception as e:
        print(f"❌ Error generando PDF: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': f'Error generando PDF: {str(e)}'
        }), 500


@app.route('/api/export_branch_pdf/<project>/<branch>', methods=['GET'])
def export_branch_pdf(project, branch):
    """Exporta todas las entradas de una rama a PDF"""
    try:
        project_path = BASE_PATH / project / "entries"

        if not project_path.exists():
            return jsonify({
                'success': False,
                'message': 'Proyecto no encontrado'
            }), 404

        # Buscar entradas de la rama
        entries = []

        for md_file in sorted(project_path.glob("*.md")):
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            entry_data = parse_frontmatter(content)

            # Filtrar por rama
            if entry_data.get('rama', '').lower() == branch.lower():
                entry_data['content'] = content
                entry_data['filename'] = md_file.name
                entries.append(entry_data)

        if not entries:
            return jsonify({
                'success': False,
                'message': f'No hay entradas para la rama "{branch}"'
            }), 404

        # Ordenar por fecha
        entries.sort(key=lambda x: x.get('fecha', ''))

        # Generar PDF
        pdf_gen = PDFGenerator()

        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_pdf:
            pdf_path = temp_pdf.name

        pdf_gen.generate_branch_pdf(entries, branch, project, pdf_path)

        # Nombre del archivo
        pdf_filename = f"{project}_{branch}_completo.pdf".replace('/', '-')

        from flask import send_file
        return send_file(
            pdf_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=pdf_filename
        )

    except Exception as e:
        print(f"❌ Error generando PDF de rama: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': f'Error generando PDF: {str(e)}'
        }), 500

if __name__ == '__main__':
    print("🚀 Iniciando Development Diary...")
    print("📂 Carpeta de diarios:", BASE_PATH.absolute())
    print("🌐 Abre tu navegador en: http://localhost:5000")
    print("⚠️  Presiona Ctrl+C para detener el servidor")
    app.run(debug=True, host='0.0.0.0', port=5000)