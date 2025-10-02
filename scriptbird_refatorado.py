#!/usr/bin/env python3
"""
Script de entrada compatível com a versão original do ScriptBird.
Este arquivo mantém compatibilidade com o arquivo original scriptbird.py
"""
import os
import sys
from pathlib import Path

# Adiciona o diretório src ao sys.path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"

if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

# Corrige problemas de OpenGL/Qt no Linux
os.environ.setdefault('QT_XCB_GL_INTEGRATION', 'none')

# Importa e executa a aplicação principal
if __name__ == "__main__":
    try:
        # Executa diretamente o código do main
        from PyQt5.QtWidgets import QApplication
        
        # Importa a janela principal
        from ui.main_window import MainWindow
        
        # Função principal
        app = QApplication(sys.argv)
        app.setQuitOnLastWindowClosed(False)
        
        window = MainWindow()
        window.show()
        
        sys.exit(app.exec_())
        
    except ImportError as e:
        print(f"Erro ao importar aplicação: {e}")
        print("Certifique-se de que todas as dependências estão instaladas:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Erro ao executar aplicação: {e}")
        sys.exit(1)