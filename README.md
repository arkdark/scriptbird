<div align="center">
  <img src="logos/icone.png" alt="ScriptBird Logo" width="100"/>
</div>

<h1 align="center">ScriptBird</h1>

<p align="center">
  Uma aplicação em Python + PyQt5 que executa scripts automatizados para consultas em banco de dados Firebird.<br>
  Pensada para rodar em segundo plano.
</p>

---

## 🚀 Sobre o Projeto

**ScriptBird** é um assistente automatizado que lê e executa scripts `.ini` programados com ações especificas que podem ser repetitivas. Ideal para tarefas como geração de relatórios ou extrações periódicas.

## 🧠 Funcionalidades

- ✅ Interface em PyQt5 simples e direta.
- ✅ Execução automática ao abrir, com base no `config.ini`.
- ✅ Conexão com banco de dados Firebird local ou remoto.
- ✅ Seleção e leitura de scripts `.ini` externos.
- ✅ Execução de tarefas programadas desde extração de dados ou geração de relatórios com SQL.
- ✅ Ícone na bandeja do sistema com execução em segundo plano.
- ✅ Log detalhado com autorrolagem.

## 💾 Estrutura esperada do script de ação `.ini`

```ini
[VARIAVEIS]
CAMPO1 = VALOR1

[ACAO]
EXECUTAR = FUNCAO_PROGRAMADA_NO_CODIGO
```
> Há um arquivo na pasta Scripts como exemplo do `.ini`

## 🔧 Requisitos

- Python 3.10
- Firebird instalado (cliente ou embedded)
- Bibliotecas:
  - `fdb`
  - `PyQt5`
  - `pandas`
  - `openpyxl`
  - `PyQt5_sip`

Instale com:

```bash
pip install -r requirements.txt
```

## ⚙️ Executando

1. Clone ou baixe este repositório.
2. Crie um ambiente virtual (recomendado):
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
3. Instale as dependências.
4. Execute o app:

   ```bash
   python scriptbird.py
   ```

## 🛠 Compilação para .exe

Utilize o [auto-py-to-exe](https://github.com/brentvollebregt/auto-py-to-exe) para gerar o executável:

- Importe o arquivo `build.json`

## 📂 Arquivo de configuração

O `config.ini` é criado automaticamente após salvar os dados de conexão com o BD no app.

---

## 📸 Captura de Tela
### Interface
<img src="screenshots\Screenshot_1.png" width='500rem'><br>
### Icone na Tray
<img src="screenshots\Screenshot_2.png">

---

## 🧪 Contribuição

Sugestões, melhorias e bugs podem ser abertos como issues.  
Pull requests são bem-vindos!

---

## 📄 Licença

Este projeto está licenciado sob os termos da [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).  
Consulte o arquivo [`LICENSE`](./LICENSE) para mais detalhes.

---

## ☕ Apoie este projeto

Se este projeto te ajudou, considere apoiar com um café:

[![Apoiar via PicPay](https://img.shields.io/badge/PicPay-Apoiar-21C25E?style=for-the-badge&logo=picpay)](https://picpay.me/lucas.t.sousa/5.0)

> Feito com 💻 por Lucas Sousa
