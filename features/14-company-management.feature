@CompanyManagement
Feature: Company Management (Gestao da Companhia)

  # Testes para a funcionalidade de Gestao da Companhia
  # URL: /company_mgt/
  # Inclui: Configuracoes Gerais, Produtos/Inventario, Usuarios/Permissoes

  # ========================================
  # Navegacao Principal
  # ========================================

  @smoke_company_mgt
  Scenario: Navigate to Company Management
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Company Management
    Then Company Management page should be displayed

  # ========================================
  # Configuracoes Gerais
  # ========================================

  @company_settings
  Scenario: View Company Settings
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Company Management
    And Click on Company Settings
    Then Company Settings modal should be displayed

  @company_settings_edit
  Scenario: Edit Company Settings
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Company Management
    And Click on Company Settings
    And Update company information
    And Click on Save Company Settings
    Then Company Settings should be updated successfully

  @pdf_customization
  Scenario: View PDF Customization Settings
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Company Management
    And Click on PDF Customization Setting
    Then PDF Customization page should be displayed

  @third_party_logistics
  Scenario: View Third Party Logistics Providers
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Company Management
    And Click on Third Party Logistics Providers
    Then Third Party Logistics Providers page should be displayed

  @third_party_logistics_add
  Scenario: Add Third Party Logistics Provider
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Company Management
    And Click on Third Party Logistics Providers
    And Click on Add Provider button
    And Fill provider information
    And Click on Save Provider
    Then Provider should be added successfully

  @license_types
  Scenario: View License Types
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Company Management
    And Click on License Type Management
    Then License Types page should be displayed

  @license_types_add
  Scenario: Add License Type
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Company Management
    And Click on License Type Management
    And Click on Add License Type button
    And Fill license type information
    And Click on Save License Type
    Then License Type should be added successfully

  @event_notifications
  Scenario: View Event Notifications
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Company Management
    And Click on Event Notification Actions
    Then Event Notifications page should be displayed

  @event_notifications_add
  Scenario: Add Event Notification
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Company Management
    And Click on Event Notification Actions
    And Click on Add Notification button
    And Fill notification information
    And Click on Save Notification
    Then Notification should be added successfully

  @workflow_automation
  Scenario: View Workflow Automation
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Company Management
    And Click on Workflow Automation
    Then Workflow Automation page should be displayed

  @workflow_automation_add
  Scenario: Add Workflow Trigger
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Company Management
    And Click on Workflow Automation
    And Click on Add Trigger button
    And Fill trigger information
    And Click on Save Trigger
    Then Trigger should be added successfully

  @usage_meter
  Scenario: View Usage Meter
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Company Management
    And Click on Usage Meter
    Then Usage Meter modal should be displayed
    And Usage statistics should be shown

  # ========================================
  # Produtos e Inventario
  # ========================================

  @product_requirements
  Scenario: View Product Requirements Groups
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Company Management
    And Click on Product Requirements Groups
    Then Product Requirements Groups page should be displayed

  @product_requirements_add
  Scenario: Add Product Requirements Group
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Company Management
    And Click on Product Requirements Groups
    And Click on Add Group button
    And Fill group information
    And Click on Save Group
    Then Product Requirements Group should be added successfully

  @product_categories
  Scenario: View Product Categories
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Company Management
    And Click on Product Categories
    Then Product Categories page should be displayed

  @product_categories_add
  Scenario: Add Product Category
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Company Management
    And Click on Product Categories
    And Click on Add Category button
    And Fill category information
    And Click on Save Category
    Then Product Category should be added successfully

  @manufacturers
  Scenario: View Manufacturers
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Company Management
    And Click on Manufacturers
    Then Manufacturers page should be displayed

  @manufacturers_add
  Scenario: Add Manufacturer
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Company Management
    And Click on Manufacturers
    And Click on Add Manufacturer button
    And Fill manufacturer information
    And Click on Save Manufacturer
    Then Manufacturer should be added successfully

  @packaging_types
  Scenario: View Packaging Types
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Company Management
    And Click on Packaging Types Management
    Then Packaging Types page should be displayed

  @dosage_forms
  Scenario: View Dosage Forms
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Company Management
    And Click on Dosage Forms Management
    Then Dosage Forms page should be displayed

  @product_serialization
  Scenario: View Product Serialization Policies
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Company Management
    And Click on Product Serialization
    Then Product Serialization page should be displayed

  @container_serialization
  Scenario: View Container Serialization Policies
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Company Management
    And Click on Container Serialization
    Then Container Serialization page should be displayed

  @shipping_carriers
  Scenario: View Shipping Carriers
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Company Management
    And Click on Shipping Carriers Management
    Then Shipping Carriers page should be displayed

  @shipping_carriers_add
  Scenario: Add Shipping Carrier
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Company Management
    And Click on Shipping Carriers Management
    And Click on Add Carrier button
    And Fill carrier information
    And Click on Save Carrier
    Then Shipping Carrier should be added successfully

  @inventory_adjustment_reasons
  Scenario: View Inventory Adjustment Reasons
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Company Management
    And Click on Inventory Adjustment Reasons
    Then Inventory Adjustment Reasons page should be displayed

  @transformation_policies
  Scenario: View Transformation Policies
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Company Management
    And Click on Transformation Policies
    Then Transformation Policies page should be displayed

  # ========================================
  # Usuarios, Acesso e Permissoes
  # ========================================

  @staff_management
  Scenario: View Staff Management
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Company Management
    And Click on Staff Management
    Then Staff Management page should be displayed

  @staff_add
  Scenario: Add Staff Member
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Company Management
    And Click on Staff Management
    And Click on Add Staff button
    And Fill staff information
    And Click on Save Staff
    Then Staff member should be added successfully

  @staff_edit
  Scenario: Edit Staff Member
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Company Management
    And Click on Staff Management
    And Click on first staff member
    And Update staff information
    And Click on Save Staff
    Then Staff member should be updated successfully

  @user_roles
  Scenario: View User Roles
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Company Management
    And Click on User Roles Management
    Then User Roles page should be displayed

  @user_roles_add
  Scenario: Add User Role
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Company Management
    And Click on User Roles Management
    And Click on Add Role button
    And Fill role information
    And Set role permissions
    And Click on Save Role
    Then User Role should be added successfully

  @api_keys
  Scenario: View API Keys
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Company Management
    And Click on API Access Keys
    Then API Keys page should be displayed

  @api_keys_generate
  Scenario: Generate new API Key
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Company Management
    And Click on API Access Keys
    And Click on Generate API Key button
    And Fill API key description
    And Click on Generate
    Then API Key should be generated successfully
