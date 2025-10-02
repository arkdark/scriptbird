"""
Exceções customizadas do ScriptBird.
"""


class ScriptBirdException(Exception):
    """Exceção base do ScriptBird."""
    pass


class DatabaseConnectionError(ScriptBirdException):
    """Erro de conexão com o banco de dados."""
    pass


class DatabaseQueryError(ScriptBirdException):
    """Erro na execução de query no banco."""
    pass


class ScriptConfigurationError(ScriptBirdException):
    """Erro na configuração do script."""
    pass


class ScriptExecutionError(ScriptBirdException):
    """Erro na execução do script."""
    pass


class FileOperationError(ScriptBirdException):
    """Erro em operações de arquivo."""
    pass


class ConfigurationError(ScriptBirdException):
    """Erro de configuração geral."""
    pass