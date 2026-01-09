@PendingShipments
Feature: Pending Shipments (Remessas Pendentes)

  # Testes para a funcionalidade de Remessas Pendentes
  # URL: /shipments/pending_shipments/

  # ========================================
  # Navegacao Principal
  # ========================================

  @smoke_pending_shipments
  Scenario: Navigate to Pending Shipments
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Pending Shipments
    Then Pending Shipments page should be displayed

  # ========================================
  # Listagem e Visualizacao
  # ========================================

  @pending_shipments_list
  Scenario: View pending shipments list
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Pending Shipments
    Then Pending Shipments table should be displayed
    And Pending Shipments table should have columns

  @pending_shipments_details
  Scenario: View pending shipment details
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Pending Shipments
    And Click on first pending shipment record
    Then Pending Shipment Details modal should be displayed
    And Details should show shipment information

  # ========================================
  # Processar Remessa Pendente
  # ========================================

  @pending_shipment_process
  Scenario: Process a pending shipment
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Pending Shipments
    And Click on first pending shipment record
    And Click on Process Shipment button
    And Confirm shipment processing
    Then Shipment should be processed successfully

  @pending_shipment_complete
  Scenario: Complete a pending shipment
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Pending Shipments
    And Click on first pending shipment record
    And Scan all required serial numbers
    And Click on Complete Shipment button
    Then Shipment should be completed successfully

  # ========================================
  # Cancelar Remessa Pendente
  # ========================================

  @pending_shipment_cancel
  Scenario: Cancel a pending shipment
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Pending Shipments
    And Click on first pending shipment record
    And Click on Cancel Shipment button
    And Enter cancellation reason
    And Confirm cancellation
    Then Shipment should be cancelled successfully

  # ========================================
  # Editar Remessa Pendente
  # ========================================

  @pending_shipment_edit
  Scenario: Edit a pending shipment
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Pending Shipments
    And Click on first pending shipment record
    And Click on Edit Shipment button
    And Update shipment information
    And Click on Save Shipment
    Then Shipment should be updated successfully

  @pending_shipment_add_items
  Scenario: Add items to pending shipment
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Pending Shipments
    And Click on first pending shipment record
    And Click on Add Items button
    And Select products to add
    And Enter quantities
    And Click on Add to Shipment
    Then Items should be added to pending shipment

  @pending_shipment_remove_items
  Scenario: Remove items from pending shipment
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Pending Shipments
    And Click on first pending shipment record
    And Select items to remove
    And Click on Remove Items button
    And Confirm removal
    Then Items should be removed from pending shipment

  # ========================================
  # Pesquisa e Filtros
  # ========================================

  @pending_shipments_search
  Scenario: Search pending shipments by order number
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Pending Shipments
    And Search by order number
    Then Search results should be filtered

  @pending_shipments_filter_by_customer
  Scenario: Filter pending shipments by customer
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Pending Shipments
    And Select customer filter
    And Apply filter
    Then Records should be filtered by customer

  @pending_shipments_filter_by_date
  Scenario: Filter pending shipments by date
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Pending Shipments
    And Set date range filter
    And Apply filter
    Then Records should be filtered by date

  @pending_shipments_filter_by_status
  Scenario: Filter pending shipments by status
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Pending Shipments
    And Select status filter
    And Apply filter
    Then Records should be filtered by status

  # ========================================
  # Exportacao
  # ========================================

  @pending_shipments_export
  Scenario: Export pending shipments to CSV
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Pending Shipments
    And Click on Save As button
    And Select CSV option
    Then CSV file should be downloaded

  # ========================================
  # Acoes em Lote
  # ========================================

  @pending_shipments_bulk_process
  Scenario: Bulk process pending shipments
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Pending Shipments
    And Select multiple pending shipments
    And Click on Bulk Process button
    And Confirm bulk processing
    Then All selected shipments should be processed

  @pending_shipments_bulk_cancel
  Scenario: Bulk cancel pending shipments
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Pending Shipments
    And Select multiple pending shipments
    And Click on Bulk Cancel button
    And Enter cancellation reason
    And Confirm bulk cancellation
    Then All selected shipments should be cancelled
