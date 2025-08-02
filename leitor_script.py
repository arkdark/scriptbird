import configparser
import os
import fdb
import csv
import pandas as pd
import time
import threading
from PyQt5.QtCore import pyqtSignal, QObject


def ler_config(path):
    config = configparser.ConfigParser()
    config.read(path)
    return config

def executar_query(db_config, query):
    caminho = db_config['caminho'].strip()
    usuario = db_config['usuario'].strip()
    senha = db_config['senha'].strip()
    porta = str(db_config['porta']).strip()

    # Interpreta HOST|CAMINHO ou apenas CAMINHO
    if "|" in caminho:
        host, caminho_banco = caminho.split("|", 1)
    else:
        host = "localhost"
        caminho_banco = caminho

    # Define o DSN dependendo se é arquivo local ou caminho remoto
    if os.path.isfile(caminho_banco):
        dsn = caminho_banco
    else:
        dsn = f"{host}:{caminho_banco}"
        if porta:
            dsn = f"{dsn}?port={porta}"

    # Conecta e executa a query
    con = fdb.connect(
        dsn=dsn,
        user=usuario,
        password=senha
    )
    cur = con.cursor()
    cur.execute(query)
    colunas = [desc[0] for desc in cur.description]
    dados = cur.fetchall()
    con.close()
    return colunas, dados

def salvar_em_arquivo(variaveis, db_config):
    query = variaveis['QUERY']
    caminho = variaveis['CAMINHO'].strip()
    nome_arquivo = variaveis['NOME_ARQUIVO'].strip()
    formato = variaveis.get('FORMATO', '.xlsx').strip().lower()
    tempo_entre_execucoes = int(variaveis.get('TEMPO_ENTRE_EXECUCOES', 3600))
    repetir = variaveis.get('REPETIR', 'N').strip().upper() == 'S'

    while True:
        # Executa a query
        colunas, dados = executar_query(db_config, query)
        os.makedirs(caminho, exist_ok=True)
        arquivo = os.path.join(caminho, nome_arquivo + formato)
        if formato == '.csv':
            with open(arquivo, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(colunas)
                writer.writerows(dados)
        elif formato == '.txt':
            with open(arquivo, 'w', encoding='utf-8') as f:
                f.write('\t'.join(colunas) + '\n')
                for linha in dados:
                    f.write('\t'.join(map(str, linha)) + '\n')
        elif formato == '.xlsx':
            df = pd.DataFrame(dados, columns=colunas)
            df.to_excel(arquivo, index=False)
        else:
            raise ValueError("Formato não suportado.")

        if not repetir:
            break
        time.sleep(tempo_entre_execucoes)

def main():
    # Ler Config do Bot
    config = ler_config('config.ini')

    # Configuração do Banco de Dados
    db_config = config['DB'] 

    # Configuração do Script
    st_config = config['SCRIPT'] 

    # Caminho do Script
    script = ler_config(st_config['arquivo']) 
    
    # Extraindo Ação do script    
    acao = script['ACAO']
    variaveis = script['VARIAVEIS']

    if acao == "SALVAR_EM_ARQUIVO":
        salvar_em_arquivo(variaveis, db_config)
    elif acao == "EXECUTAR_QUERY":
        pass
    else:
        raise ValueError(f"Ação '{acao}' não reconhecida no script.")

if __name__ == "__main__":
    main()

class ScriptExecutor(QObject):
    finished = pyqtSignal()

    def __init__(self, log_callback=None):
        super().__init__()
        self._running = threading.Event()
        self._running.set()
        self.log = log_callback or print
        self._thread = threading.Thread(target=self.run)

    def start(self):
        self._thread.start()

    def stop(self):
        self._running.clear()

    def is_alive(self):
        return self._thread.is_alive()

    def join(self):
        self._thread.join()

    def run(self):
        try:
            self.log("Iniciando execução do BOT...")
            config = ler_config('config.ini')
            db_config = config['DB']
            st_config = config['SCRIPT']
            self.log(f"Carregando script: {st_config['arquivo']}")

            script = ler_config(st_config['arquivo'])
            acao = script['ACAO']
            acao = acao['EXECUTAR']
            variaveis = script['VARIAVEIS']
            self.log(f"Ação a ser executada: {acao}")

            if acao == "SALVAR_EM_ARQUIVO":
                self._salvar_em_arquivo(variaveis, db_config)
            else:
                self.log(f"Ação '{acao}' não reconhecida.")
        except Exception as e:
            self.log(f"Erro durante execução do BOT: {e}")
        finally:
            self.finished.emit()

    def _salvar_em_arquivo(self, variaveis, db_config):
        query = variaveis['QUERY']
        caminho = variaveis['CAMINHO'].strip()
        nome_arquivo = variaveis['NOME_ARQUIVO'].strip()
        formato = variaveis.get('FORMATO', '.xlsx').strip().lower()
        tempo_entre_execucoes = int(variaveis.get('TEMPO_ENTRE_EXECUCOES', 3600))
        repetir = variaveis.get('REPETIR', 'N').strip().upper() == 'S'

        while self._running.is_set():
            try:
                colunas, dados = executar_query(db_config, query)
                os.makedirs(caminho, exist_ok=True)
                arquivo = os.path.join(caminho, nome_arquivo + formato)

                if formato == '.csv':
                    with open(arquivo, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerow(colunas)
                        writer.writerows(dados)
                elif formato == '.txt':
                    with open(arquivo, 'w', encoding='utf-8') as f:
                        f.write('\t'.join(colunas) + '\n')
                        for linha in dados:
                            f.write('\t'.join(map(str, linha)) + '\n')
                elif formato == '.xlsx':
                    df = pd.DataFrame(dados, columns=colunas)
                    df.to_excel(arquivo, index=False)
                else:
                    self.log(f"Formato não suportado: {formato}")
                    return

                self.log(f"Arquivo gerado com sucesso: {arquivo}")

                if not repetir:
                    break

                for _ in range(tempo_entre_execucoes):
                    if not self._running.is_set():
                        self.log("Execução interrompida.")
                        return
                    time.sleep(1)

            except Exception as e:
                self.log(f"Erro ao processar ciclo do script: {e}")
                break
