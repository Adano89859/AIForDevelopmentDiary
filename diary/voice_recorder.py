"""
Grabador y transcriptor de voz usando Vosk
Reconocimiento de voz offline en español
"""

import queue
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer


class VoiceRecorder:
    def __init__(self, model_path="vosk-model-small-es-0.42"):
        """
        Inicializa el grabador de voz

        Args:
            model_path: Ruta al modelo de Vosk descargado
        """
        try:
            self.model = Model(model_path)
            self.recognizer = None
            self.audio_queue = queue.Queue()
            self.is_recording = False
            self.sample_rate = 16000
            print("✅ Vosk inicializado correctamente")
        except Exception as e:
            print(f"❌ Error inicializando Vosk: {e}")
            print("💡 Asegúrate de descargar el modelo de Vosk")
            self.model = None

    def audio_callback(self, indata, frames, time, status):
        """Callback que se ejecuta cuando hay audio disponible"""
        if status:
            print(f"⚠️ Estado del audio: {status}")
        self.audio_queue.put(bytes(indata))

    def start_recording(self):
        """Inicia la grabación de audio"""
        if not self.model:
            print("❌ Modelo Vosk no disponible")
            return False

        try:
            self.recognizer = KaldiRecognizer(self.model, self.sample_rate)
            self.is_recording = True

            # Iniciar stream de audio
            self.stream = sd.RawInputStream(
                samplerate=self.sample_rate,
                blocksize=8000,
                dtype='int16',
                channels=1,
                callback=self.audio_callback
            )
            self.stream.start()
            print("🎤 Grabación iniciada...")
            return True

        except Exception as e:
            print(f"❌ Error iniciando grabación: {e}")
            return False

    def stop_and_transcribe(self):
        """
        Detiene la grabación y devuelve la transcripción

        Returns:
            str: Texto transcrito
        """
        if not self.is_recording:
            return ""

        self.is_recording = False
        transcription_parts = []

        try:
            # Procesar todo el audio en la cola
            while not self.audio_queue.empty():
                data = self.audio_queue.get()

                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    text = result.get('text', '')
                    if text:
                        transcription_parts.append(text)

            # Procesar audio final
            final_result = json.loads(self.recognizer.FinalResult())
            final_text = final_result.get('text', '')
            if final_text:
                transcription_parts.append(final_text)

            # Detener stream
            self.stream.stop()
            self.stream.close()

            # Unir todas las partes
            full_transcription = ' '.join(transcription_parts).strip()

            if full_transcription:
                print(f"✅ Transcripción: {full_transcription[:50]}...")
                return full_transcription + "\n\n"
            else:
                print("⚠️ No se detectó voz")
                return ""

        except Exception as e:
            print(f"❌ Error en transcripción: {e}")
            return ""

    def is_available(self):
        """Verifica si el reconocimiento de voz está disponible"""
        return self.model is not None