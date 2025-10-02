"""
Conexão com banco de dados Firebird.
"""
from typing import List, Tuple

import fdb

from core.exceptions.scriptbird_exceptions import (
    DatabaseConnectionError,
    DatabaseQueryError,
)
from core.models.database_config import DatabaseConfig


class FirebirdConnection:
    """Gerenciador de conexão com Firebird."""
    
    def __init__(self, config: DatabaseConfig):
        """
        Inicializa a conexão.
        
        Args:
            config: Configuração do banco de dados
        """
        self.config = config
        self._connection = None
    
    def test_connection(self) -> bool:
        """
        Testa a conexão com o banco.
        
        Returns:
            True se a conexão foi bem-sucedida
            
        Raises:
            DatabaseConnectionError: Se não conseguir conectar
        """
        try:
            dsn = self.config.get_dsn()
            conn = fdb.connect(
                dsn=dsn,
                user=self.config.usuario,
                password=self.config.senha
            )
            conn.close()
            return True
        except Exception as e:
            raise DatabaseConnectionError(f"Erro ao conectar: {e}")
    
    def execute_query(self, query: str) -> Tuple[List[str], List[Tuple]]:
        """
        Executa uma query e retorna os resultados.
        
        Args:
            query: Query SQL a ser executada
            
        Returns:
            Tupla com (nomes_colunas, dados)
            
        Raises:
            DatabaseConnectionError: Se não conseguir conectar
            DatabaseQueryError: Se houver erro na execução da query
        """
        try:
            dsn = self.config.get_dsn()
            conn = fdb.connect(
                dsn=dsn,
                user=self.config.usuario,
                password=self.config.senha
            )
            
            cursor = conn.cursor()
            cursor.execute(query)
            
            # Obtém nomes das colunas
            columns = [desc[0] for desc in cursor.description]
            
            # Obtém dados
            data = cursor.fetchall()
            
            conn.close()
            
            return columns, data
            
        except fdb.Error as e:
            raise DatabaseQueryError(f"Erro na execução da query: {e}")
        except Exception as e:
            raise DatabaseConnectionError(f"Erro de conexão: {e}")
    
    def __enter__(self):
        """Context manager entry."""
        try:
            dsn = self.config.get_dsn()
            self._connection = fdb.connect(
                dsn=dsn,
                user=self.config.usuario,
                password=self.config.senha
            )
            return self
        except Exception as e:
            raise DatabaseConnectionError(f"Erro ao conectar: {e}")
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        if self._connection:
            self._connection.close()
            self._connection = None
    
    @property
    def connection(self):
        """Retorna a conexão ativa."""
        if not self._connection:
            raise DatabaseConnectionError("Conexão não estabelecida")
        return self._connection