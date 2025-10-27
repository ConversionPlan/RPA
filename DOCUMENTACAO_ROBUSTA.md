# Documentação Abrangente do Projeto RPA

## 1. Visão Geral

Este projeto é um conjunto de automações de Processos Robóticos (RPA) para o portal Track Trace RX. Ele automatiza diversas operações do portal, como login, gerenciamento de produtos, parceiros comerciais, localidades, processos de entrada e saída de mercadorias, inventário, fabricação e containers. Os testes são executados automaticamente após cada push para a branch `main` e diariamente às 6h da manhã. Também podem ser executados localmente para desenvolvimento e validação.

## 2. Tecnologias Utilizadas

* **Python**: Linguagem de programação principal.
* **Behave**: Framework BDD (Behavior-Driven Development) para Python, utilizado para estruturar e executar os testes.
* **Selenium WebDriver**: Ferramenta para automação de navegadores web, utilizada para interagir com o portal Track Trace RX.
* **WebDriver Manager**: Gerencia automaticamente as versões do driver do navegador (ex: ChromeDriver).
* **ReportLab**: Utilizado para gerar relatórios em PDF.
* **Faker**: Gera dados falsos para testes.
* **Slack SDK**: Integração com o Slack para notificações.
* **python-dotenv**: Carrega variáveis de ambiente de um arquivo `.env`.

## 3. Estrutura do Projeto

```
RPA-main/
├── .env                      # Arquivo de variáveis de ambiente (ex: token do Slack)
├── .gitignore                # Arquivo para ignorar arquivos/diretórios no Git
├── DOCUMENTACAO_ROBUSTA.md   # Esta documentação
├── QWEN.md                   # Documentação gerada automaticamente
├── README.md                 # Instruções básicas de execução
├── requirements.txt          # Lista de dependências Python
├── features/                 # Diretório contendo os testes BDD
│   ├── steps/                # Implementação dos passos dos testes (Python)
│   │   ├── __pycache__/      # Diretório de cache do Python
│   │   ├── auth.py           # Passos relacionados ao login
│   │   ├── container.py      # Passos relacionados a containers
│   │   ├── epcis-generator.py # Geração de arquivos EPCIS
│   │   ├── inbound.py        # Passos relacionados a processos de entrada
│   │   ├── inventory.py      # Passos relacionados ao inventário
│   │   ├── location.py       # Passos relacionados a localidades
│   │   ├── manufacture.py    # Passos relacionados à fabricação
│   │   ├── outbound.py       # Passos relacionados a processos de saída
│   │   ├── performance-test.py # Testes de performance
│   │   ├── product.py        # Passos relacionados a produtos
│   │   ├── trading_partner.py # Passos relacionados a parceiros comerciais
│   │   └── utils.py          # Funções utilitárias
│   ├── 01-login.feature      # Cenários de teste para login
│   ├── 02-product.feature    # Cenários de teste para produtos
│   ├── 03-trading-partner.feature # Cenários de teste para parceiros comerciais
│   ├── 04-location.feature   # Cenários de teste para localidades
│   ├── 05-inbound.feature    # Cenários de teste para processos de entrada
│   ├── 06-outbound.feature   # Cenários de teste para processos de saída
│   ├── 07-inventory.feature  # Cenários de teste para inventário
│   ├── 08-manufacture.feature # Cenários de teste para fabricação
│   ├── 09-container.feature  # Cenários de teste para containers
│   └── 99-performance-test.feature # Cenários de teste de performance
├── report/                   # Diretório para armazenar relatórios e resultados
│   ├── output/               # Diretório para saídas intermediárias
│   └── test_times.json       # Arquivo JSON com tempos de execução dos testes
└── __pycache__/              # Diretório de cache do Python (gerado automaticamente)
```

## 4. Instalação e Configuração

### 4.1. Pré-requisitos

* Python 3.7 ou superior instalado.
* Acesso ao portal Track Trace RX (ambiente de QA).
* (Opcional) Conta no Slack para notificações.

### 4.2. Instalação das Dependências

1. Navegue até o diretório raiz do projeto.
2. Execute o comando:
   ```bash
   pip install -r requirements.txt
   ```

### 4.3. Configuração do Ambiente

* Crie um arquivo `.env` na raiz do projeto (se ainda não existir) e adicione as variáveis de ambiente necessárias, como o token do Slack:
  ```
  SLACK_BOT_TOKEN = "seu_token_aqui"
  ```

## 5. Execução dos Testes

### 5.1. Executar Todos os Testes

Para executar todos os testes definidos:

```bash
behave
```

### 5.2. Executar um Teste Específico

Para executar apenas um arquivo de feature específico:

```bash
behave .\features\{NOME_DO_ARQUIVO.feature}
```

Exemplo:
```bash
behave .\features\01-login.feature
```

### 5.3. Executar em Modo Headless

Para executar os testes sem abrir o navegador (modo headless):

```bash
HEADLESS=True behave
```

Ou para um teste específico:

```bash
HEADLESS=True behave .\features\01-login.feature
```

## 6. Geração de Relatórios

### 6.1. Gerar Arquivo JSON de Resultados

Para gerar um arquivo JSON com os resultados dos testes:

```bash
behave --format json.pretty --outfile report\output\results.json
```

### 6.2. Gerar Relatório PDF

Para gerar o relatório em PDF a partir do arquivo JSON gerado:

```bash
python .\reports\generate_pdf_py
```

O relatório PDF será salvo em: `.\\reports\\Track_Validation.pdf`

## 7. Desenvolvimento e Manutenção

### 7.1. Estrutura dos Testes (BDD)

Os testes são escritos em Gherkin (`.feature`) e implementados em Python (`.py`).

* **Feature Files (`.feature`)**: Descrevem os cenários de teste em linguagem natural (Given, When, Then).
* **Step Definitions (`.py`)**: Contêm a implementação em Python dos passos definidos nos arquivos `.feature`.

### 7.2. Adicionando Novos Testes

1. Crie um novo arquivo `.feature` no diretório `features/`.
2. Defina os cenários de teste usando a sintaxe Gherkin.
3. Crie ou modifique os arquivos de step definitions em `features/steps/` para implementar os passos dos novos cenários.
4. Execute os testes para verificar o funcionamento.

### 7.3. Boas Práticas

* **Nomes Descritivos**: Use nomes claros e descritivos para features, cenários e funções.
* **Reutilização de Steps**: Crie steps genéricos que possam ser reutilizados em diferentes cenários.
* **Tratamento de Erros**: Implemente tratamento de exceções adequado para lidar com falhas inesperadas.
* **Esperas Explícitas**: Utilize `WebDriverWait` para esperar que elementos estejam presentes ou interativos, em vez de `time.sleep`.
* **Seletores Robustos**: Prefira seletores que sejam menos propensos a mudanças na estrutura HTML (ex: IDs, classes específicas) em vez de XPath complexos.