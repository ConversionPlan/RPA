@MyAccount
Feature: My Account (Minha Conta)

  # Testes para a funcionalidade de Minha Conta
  # URL: /my_account/

  # ========================================
  # Navegacao Principal
  # ========================================

  @smoke_my_account
  Scenario: Navigate to My Account
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on My Account
    Then My Account page should be displayed

  # ========================================
  # Perfil de Usuario
  # ========================================

  @user_profile_view
  Scenario: View user profile
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on My Account
    And Click on User Profile
    Then User Profile modal should be displayed
    And Profile information should be shown

  @user_profile_edit
  Scenario: Edit user profile
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on My Account
    And Click on User Profile
    And Update profile first name
    And Update profile last name
    And Click on Save Profile
    Then Profile should be updated successfully

  # ========================================
  # Alterar Senha
  # ========================================

  @change_password
  Scenario: Change user password
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on My Account
    And Click on Change Password
    And Enter current password
    And Enter new password
    And Confirm new password
    And Click on Change Password button
    Then Password should be changed successfully

  @change_password_mismatch
  Scenario: Change password with mismatched confirmation
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on My Account
    And Click on Change Password
    And Enter current password
    And Enter new password
    And Enter different confirmation password
    And Click on Change Password button
    Then Password mismatch error should be displayed

  # ========================================
  # Configuracoes de Interface
  # ========================================

  @ui_settings_view
  Scenario: View UI settings
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on My Account
    And Click on UI Settings
    Then UI Settings modal should be displayed

  @ui_settings_change_language
  Scenario: Change interface language
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on My Account
    And Click on UI Settings
    And Select language preference
    And Click on Save UI Settings
    Then Language should be changed successfully

  @ui_settings_change_timezone
  Scenario: Change timezone
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on My Account
    And Click on UI Settings
    And Select timezone preference
    And Click on Save UI Settings
    Then Timezone should be changed successfully

  # ========================================
  # Autenticacao em Duas Etapas (2FA)
  # ========================================

  @2fa_view
  Scenario: View 2FA settings
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on My Account
    And Click on Two Factor Authentication
    Then 2FA settings page should be displayed

  @2fa_enable
  Scenario: Enable 2FA
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on My Account
    And Click on Two Factor Authentication
    And Click on Enable 2FA button
    And Scan QR code or enter key manually
    And Enter verification code
    And Click on Confirm
    Then 2FA should be enabled successfully

  @2fa_disable
  Scenario: Disable 2FA
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on My Account
    And Click on Two Factor Authentication
    And Click on Disable 2FA button
    And Enter current password
    And Confirm disable
    Then 2FA should be disabled successfully

  # ========================================
  # Notificacoes
  # ========================================

  @notifications_view
  Scenario: View notifications settings
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on My Account
    And Click on Notifications
    Then Notifications settings page should be displayed

  @notifications_configure
  Scenario: Configure notification preferences
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on My Account
    And Click on Notifications
    And Enable email notifications
    And Select notification events
    And Click on Save Notifications
    Then Notification preferences should be saved successfully

  @notifications_disable
  Scenario: Disable all notifications
    Given User exists
    And Is Logged In
    When Open dashboard page
    And Open sandwich menu
    And Click on My Account
    And Click on Notifications
    And Disable all notification types
    And Click on Save Notifications
    Then All notifications should be disabled
