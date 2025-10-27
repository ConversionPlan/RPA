# Documento de Falhas Identificadas no Projeto RPA

Este documento detalha as falhas identificadas durante a execução dos testes automatizados do projeto RPA. O objetivo é categorizar os erros, identificar suas causas prováveis e propor soluções ou áreas de investigação para correção.

## 1. Resumo dos Resultados da Execução

Na execução recente dos testes com o comando `behave`, foram observados os seguintes resultados:

*   **Total de Cenários:** 23
*   **Cenários com Sucesso:** 2
*   **Cenários com Falhas:** 0
*   **Cenários com Erros:** 21

A taxa de sucesso foi muito baixa (apenas 2 cenários passaram), indicando problemas generalizados no conjunto de testes ou no ambiente de teste.

## 2. Análise de Falhas por Categoria

### 2.1. `NoSuchElementException` (Erro mais frequente)

#### 2.1.1. Descrição
Esta exceção ocorre quando o Selenium WebDriver não consegue localizar um elemento na página usando o seletor especificado (XPath, ID, etc.). O elemento simplesmente não está presente no DOM no momento em que o script tenta interagir com ele.

#### 2.1.2. Padrões Identificados
Vários padrões de erro `NoSuchElementException` foram identificados:

1.  **Sidebar Menu Toggle**:
    *   **Seletor XPath:** `//div[contains(@class, 'sidebar_menu_toggle_dis')]/a`
    *   **Localização:** Função `open_sandwich_menu` no arquivo `features/steps/product.py`, linha 54.
    *   **Impacto:** Esta falha afeta praticamente todos os testes que requerem navegação pelo menu, pois o menu não é aberto.
    *   **Causa Provável:** O seletor XPath pode estar desatualizado em relação à estrutura HTML atual do portal. É comum que classes CSS como `sidebar_menu_toggle_dis` sejam dinâmicas e mudem de nome com base no estado do elemento (ex: `sidebar_menu_toggle_en` quando habilitado).

2.  **Manufacture Lot and Serial Request**:
    *   **Seletor XPath:** `//label[text()='Manufacture Lot and Serial Request']`
    *   **Localização:** Função `click_manufacture_lot_serial_request` no arquivo `features/steps/manufacture.py`, linha 160.
    *   **Impacto:** Afeta os testes relacionados à funcionalidade de fabricação.
    *   **Causa Provável:** O texto do label pode ter sido alterado no portal ou o elemento pode não estar sendo carregado corretamente.

#### 2.1.3. Causas Prováveis Gerais
1.  **Mudança na Interface do Usuário (UI):** A estrutura HTML do portal Track Trace RX pode ter sido alterada, tornando os seletores XPath e ID obsoletos.
2.  **Timing Issues (Problemas de Timing):** O script pode estar tentando encontrar o elemento antes que ele seja carregado ou renderizado completamente. Isso é comum em aplicações web modernas com carregamento assíncrono.
3.  **Seletores Frágeis:** O uso excessivo de XPath complexos pode tornar os testes frágeis a pequenas mudanças na estrutura da página.

#### 2.1.4. Soluções Propostas
1.  **Atualizar Seletores:** Verificar manualmente a estrutura HTML das páginas no navegador (usando DevTools) e atualizar os seletores XPath/ID nos arquivos `.py`.
2.  **Implementar Esperas Explícitas:** Substituir `time.sleep` e `find_element` direto por `WebDriverWait` com condições esperadas (Expected Conditions) como `element_to_be_clickable` ou `presence_of_element_located`. Isso garante que o script espere até que o elemento esteja realmente disponível.
    ```python
    # Exemplo de espera explícita
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    wait = WebDriverWait(context.driver, 10) # Espera até 10 segundos
    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'sidebar_menu_toggle_en')]/a")))
    element.click()
    ```
3.  **Melhorar Tratamento de Erros:** Adicionar logs mais detalhados nos blocos `except` para facilitar a identificação de qual elemento específico está faltando.

### 2.2. `SessionNotCreatedException`

#### 2.2.1. Descrição
Esta exceção ocorre quando o Selenium não consegue iniciar uma nova sessão do navegador. Isso pode acontecer por diversos motivos relacionados à configuração do ambiente.

#### 2.2.2. Padrões Identificados

1.  **Browser Disconnection**:
    *   **Mensagem de Erro:** "session not created from disconnected: unable to connect to renderer"
    *   **Localização:** Ocorreu durante o teste de performance do dashboard.
    *   **Causa Provável:** O navegador Chrome pode estar travando ou desconectando durante a criação da sessão. Isso pode ser devido a:
        *   **Incompatibilidade Chrome/ChromeDriver:** A versão do Chrome instalada localmente (140.0.7339.127) pode não ser compatível com a versão do ChromeDriver gerenciada pelo `webdriver-manager`.
        *   **Recursos do Sistema:** O sistema pode estar ficando sem memória ou CPU durante a inicialização do Chrome.
        *   **Opções do Chrome:** Alguma das opções específicas definidas no `auth.py` (como `--remote-debugging-port=9222` ou outras) pode estar causando instabilidade.

2.  **AttributeError subsequente**:
    *   **Mensagem de Erro:** "'Context' object has no attribute 'driver'"
    *   **Localização:** Ocorreu ao tentar fechar o driver (`context.driver.close()`) dentro da função `ends_timer` após uma `SessionNotCreatedException`.
    *   **Causa Provável:** Como a sessão não foi criada com sucesso, o atributo `context.driver` nunca foi inicializado. O código de tratamento de erro está tentando usar um objeto que não existe.

#### 2.2.3. Soluções Propostas
1.  **Verificar Compatibilidade Chrome/ChromeDriver:** Garantir que a versão do ChromeDriver seja compatível com a versão do Chrome instalada. Considere especificar uma versão fixa do ChromeDriver no código ou atualizar o Chrome.
2.  **Monitorar Recursos do Sistema:** Durante a execução dos testes, monitore o uso de memória e CPU para identificar se há gargalos.
3.  **Minimizar Opções do Chrome:** Tentar executar os testes com um conjunto mínimo de opções no `Options()` para identificar se alguma opção específica está causando o problema.
4.  **Corrigir Tratamento de Erros:** No `ends_timer`, verificar se `context.driver` existe antes de tentar fechá-lo:
    ```python
    # Em features/steps/auth.py, função ends_timer
    def ends_timer(context, e=None):
        # ... código existente para log de erro ...
        
        # Verificar se o driver foi inicializado antes de tentar fechar
        if hasattr(context, 'driver') and context.driver is not None:
            try:
                context.driver.close()
            except Exception as close_error:
                print(f"Erro ao fechar o driver: {close_error}")
        else:
            print("Driver não inicializado, pulando fechamento.")
        
        # ... restante do código ...
    ```

## 3. Outras Considerações

*   **Ambiente de Teste:** O README menciona que alguns testes (como o de EPCIS Inbound) estão bloqueados no ambiente de QA. Isso pode explicar parte das falhas, mas não justifica a maioria dos erros de `NoSuchElementException`.
*   **Dados de Teste:** Certifique-se de que os dados de teste (usuário, senha, URLs) estão corretos e que o ambiente de QA está acessível e estável.

## 4. Próximos Passos Recomendados

1.  **Priorizar Correção do Menu:** Como a falha no menu afeta a maioria dos testes, corrigir o seletor `//div[contains(@class, 'sidebar_menu_toggle_dis')]/a` deve ser a primeira prioridade.
2.  **Revisar Todos os Seletores:** Realizar uma revisão sistemática de todos os seletores XPath e ID nos arquivos de steps para atualizá-los conforme a UI atual.
3.  **Implementar Esperas Explícitas:** Substituir todas as esperas implícitas (`time.sleep`) e buscas diretas por esperas explícitas.
4.  **Testar Compatibilidade:** Verificar e, se necessário, atualizar a versão do ChromeDriver.
5.  **Executar Testes Individualmente:** Após as correções, executar os testes individualmente para validar cada funcionalidade antes de uma execução completa.