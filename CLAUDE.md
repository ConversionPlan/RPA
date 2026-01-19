# RPA Project - Automação de Testes

## Visão Geral
Projeto de automação de testes RPA para o portal Track Trace RX usando Behave/BehavEX.

## Stack Tecnológica
- **Framework de Testes**: Behave (BDD) / BehavEX
- **Linguagem**: Python 3.13+
- **Automação de Browser**: Selenium + ChromeDriver
- **Formato de Testes**: Gherkin (.feature files)

## Estrutura do Projeto
```
features/
  ├── steps/              # Implementação dos steps (Python)
  │   ├── auth.py         # Login e autenticação
  │   ├── product.py      # CRUD de produtos
  │   ├── trading_partner.py  # Vendors e Customers
  │   ├── location.py     # Localizações
  │   ├── inbound.py      # Recebimentos
  │   ├── outbound.py     # Expedições
  │   ├── inventory.py    # Inventário
  │   ├── manufacture.py  # Manufatura
  │   ├── container.py    # Containers
  │   └── utils.py        # Funções utilitárias
  ├── *.feature           # Cenários de teste
  └── environment.py      # Hooks do Behave
report/
  ├── output/             # Resultados dos testes
  ├── bot.py              # Bot do Slack
  └── print_errors.py     # Análise de erros
```

## Comandos Principais

### Executar todos os testes
```bash
source venv/bin/activate
HEADLESS=True python -m behave
```

### Executar feature específica
```bash
HEADLESS=True python -m behave features/01-login.feature
```

### Executar com BehavEX (paralelo)
```bash
HEADLESS=True behavex --parallel-processes 4 --parallel-scheme feature -o report/output
```

### Executar com relatório JSON
```bash
HEADLESS=True python -m behave --format json.pretty --outfile report/output/results.json
```

## Comandos Customizados
- `/run-tests [args]` - Executa testes
- `/auto-fix-tests [args]` - Executa, analisa erros e corrige automaticamente

## Problemas Comuns e Soluções

### Chrome não inicia (DevToolsActivePort error)
- **Causa**: Configuração headless incompatível
- **Arquivo**: `features/steps/auth.py` função `launchBrowser`
- **Solução**: Verificar opções `--no-sandbox`, `--disable-dev-shm-usage`

### Timeout em elementos
- **Causa**: Elemento demora para carregar
- **Arquivo**: `features/steps/utils.py`
- **Solução**: Aumentar `WebDriverWait` timeout

### Modal não fecha
- **Causa**: Modal ainda animando
- **Arquivo**: `features/steps/stability_improvements.py`
- **Solução**: Adicionar `time.sleep()` ou wait explícito

### Login falha
- **Causa**: Credenciais ou URL incorretas
- **Arquivo**: `features/steps/auth.py`
- **Verificar**: URL do portal e credenciais

## Variáveis de Ambiente
- `HEADLESS` - True/False para modo headless do Chrome
- `SLACK_BOT_TOKEN` - Token do bot do Slack para notificações

## CI/CD
Pipeline configurada em `.github/workflows/github-actions.yml`:
- Executa a cada push na main
- Executa a cada 3 horas (cron)
- Posta resultados no Slack
- Gera PDF de relatório
- Upload para MinIO

## Credenciais de Teste
- URL: https://qualityportal.qa-test.tracktraceweb.com/auth
- Usuário: teste@teste.com
- Senha: Mudar@12345343
