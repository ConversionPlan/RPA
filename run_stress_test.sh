#!/bin/bash

# =============================================================================
# SCRIPT DE EXECUCAO DO STRESS TEST - INBOUND FILE PROCESSING
# =============================================================================
# Uso:
#   ./run_stress_test.sh                    # Executa teste rapido de validacao
#   ./run_stress_test.sh quick              # Teste rapido (2 arquivos)
#   ./run_stress_test.sh manual             # Apenas Manual Upload (gradual)
#   ./run_stress_test.sh electronic         # Apenas Electronic File (gradual)
#   ./run_stress_test.sh comparison         # Teste comparativo
#   ./run_stress_test.sh limit-manual       # Descobre limite do Manual Upload
#   ./run_stress_test.sh limit-electronic   # Descobre limite do Electronic File
#   ./run_stress_test.sh all                # Executa todos os testes
#   ./run_stress_test.sh headless           # Executa sem interface grafica
# =============================================================================

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Diretorio do projeto
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

# Ativar venv se existir
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Funcao de ajuda
show_help() {
    echo -e "${BLUE}============================================================${NC}"
    echo -e "${BLUE}  STRESS TEST - INBOUND FILE PROCESSING${NC}"
    echo -e "${BLUE}============================================================${NC}"
    echo ""
    echo -e "Uso: ${GREEN}./run_stress_test.sh [opcao]${NC}"
    echo ""
    echo "Opcoes:"
    echo -e "  ${YELLOW}quick${NC}              Teste rapido de validacao (2 arquivos)"
    echo -e "  ${YELLOW}manual${NC}             Testes graduais de Manual Upload (5-100 arquivos)"
    echo -e "  ${YELLOW}electronic${NC}         Testes graduais de Electronic File (5-50 arquivos)"
    echo -e "  ${YELLOW}comparison${NC}         Teste comparativo entre os dois metodos"
    echo -e "  ${YELLOW}limit-manual${NC}       Descobre limite maximo do Manual Upload"
    echo -e "  ${YELLOW}limit-electronic${NC}   Descobre limite maximo do Electronic File"
    echo -e "  ${YELLOW}all${NC}                Executa todos os testes"
    echo -e "  ${YELLOW}headless${NC}           Adiciona modo headless (sem interface grafica)"
    echo ""
    echo "Exemplos:"
    echo -e "  ${GREEN}./run_stress_test.sh quick${NC}"
    echo -e "  ${GREEN}./run_stress_test.sh manual headless${NC}"
    echo -e "  ${GREEN}HEADLESS=True ./run_stress_test.sh all${NC}"
    echo ""
}

# Verificar argumentos
MODE=${1:-"quick"}
HEADLESS_FLAG=""

# Verificar se headless foi passado como segundo argumento
if [ "$2" == "headless" ] || [ "$MODE" == "headless" ]; then
    export HEADLESS=True
    HEADLESS_FLAG=" (Modo Headless)"
    if [ "$MODE" == "headless" ]; then
        MODE="quick"
    fi
fi

# Criar diretorio de relatorios
mkdir -p report/stress_test

echo -e "${BLUE}============================================================${NC}"
echo -e "${BLUE}  INICIANDO STRESS TEST${HEADLESS_FLAG}${NC}"
echo -e "${BLUE}============================================================${NC}"
echo ""
echo -e "Data/Hora: $(date '+%Y-%m-%d %H:%M:%S')"
echo -e "Modo: ${YELLOW}${MODE}${NC}"
echo ""

# Executar teste baseado no modo
case $MODE in
    "quick")
        echo -e "${GREEN}Executando teste rapido de validacao...${NC}"
        python -m behave features/98-stress-test-inbound.feature --tags=@Quick
        ;;

    "manual")
        echo -e "${GREEN}Executando testes de Manual Upload (gradual)...${NC}"
        python -m behave features/98-stress-test-inbound.feature --tags=@ManualUpload
        ;;

    "electronic")
        echo -e "${GREEN}Executando testes de Electronic File (gradual)...${NC}"
        python -m behave features/98-stress-test-inbound.feature --tags=@ElectronicFile
        ;;

    "comparison")
        echo -e "${GREEN}Executando teste comparativo...${NC}"
        python -m behave features/98-stress-test-inbound.feature --tags=@Comparison
        ;;

    "limit-manual")
        echo -e "${GREEN}Descobrindo limite do Manual Upload...${NC}"
        python -m behave features/98-stress-test-inbound.feature --tags=@SystemLimit --tags=@Manual
        ;;

    "limit-electronic")
        echo -e "${GREEN}Descobrindo limite do Electronic File...${NC}"
        python -m behave features/98-stress-test-inbound.feature --tags=@SystemLimit --tags=@Electronic
        ;;

    "all")
        echo -e "${GREEN}Executando todos os testes de stress...${NC}"
        python -m behave features/98-stress-test-inbound.feature --tags=@StressTest
        ;;

    "help"|"-h"|"--help")
        show_help
        exit 0
        ;;

    *)
        echo -e "${RED}Opcao invalida: ${MODE}${NC}"
        show_help
        exit 1
        ;;
esac

# Verificar resultado
EXIT_CODE=$?

echo ""
echo -e "${BLUE}============================================================${NC}"
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}  STRESS TEST CONCLUIDO COM SUCESSO${NC}"
else
    echo -e "${RED}  STRESS TEST CONCLUIDO COM ERROS${NC}"
fi
echo -e "${BLUE}============================================================${NC}"
echo ""
echo -e "Relatorios salvos em: ${YELLOW}report/stress_test/${NC}"
echo ""

# Listar relatorios gerados
if [ -d "report/stress_test" ]; then
    echo "Ultimos relatorios:"
    ls -lt report/stress_test/*.txt 2>/dev/null | head -5
fi

exit $EXIT_CODE
