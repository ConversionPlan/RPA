@Container
Feature: Container Management
  Como um usuário do sistema
  Eu quero gerenciar containers de inventário
  Para controlar e rastrear os containers do estoque

  # ============================================================
  # CENÁRIO DE SMOKE TEST - Navegação básica
  # ============================================================

  @smoke_container
  Scenario: Navigate to Container Management
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Container Management
    Then End test

  # ============================================================
  # CENÁRIOS COMPLETOS - Create/Delete Container
  # ============================================================
  # Estes cenários usam validações robustas:
  # - assert_datetime_near(): tolerância de 5 minutos para data
  # - assert_record_count_changed(): tolerância para concorrência
  # - assert_container_created/deleted(): validações compostas
  # ============================================================

  @skip @create_container
  Scenario: Create a Container with validated date and count
    """
    Validações realizadas:
    1. Container aparece na lista após criação
    2. Data de criação está correta (tolerância: 5 min)
    3. Contagem de registros aumentou em 1
    """
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Container Management
    And Click on Create New Container
    And Click on Save
    And Click on Dismiss
    And Click on List/Search Containers in Inventory
    Then Container should be created
    And End test

  @skip @delete_container
  Scenario: Delete a Container with validated removal and count
    """
    Validações realizadas:
    1. Container criado para o teste (setup)
    2. Serial do container é salvo para rastreamento
    3. Após deleção: container não aparece mais OU tem status DELETED/INACTIVE
    4. Contagem de registros diminuiu em 1
    """
    Given User exists
    And Is Logged In
    And There is a Container Created
    When Click on List/Search Containers in Inventory
    And Save Amount of Records
    And Save Container Serial
    And Open sandwich menu
    And Click on Container Management
    And Click on Delete container
    And Input Saved Serial
    And Click on OK - Deletion
    And Click on List/Search Containers in Inventory
    Then Container should be deleted
    And End test

  # ============================================================
  # CENÁRIOS FUTUROS (exemplos de como expandir)
  # ============================================================

  # @skip @update_container
  # Scenario: Update Container and verify updated_at timestamp
  #   """
  #   Validações realizadas:
  #   1. Container existe com dados originais
  #   2. Após update: dados modificados corretamente
  #   3. UPDATED_AT atualizado (tolerância: 5 min)
  #   4. CREATED_AT permanece inalterado
  #   """
  #   Given User exists
  #   And Is Logged In
  #   And There is a Container Created
  #   When Update Container details
  #   Then Container updated_at should be recent
  #   And Container created_at should remain unchanged
  #   And End test
