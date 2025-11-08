Feature: SSH CPE Device Connectivity
  As a network engineer
  I want to connect to CPE devices via SSH
  So that I can manage and monitor the devices remotely

  Background:
    Given a CPE device is configured in the inventory

  Scenario: Establish SSH connection to CPE device
    When I connect to the CPE device via SSH
    Then the connection should be successful
    And I should be able to execute commands

  Scenario: Retrieve system information from CPE
    When I connect to the CPE device via SSH
    And I query the system hostname
    Then I should receive a valid hostname
    When I query the kernel version
    Then I should receive a valid kernel version
    When I query the system uptime
    Then I should receive uptime information

  Scenario: Retrieve network information from CPE
    When I connect to the CPE device via SSH
    And I query the IP address configuration
    Then I should receive IP address information
    When I query the routing table
    Then I should receive routing information

  Scenario: Perform file operations on CPE
    When I connect to the CPE device via SSH
    And I create a test file with content "Boardfarm SSH test"
    Then the file should be created successfully
    When I read the test file
    Then the content should match "Boardfarm SSH test"
    And I cleanup the test file

  Scenario: Retrieve memory information from CPE
    When I connect to the CPE device via SSH
    And I query the memory usage
    Then I should receive memory information
    And the memory information should contain usage statistics

  Scenario: Retrieve disk usage from CPE
    When I connect to the CPE device via SSH
    And I query the disk usage
    Then I should receive disk usage information
    And the disk information should contain filesystem details
