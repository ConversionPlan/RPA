#!/bin/bash
# Script para rodar testes RPA e postar resultados no Slack
# Executado a cada 3 horas via cron

# Definir PATH completo (cron não herda o PATH do sistema)
export PATH="/usr/local/bin:/usr/bin:/bin:/home/filipe/.local/bin:$PATH"

# Diretório do projeto
PROJECT_DIR="/home/filipe/Área de trabalho/RPA"
LOG_FILE="/tmp/rpa_tests.log"

# Iniciar log
echo "========================================" >> "$LOG_FILE"
echo "[$(date)] Iniciando execução dos testes" >> "$LOG_FILE"

# Entrar no diretório
cd "$PROJECT_DIR" || { echo "[$(date)] ERRO: Não foi possível entrar no diretório" >> "$LOG_FILE"; exit 1; }

# Limpar processos anteriores
pkill -9 chrome 2>/dev/null
pkill -9 chromedriver 2>/dev/null
sleep 2

# Ativar ambiente virtual
source "$PROJECT_DIR/venv/bin/activate" || { echo "[$(date)] ERRO: Não foi possível ativar venv" >> "$LOG_FILE"; exit 1; }

# Limpar resultados anteriores
rm -f report/output/results.json report/output/report.json

# Rodar testes
export HEADLESS=True
echo "[$(date)] Iniciando behave..." >> "$LOG_FILE"
python -m behave --tags="~@skip" --format json.pretty --outfile report/output/results.json 2>> "$LOG_FILE"
BEHAVE_EXIT=$?
echo "[$(date)] Behave finalizado com código: $BEHAVE_EXIT" >> "$LOG_FILE"

# Verificar se o arquivo de resultados foi criado
if [ -f "report/output/results.json" ]; then
    echo "[$(date)] Arquivo results.json criado com sucesso" >> "$LOG_FILE"
else
    echo "[$(date)] ERRO: Arquivo results.json não foi criado" >> "$LOG_FILE"
fi

# Postar no Slack
echo "[$(date)] Postando no Slack..." >> "$LOG_FILE"
python report/bot.py 2>> "$LOG_FILE"
SLACK_EXIT=$?
echo "[$(date)] Slack bot finalizado com código: $SLACK_EXIT" >> "$LOG_FILE"

echo "[$(date)] Execução finalizada" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"
