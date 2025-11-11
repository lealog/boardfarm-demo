Feature: DMCLI GET and SET Operations
  As a QA engineer
  I want to perform GET and SET operations via DMCLI
  So that I can verify device configuration and management

  Background:
    Given an RDK CPE device is available in the inventory
    And I am connected to an RDK CPE device
    And the DMCLI tool is available on the device

  Scenario: Get device hardware information via DMCLI
    When I get the parameter "Device.DeviceInfo.SerialNumber" using DMCLI
    Then the DMCLI command should succeed
    And the parameter value should not be empty
    When I get the parameter "Device.DeviceInfo.HardwareVersion" using DMCLI
    Then the DMCLI command should succeed
    And the parameter value should not be empty