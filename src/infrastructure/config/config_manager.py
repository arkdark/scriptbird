"""
Gerenciador de configurações do ScriptBird.
"""
import configparser
import os
import sys
from pathlib import Path

# Adiciona o diretório src ao path para imports
src_path = Path(__file__).parent.parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from core.exceptions.scriptbird_exceptions import ConfigurationError
from core.models.database_config import DatabaseConfig
from core.models.script_config import ScriptAction, ScriptConfig


class ConfigManager:
    """Gerenciador de configurações do aplicativo."""
    
    def __init__(self, config_file: str = "config.ini"):
        """
        Inicializa o gerenciador de configurações.
        
        Args:
            config_file: Caminho do arquivo de configuração
        """
        self.config_file = config_file
        self.config = configparser.ConfigParser()
    
    def load_config(self) -> tuple[DatabaseConfig, ScriptConfig]:
        """
        Carrega as configurações do arquivo.
        
        Returns:
            Tupla com configurações do banco e script
            
        Raises:
            ConfigurationError: Se houver erro ao carregar configurações
        """
        try:
            if os.path.exists(self.config_file):
                self.config.read(self.config_file)
            
            # Configuração do banco
            db_section = self.config['DB'] if 'DB' in self.config else {}
            db_config = DatabaseConfig.from_dict(dict(db_section))
            
            # Configuração do script
            script_section = self.config['SCRIPT'] if 'SCRIPT' in self.config else {}
            script_config = ScriptConfig.from_dict(dict(script_section))
            
            return db_config, script_config
            
        except Exception as e:
            raise ConfigurationError(f"Erro ao carregar configurações: {e}")
    
    def save_config(self, db_config: DatabaseConfig, script_config: ScriptConfig):
        """
        Salva as configurações no arquivo.
        
        Args:
            db_config: Configurações do banco
            script_config: Configurações do script
            
        Raises:
            ConfigurationError: Se houver erro ao salvar configurações
        """
        try:
            self.config['DB'] = db_config.to_dict()
            self.config['SCRIPT'] = script_config.to_dict()
            
            with open(self.config_file, 'w') as f:
                self.config.write(f)
                
        except Exception as e:
            raise ConfigurationError(f"Erro ao salvar configurações: {e}")
    
    def update_script_path(self, script_path: str):
        """
        Atualiza apenas o caminho do script.
        
        Args:
            script_path: Novo caminho do script
        """
        try:
            if os.path.exists(self.config_file):
                self.config.read(self.config_file)
            
            if 'SCRIPT' not in self.config:
                self.config['SCRIPT'] = {}
            
            self.config['SCRIPT']['arquivo'] = script_path.strip()
            
            with open(self.config_file, 'w') as f:
                self.config.write(f)
                
        except Exception as e:
            raise ConfigurationError(f"Erro ao atualizar caminho do script: {e}")
    
    def load_script_action(self, script_path: str) -> ScriptAction:
        """
        Carrega ação do arquivo de script.
        
        Args:
            script_path: Caminho do arquivo de script
            
        Returns:
            Ação do script carregada
            
        Raises:
            ConfigurationError: Se houver erro ao carregar script
        """
        try:
            if not os.path.exists(script_path):
                raise ConfigurationError(f"Arquivo de script não encontrado: {script_path}")
            
            script_config = configparser.ConfigParser()
            script_config.read(script_path)
            
            if 'ACAO' not in script_config or 'VARIAVEIS' not in script_config:
                raise ConfigurationError("Script deve conter seções [ACAO] e [VARIAVEIS]")
            
            acao_section = dict(script_config['ACAO'])
            variaveis_section = dict(script_config['VARIAVEIS'])
            
            return ScriptAction.from_config_sections(acao_section, variaveis_section)
            
        except Exception as e:
            if isinstance(e, ConfigurationError):
                raise
            raise ConfigurationError(f"Erro ao carregar script: {e}")