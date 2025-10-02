"""
Serviço para operações de arquivo.
"""
import csv
import os
from typing import List, Tuple

import pandas as pd

from core.exceptions.scriptbird_exceptions import FileOperationError


class FileService:
    """Serviço para operações de arquivo."""
    
    @staticmethod
    def save_to_file(
        columns: List[str], 
        data: List[Tuple], 
        file_path: str, 
        file_format: str = '.xlsx'
    ):
        """
        Salva dados em arquivo.
        
        Args:
            columns: Nomes das colunas
            data: Dados a serem salvos
            file_path: Caminho completo do arquivo
            file_format: Formato do arquivo (.xlsx, .csv, .txt)
            
        Raises:
            FileOperationError: Se houver erro ao salvar arquivo
        """
        try:
            # Cria diretório se não existir
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            file_format = file_format.lower().strip()
            
            if file_format == '.csv':
                FileService._save_to_csv(columns, data, file_path)
            elif file_format == '.txt':
                FileService._save_to_txt(columns, data, file_path)
            elif file_format == '.xlsx':
                FileService._save_to_xlsx(columns, data, file_path)
            else:
                raise FileOperationError(f"Formato não suportado: {file_format}")
                
        except Exception as e:
            if isinstance(e, FileOperationError):
                raise
            raise FileOperationError(f"Erro ao salvar arquivo: {e}")
    
    @staticmethod
    def _save_to_csv(columns: List[str], data: List[Tuple], file_path: str):
        """Salva dados em arquivo CSV."""
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(columns)
            writer.writerows(data)
    
    @staticmethod
    def _save_to_txt(columns: List[str], data: List[Tuple], file_path: str):
        """Salva dados em arquivo TXT."""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\t'.join(columns) + '\n')
            for row in data:
                f.write('\t'.join(map(str, row)) + '\n')
    
    @staticmethod
    def _save_to_xlsx(columns: List[str], data: List[Tuple], file_path: str):
        """Salva dados em arquivo Excel."""
        df = pd.DataFrame(data, columns=columns)
        df.to_excel(file_path, index=False)
    
    @staticmethod
    def ensure_directory_exists(file_path: str):
        """
        Garante que o diretório do arquivo existe.
        
        Args:
            file_path: Caminho do arquivo
        """
        directory = os.path.dirname(file_path)
        if directory:
            os.makedirs(directory, exist_ok=True)