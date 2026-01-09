@StressTest @Inbound
Feature: Stress Test - Inbound File Processing
  Teste de stress para medir tempo de processamento e volume maximo de arquivos
  no sistema Inbound via Manual File Upload e Electronic File

  # =============================================================================
  # STRESS TEST - MANUAL FILE UPLOAD
  # Testa o upload de arquivos EPCIS XML via interface Utilities
  # =============================================================================

  @ManualUpload @Gradual
  Scenario Outline: Stress Test - Manual File Upload (<batch_size> arquivos)
    Given User exists
    And Is Logged In
    And Stress test metrics are initialized
    When Prepare <batch_size> EPCIS files for upload
    And Start stress test timer
    And Process batch of <batch_size> files via Manual Upload
    And Stop stress test timer
    Then Record stress test metrics for "Manual Upload" with <batch_size> files
    And Generate stress test report
    And End test

    Examples:
      | batch_size |
      | 5          |
      | 10         |
      | 25         |
      | 50         |
      | 100        |

  # =============================================================================
  # STRESS TEST - ELECTRONIC FILE (EPCIS GENERATOR)
  # Testa a geracao e processamento de arquivos via EPCIS Generator
  # =============================================================================

  @ElectronicFile @Gradual
  Scenario Outline: Stress Test - Electronic File Processing (<batch_size> arquivos)
    Given User exists
    And Is Logged In
    And Stress test metrics are initialized
    When Start stress test timer
    And Generate and process <batch_size> electronic files
    And Stop stress test timer
    Then Record stress test metrics for "Electronic File" with <batch_size> files
    And Generate stress test report
    And End test

    Examples:
      | batch_size |
      | 5          |
      | 10         |
      | 25         |
      | 50         |

  # =============================================================================
  # STRESS TEST - COMPARATIVO
  # Compara performance entre os dois metodos
  # =============================================================================

  @Comparison
  Scenario: Stress Test - Comparacao Manual Upload vs Electronic File
    Given User exists
    And Is Logged In
    And Stress test metrics are initialized
    # Teste Manual Upload
    When Prepare 10 EPCIS files for upload
    And Start stress test timer
    And Process batch of 10 files via Manual Upload
    And Stop stress test timer
    And Record stress test metrics for "Manual Upload" with 10 files
    # Teste Electronic File
    And Start stress test timer
    And Generate and process 10 electronic files
    And Stop stress test timer
    And Record stress test metrics for "Electronic File" with 10 files
    # Relatorio comparativo
    Then Generate comparative stress test report
    And End test

  # =============================================================================
  # STRESS TEST - LIMITE DO SISTEMA
  # Descobre o limite maximo de arquivos que o sistema suporta
  # =============================================================================

  @SystemLimit @Manual
  Scenario: Stress Test - Descobrir Limite do Sistema (Manual Upload)
    Given User exists
    And Is Logged In
    And Stress test metrics are initialized
    When Find system limit for Manual Upload starting from 10 files
    Then Generate system limit report for "Manual Upload"
    And End test

  @SystemLimit @Electronic
  Scenario: Stress Test - Descobrir Limite do Sistema (Electronic File)
    Given User exists
    And Is Logged In
    And Stress test metrics are initialized
    When Find system limit for Electronic File starting from 5 files
    Then Generate system limit report for "Electronic File"
    And End test

  # =============================================================================
  # STRESS TEST RAPIDO - PARA VALIDACAO
  # Cenario rapido para validar se o stress test esta funcionando
  # =============================================================================

  @Quick @Validation
  Scenario: Stress Test - Validacao Rapida (2 arquivos)
    Given User exists
    And Is Logged In
    And Stress test metrics are initialized
    When Prepare 2 EPCIS files for upload
    And Start stress test timer
    And Process batch of 2 files via Manual Upload
    And Stop stress test timer
    Then Record stress test metrics for "Manual Upload" with 2 files
    And Generate stress test report
    And End test

  # =============================================================================
  # STRESS TEST CUSTOMIZADO - 30 ARQUIVOS
  # =============================================================================

  @Custom @Load30
  Scenario: Stress Test - Carga Alta (30 arquivos)
    Given User exists
    And Is Logged In
    And Stress test metrics are initialized
    When Prepare 30 EPCIS files for upload
    And Start stress test timer
    And Process batch of 30 files via Manual Upload
    And Stop stress test timer
    Then Record stress test metrics for "Manual Upload" with 30 files
    And Generate stress test report
    And End test

  @Custom @Load500 @Sequential
  Scenario: Stress Test - Carga Extrema Sequencial (500 arquivos - 1 sessao)
    Given User exists
    And Is Logged In
    And Stress test metrics are initialized
    When Prepare 500 EPCIS files for upload
    And Start stress test timer
    And Process batch of 500 files via Manual Upload
    And Stop stress test timer
    Then Record stress test metrics for "Sequential Upload (1 session)" with 500 files
    And Generate stress test report
    And End test

  # =============================================================================
  # STRESS TEST PARALELO - MULTIPLAS SESSOES SIMULTANEAS
  # Testa processamento paralelo com N browsers rodando simultaneamente
  # =============================================================================

  @Parallel @Load50
  Scenario: Stress Test - Paralelo 50 arquivos (5 sessoes x 10 arquivos)
    Given User exists
    And Stress test metrics are initialized
    When Prepare 50 EPCIS files for upload
    And Start stress test timer
    And Process 50 files in parallel with 5 sessions
    And Stop stress test timer
    Then Record stress test metrics for "Parallel Upload (5 sessions)" with 50 files
    And Generate stress test report
    And End test

  @Parallel @Load100
  Scenario: Stress Test - Paralelo 100 arquivos (10 sessoes x 10 arquivos)
    Given User exists
    And Stress test metrics are initialized
    When Prepare 100 EPCIS files for upload
    And Start stress test timer
    And Process 100 files in parallel with 10 sessions
    And Stop stress test timer
    Then Record stress test metrics for "Parallel Upload (10 sessions)" with 100 files
    And Generate stress test report
    And End test

  @Parallel @Load200
  Scenario: Stress Test - Paralelo 200 arquivos (10 sessoes x 20 arquivos)
    Given User exists
    And Stress test metrics are initialized
    When Prepare 200 EPCIS files for upload
    And Start stress test timer
    And Process 200 files in parallel with 10 sessions
    And Stop stress test timer
    Then Record stress test metrics for "Parallel Upload (10 sessions)" with 200 files
    And Generate stress test report
    And End test

  @Parallel @Comparison
  Scenario: Stress Test - Comparativo Sequencial vs Paralelo (20 arquivos)
    Given User exists
    And Is Logged In
    And Stress test metrics are initialized
    # Teste Sequencial
    When Prepare 20 EPCIS files for upload
    And Start stress test timer
    And Process batch of 20 files via Manual Upload
    And Stop stress test timer
    And Record stress test metrics for "Sequential" with 20 files
    # Teste Paralelo
    And Prepare 20 EPCIS files for upload
    And Start stress test timer
    And Process 20 files in parallel with 4 sessions
    And Stop stress test timer
    And Record stress test metrics for "Parallel (4 sessions)" with 20 files
    Then Generate stress test report
    And End test
