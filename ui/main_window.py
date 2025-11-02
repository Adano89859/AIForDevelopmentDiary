"""
Ventana principal de Development Diary
Implementación en Tkinter del diseño moderno
"""

import tkinter as tk
from tkinter import scrolledtext
from ui.styles import AppStyles
from diary.diary_manager import DiaryManager
from diary.voice_recorder import VoiceRecorder


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Development Diary")
        self.root.geometry("950x750")
        self.root.configure(bg=AppStyles.BG_DARK)

        # Managers
        self.diary_manager = DiaryManager()
        self.voice_recorder = VoiceRecorder()

        # Estado
        self.is_recording = False
        self.ai_enabled = tk.BooleanVar(value=True)

        # Variables de formulario
        self.author_var = tk.StringVar()
        self.project_var = tk.StringVar()
        self.branch_var = tk.StringVar()
        self.commit_var = tk.StringVar()

        self.setup_ui()

    def setup_ui(self):
        """Configura toda la interfaz"""
        # Frame principal con padding
        main_frame = tk.Frame(self.root, bg=AppStyles.BG_DARK)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        # Header
        self.create_header(main_frame)

        # Card principal (simulando glassmorphism)
        card_frame = tk.Frame(
            main_frame,
            bg=AppStyles.BG_GLASS,
            highlightbackground=AppStyles.BORDER_GLASS,
            highlightthickness=2
        )
        card_frame.pack(fill=tk.BOTH, expand=True, pady=20)

        # Contenido del card
        content_frame = tk.Frame(card_frame, bg=AppStyles.BG_GLASS)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Primera fila: Autor y Proyecto
        self.create_input_row(
            content_frame,
            [("👤 Autor", self.author_var, "Tu nombre"),
             ("📁 Proyecto", self.project_var, "Nombre del proyecto")]
        )

        # Segunda fila: Rama y Commit
        self.create_input_row(
            content_frame,
            [("🌿 Rama", self.branch_var, "feature/nueva-funcionalidad"),
             ("💡 Commit/Problema", self.commit_var, "Fix: Error en validación")]
        )

        # Área de notas
        self.create_notes_area(content_frame)

        # Barra de acciones
        self.create_action_bar(content_frame)

        # Mensaje de éxito (oculto inicialmente)
        self.success_frame = tk.Frame(content_frame, bg=AppStyles.BG_GLASS)
        self.success_label = tk.Label(
            self.success_frame,
            text="🎉 Tu progreso ha sido documentado. ¡Cada paso cuenta!",
            font=AppStyles.FONT_LABEL,
            fg="#86efac",  # green-300
            bg="#166534",  # green-900
            pady=12,
            padx=20
        )
        self.success_label.pack(fill=tk.X)

        # Footer motivacional
        self.create_footer(main_frame)

    def create_header(self, parent):
        """Crea el header con título"""
        header_frame = tk.Frame(parent, bg=AppStyles.BG_DARK)
        header_frame.pack(pady=(0, 10))

        # Icono + Título
        title_container = tk.Frame(header_frame, bg=AppStyles.BG_DARK)
        title_container.pack()

        icon_label = tk.Label(
            title_container,
            text="📝",
            font=("Segoe UI", 32),
            bg=AppStyles.BG_DARK
        )
        icon_label.pack(side=tk.LEFT, padx=(0, 10))

        title = tk.Label(
            title_container,
            text="Development Diary",
            font=AppStyles.FONT_TITLE,
            fg=AppStyles.TEXT_WHITE,
            bg=AppStyles.BG_DARK
        )
        title.pack(side=tk.LEFT)

        subtitle = tk.Label(
            header_frame,
            text="Cada línea de código merece ser recordada ✨",
            font=AppStyles.FONT_SUBTITLE,
            fg=AppStyles.TEXT_PURPLE_200,
            bg=AppStyles.BG_DARK
        )
        subtitle.pack(pady=(5, 0))

    def create_input_row(self, parent, fields):
        """Crea una fila con inputs mejorados"""
        row_frame = tk.Frame(parent, bg=AppStyles.BG_GLASS)
        row_frame.pack(fill=tk.X, pady=8)

        for label_text, var, placeholder in fields:
            field_frame = tk.Frame(row_frame, bg=AppStyles.BG_GLASS)
            field_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=6)

            label = tk.Label(
                field_frame,
                text=label_text,
                font=AppStyles.FONT_LABEL,
                fg=AppStyles.TEXT_PURPLE_200,
                bg=AppStyles.BG_GLASS,
                anchor=tk.W
            )
            label.pack(anchor=tk.W, pady=(0, 5))

            # Frame para el input con borde
            entry_container = tk.Frame(
                field_frame,
                bg=AppStyles.BG_DARK,
                highlightbackground=AppStyles.BORDER_GLASS,
                highlightthickness=1
            )
            entry_container.pack(fill=tk.X)

            entry = tk.Entry(
                entry_container,
                textvariable=var,
                font=AppStyles.FONT_INPUT,
                bg=AppStyles.BG_DARK,
                fg=AppStyles.TEXT_WHITE,
                insertbackground=AppStyles.PURPLE_400,
                relief=tk.FLAT,
                bd=0
            )
            entry.pack(fill=tk.X, padx=12, pady=10)

            # Placeholder simulation
            if not var.get():
                entry.insert(0, placeholder)
                entry.config(fg=AppStyles.TEXT_PURPLE_300)

            def on_focus_in(e, ent=entry, ph=placeholder, container=entry_container, v=var):
                if ent.get() == ph:
                    ent.delete(0, tk.END)
                    ent.config(fg=AppStyles.TEXT_WHITE)
                container.config(highlightbackground=AppStyles.PURPLE_500, highlightthickness=2)

            def on_focus_out(e, ent=entry, ph=placeholder, container=entry_container, v=var):
                if not ent.get():
                    ent.insert(0, ph)
                    ent.config(fg=AppStyles.TEXT_PURPLE_300)
                container.config(highlightbackground=AppStyles.BORDER_GLASS, highlightthickness=1)

            def on_change(e, ent=entry, ph=placeholder):
                if ent.get() != ph:
                    ent.config(fg=AppStyles.TEXT_WHITE)

            entry.bind("<FocusIn>", on_focus_in)
            entry.bind("<FocusOut>", on_focus_out)
            entry.bind("<KeyRelease>", on_change)

    def create_notes_area(self, parent):
        """Crea el área de notas con botón de grabación"""
        notes_frame = tk.Frame(parent, bg=AppStyles.BG_GLASS)
        notes_frame.pack(fill=tk.BOTH, expand=True, pady=12)

        # Header del área de notas
        notes_header = tk.Frame(notes_frame, bg=AppStyles.BG_GLASS)
        notes_header.pack(fill=tk.X, pady=(0, 8))

        notes_label = tk.Label(
            notes_header,
            text="📅 Notas de desarrollo",
            font=AppStyles.FONT_LABEL,
            fg=AppStyles.TEXT_PURPLE_200,
            bg=AppStyles.BG_GLASS
        )
        notes_label.pack(side=tk.LEFT)

        # Botón de grabar mejorado
        self.record_button = tk.Button(
            notes_header,
            text="🎤 Grabar",
            font=AppStyles.FONT_BUTTON,
            bg=AppStyles.BG_DARK,
            fg=AppStyles.TEXT_PURPLE_200,
            relief=tk.FLAT,
            cursor="hand2",
            command=self.toggle_recording,
            padx=15,
            pady=6,
            activebackground="#1e293b",
            activeforeground=AppStyles.TEXT_PURPLE_200
        )
        self.record_button.pack(side=tk.RIGHT)

        # Efecto hover en botón grabar
        def on_enter_record(e):
            if not self.is_recording:
                self.record_button.config(bg="#1e293b")

        def on_leave_record(e):
            if not self.is_recording:
                self.record_button.config(bg=AppStyles.BG_DARK)

        self.record_button.bind("<Enter>", on_enter_record)
        self.record_button.bind("<Leave>", on_leave_record)

        # Container para el área de texto
        text_container = tk.Frame(
            notes_frame,
            bg=AppStyles.BG_DARK,
            highlightbackground=AppStyles.BORDER_GLASS,
            highlightthickness=1
        )
        text_container.pack(fill=tk.BOTH, expand=True)

        # Área de texto
        self.notes_text = scrolledtext.ScrolledText(
            text_container,
            font=AppStyles.FONT_INPUT,
            bg=AppStyles.BG_DARK,
            fg=AppStyles.TEXT_WHITE,
            insertbackground=AppStyles.PURPLE_400,
            relief=tk.FLAT,
            wrap=tk.WORD,
            padx=12,
            pady=10,
            bd=0
        )
        self.notes_text.pack(fill=tk.BOTH, expand=True)

        # Placeholder
        placeholder_text = "Describe lo que has hecho hoy... La IA lo convertirá en un resumen profesional ✨"
        self.notes_text.insert("1.0", placeholder_text)
        self.notes_text.config(fg=AppStyles.TEXT_PURPLE_300)

        def on_focus_in_text(e):
            if self.notes_text.get("1.0", tk.END).strip() == placeholder_text:
                self.notes_text.delete("1.0", tk.END)
                self.notes_text.config(fg=AppStyles.TEXT_WHITE)
            text_container.config(highlightbackground=AppStyles.PURPLE_500, highlightthickness=2)

        def on_focus_out_text(e):
            if not self.notes_text.get("1.0", tk.END).strip():
                self.notes_text.insert("1.0", placeholder_text)
                self.notes_text.config(fg=AppStyles.TEXT_PURPLE_300)
            text_container.config(highlightbackground=AppStyles.BORDER_GLASS, highlightthickness=1)

        self.notes_text.bind("<FocusIn>", on_focus_in_text)
        self.notes_text.bind("<FocusOut>", on_focus_out_text)

    def create_action_bar(self, parent):
        """Crea la barra de acciones con toggle IA y botón guardar"""
        action_frame = tk.Frame(parent, bg=AppStyles.BG_GLASS)
        action_frame.pack(fill=tk.X, pady=15)

        # Línea separadora
        separator = tk.Frame(parent, bg=AppStyles.BORDER_GLASS, height=1)
        separator.pack(fill=tk.X, pady=(0, 15))

        # Toggle IA (izquierda)
        ai_frame = tk.Frame(action_frame, bg=AppStyles.BG_GLASS)
        ai_frame.pack(side=tk.LEFT)

        ai_check = tk.Checkbutton(
            ai_frame,
            text="✨ Mejorar con IA",
            variable=self.ai_enabled,
            font=AppStyles.FONT_LABEL,
            fg=AppStyles.TEXT_PURPLE_200,
            bg=AppStyles.BG_GLASS,
            selectcolor=AppStyles.BG_DARK,
            activebackground=AppStyles.BG_GLASS,
            activeforeground=AppStyles.TEXT_PURPLE_200,
            cursor="hand2",
            highlightthickness=0
        )
        ai_check.pack()

        # Botón guardar mejorado (derecha)
        self.save_button = tk.Button(
            action_frame,
            text="💾 Guardar Entrada",
            font=AppStyles.FONT_BUTTON,
            bg=AppStyles.PURPLE_500,
            fg=AppStyles.TEXT_WHITE,
            relief=tk.FLAT,
            cursor="hand2",
            command=self.save_entry,
            padx=25,
            pady=12,
            activebackground=AppStyles.PURPLE_400,
            activeforeground=AppStyles.TEXT_WHITE
        )
        self.save_button.pack(side=tk.RIGHT)

        # Efecto hover
        def on_enter(e):
            self.save_button.config(bg=AppStyles.PURPLE_400)

        def on_leave(e):
            self.save_button.config(bg=AppStyles.PURPLE_500)

        self.save_button.bind("<Enter>", on_enter)
        self.save_button.bind("<Leave>", on_leave)

    def create_footer(self, parent):
        """Crea el footer motivacional"""
        footer = tk.Label(
            parent,
            text="💡 Documentar no es perder tiempo, es invertir en tu futuro yo",
            font=("Segoe UI", 11),
            fg=AppStyles.TEXT_PURPLE_300,
            bg=AppStyles.BG_DARK
        )
        footer.pack(pady=10)

    def toggle_recording(self):
        """Activa/desactiva la grabación de voz"""
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        """Inicia la grabación"""
        if not self.voice_recorder.is_available():
            print("⚠️ Reconocimiento de voz no disponible")
            return

        success = self.voice_recorder.start_recording()
        if success:
            self.is_recording = True
            self.record_button.config(
                text="🔴 Grabando...",
                bg=AppStyles.RED_500,
                fg=AppStyles.TEXT_WHITE
            )

    def stop_recording(self):
        """Detiene la grabación y transcribe"""
        self.is_recording = False
        self.record_button.config(
            text="🎤 Grabar",
            bg=AppStyles.BG_DARK,
            fg=AppStyles.TEXT_PURPLE_200
        )

        # Obtener transcripción
        transcription = self.voice_recorder.stop_and_transcribe()

        # Añadir al área de notas
        placeholder = "Describe lo que has hecho hoy... La IA lo convertirá en un resumen profesional ✨"
        current_text = self.notes_text.get("1.0", tk.END).strip()

        if current_text == placeholder or not current_text:
            self.notes_text.delete("1.0", tk.END)
            self.notes_text.insert("1.0", transcription)
        else:
            self.notes_text.insert(tk.END, "\n" + transcription)

        self.notes_text.config(fg=AppStyles.TEXT_WHITE)

    def save_entry(self):
        """Guarda la entrada del diario"""
        # Obtener valores (ignorando placeholders)
        author = self.author_var.get()
        if author == "Tu nombre":
            author = ""

        project = self.project_var.get()
        if project == "Nombre del proyecto":
            project = ""

        branch = self.branch_var.get()
        if branch == "feature/nueva-funcionalidad":
            branch = ""

        commit = self.commit_var.get()
        if commit == "Fix: Error en validación":
            commit = ""

        notes = self.notes_text.get("1.0", tk.END).strip()
        if notes == "Describe lo que has hecho hoy... La IA lo convertirá en un resumen profesional ✨":
            notes = ""

        entry_data = {
            'author': author,
            'project': project,
            'branch': branch,
            'commit_problem': commit,
            'notes': notes
        }

        # Validar que al menos tenga notas
        if not notes:
            print("⚠️ No hay contenido para guardar")
            return

        # Guardar con o sin IA
        use_ai = self.ai_enabled.get()
        success = self.diary_manager.save_entry(entry_data, use_ai)

        if success:
            self.show_success_message()
            self.clear_form()

    def show_success_message(self):
        """Muestra mensaje de éxito"""
        # Mostrar frame de éxito
        self.success_frame.pack(fill=tk.X, pady=(10, 0))

        # Cambiar color del botón temporalmente
        self.save_button.config(
            text="✅ ¡Guardado!",
            bg=AppStyles.GREEN_500
        )

        # Restaurar después de 2 segundos
        self.root.after(2000, self.hide_success_message)

    def hide_success_message(self):
        """Oculta el mensaje de éxito"""
        self.success_frame.pack_forget()
        self.save_button.config(
            text="💾 Guardar Entrada",
            bg=AppStyles.PURPLE_500
        )

    def clear_form(self):
        """Limpia el formulario después de guardar"""
        # Limpiar notas y commit
        placeholder = "Describe lo que has hecho hoy... La IA lo convertirá en un resumen profesional ✨"
        self.notes_text.delete("1.0", tk.END)
        self.notes_text.insert("1.0", placeholder)
        self.notes_text.config(fg=AppStyles.TEXT_PURPLE_300)

        self.commit_var.set("Fix: Error en validación")

        # Mantener autor, proyecto y rama para siguientes entradas