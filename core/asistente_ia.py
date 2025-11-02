"""
Versión simplificada del asistente para el diario
"""

import requests


class AsistenteIA:
    def __init__(self):
        self.ollama_url = "http://localhost:11434/api/generate"
        self.modelo = "llama3.1:8b"

    def generar_respuesta_ollama(self, prompt):
        """
        Genera respuesta usando Ollama

        Args:
            prompt: Texto del prompt

        Returns:
            str: Respuesta de la IA
        """
        try:
            resp = requests.post(
                self.ollama_url,
                json={
                    "model": self.modelo,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "num_predict": 2048
                    }
                },
                timeout=120
            )

            if resp.status_code == 200:
                data = resp.json()
                return data.get("response", "").strip()
            else:
                return f"Error HTTP {resp.status_code}"

        except Exception as e:
            print(f"❌ Error con IA: {e}")
            return ""  # Devolver vacío si falla