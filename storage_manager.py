import json
import os
import time
import logging

# Configuração de Logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app_debug.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

RECORDINGS_DIR = "recordings"

def ensure_recordings_dir():
    """Garante que a pasta de perfis exista."""
    if not os.path.exists(RECORDINGS_DIR):
        try:
            os.makedirs(RECORDINGS_DIR)
            logger.info(f"Diretório I/O criado: {RECORDINGS_DIR}")
        except Exception as e:
            logger.error(f"Falha ao criar diretório: {e}")

def save_recording(name, events, duration):
    """Salva um novo perfil de inputs."""
    ensure_recordings_dir()
    
    # Sanitização do nome do arquivo
    safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).strip()
    if not safe_name:
        safe_name = f"perfil_{int(time.time())}"
    
    filename = os.path.join(RECORDINGS_DIR, f"{safe_name}.json")
    
    data = {
        "version": "1.1",
        "name": name,
        "duration": duration,
        "created_at": time.time(),
        "event_count": len(events),
        "events": events
    }
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"Dados Puros de input salvos com sucesso: {filename}")
        return True, filename
    except IOError as e:
        logger.error(f"Erro de E/S ao salvar payload {filename}: {e}")
        return False, f"Erro de disco: {e}"
    except Exception as e:
        logger.error(f"Erro inesperado ao alocar memoria local: {e}")
        return False, str(e)

def load_recording(path):
    """Carrega os dados de um perfil específico."""
    if not os.path.exists(path):
        logger.warning(f"Tentativa de carregar pacote inexistente: {path}")
        return None
        
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except json.JSONDecodeError:
        logger.error(f"Pacote de dados serializados corrompido: {path}")
    except Exception as e:
        logger.error(f"Erro ao carregar blocos I/O de {path}: {e}")
    return None

def list_recordings():
    """Retorna a lista de perfis salvos."""
    ensure_recordings_dir()
    files = [f for f in os.listdir(RECORDINGS_DIR) if f.endswith('.json')]
    recordings = []
    
    for f in files:
        path = os.path.join(RECORDINGS_DIR, f)
        try:
            with open(path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                recordings.append({
                    "filename": f,
                    "path": path,
                    "name": data.get("name", f),
                    "duration": data.get("duration", 0),
                    "created_at": data.get("created_at", 0),
                    "event_count": data.get("event_count", len(data.get("events", [])))
                })
        except Exception as e:
            logger.error(f"Erro ao processar cabecalho de {f}: {e}")
            
    recordings.sort(key=lambda x: x["created_at"], reverse=True)
    return recordings

def delete_recording(path):
    """Exclui fisicamente um arquivo de dados do HD."""
    try:
        if os.path.exists(path):
            os.remove(path)
            logger.info(f"Perfil isolado excluido: {path}")
            return True
        else:
            logger.warning(f"Arquivo I/O ja deletado: {path}")
    except PermissionError:
        logger.error(f"Permissao negada na partição bloqueada: {path}")
    except Exception as e:
        logger.error(f"Erro ao destruir {path}: {e}")
    return False
