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

app = Flask(__name__)
CORS(app)

# Configuración
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.1:8b"
BASE_PATH = Path("Development Diary")
BASE_PATH.mkdir(exist_ok=True)


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

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')


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

        # Generar nombre de archivo
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{timestamp}.md"
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
                    "temperature": 0.5,  # Más creativo que antes
                    "num_predict": 1536,  # Más espacio para formato rico
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

@app.route('/api/shutdown', methods=['POST'])
def shutdown():
    """Detiene el servidor Flask"""
    print("🛑 Deteniendo servidor...")
    os.kill(os.getpid(), signal.SIGINT)
    return jsonify({'success': True, 'message': 'Servidor detenido'})

if __name__ == '__main__':
    print("🚀 Iniciando Development Diary...")
    print("📂 Carpeta de diarios:", BASE_PATH.absolute())
    print("🌐 Abre tu navegador en: http://localhost:5000")
    print("⚠️  Presiona Ctrl+C para detener el servidor")
    app.run(debug=True, host='0.0.0.0', port=5000)