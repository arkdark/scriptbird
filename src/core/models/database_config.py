"""
Modelo de configuração do banco de dados.
"""
import os
from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    """Configuração do banco de dados Firebird."""
    
    caminho: str = ""
    usuario: str = "SYSDBA"
    senha: str = "masterkey"
    porta: str = "3050"
    
    def is_valid(self) -> bool:
        """Verifica se a configuração é válida."""
        return bool(self.caminho and self.usuario and self.senha)
    
    def get_dsn(self) -> str:
        """
        Constrói o DSN para conexão com Firebird.
        
        Returns:
            DSN formatado para conexão
        """
        caminho = self.caminho.strip()
        
        # Verifica se tem host|caminho
        if "|" in caminho:
            host, caminho_banco = caminho.split("|", 1)
        else:
            host = "localhost"
            caminho_banco = caminho
        
        # Verifica se é um arquivo local existente
        if os.path.isfile(caminho_banco):
            return caminho_banco
        else:
            # Conexão remota
            if self.porta:
                return f"{host}:{self.porta}:{caminho_banco}"
            else:
                return f"{host}:{caminho_banco}"
    
    @classmethod
    def from_dict(cls, data: dict) -> 'DatabaseConfig':
        """Cria uma instância a partir de um dicionário."""
        return cls(
            caminho=data.get('caminho', ''),
            usuario=data.get('usuario', 'SYSDBA'),
            senha=data.get('senha', 'masterkey'),
            porta=data.get('porta', '3050')
        )
    
    def to_dict(self) -> dict:
        """Converte para dicionário."""
        return {
            'caminho': self.caminho,
            'usuario': self.usuario,
            'senha': self.senha,
            'porta': self.porta
        }