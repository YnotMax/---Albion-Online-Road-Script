import customtkinter as ctk
import time
import logging
import sys
from pynput import keyboard
from recorder import ActionRecorder
from player import ActionPlayer
import storage_manager

# Inicializar Logging
logger = logging.getLogger(__name__)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gerenciador de Perifericos HD")
        self.geometry("1000x700")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Temas
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # Componentes
        self.recorder = ActionRecorder()
        self.player = ActionPlayer()
        self.is_recording = False
        self.is_playing = False
        self.selected_rec = None

        # Layout Principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._setup_sidebar()
        self._setup_main_tabs()
        self._setup_hotkeys()
        
        self.load_recordings_list()
        self.after(500, self._show_welcome_msg)

    def _setup_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(3, weight=1)

        ctk.CTkLabel(self.sidebar, text="🔊 AUDIO & PERIFERICOS", 
                     font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, padx=20, pady=(30, 10))
        
        ctk.CTkLabel(self.sidebar, text="Driver Utility v10.0", text_color="cyan",
                     font=ctk.CTkFont(size=11)).grid(row=1, column=0, padx=20, pady=(0, 20))

        self.refresh_btn = ctk.CTkButton(self.sidebar, text="🔄 Atualizar Biblioteca", 
                                         command=self.load_recordings_list, height=35)
        self.refresh_btn.grid(row=2, column=0, padx=20, pady=10)
        
        self.scroll_list = ctk.CTkScrollableFrame(self.sidebar, label_text="Meus Perfis")
        self.scroll_list.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")

        self.delete_btn = ctk.CTkButton(self.sidebar, text="🗑️ Remover Perfil", 
                                        fg_color="#6B0000", hover_color="#990000",
                                        state="disabled", command=self.confirm_delete)
        self.delete_btn.grid(row=4, column=0, padx=20, pady=20)

    def _setup_main_tabs(self):
        self.tabview = ctk.CTkTabview(self, corner_radius=15)
        self.tabview.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        self.tab_main = self.tabview.add("🎮 Painel de Controle")
        self.tab_guide = self.tabview.add("📖 Informacoes do Driver")
        
        self._setup_control_panel()
        self._setup_interactive_guide()

    def _setup_control_panel(self):
        # Stepper Visual
        self.stepper_frame = ctk.CTkFrame(self.tab_main, fg_color="transparent")
        self.stepper_frame.pack(fill="x", padx=20, pady=20)
        
        self.steps = []
        step_texts = ["1. MAPEAR (F9)", "2. APLICAR", "3. EXECUTAR (F8)"]
        for i, text in enumerate(step_texts):
            lbl = ctk.CTkLabel(self.stepper_frame, text=text, 
                               font=ctk.CTkFont(size=14, weight="bold"),
                               text_color="gray")
            lbl.pack(side="left", expand=True)
            self.steps.append(lbl)
        
        # Área de Status Central
        self.status_container = ctk.CTkFrame(self.tab_main, height=150, corner_radius=15, border_width=2, border_color="#333")
        self.status_container.pack(fill="x", padx=40, pady=10)
        self.status_container.pack_propagate(False)

        self.status_label = ctk.CTkLabel(self.status_container, text="Aguardando Ação", 
                                         font=ctk.CTkFont(size=28, weight="bold"))
        self.status_label.place(relx=0.5, rely=0.4, anchor="center")
        
        self.hint_label = ctk.CTkLabel(self.status_container, text="Dica: Comece mapeando um novo perfil de uso", 
                                       text_color="gray", font=ctk.CTkFont(size=14))
        self.hint_label.place(relx=0.5, rely=0.7, anchor="center")

        # Configurações Rápidas
        self.config_frame = ctk.CTkFrame(self.tab_main, fg_color="transparent")
        self.config_frame.pack(pady=20)
        
        self.loop_var = ctk.BooleanVar(value=False)
        self.loop_switch = ctk.CTkSwitch(self.config_frame, text="Repeticao Infinita (Loop)", variable=self.loop_var)
        self.loop_switch.pack(side="left", padx=20)

        # Botões Principais com Atalhos Explicitados
        self.btn_frame = ctk.CTkFrame(self.tab_main, fg_color="transparent")
        self.btn_frame.pack(fill="x", padx=40, pady=20)
        self.btn_frame.grid_columnconfigure((0, 1), weight=1)

        self.btn_record = ctk.CTkButton(self.btn_frame, text="⏺ NOVO MAPEAMENTO\n[Atalho: F9]", 
                                        command=self.start_record_flow, height=100,
                                        fg_color="#1B5E20", hover_color="#2E7D32",
                                        font=ctk.CTkFont(size=16, weight="bold"))
        self.btn_record.grid(row=0, column=0, padx=10, sticky="ew")
        
        self.btn_play = ctk.CTkButton(self.btn_frame, text="▶ EXECUTAR\n[Atalho: F8]", 
                                      command=self.toggle_play, height=100,
                                      state="disabled", font=ctk.CTkFont(size=16, weight="bold"))
        self.btn_play.grid(row=0, column=1, padx=10, sticky="ew")

        # Atalho de Emergência
        self.btn_stop = ctk.CTkButton(self.tab_main, text="⏹ RESETAR CONTROLADOR (TECLA F10)", 
                                      command=self.stop_all, height=60,
                                      fg_color="#4D0000", border_width=2,
                                      border_color="#FF4C4C", text_color="#FF4C4C",
                                      hover_color="#7A0000")
        self.btn_stop.pack(fill="x", padx=50, pady=(20, 0))

    def _setup_interactive_guide(self):
        guide_container = ctk.CTkScrollableFrame(self.tab_guide, fg_color="transparent")
        guide_container.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(guide_container, text="🛡️ Configuracoes de Sistema", 
                     font=ctk.CTkFont(size=22, weight="bold"), text_color="cyan").pack(pady=(0, 20))

        # Avisos de Segurança
        ctk.CTkLabel(guide_container, text="Utilidade desenhada para otimizar perifericos removendo latencias de processamento visual.", 
                     wraplength=650, text_color="orange", justify="left").pack(pady=10)

        cards = [
            ("⌨️ Atalhos Principais", "F9: Iniciar/Parar Mapeamento\nF8: Executar Perfil de I/O\nF10: Reset Físico (Para tudo na hora)"),
            ("🎬 Configurar Perfil", "Aperte F9. O sistema contará 3 segundos para sincronizar o buffer. Ao finalizar pressone F9 novamente."),
            ("🕵️ Interpolacao Dinamica", "O controlador injeta micro-variacoes no tempo de resposta para calibragem natural do mouse/teclado."),
            ("🎮 Otimizacao de Resposta", "Reduz a latencia de input limitando sobrecarga do barramento USB.")
        ]

        for title, desc in cards:
            card = ctk.CTkFrame(guide_container, corner_radius=10, border_width=1, border_color="#333")
            card.pack(fill="x", pady=10, padx=5)
            ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=16, weight="bold"), text_color="cyan").pack(padx=15, pady=(10, 5), anchor="w")
            ctk.CTkLabel(card, text=desc, wraplength=600, justify="left").pack(padx=15, pady=(0, 15), anchor="w")

    def _update_stepper(self, step_idx):
        for i, lbl in enumerate(self.steps):
            if i == step_idx:
                lbl.configure(text_color="orange", font=ctk.CTkFont(size=16, weight="bold"))
            else:
                lbl.configure(text_color="gray", font=ctk.CTkFont(size=14, weight="bold"))

    def _show_welcome_msg(self):
        self.status_label.configure(text="Sincronizacao Ativa", text_color="cyan")
        self.after(2000, lambda: self._update_stepper(0))

    def load_recordings_list(self):
        for widget in self.scroll_list.winfo_children():
            widget.destroy()
        
        recs = storage_manager.list_recordings()
        for rec in recs:
            btn = ctk.CTkButton(self.scroll_list, 
                                text=f"• {rec['name']} ({rec['duration']:.1f}s)", 
                                fg_color="transparent", anchor="w",
                                hover_color="#222",
                                command=lambda r=rec: self.select_recording(r))
            btn.pack(fill="x", pady=2)
        
        if not recs:
            ctk.CTkLabel(self.scroll_list, text="Nenhum perfil de I/O listado.", text_color="gray").pack(pady=20)

    def _play_beep(self, msg_type):
        """Emite feedbacks sonoros para ações sem precisar olhar para o app."""
        import winsound
        try:
            if msg_type == "start":
                winsound.Beep(700, 150)
                winsound.Beep(1000, 200)
            elif msg_type == "stop":
                winsound.Beep(1000, 150)
                winsound.Beep(700, 200)
            elif msg_type == "count":
                winsound.Beep(800, 100)
            elif msg_type == "error":
                winsound.Beep(400, 500)
        except Exception as e:
            logger.debug(f"Erro ao emitir bipe: {e}")

    def select_recording(self, rec):
        self.selected_rec = rec
        self.hint_label.configure(text=f"Pronto para carregar buffers de: '{rec['name']}'", text_color="#E0E0E0")
        self.btn_play.configure(state="normal")
        self.delete_btn.configure(state="normal")
        self._update_stepper(2)
        self._play_beep("count")

    def start_record_flow(self):
        if self.is_recording:
            self.stop_all()
            return
        self._countdown(3)

    def _countdown(self, seconds):
        if seconds > 0:
            self.status_label.configure(text=f"Liberando I/O em: {seconds}", text_color="orange")
            self.hint_label.configure(text="Sincronizacao de interrupcao iniciando!")
            self._play_beep("count")
            self.after(1000, lambda: self._countdown(seconds - 1))
        else:
            self._start_recording()

    def _start_recording(self):
        self.is_recording = True
        self.status_label.configure(text="🔴 MAPEAMENTO ATIVO", text_color="red")
        self.hint_label.configure(text="Sinais interceptados. F10 finaliza.")
        self.btn_record.configure(text="⏹ CANCELAR MAPEAMENTO\n[F9 ou F10]", fg_color="#8B0000")
        self._update_stepper(1)
        self._play_beep("start")
        self.recorder.start()

    def toggle_play(self):
        if self.is_playing:
            self.stop_all()
        else:
            self.start_playing()

    def start_playing(self):
        if not self.selected_rec: 
            self._play_beep("error")
            return
        data = storage_manager.load_recording(self.selected_rec['path'])
        if not data: 
            self._play_beep("error")
            return
            
        self.is_playing = True
        self.status_label.configure(text="🟢 ENVIANDO PACOTES (EXEC)", text_color="green")
        self.hint_label.configure(text="Canal I/O bloqueado. F10 para abortar rotina.")
        self.btn_play.configure(text="⏹ PARAR ROTINA\n[F8 ou F10]", fg_color="#8B0000")
        
        self._play_beep("start")
        events = data.get('events', [])
        loop = self.loop_var.get()
        self.player.play(events, on_finish=self._on_play_done, repeat=loop)

    def _on_play_done(self):
        self._play_beep("stop")
        self.after(0, self._reset_ui)

    def stop_all(self):
        stopped_something = False
        if self.is_recording:
            events, duration = self.recorder.stop()
            self.is_recording = False
            self._save_flow(events, duration)
            stopped_something = True
        
        if self.is_playing:
            self.player.stop()
            self.is_playing = False
            stopped_something = True
        
        if stopped_something:
            self._play_beep("stop")
        self._reset_ui()

    def _save_flow(self, events, duration):
        if not events or len(events) < 5:
            self.status_label.configure(text="Buffer descartado", text_color="white")
            return

        dialog = ctk.CTkInputDialog(text="Identificacao do Perfil de Entrada:", title="Salvar Buffer")
        name = dialog.get_input()
        if name:
            storage_manager.save_recording(name, events, duration)
            self.load_recordings_list()
            self.status_label.configure(text="Perfil de I/O Salvo!", text_color="green")
            self._update_stepper(2)

    def _reset_ui(self):
        self.status_label.configure(text="Sincronizacao Ativa", text_color="white")
        self.hint_label.configure(text="Aguardando evento I/O (F8/F9)")
        self.btn_record.configure(text="⏺ NOVO MAPEAMENTO\n[Atalho: F9]", fg_color="#1B5E20")
        self.btn_play.configure(text="▶ EXECUTAR\n[Atalho: F8]")
        if self.selected_rec:
            self.btn_play.configure(state="normal")
            self._update_stepper(2)
        else:
            self._update_stepper(0)

    def confirm_delete(self):
        if not self.selected_rec: return
        dialog = ctk.CTkInputDialog(text=f"Excluir '{self.selected_rec['name']}'?\nDigite 'SIM':", title="Remover")
        if dialog.get_input() == "SIM":
            storage_manager.delete_recording(self.selected_rec['path'])
            self.selected_rec = None
            self.load_recordings_list()
            self._reset_ui()

    def _setup_hotkeys(self):
        self.hotkey_listener = keyboard.GlobalHotKeys({
            '<f10>': lambda: self.after(0, self.stop_all),
            '<f9>': lambda: self.after(0, self.start_record_flow),
            '<f8>': lambda: self.after(0, self.toggle_play)
        })
        self.hotkey_listener.start()

    def on_closing(self):
        self.stop_all()
        if hasattr(self, 'hotkey_listener'): self.hotkey_listener.stop()
        self.destroy()
        sys.exit(0)

if __name__ == "__main__":
    app = App()
    app.mainloop()
