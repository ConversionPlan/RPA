@SalesOrder
Feature: Sales Order (Pedido de Vendas)

  # Testes para a funcionalidade de Pedido de Vendas
  # URL: /transactions/sales_order/

  @smoke_sales_order
  Scenario: Navigate to Sales Order
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Sales Order
    Then Sales Order page should be displayed

  @sales_order_list
  Scenario: Verify Sales Order list is displayed
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Sales Order
    Then Sales Order table should have columns
    And Sales Order records should be displayed

  @sales_order_search
  Scenario: Search Sales Order by order number
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Sales Order
    And Search Sales Order by order number
    Then Search results should be filtered

  @sales_order_details
  Scenario: View Sales Order details
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Sales Order
    And Click on first Sales Order record
    Then Sales Order Details modal should be displayed
    And Sales Order Details should show order information

  @sales_order_export
  Scenario: Export Sales Order data to CSV
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Sales Order
    And Click on Save As button
    And Select CSV option from Save As menu
    Then CSV file should be downloaded
