"""
Executor de scripts do ScriptBird.
"""
import os
import threading
import time
from typing import Callable, Optional

from PyQt5.QtCore import QObject, pyqtSignal

from core.exceptions.scriptbird_exceptions import ScriptConfigurationError
from core.models.database_config import DatabaseConfig
from core.models.script_config import ScriptAction

from .database_service import DatabaseService
from .file_service import FileService


class ScriptExecutor(QObject):
    """Executor de scripts em thread separada."""
    
    finished = pyqtSignal()
    
    def __init__(self, 
                 db_config: DatabaseConfig, 
                 script_action: ScriptAction,
                 log_callback: Optional[Callable[[str], None]] = None):
        """
        Inicializa o executor.
        
        Args:
            db_config: Configuração do banco de dados
            script_action: Ação do script a ser executada
            log_callback: Função de callback para logs
        """
        super().__init__()
        self.db_config = db_config
        self.script_action = script_action
        self.log_callback = log_callback or print
        self._running = threading.Event()
        self._running.set()
        self._thread = None
    
    def start(self):
        """Inicia a execução em thread separada."""
        self._thread = threading.Thread(target=self._run)
        self._thread.start()
    
    def stop(self):
        """Para a execução."""
        self._running.clear()
    
    def is_alive(self) -> bool:
        """Verifica se a thread está ativa."""
        return self._thread.is_alive() if self._thread else False
    
    def join(self):
        """Aguarda a thread terminar."""
        if self._thread:
            self._thread.join()
    
    def _run(self):
        """Executa o script."""
        try:
            self._log("Iniciando execução do BOT...")
            
            if self.script_action.executar == "SALVAR_EM_ARQUIVO":
                self._execute_save_to_file()
            else:
                self._log(f"Ação '{self.script_action.executar}' não reconhecida.")
                
        except Exception as e:
            self._log(f"Erro durante execução do BOT: {e}")
        finally:
            self.finished.emit()
    
    def _execute_save_to_file(self):
        """Executa a ação de salvar em arquivo."""
        # Validação das variáveis necessárias
        query = self.script_action.get_variable('QUERY')
        caminho = self.script_action.get_variable('CAMINHO', '').strip()
        nome_arquivo = self.script_action.get_variable('NOME_ARQUIVO', '').strip()
        formato = self.script_action.get_variable('FORMATO', '.xlsx').strip().lower()
        tempo_entre_execucoes = self.script_action.get_int_variable('TEMPO_ENTRE_EXECUCOES', 3600)
        repetir = self.script_action.get_bool_variable('REPETIR', False)
        
        if not query:
            raise ScriptConfigurationError("Variável QUERY não definida no script")
        if not caminho:
            raise ScriptConfigurationError("Variável CAMINHO não definida no script")
        if not nome_arquivo:
            raise ScriptConfigurationError("Variável NOME_ARQUIVO não definida no script")
        
        self._log(f"Ação a ser executada: {self.script_action.executar}")
        
        # Serviços
        db_service = DatabaseService(self.db_config)
        file_service = FileService()
        
        while self._running.is_set():
            try:
                # Executa a query
                self._log("Executando consulta SQL...")
                columns, data = db_service.execute_query(query)
                
                # Monta o caminho completo do arquivo
                file_path = os.path.join(caminho, nome_arquivo + formato)
                
                # Salva o arquivo
                self._log(f"Salvando dados em: {file_path}")
                file_service.save_to_file(columns, data, file_path, formato)
                
                self._log(f"Arquivo gerado com sucesso: {file_path}")
                self._log(f"Total de registros: {len(data)}")
                
                if not repetir:
                    self._log("Execução única concluída.")
                    break
                
                # Aguarda o tempo especificado
                self._log(f"Aguardando {tempo_entre_execucoes} segundos para próxima execução...")
                for _ in range(tempo_entre_execucoes):
                    if not self._running.is_set():
                        self._log("Execução interrompida.")
                        return
                    time.sleep(1)
                
            except Exception as e:
                self._log(f"Erro ao processar ciclo do script: {e}")
                break
    
    def _log(self, message: str):
        """Registra uma mensagem de log."""
        if self.log_callback:
            self.log_callback(message)