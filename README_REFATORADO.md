# ScriptBird - Versão Refatorada

<div align="center">
  <img src="assets/icons/icon.ico" alt="ScriptBird Logo" width="100"/>
</div>

<h1 align="center">ScriptBird</h1>

<p align="center">
  Uma aplicação em Python + PyQt5 que executa scripts automatizados para consultas em banco de dados Firebird.<br>
  <strong>Versão refatorada com arquitetura limpa e código organizado.</strong>
</p>

---

## 🚀 Sobre o Projeto

**ScriptBird** é um assistente automatizado que lê e executa scripts `.ini` programados com ações específicas que podem ser repetitivas. Ideal para tarefas como geração de relatórios ou extrações periódicas.

### ✨ Melhorias da Refatoração

- 🏗️ **Arquitetura Limpa**: Separação clara entre UI, lógica de negócio e infraestrutura
- 📁 **Organização**: Estrutura de pastas profissional e modular
- 🧪 **Testável**: Código preparado para testes unitários
- 🔧 **Manutenível**: Código mais fácil de entender e modificar
- 🔗 **Reutilizável**: Componentes independentes e reutilizáveis
- 📝 **Documentado**: Código bem documentado com docstrings

## 📂 Nova Estrutura do Projeto

```
scriptbird/
├── src/                          # Código fonte principal
│   ├── core/                     # Lógica de negócio central
│   │   ├── models/              # Modelos de dados
│   │   │   ├── database_config.py
│   │   │   └── script_config.py
│   │   ├── services/            # Serviços de negócio
│   │   │   ├── database_service.py
│   │   │   ├── script_executor.py
│   │   │   └── file_service.py
│   │   └── exceptions/          # Exceções customizadas
│   │       └── scriptbird_exceptions.py
│   ├── infrastructure/          # Detalhes de implementação
│   │   ├── config/
│   │   │   └── config_manager.py
│   │   └── database/
│   │       └── firebird_connection.py
│   ├── ui/                      # Interface do usuário
│   │   ├── main_window.py       # Janela principal refatorada
│   │   ├── generated/           # Arquivos gerados pelo Designer
│   │   │   └── ui_main_window.py
│   │   └── components/          # Componentes reutilizáveis
│   │       └── system_tray.py
│   ├── utils/                   # Utilitários
│   │   ├── logger.py
│   │   └── resource_path.py
│   └── main.py                  # Ponto de entrada principal
├── assets/                      # Recursos estáticos
│   └── icons/
│       └── icon.ico
├── scripts/                     # Scripts de exemplo
│   └── produtos.ini
├── tests/                       # Testes unitários
│   └── test_database_service.py
├── config.ini                   # Configuração
├── requirements.txt
├── setup.py                     # Para instalação
├── scriptbird_refactored.py     # Script compatível com versão original
└── README_REFACTORED.md         # Esta documentação
```

## 🧠 Funcionalidades (Mantidas)

- ✅ Interface em PyQt5 simples e direta
- ✅ Execução automática ao abrir, com base no `config.ini`
- ✅ Conexão com banco de dados Firebird local ou remoto
- ✅ Seleção e leitura de scripts `.ini` externos
- ✅ Execução de tarefas programadas desde extração de dados ou geração de relatórios com SQL
- ✅ Ícone na bandeja do sistema com execução em segundo plano
- ✅ Log detalhado com autorrolagem

## 🔧 Componentes da Nova Arquitetura

### Core (Lógica de Negócio)

- **Models**: `DatabaseConfig`, `ScriptConfig`, `ScriptAction`
- **Services**: `DatabaseService`, `FileService`, `ScriptExecutor`
- **Exceptions**: Exceções customizadas para melhor tratamento de erros

### Infrastructure (Implementação)

- **Config**: `ConfigManager` para gerenciamento de configurações
- **Database**: `FirebirdConnection` para conexão com banco

### UI (Interface)

- **MainWindow**: Janela principal refatorada
- **SystemTray**: Componente de sistema tray reutilizável
- **Generated**: Arquivos gerados pelo Qt Designer

### Utils (Utilitários)

- **Logger**: Sistema de logging customizado
- **ResourcePath**: Resolução de caminhos para recursos

## ⚙️ Executando a Versão Refatorada

### Opção 1: Usando o script compatível
```bash
python scriptbird_refactored.py
```

### Opção 2: Executando diretamente
```bash
cd src
python main.py
```

### Opção 3: Instalação como pacote
```bash
pip install -e .
scriptbird
```

## 🧪 Executando Testes

```bash
python -m pytest tests/
```

ou

```bash
cd tests
python -m unittest discover
```

## 📋 Requisitos (Mantidos)

- Python 3.8+
- Firebird instalado (cliente ou embedded)
- Bibliotecas (mesmo requirements.txt):
  - `fdb`
  - `PyQt5`
  - `pandas`
  - `openpyxl`
  - `PyQt5_sip`

## 🔄 Migração da Versão Original

A nova estrutura é **totalmente compatível** com a versão original:

1. **Configurações**: O mesmo `config.ini` é utilizado
2. **Scripts**: Os mesmos arquivos `.ini` de script funcionam
3. **Interface**: A interface é idêntica à original
4. **Funcionalidades**: Todas as funcionalidades são mantidas

### Arquivos Originais Mapeados

| Arquivo Original | Novo Local |
|-----------------|------------|
| `scriptbird.py` | `src/ui/main_window.py` |
| `leitor_script.py` | `src/core/services/script_executor.py` |
| `scriptbird_ui.py` | `src/ui/generated/ui_main_window.py` |

## 🏗 Benefícios da Refatoração

### 1. **Separação de Responsabilidades**
- Cada classe tem uma responsabilidade específica
- Facilita manutenção e testes

### 2. **Código Mais Limpo**
- Eliminação de código duplicado
- Melhor organização de imports
- Tratamento de erros consistente

### 3. **Extensibilidade**
- Fácil adição de novos tipos de ação
- Novos formatos de arquivo
- Diferentes tipos de banco de dados

### 4. **Testabilidade**
- Componentes isolados e testáveis
- Mocks e stubs facilmente implementáveis

### 5. **Profissionalismo**
- Estrutura que segue boas práticas
- Código que inspira confiança
- Documentação clara

## 📄 Licença

Este projeto continua licenciado sob os termos da [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).

---

## 🤝 Comparação: Antes vs Depois

### Antes (Estrutura Original)
```
scriptbird/
├── scriptbird.py          # 302 linhas - UI + lógica + config
├── leitor_script.py       # 200 linhas - funções soltas + classes
├── scriptbird_ui.py       # Gerado automaticamente
├── config.ini
├── requirements.txt
└── scripts/
```

### Depois (Estrutura Refatorada)
```
scriptbird/
├── src/                   # Código organizado por responsabilidade
│   ├── core/             # Lógica de negócio isolada
│   ├── infrastructure/   # Detalhes de implementação
│   ├── ui/              # Interface separada
│   └── utils/           # Utilitários reutilizáveis
├── tests/               # Testes unitários
├── assets/              # Recursos organizados
└── setup.py             # Instalação profissional
```

A refatoração mantém **100% da funcionalidade original** enquanto torna o código **muito mais profissional, organizando e manutenível**.