"""
Ponto de entrada principal do ScriptBird.
"""
import os
import sys
from pathlib import Path

from PyQt5.QtWidgets import QApplication

# Corrige problemas de OpenGL/Qt no Linux
os.environ.setdefault('QT_XCB_GL_INTEGRATION', 'none')

# Configura o path para os módulos
src_path = Path(__file__).parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

try:
    from ui.main_window import MainWindow
except ImportError as e:
    print(f"Erro ao importar MainWindow: {e}")
    sys.exit(1)


def main():
    """Função principal da aplicação."""
    # Cria aplicação
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    # Cria e exibe janela principal
    try:
        window = MainWindow()
        window.show()
    except Exception as e:
        print(f"Erro ao criar janela principal: {e}")
        sys.exit(1)
    
    # Executa aplicação
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()