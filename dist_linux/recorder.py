import time
import logging
from pynput import mouse, keyboard

logger = logging.getLogger(__name__)

class ActionRecorder:
    """Classe responsável por monitorar de forma invisivel buffers de entrada."""
    def __init__(self):
        self.events = []
        self.start_time = None
        self.mouse_listener = None
        self.keyboard_listener = None
        self.running = False
        self.stop_callback = None
        self._last_mouse_pos = (0, 0)
        self._min_move_threshold = 2 # Filtro de ruido

    def start(self, on_stop=None):
        """Inicia a interceptacao de I/O em background."""
        if self.running:
            return
        
        self.events = []
        self.start_time = time.perf_counter()
        self.stop_callback = on_stop
        self.running = True

        self.mouse_listener = mouse.Listener(
            on_move=self._on_move,
            on_click=self._on_click,
            on_scroll=self._on_scroll)
        
        self.keyboard_listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release)

        self.mouse_listener.start()
        self.keyboard_listener.start()
        logger.info("Monitor de Interrupcao I/O ativo.")

    def stop(self):
        """Para o monitoramento passivo do usuario e salva o escopo."""
        if not self.running:
            return [], 0
            
        self.running = False
        
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        
        duration = time.perf_counter() - self.start_time
        logger.info(f"Monitor off. {len(self.events)} sinais I/O interceptados em {duration:.2f}s.")
        
        if self.stop_callback:
            try:
                self.stop_callback()
            except Exception as e:
                logger.error(f"Erro no hook de liberacao da thread: {e}")
        
        return self.events, duration

    def _get_time_delta(self):
        return time.perf_counter() - self.start_time

    def _on_move(self, x, y):
        if not self.running: return
        
        # Filtro de otimização: Evita gravar movimentos insignificantes (jitter)
        # Isso reduz o tamanho do arquivo JSON consideravelmente.
        dx = abs(x - self._last_mouse_pos[0])
        dy = abs(y - self._last_mouse_pos[1])
        
        if dx > self._min_move_threshold or dy > self._min_move_threshold:
            self.events.append({
                "type": "move",
                "x": x,
                "y": y,
                "time": self._get_time_delta()
            })
            self._last_mouse_pos = (x, y)

    def _on_click(self, x, y, button, pressed):
        if not self.running: return
        self.events.append({
            "type": "click",
            "x": x,
            "y": y,
            "button": str(button),
            "pressed": pressed,
            "time": self._get_time_delta()
        })
        # Força atualização da última posição no clique
        self._last_mouse_pos = (x, y)

    def _on_scroll(self, x, y, dx, dy):
        if not self.running: return
        self.events.append({
            "type": "scroll",
            "x": x,
            "y": y,
            "dx": dx,
            "dy": dy,
            "time": self._get_time_delta()
        })

    def _on_press(self, key):
        if not self.running: return
        try:
            k = key.char
        except AttributeError:
            k = str(key)
        
        self.events.append({
            "type": "press",
            "key": k,
            "time": self._get_time_delta()
        })

    def _on_release(self, key):
        if not self.running: return
        try:
            k = key.char
        except AttributeError:
            k = str(key)
            
        self.events.append({
            "type": "release",
            "key": k,
            "time": self._get_time_delta()
        })
