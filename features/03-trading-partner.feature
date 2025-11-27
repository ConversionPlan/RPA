@Trading_Partners
Feature: Trading Partners

  # Cenário simplificado - apenas criar o Trading Partner básico (sem endereços)
  Scenario: Create a Vendor (Basic)
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Trading Partners
    And Click on Add - Trading Partner Page
    And Add Trading Partner Name
    And Add Trading Partner GS1 ID (GLN)
    And Add Trading Partner GS1 Company Prefix
    And Add Trading Partner GS1 ID (SGLN)
    And Click on Add
    Then Trading Partner should be created
    And End test

  # Cenário simplificado - apenas criar Customer básico (sem endereços)
  Scenario: Create a Customer (Basic)
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Trading Partners
    And Click on Add - Trading Partner Page
    And Add Trading Partner Name
    And Select Trading Partner Type as Customer
    And Add Trading Partner GS1 ID (GLN)
    And Add Trading Partner GS1 Company Prefix
    And Add Trading Partner GS1 ID (SGLN)
    And Click on Add
    Then Trading Partner should be created
    And End test

  # Cenários completos com endereços - temporariamente desabilitados
  @skip
  Scenario: Create a Vendor with Addresses
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Trading Partners
    And Click on Add - Trading Partner Page
    And Add Trading Partner Name
    And Add Trading Partner GS1 ID (GLN)
    And Add Trading Partner GS1 Company Prefix
    And Add Trading Partner GS1 ID (SGLN)
    And Click on Add
    And Search Trading Partner by Name
    And Click on the Pencil next to its Name
    And Click on Address Tab
    And Click on Add - Address
    And Add Ship From Address Nickname
    And Add Address GLN
    And Add Address SGLN
    And Add Ship From Address Recipient Name
    And Add Address Line 1
    And Add Address City
    And Add Address ZIP
    And Click on Add - Save Address
    And Click on Add - Address
    And Add Main Address Nickname
    And Add Second Address GLN
    And Add Second Address SGLN
    And Add Main Address Recipient Name
    And Add Address Line 1
    And Add Address City
    And Add Address ZIP
    And Click on Add - Save Address
    And Click on Save
    Then Trading Partner should be saved
    And End test

  @skip
  Scenario: Create a Customer with Addresses
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on Trading Partners
    And Click on Add - Trading Partner Page
    And Add Trading Partner Name
    And Select Trading Partner Type as Customer
    And Add Trading Partner GS1 ID (GLN)
    And Add Trading Partner GS1 Company Prefix
    And Add Trading Partner GS1 ID (SGLN)
    And Click on Add
    And Search Trading Partner by Name
    And Click on the Pencil next to its Name
    And Click on Address Tab
    And Click on Add - Address
    And Add Ship To Address Nickname
    And Add Address GLN
    And Add Address SGLN
    And Add Ship To Address Recipient Name
    And Add Address Line 1
    And Add Address City
    And Add Address ZIP
    And Click on Add - Save Address
    And Click on Add - Address
    And Add Main Address Nickname
    And Add Second Address GLN
    And Add Second Address SGLN
    And Add Main Address Recipient Name
    And Add Address Line 1
    And Add Address City
    And Add Address ZIP
    And Click on Add - Save Address
    And Click on Save
    Then Trading Partner should be saved
    And End test
