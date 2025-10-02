"""
Janela principal do ScriptBird refatorada.
"""
import sys
from pathlib import Path

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog, QMainWindow

# Adiciona o diretório src ao path
src_path = Path(__file__).parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

try:
    from core.models.database_config import DatabaseConfig
    from core.models.script_config import ScriptConfig
    from core.services.database_service import DatabaseService
    from core.services.script_executor import ScriptExecutor
    from infrastructure.config.config_manager import ConfigManager
    from ui.components.system_tray import SystemTray
    from ui.generated.ui_main_window import Ui_MainWindow
    from utils.logger import ScriptBirdLogger
    from utils.resource_path import resource_path
except ImportError as e:
    print(f"Erro de importação: {e}")
    # Fallbacks básicos para desenvolvimento/teste
    from PyQt5.QtCore import QObject, pyqtSignal
    
    class Ui_MainWindow:
        def setupUi(self, window): pass
        def retranslateUi(self, window): pass
    
    class SystemTray(QObject):
        show_window = pyqtSignal()
        def __init__(self, parent): 
            super().__init__(parent)
        def show_message(self, title, message):
            pass
    
    class ConfigManager:
        def load_config(self): 
            return DatabaseConfig(), ScriptConfig()
        def save_config(self, db, script): 
            pass
        def update_script_path(self, path): 
            pass
        def load_script_action(self, path): 
            return None
    
    class ScriptBirdLogger:
        def __init__(self, callback=None): 
            self.callback = callback
        def info(self, msg): 
            if self.callback: 
                self.callback(msg)
        def error(self, msg): 
            if self.callback: 
                self.callback(f"ERRO: {msg}")
    
    class DatabaseConfig:
        def __init__(self): 
            self.caminho = ""
            self.usuario = "SYSDBA"
            self.senha = "masterkey"
            self.porta = "3050"
        def is_valid(self): 
            return False
    
    class ScriptConfig:
        def __init__(self): 
            self.arquivo = ""
        def is_valid(self): 
            return False
    
    class DatabaseService:
        def __init__(self, config): pass
        def test_connection(self): return False
    
    class ScriptExecutor(QObject):
        finished = pyqtSignal()
        def __init__(self, db_config, script_action, log_callback): 
            super().__init__()
        def start(self): pass
        def stop(self): pass
        def is_alive(self): return False
        def join(self): pass
    
    def resource_path(relative_path): 
        return relative_path


class MainWindow(QMainWindow, Ui_MainWindow):
    """Janela principal do ScriptBird."""
    
    def __init__(self):
        """Inicializa a janela principal."""
        super().__init__()
        self.setupUi(self)
        
        # Configuração da janela
        self._setup_window()
        
        # Componentes
        self.system_tray = SystemTray(self)
        self.config_manager = ConfigManager()
        self.logger = ScriptBirdLogger(self._log_to_ui)
        
        # Estado
        self.bot_running = False
        self.script_executor = None
        self.db_config = DatabaseConfig()
        self.script_config = ScriptConfig()
        
        # Configuração inicial
        self._setup_connections()
        self._setup_initial_state()
        self._load_configuration()
        self._check_auto_execution()
    
    def _setup_window(self):
        """Configura a janela principal."""
        try:
            icon_path = resource_path("assets/icons/icon.ico")
            self.setWindowIcon(QIcon(icon_path))
        except Exception:
            pass
        
        self.setWindowTitle("ScriptBird")
    
    def _setup_connections(self):
        """Configura as conexões de sinais e slots."""
        # Conexões dos botões
        if hasattr(self, 'btn_SalvarBD'):
            self.btn_SalvarBD.clicked.connect(self._save_config)
        if hasattr(self, 'btn_TestarBD'):
            self.btn_TestarBD.clicked.connect(self._test_connection)
        if hasattr(self, 'btn_AbrirExploradorBD'):
            self.btn_AbrirExploradorBD.clicked.connect(self._select_database_file)
        if hasattr(self, 'btn_AbrirExploradorScript'):
            self.btn_AbrirExploradorScript.clicked.connect(self._select_script_file)
        if hasattr(self, 'btn_EditarCaminhoBD'):
            self.btn_EditarCaminhoBD.clicked.connect(self._enable_database_editing)
        if hasattr(self, 'btn_IniciarBot'):
            self.btn_IniciarBot.clicked.connect(self._start_bot)
        if hasattr(self, 'btn_PararBot'):
            self.btn_PararBot.clicked.connect(self._stop_bot)
        
        # System tray
        self.system_tray.show_window.connect(self._show_window)
    
    def _setup_initial_state(self):
        """Configura o estado inicial da interface."""
        # Desativa campos de BD
        if hasattr(self, 'ca_CaminhoBD'):
            self.ca_CaminhoBD.setEnabled(False)
        if hasattr(self, 'ca_UsuarioBD'):
            self.ca_UsuarioBD.setEnabled(False)
        if hasattr(self, 'ca_SenhaBD'):
            self.ca_SenhaBD.setEnabled(False)
        if hasattr(self, 'ca_PortaBD'):
            self.ca_PortaBD.setEnabled(False)
        if hasattr(self, 'btn_AbrirExploradorBD'):
            self.btn_AbrirExploradorBD.setEnabled(False)
        if hasattr(self, 'btn_SalvarBD'):
            self.btn_SalvarBD.setEnabled(False)
        
        # Botões sempre ativos
        if hasattr(self, 'btn_TestarBD'):
            self.btn_TestarBD.setEnabled(True)
        if hasattr(self, 'btn_EditarCaminhoBD'):
            self.btn_EditarCaminhoBD.setEnabled(True)
        
        # Estado inicial dos botões de bot
        if hasattr(self, 'btn_IniciarBot'):
            self.btn_IniciarBot.setEnabled(True)
        if hasattr(self, 'btn_PararBot'):
            self.btn_PararBot.setEnabled(False)
    
    def _load_configuration(self):
        """Carrega configurações do arquivo."""
        try:
            self.db_config, self.script_config = self.config_manager.load_config()
            
            # Atualiza interface
            if hasattr(self, 'ca_CaminhoBD'):
                self.ca_CaminhoBD.setText(self.db_config.caminho)
            if hasattr(self, 'ca_UsuarioBD'):
                self.ca_UsuarioBD.setText(self.db_config.usuario)
            if hasattr(self, 'ca_SenhaBD'):
                self.ca_SenhaBD.setText(self.db_config.senha)
            if hasattr(self, 'ca_PortaBD'):
                self.ca_PortaBD.setText(self.db_config.porta)
            if hasattr(self, 'ca_CaminhoScript'):
                self.ca_CaminhoScript.setText(self.script_config.arquivo)
            
            self.logger.info("Configurações carregadas com sucesso.")
            
        except Exception as e:
            self.logger.error(f"Erro ao carregar configurações: {e}")
    
    def _check_auto_execution(self):
        """Verifica se deve executar automaticamente."""
        # Atualiza configurações da UI
        self._update_config_from_ui()
        
        # Valida configurações
        if not self.db_config.is_valid():
            self.logger.info("Configuração do banco incompleta. BOT não iniciado.")
            return
        
        if not self.script_config.is_valid():
            self.logger.info("Script não encontrado. BOT não iniciado.")
            return
        
        # Testa conexão
        try:
            db_service = DatabaseService(self.db_config)
            if db_service.test_connection():
                self._start_bot(auto=True)
            else:
                self.logger.error("Falha ao conectar no banco. BOT não iniciado.")
        except Exception as e:
            self.logger.error(f"Falha ao conectar no banco. BOT não iniciado. Erro: {e}")
    
    def _update_config_from_ui(self):
        """Atualiza configurações a partir da UI."""
        if hasattr(self, 'ca_CaminhoBD'):
            self.db_config.caminho = self.ca_CaminhoBD.text().strip()
        if hasattr(self, 'ca_UsuarioBD'):
            self.db_config.usuario = self.ca_UsuarioBD.text().strip()
        if hasattr(self, 'ca_SenhaBD'):
            self.db_config.senha = self.ca_SenhaBD.text().strip()
        if hasattr(self, 'ca_PortaBD'):
            self.db_config.porta = self.ca_PortaBD.text().strip()
        if hasattr(self, 'ca_CaminhoScript'):
            self.script_config.arquivo = self.ca_CaminhoScript.text().strip()
    
    def _start_bot(self, auto=False):
        """Inicia o bot."""
        if self.bot_running:
            self.logger.info("BOT já está em execução.")
            return
        
        try:
            # Atualiza configurações
            self._update_config_from_ui()
            
            # Carrega ação do script
            script_action = self.config_manager.load_script_action(self.script_config.arquivo)
            
            # Inicia executor
            self.script_executor = ScriptExecutor(
                self.db_config, 
                script_action, 
                self.logger.info
            )
            self.script_executor.finished.connect(self._on_bot_finished)
            self.script_executor.start()
            
            # Atualiza estado
            self.bot_running = True
            if hasattr(self, 'btn_IniciarBot'):
                self.btn_IniciarBot.setEnabled(False)
            if hasattr(self, 'btn_PararBot'):
                self.btn_PararBot.setEnabled(True)
            
            if auto:
                self.logger.info("BOT iniciado automaticamente com base nas configurações.")
            else:
                self.logger.info("BOT iniciado manualmente.")
                
        except Exception as e:
            self.logger.error(f"Erro ao iniciar BOT: {e}")
    
    def _stop_bot(self):
        """Para o bot."""
        if not self.bot_running:
            return
        
        if self.script_executor:
            self.script_executor.stop()
            if self.script_executor.is_alive():
                self.script_executor.join()
            self.script_executor = None
        
        self._on_bot_finished()
    
    def _on_bot_finished(self):
        """Callback quando o bot termina."""
        self.bot_running = False
        if hasattr(self, 'btn_IniciarBot'):
            self.btn_IniciarBot.setEnabled(True)
        if hasattr(self, 'btn_PararBot'):
            self.btn_PararBot.setEnabled(False)
        self.logger.info("BOT parado com sucesso.")
    
    def _save_config(self):
        """Salva configurações."""
        try:
            self._update_config_from_ui()
            self.config_manager.save_config(self.db_config, self.script_config)
            self.logger.info("Configurações salvas com sucesso.")
            self._setup_initial_state()
        except Exception as e:
            self.logger.error(f"Erro ao salvar configurações: {e}")
    
    def _test_connection(self):
        """Testa conexão com o banco."""
        try:
            self._update_config_from_ui()
            db_service = DatabaseService(self.db_config)
            db_service.test_connection()
            self.logger.info("Conexão com banco realizada com sucesso.")
        except Exception as e:
            self.logger.error(f"Erro ao conectar: {e}")
    
    def _select_database_file(self):
        """Seleciona arquivo de banco de dados."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Selecionar banco de dados", 
            "", 
            "Arquivos FDB (*.FDB);;Todos (*)"
        )
        if file_path and hasattr(self, 'ca_CaminhoBD'):
            self.ca_CaminhoBD.setText(file_path)
            self.logger.info(f"Caminho do banco selecionado: {file_path}")
    
    def _select_script_file(self):
        """Seleciona arquivo de script."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Selecionar script", 
            "", 
            "Arquivos de Script (*.ini);;Todos (*)"
        )
        if file_path and hasattr(self, 'ca_CaminhoScript'):
            self.ca_CaminhoScript.setText(file_path)
            self.logger.info(f"Script selecionado: {file_path}")
            self._update_script_config(file_path)
    
    def _update_script_config(self, script_path: str):
        """Atualiza configuração do script."""
        try:
            self.config_manager.update_script_path(script_path)
            self.logger.info("Caminho do script salvo automaticamente no config.ini.")
        except Exception as e:
            self.logger.error(f"Erro ao salvar caminho do script: {e}")
    
    def _enable_database_editing(self):
        """Habilita edição das configurações do banco."""
        if hasattr(self, 'ca_CaminhoBD'):
            self.ca_CaminhoBD.setEnabled(True)
        if hasattr(self, 'ca_UsuarioBD'):
            self.ca_UsuarioBD.setEnabled(True)
        if hasattr(self, 'ca_SenhaBD'):
            self.ca_SenhaBD.setEnabled(True)
        if hasattr(self, 'ca_PortaBD'):
            self.ca_PortaBD.setEnabled(True)
        if hasattr(self, 'btn_AbrirExploradorBD'):
            self.btn_AbrirExploradorBD.setEnabled(True)
        if hasattr(self, 'btn_SalvarBD'):
            self.btn_SalvarBD.setEnabled(True)
        
        self.logger.info("Edição das configurações do banco ativada.")
    
    def _show_window(self):
        """Mostra a janela."""
        self.showNormal()
        self.activateWindow()
    
    def _log_to_ui(self, message: str):
        """Registra mensagem na UI."""
        if hasattr(self, 'campoLogs'):
            self.campoLogs.appendPlainText(message)
            # Auto-scroll
            scrollbar = self.campoLogs.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())
    
    def closeEvent(self, a0):  # type: ignore
        """Manipula evento de fechamento da janela."""
        if hasattr(a0, 'ignore'):
            a0.ignore()  # type: ignore
        self.hide()
        if hasattr(self.system_tray, 'show_message'):
            self.system_tray.show_message("ScriptBird", "Executando em segundo plano.")