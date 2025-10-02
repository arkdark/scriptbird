"""
Serviço de banco de dados do ScriptBird.
"""
import sys
from pathlib import Path
from typing import List, Tuple

from core.models.database_config import DatabaseConfig

# Adiciona o diretório src ao path
src_path = Path(__file__).parent.parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from infrastructure.database.firebird_connection import FirebirdConnection


class DatabaseService:
    """Serviço para operações de banco de dados."""
    
    def __init__(self, config: DatabaseConfig):
        """
        Inicializa o serviço.
        
        Args:
            config: Configuração do banco de dados
        """
        self.config = config
        self.connection = FirebirdConnection(config)
    
    def test_connection(self) -> bool:
        """
        Testa a conexão com o banco.
        
        Returns:
            True se a conexão foi bem-sucedida
        """
        return self.connection.test_connection()
    
    def execute_query(self, query: str) -> Tuple[List[str], List[Tuple]]:
        """
        Executa uma query SQL.
        
        Args:
            query: Query SQL a ser executada
            
        Returns:
            Tupla com (nomes_colunas, dados)
        """
        return self.connection.execute_query(query)
    
    def validate_config(self) -> bool:
        """
        Valida se a configuração do banco é válida.
        
        Returns:
            True se a configuração é válida
        """
        return self.config.is_valid()