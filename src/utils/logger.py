"""
Sistema de logging para o ScriptBird.
"""
import logging
from datetime import datetime
from typing import Callable, Optional


class ScriptBirdLogger:
    """Logger customizado para o ScriptBird."""
    
    def __init__(self, log_callback: Optional[Callable[[str], None]] = None):
        """
        Inicializa o logger.
        
        Args:
            log_callback: Função de callback para exibir logs na UI
        """
        self.log_callback = log_callback
        self._setup_logger()
    
    def _setup_logger(self):
        """Configura o logger padrão."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        self.logger = logging.getLogger('ScriptBird')
    
    def info(self, message: str):
        """Log de informação."""
        formatted_message = self._format_message(message)
        self.logger.info(message)
        if self.log_callback:
            self.log_callback(formatted_message)
    
    def error(self, message: str):
        """Log de erro."""
        formatted_message = self._format_message(message, level="ERRO")
        self.logger.error(message)
        if self.log_callback:
            self.log_callback(formatted_message)
    
    def warning(self, message: str):
        """Log de aviso."""
        formatted_message = self._format_message(message, level="AVISO")
        self.logger.warning(message)
        if self.log_callback:
            self.log_callback(formatted_message)
    
    def _format_message(self, message: str, level: str = "INFO") -> str:
        """Formata a mensagem para exibição na UI."""
        now = datetime.now().strftime("[%H:%M:%S]")
        if level == "INFO":
            return f"{now} {message}"
        else:
            return f"{now} {level}: {message}"