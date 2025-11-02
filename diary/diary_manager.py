"""
Gestor del diario de desarrollo
Maneja la creación y guardado de entradas
"""

import os
import requests  # ← AÑADIR ESTE IMPORT
from datetime import datetime
from pathlib import Path
from diary.markdown_generator import MarkdownGenerator


class DiaryManager:
    def __init__(self):
        self.base_path = Path("Development Diary")
        self.base_path.mkdir(exist_ok=True)

        self.markdown_gen = MarkdownGenerator()

        # Configuración de Ollama
        self.ollama_url = "http://localhost:11434/api/generate"
        self.modelo = "llama3.1:8b"  # Tu modelo

    def save_entry(self, entry_data, use_ai=True):
        """
        Guarda una entrada del diario

        Args:
            entry_data: Dict con author, project, branch, commit_problem, notes
            use_ai: Si usar IA para mejorar el texto

        Returns:
            bool: True si se guardó correctamente
        """
        try:
            # Crear carpeta del proyecto
            project_name = entry_data['project'] or "Sin_Proyecto"
            project_path = self.base_path / project_name / "entries"
            project_path.mkdir(parents=True, exist_ok=True)

            # Procesar con IA si está activado
            if use_ai and entry_data['notes']:
                print("🤖 Mejorando texto con IA...")
                improved_notes = self.improve_with_ai(entry_data)
            else:
                improved_notes = entry_data['notes']

            # Generar nombre de archivo con timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{timestamp}.md"
            filepath = project_path / filename

            # Generar contenido markdown
            markdown_content = self.markdown_gen.generate(
                entry_data,
                improved_notes
            )

            # Guardar archivo
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(markdown_content)

            print(f"✅ Entrada guardada: {filepath}")
            return True

        except Exception as e:
            print(f"❌ Error guardando entrada: {e}")
            return False

    def improve_with_ai(self, entry_data):
        """
        Mejora las notas usando Ollama (llama3.1:8b)

        Args:
            entry_data: Diccionario con los datos de la entrada

        Returns:
            str: Texto mejorado por la IA
        """
        prompt = f"""Eres un asistente técnico que reformatea notas de desarrollo.

    CONTEXTO:
    - Proyecto: {entry_data['project']}
    - Rama: {entry_data['branch']}
    - Commit/Problema: {entry_data['commit_problem']}

    NOTAS DEL DESARROLLADOR:
    {entry_data['notes']}

    INSTRUCCIONES ESTRICTAS:
    1. Reformatea el texto usando Markdown (headers ##, listas -, código ```)
    2. Organiza en secciones solo SI la información lo permite
    3. NO inventes detalles técnicos (nombres de archivos, funciones, errores)
    4. NO añadas ejemplos de código que no estén en las notas
    5. NO asumas problemas o soluciones que no se mencionan
    6. Si las notas son breves, mantén el resumen breve
    7. Sé literal con la información dada

    Responde SOLO con el texto reformateado, sin introducciones.

    RESUMEN:"""

        try:
            print(f"🧠 Consultando a {self.modelo}...")

            resp = requests.post(
                self.ollama_url,
                json={
                    "model": self.modelo,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.3,  # ← REDUCIDO de 0.7 para ser más conservador
                        "num_predict": 1024,  # ← REDUCIDO de 2048 para respuestas más concisas
                        "top_k": 20,  # ← REDUCIDO de 40
                        "top_p": 0.8  # ← REDUCIDO de 0.9
                    }
                },
                timeout=120
            )

            if resp.status_code == 200:
                data = resp.json()
                respuesta = data.get("response", "").strip()

                if respuesta:
                    print(f"✅ Texto mejorado por IA ({len(respuesta)} caracteres)")
                    return respuesta
                else:
                    print("⚠️ IA devolvió respuesta vacía, usando texto original")
                    return entry_data['notes']
            else:
                print(f"❌ Error HTTP {resp.status_code}, usando texto original")
                return entry_data['notes']

        except requests.exceptions.ConnectionError:
            print("❌ No se pudo conectar a Ollama. ¿Está corriendo? (ollama serve)")
            print("📝 Guardando texto original sin procesar")
            return entry_data['notes']
        except requests.exceptions.Timeout:
            print("⏰ Timeout esperando respuesta de IA, usando texto original")
            return entry_data['notes']
        except Exception as e:
            print(f"❌ Error con IA: {e}")
            print("📝 Usando texto original")
            return entry_data['notes']