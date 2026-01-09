@Transformation
Feature: Transformation (Transformacao)

  # Testes para a funcionalidade de Transformacao
  # URL: /transformation/

  # ========================================
  # Navegacao Principal
  # ========================================

  @smoke_transformation
  Scenario: Navigate to Transformation
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Transformation
    Then Transformation page should be displayed

  # ========================================
  # Listagem e Visualizacao
  # ========================================

  @transformation_list
  Scenario: View transformation list
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Transformation
    Then Transformation table should be displayed
    And Transformation table should have columns

  @transformation_details
  Scenario: View transformation details
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Transformation
    And Click on first transformation record
    Then Transformation Details modal should be displayed
    And Transformation Details should show input and output products

  # ========================================
  # Criar Transformacao
  # ========================================

  @transformation_create
  Scenario: Create new transformation
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Transformation
    And Click on Create Transformation button
    And Select transformation location
    And Select input products
    And Scan input product serial numbers
    And Select output product
    And Enter output product quantity
    And Click on Execute Transformation
    Then Transformation should be created successfully

  @transformation_with_lot
  Scenario: Create transformation with lot assignment
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Transformation
    And Click on Create Transformation button
    And Select transformation location
    And Select input products
    And Scan input product serial numbers
    And Select output product
    And Enter output product quantity
    And Assign lot number to output
    And Assign expiration date to output
    And Click on Execute Transformation
    Then Transformation with lot should be created successfully

  @transformation_with_serial
  Scenario: Create transformation with serial number generation
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Transformation
    And Click on Create Transformation button
    And Select transformation location
    And Select input products
    And Scan input product serial numbers
    And Select serialized output product
    And Enter output product quantity
    And Generate serial numbers for output
    And Click on Execute Transformation
    Then Transformation with serials should be created successfully

  # ========================================
  # Tipos de Transformacao
  # ========================================

  @transformation_repackaging
  Scenario: Perform repackaging transformation
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Transformation
    And Click on Create Transformation button
    And Select Repackaging transformation type
    And Select source product
    And Scan source serial numbers
    And Select target packaging
    And Click on Execute Transformation
    Then Repackaging should be completed successfully

  @transformation_splitting
  Scenario: Perform splitting transformation
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Transformation
    And Click on Create Transformation button
    And Select Splitting transformation type
    And Select source product
    And Scan source serial number
    And Define split quantities
    And Click on Execute Transformation
    Then Splitting should be completed successfully

  @transformation_combining
  Scenario: Perform combining transformation
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Transformation
    And Click on Create Transformation button
    And Select Combining transformation type
    And Select source products
    And Scan multiple source serial numbers
    And Select combined output product
    And Click on Execute Transformation
    Then Combining should be completed successfully

  # ========================================
  # Pesquisa e Filtros
  # ========================================

  @transformation_search
  Scenario: Search transformation by serial number
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Transformation
    And Search by serial number
    Then Search results should be filtered

  @transformation_filter_by_date
  Scenario: Filter transformations by date
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Transformation
    And Set date range filter
    And Apply filter
    Then Records should be filtered by date

  @transformation_filter_by_product
  Scenario: Filter transformations by product
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Transformation
    And Select product filter
    And Apply filter
    Then Records should be filtered by product

  # ========================================
  # Exportacao
  # ========================================

  @transformation_export
  Scenario: Export transformation data to CSV
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Transformation
    And Click on Save As button
    And Select CSV option
    Then CSV file should be downloaded

  # ========================================
  # Validacoes
  # ========================================

  @transformation_validate_input
  Scenario: Validate transformation input products
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Transformation
    And Click on Create Transformation button
    And Select transformation location
    And Try to scan invalid serial number
    Then Invalid serial error should be displayed

  @transformation_validate_quantity
  Scenario: Validate transformation output quantity
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Transformation
    And Click on Create Transformation button
    And Select input products
    And Scan input serial numbers
    And Enter invalid output quantity
    Then Quantity validation error should be displayed
