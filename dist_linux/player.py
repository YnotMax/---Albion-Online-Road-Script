import time
import threading
import random
import logging
from pynput import mouse, keyboard

logger = logging.getLogger(__name__)

class ActionPlayer:
    """Classe responsável por injetar eventos no Kernel."""
    def __init__(self):
        self.mouse_controller = mouse.Controller()
        self.keyboard_controller = keyboard.Controller()
        self.running = False
        self.thread = None

    def play(self, events, on_finish=None, repeat=False):
        """Inicia injeção em uma thread separada."""
        if self.running:
            logger.warning("Canal de I/O ocupado.")
            return
            
        self.running = True
        self.thread = threading.Thread(target=self._play_thread, args=(events, on_finish, repeat))
        self.thread.daemon = True
        self.thread.start()
        logger.info(f"Sinal de saida ativado (Ciclo={repeat}).")

    def stop(self):
        """Solicita a interrupcao via software."""
        self.running = False
        logger.info("Interrupcao (kill) enviada ao barramento.")

    def _play_thread(self, events, on_finish, repeat):
        if not events:
            logger.warning("Buffer vazio descartado.")
            self.running = False
            if on_finish: on_finish()
            return

        sorted_events = sorted(events, key=lambda e: e['time'])
        
        while self.running:
            start_time = time.perf_counter()
            
            try:
                for event in sorted_events:
                    if not self.running:
                        break
                    
                    target_time = start_time + event['time']
                    
                    while True:
                        now = time.perf_counter()
                        remaining = target_time - now
                        
                        if remaining <= 0:
                            break
                        
                        if remaining > 0.02:
                            if remaining > 0.1:
                                if not self.running: break
                                time.sleep(0.05)
                            else:
                                time.sleep(0.01)
                        else:
                            pass
                    
                    if self.running:
                        self._execute_event(event)

            except Exception as e:
                logger.error(f"Kernel Panic simulado ou falha de injecao: {e}")
                break
            
            if not repeat or not self.running:
                break
                
            time.sleep(0.5)

        self.running = False
        logger.info("Envio de pacotes finalizado.")
        if on_finish:
            try:
                on_finish()
            except Exception as e:
                logger.error(f"Erro no fechamento da porta logica: {e}")

    def _execute_event(self, event):
        try:
            etype = event['type']
            
            if etype == 'move':
                self.mouse_controller.position = (event['x'], event['y'])
                
            elif etype == 'click':
                btn = self._get_mouse_button(event['button'])
                self.mouse_controller.position = (event['x'], event['y'])
                if event['pressed']:
                    self.mouse_controller.press(btn)
                else:
                    self.mouse_controller.release(btn)
                    
            elif etype == 'scroll':
                self.mouse_controller.position = (event['x'], event['y'])
                self.mouse_controller.scroll(event['dx'], event['dy'])
                
            elif etype == 'press':
                key = self._get_key(event['key'])
                self.keyboard_controller.press(key)
                
            elif etype == 'release':
                key = self._get_key(event['key'])
                self.keyboard_controller.release(key)
        except Exception as e:
            logger.debug(f"Falha ao executar evento {event.get('type')}: {e}")

    def _get_mouse_button(self, btn_str):
        if 'Button.left' in btn_str: return mouse.Button.left
        if 'Button.right' in btn_str: return mouse.Button.right
        if 'Button.middle' in btn_str: return mouse.Button.middle
        return mouse.Button.left

    def _get_key(self, key_str):
        if key_str.startswith('Key.'):
            attr = key_str.split('.')[1]
            # Algumas teclas especiais podem ter nomes diferentes ou faltar no enum
            return getattr(keyboard.Key, attr, keyboard.Key.esc)
        return key_str
