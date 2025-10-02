"""
Componente de sistema tray para o ScriptBird.
"""
import sys
from pathlib import Path

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QApplication, QMenu, QSystemTrayIcon

# Adiciona o diretório src ao path
src_path = Path(__file__).parent.parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

try:
    from utils.resource_path import resource_path
except ImportError:
    def resource_path(relative_path: str) -> str:
        """Fallback para resource_path."""
        import os
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)  # type: ignore
        return os.path.join(os.path.abspath("."), relative_path)


class SystemTray(QObject):
    """Componente de sistema tray."""
    
    show_window = pyqtSignal()
    
    def __init__(self, parent=None):
        """
        Inicializa o sistema tray.
        
        Args:
            parent: Widget pai
        """
        super().__init__(parent)
        self.tray = QSystemTrayIcon(parent)
        self._setup_tray()
    
    def _setup_tray(self):
        """Configura o ícone e menu do sistema tray."""
        # Configura o ícone
        try:
            icon_path = resource_path("assets/icons/icon.ico")
            tray_icon = QIcon(icon_path)
        except Exception:
            # Fallback para ícone padrão
            tray_icon = QIcon()
        
        self.tray.setIcon(tray_icon)
        self.tray.setVisible(True)
        
        # Cria o menu
        menu = QMenu()
        
        # Ação para abrir a janela
        open_action = QAction("Abrir", self)
        open_action.triggered.connect(self.show_window.emit)
        
        # Ação para sair
        quit_action = QAction("Sair", self)
        app = QApplication.instance()
        if app:
            quit_action.triggered.connect(app.quit)
        
        # Adiciona ações ao menu
        menu.addAction(open_action)
        menu.addSeparator()
        menu.addAction(quit_action)
        
        # Define o menu no tray
        self.tray.setContextMenu(menu)
        
        # Conecta double-click
        self.tray.activated.connect(self._on_tray_activated)
    
    def _on_tray_activated(self, reason):
        """Manipula ativação do tray icon."""
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show_window.emit()
    
    def show_message(self, title: str, message: str):
        """
        Exibe uma mensagem no tray.
        
        Args:
            title: Título da mensagem
            message: Texto da mensagem
        """
        self.tray.showMessage(title, message)
    
    def set_visible(self, visible: bool):
        """
        Define a visibilidade do tray icon.
        
        Args:
            visible: True para mostrar, False para ocultar
        """
        self.tray.setVisible(visible)