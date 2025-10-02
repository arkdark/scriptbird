import sys
import os
import fdb
import configparser
from datetime import datetime
from leitor_script import ScriptExecutor

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QSystemTrayIcon,
    QMenu, QAction, QFileDialog
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject
from scriptbird_ui import Ui_MainWindow

CONFIG_FILE = "config.ini"

def resource_path(relative_path):
    """Resolve o caminho de recursos mesmo quando empacotado pelo PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class LogBridge(QObject):
    log_signal = pyqtSignal(str)

class ScriptBird(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(resource_path("icon.ico")))
        self.setWindowTitle("ScriptBird")

        self.bot_rodando = False
        
        self.log_bridge = LogBridge()
        self.log_bridge.log_signal.connect(self.log_threadsafe)

        self.setup_tray_icon()
        self.configurar_estado_inicial()
        self.load_config()
        self.verificar_autoexecucao()
        self.worker = None

        # Conexões dos botões
        self.btn_SalvarBD.clicked.connect(self.save_config)
        self.btn_TestarBD.clicked.connect(self.test_connection)
        self.btn_AbrirExploradorBD.clicked.connect(self.select_database_file)
        self.btn_AbrirExploradorScript.clicked.connect(self.select_script_file)
        self.btn_EditarCaminhoBD.clicked.connect(self.habilitar_edicao_banco)
        self.btn_IniciarBot.clicked.connect(self.iniciar_bot)
        self.btn_PararBot.clicked.connect(self.parar_bot)

    def configurar_estado_inicial(self):
        # Desativa todos os campos de BD
        self.ca_CaminhoBD.setEnabled(False)
        self.ca_UsuarioBD.setEnabled(False)
        self.ca_SenhaBD.setEnabled(False)
        self.ca_PortaBD.setEnabled(False)
        self.btn_AbrirExploradorBD.setEnabled(False)
        self.btn_SalvarBD.setEnabled(False)

        # Testar e Editar continuam ativos
        self.btn_TestarBD.setEnabled(True)
        self.btn_EditarCaminhoBD.setEnabled(True)

    def habilitar_edicao_banco(self):
        self.ca_CaminhoBD.setEnabled(True)
        self.ca_UsuarioBD.setEnabled(True)
        self.ca_SenhaBD.setEnabled(True)
        self.ca_PortaBD.setEnabled(True)
        self.btn_AbrirExploradorBD.setEnabled(True)
        self.btn_SalvarBD.setEnabled(True)
        self.log("Edição das configurações do banco ativada.")

    def verificar_autoexecucao(self):
        # Verifica se todos os campos críticos existem e são válidos
        caminho = self.ca_CaminhoBD.text().strip()
        usuario = self.ca_UsuarioBD.text().strip()
        senha = self.ca_SenhaBD.text().strip()
        script = self.ca_CaminhoScript.text().strip()
        porta = self.ca_PortaBD.text().strip()

        if not caminho or not usuario or not senha:
            self.log("Configuração do banco incompleta. BOT não iniciado.")
            self.btn_IniciarBot.setEnabled(True)
            self.btn_PararBot.setEnabled(False)
            return

        if not os.path.exists(script):
            self.log("Script não encontrado. BOT não iniciado.")
            self.btn_IniciarBot.setEnabled(True)
            self.btn_PararBot.setEnabled(False)
            return

        # Testa conexão
        try:
            # Verifica se foi informado HOST|CAMINHO
            if "|" in caminho:
                host, caminho_banco = caminho.split("|", 1)
            else:
                host = "localhost"
                caminho_banco = caminho

            # Verifica se é um arquivo local existente
            if os.path.isfile(caminho_banco):
                dsn = caminho_banco
            else:
                dsn = f"{host}:{porta}:{caminho_banco}"
                if porta:
                    dsn = f"{dsn}"

            conn = fdb.connect(dsn=dsn, user=usuario, password=senha)
            conn.close()
            self.iniciar_bot(auto=True)

        except Exception as e:
            self.log(f"Falha ao conectar no banco. BOT não iniciado. Erro: {e}")
            self.btn_IniciarBot.setEnabled(True)
            self.btn_PararBot.setEnabled(False)


    def iniciar_bot(self, auto=False):
        if self.bot_rodando:
            self.log("BOT já está em execução.")
            return

        self.bot_rodando = True
        self.btn_IniciarBot.setEnabled(False)
        self.btn_PararBot.setEnabled(True)

        if auto:
            self.log("BOT iniciado automaticamente com base nas configurações.")
        else:
            self.log("BOT iniciado manualmente.")

        # Inicia thread
        self.worker = ScriptExecutor(log_callback=self.log_bridge.log_signal.emit)
        self.worker.finished.connect(self.parar_bot)
        self.worker.start()

    def parar_bot(self):
        if not self.bot_rodando:
            return

        if self.worker:
            self.worker.stop()
            if self.worker.is_alive():
                self.worker.join()
            self.worker = None

        self.bot_rodando = False
        self.btn_IniciarBot.setEnabled(True)
        self.btn_PararBot.setEnabled(False)
        self.log("BOT parado com sucesso.")

    def log(self, message):
        now = datetime.now().strftime("[%H:%M:%S]")
        self.campoLogs.appendPlainText(f"{now} {message}")
        self.campoLogs.verticalScrollBar().setValue(
            self.campoLogs.verticalScrollBar().maximum()
        )

    def setup_tray_icon(self):
        self.tray = QSystemTrayIcon(self)
        tray_icon = QIcon(resource_path("icon.ico"))
        self.setWindowIcon(tray_icon)
        self.tray.setIcon(tray_icon)
        self.tray.setVisible(True)

        menu = QMenu()
        open_action = QAction("Abrir", self)
        quit_action = QAction("Sair", self)

        open_action.triggered.connect(self.showNormal)
        quit_action.triggered.connect(QApplication.instance().quit)

        menu.addAction(open_action)
        menu.addAction(quit_action)

        self.tray.setContextMenu(menu)
        self.tray.activated.connect(self.on_tray_icon_activated)

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.showNormal()
            self.activateWindow()

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray.showMessage("ScriptBird", "Executando em segundo plano.")

    def load_config(self):
        if not os.path.exists(CONFIG_FILE):
            self.log("Arquivo de configuração não encontrado. Será criado ao salvar.")
            return

        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)

        self.ca_CaminhoBD.setText(config.get("DB", "caminho", fallback=""))
        self.ca_UsuarioBD.setText(config.get("DB", "usuario", fallback=""))
        self.ca_SenhaBD.setText(config.get("DB", "senha", fallback=""))
        self.ca_PortaBD.setText(config.get("DB", "porta", fallback=""))
        self.ca_CaminhoScript.setText(config.get("SCRIPT", "arquivo", fallback=""))

        self.log("Configurações carregadas com sucesso.")


    def save_config(self):
        config = configparser.ConfigParser()

        config["DB"] = {
            "caminho": self.ca_CaminhoBD.text(),
            "usuario": self.ca_UsuarioBD.text(),
            "senha": self.ca_SenhaBD.text(),
            "porta": self.ca_PortaBD.text()
        }

        config["SCRIPT"] = {
            "arquivo": self.ca_CaminhoScript.text()
        }

        with open(CONFIG_FILE, "w") as f:
            config.write(f)

        self.log("Configurações salvas com sucesso.")
        self.configurar_estado_inicial()

    def test_connection(self):
        caminho = self.ca_CaminhoBD.text()
        usuario = self.ca_UsuarioBD.text()
        senha = self.ca_SenhaBD.text()
        porta = self.ca_PortaBD.text()

        try:
            # Verifica se tem host|caminho
            if "|" in caminho:
                host, caminho_banco = caminho.split("|", 1)
            else:
                host = "localhost"
                caminho_banco = caminho

            # Verifica se o caminho é um arquivo local
            if os.path.isfile(caminho_banco):
                dsn = caminho_banco  # Caminho absoluto local, usado diretamente
            else:
                # Se tiver porta, monta com ela; senão, usa padrão do Firebird (3050)
                dsn = f"{host}:{porta}:{caminho_banco}" if porta else f"{host}:{caminho_banco}"

            conn = fdb.connect(dsn=dsn, user=usuario, password=senha)
            conn.close()
            self.log("Conexão com banco realizada com sucesso.")
        except Exception as e:
            self.log(f"Erro ao conectar: {e}")

    def select_database_file(self):
        caminho, _ = QFileDialog.getOpenFileName(
            self, "Selecionar banco de dados", "", "Arquivos FDB (*.FDB);;Todos (*)"
        )
        if caminho:
            self.ca_CaminhoBD.setText(caminho)
            self.log(f"Caminho do banco selecionado: {caminho}")

    def select_script_file(self):
        caminho, _ = QFileDialog.getOpenFileName(
            self, "Selecionar script", "", "Arquivos de Script (*.ini);;Todos (*)"
        )
        if caminho:
            self.ca_CaminhoScript.setText(caminho)
            self.log(f"Script selecionado: {caminho}")
            self.atualizar_config_script(caminho)

    def atualizar_config_script(self, caminho_script):
        config = configparser.ConfigParser()
        if os.path.exists(CONFIG_FILE):
            config.read(CONFIG_FILE)

        # Garante a seção SCRIPT
        if 'SCRIPT' not in config:
            config['SCRIPT'] = {}

        config['SCRIPT']['arquivo'] = caminho_script.strip()

        with open(CONFIG_FILE, "w") as f:
            config.write(f)

        self.log("Caminho do script salvo automaticamente no config.ini.")

    @pyqtSlot(str)
    def log_threadsafe(self, message):
        self.log(message)  # já faz append no campo de log


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    window = ScriptBird()
    window.show()
    sys.exit(app.exec_())
