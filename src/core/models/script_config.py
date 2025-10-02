"""
Modelo de configuração do script.
"""
import os
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class ScriptConfig:
    """Configuração do script de execução."""
    
    arquivo: str = ""
    
    def is_valid(self) -> bool:
        """Verifica se a configuração é válida."""
        return bool(self.arquivo and os.path.exists(self.arquivo))
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ScriptConfig':
        """Cria uma instância a partir de um dicionário."""
        return cls(arquivo=data.get('arquivo', ''))
    
    def to_dict(self) -> dict:
        """Converte para dicionário."""
        return {'arquivo': self.arquivo}


@dataclass
class ScriptAction:
    """Representa uma ação do script."""
    
    executar: str
    variaveis: Dict[str, Any]
    
    @classmethod
    def from_config_sections(cls, acao_section: dict, variaveis_section: dict) -> 'ScriptAction':
        """Cria uma instância a partir das seções do arquivo de configuração."""
        return cls(
            executar=acao_section.get('EXECUTAR', ''),
            variaveis=dict(variaveis_section)
        )
    
    def get_variable(self, name: str, default: Any = None) -> Any:
        """Obtém uma variável do script."""
        return self.variaveis.get(name, default)
    
    def get_int_variable(self, name: str, default: int = 0) -> int:
        """Obtém uma variável inteira do script."""
        try:
            return int(self.variaveis.get(name, default))
        except (ValueError, TypeError):
            return default
    
    def get_bool_variable(self, name: str, default: bool = False) -> bool:
        """Obtém uma variável booleana do script."""
        value = self.variaveis.get(name, 'N' if not default else 'S')
        return str(value).strip().upper() == 'S'