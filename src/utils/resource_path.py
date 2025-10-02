"""
Utilitário para resolução de caminhos de recursos.
Compatível com PyInstaller.
"""
import os
import sys


def resource_path(relative_path: str) -> str:
    """
    Resolve o caminho de recursos mesmo quando empacotado pelo PyInstaller.
    
    Args:
        relative_path: Caminho relativo do recurso
        
    Returns:
        Caminho absoluto do recurso
    """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)  # type: ignore
    return os.path.join(os.path.abspath("."), relative_path)