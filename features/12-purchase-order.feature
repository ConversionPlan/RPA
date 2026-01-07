@PurchaseOrder
Feature: Purchase Order (Pedido de Compra)

  # Testes para a funcionalidade de Pedido de Compra
  # URL: /transactions/purchase_order

  @smoke_purchase_order
  Scenario: Navigate to Purchase Order
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Purchase Order
    Then Purchase Order page should be displayed

  @purchase_order_list
  Scenario: Verify Purchase Order list is displayed
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Purchase Order
    Then Purchase Order table should have columns
    And Purchase Order records should be displayed

  @purchase_order_search
  Scenario: Search Purchase Order by order number
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Purchase Order
    And Search Purchase Order by order number
    Then Search results should be filtered

  @purchase_order_details
  Scenario: View Purchase Order details
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Purchase Order
    And Click on first Purchase Order record
    Then Purchase Order Details modal should be displayed
    And Purchase Order Details should show order information

  @purchase_order_export
  Scenario: Export Purchase Order data to CSV
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Purchase Order
    And Click on Save As button
    And Select CSV option from Save As menu
    Then CSV file should be downloaded
