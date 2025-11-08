Feature: RDK CPE Advanced Features
  As a network engineer
  I want to access advanced RDK CPE features
  So that I can retrieve detailed device information and perform diagnostics

  Background:
    Given an RDK CPE device is available in the inventory

  Scenario: Connect to RDK CPE via SSH
    When I establish an SSH connection to the RDK CPE
    Then the RDK CPE connection should be successful
    And I should be able to execute RDK-specific commands

  @slow
  Scenario: Retrieve hardware information from RDK CPE
    Given I am connected to an RDK CPE device
    When I query the device serial number
    Then I should receive a valid serial number
    When I query the device MAC address
    Then I should receive a valid MAC address

  @slow
  Scenario: Access DMCLI interface on RDK CPE
    Given I am connected to an RDK CPE device
    And the DMCLI tool is available on the device
    When I query the device model name using DMCLI
    Then I should receive the device model information
    When I query the device serial number using DMCLI
    Then I should receive the device serial via DMCLI
    When I query the software version using DMCLI
    Then I should receive the software version information
