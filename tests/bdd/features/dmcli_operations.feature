Feature: DMCLI GET and SET Operations
  As a QA engineer
  I want to perform GET and SET operations via DMCLI
  So that I can verify device configuration and management

  Background:
    Given an RDK CPE device is available in the inventory
    And I am connected to an RDK CPE device
    And the DMCLI tool is available on the device

  Scenario: Get a parameter value using DMCLI
    When I get the parameter "Device.DeviceInfo.ModelName" using DMCLI
    Then the DMCLI command should succeed
    And the parameter value should not be empty

  Scenario: Set and verify a parameter using DMCLI
    When I get the parameter "Device.DeviceInfo.X_CISCO_COM_LED_Flash" using DMCLI
    And I save the original value
    When I set the parameter "Device.DeviceInfo.X_CISCO_COM_LED_Flash" to "true" using DMCLI
    Then the DMCLI command should succeed
    When I get the parameter "Device.DeviceInfo.X_CISCO_COM_LED_Flash" using DMCLI
    Then the parameter value should be "true"
    When I restore the parameter to its original value

  Scenario: Get device hardware information via DMCLI
    When I get the parameter "Device.DeviceInfo.SerialNumber" using DMCLI
    Then the DMCLI command should succeed
    And the parameter value should not be empty
    When I get the parameter "Device.DeviceInfo.HardwareVersion" using DMCLI
    Then the DMCLI command should succeed
    And the parameter value should not be empty

  Scenario: Get device software version via DMCLI
    When I get the parameter "Device.DeviceInfo.SoftwareVersion" using DMCLI
    Then the DMCLI command should succeed
    And the parameter value should not be empty
    And the parameter value should match the pattern ".*[0-9]+.*"

  Scenario: Get network interface information via DMCLI
    When I get the parameter "Device.IP.Interface.1.IPv4Address.1.IPAddress" using DMCLI
    Then the DMCLI command should succeed
    And the parameter value should be a valid IP address

  Scenario: Verify read-only parameter cannot be set
    When I attempt to set the parameter "Device.DeviceInfo.SerialNumber" to "TEST123" using DMCLI
    Then the DMCLI command should fail
    And the error message should contain "read-only" or "not writable"

  Scenario: Get multiple related parameters
    When I get the following parameters using DMCLI:
      | Parameter                                  |
      | Device.DeviceInfo.Manufacturer             |
      | Device.DeviceInfo.ModelName                |
      | Device.DeviceInfo.SoftwareVersion          |
    Then all DMCLI commands should succeed
    And all parameter values should not be empty

  Scenario: Set a numeric parameter
    When I get the parameter "Device.WiFi.Radio.1.Channel" using DMCLI
    And I save the original value
    When I set the parameter "Device.WiFi.Radio.1.Channel" to "6" using DMCLI
    Then the DMCLI command should succeed
    When I get the parameter "Device.WiFi.Radio.1.Channel" using DMCLI
    Then the parameter value should be "6"
    When I restore the parameter to its original value

  Scenario: Verify parameter data type
    When I get the parameter "Device.WiFi.Radio.1.Enable" using DMCLI
    Then the DMCLI command should succeed
    And the parameter value should be a boolean

  Scenario: Set a boolean parameter
    When I get the parameter "Device.WiFi.Radio.1.Enable" using DMCLI
    And I save the original value
    When I set the parameter "Device.WiFi.Radio.1.Enable" to "false" using DMCLI
    Then the DMCLI command should succeed
    When I get the parameter "Device.WiFi.Radio.1.Enable" using DMCLI
    Then the parameter value should be "false"
    When I restore the parameter to its original value
