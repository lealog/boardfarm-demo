# BDD vs Traditional Testing - Side-by-Side Comparison

This document shows the same tests written in both traditional pytest and BDD style using pytest-bdd.

## Example 1: Basic Connection Test

### Traditional Pytest
**File:** `tests/tests_ssh_cpe.py`

```python
def test_ssh_cpe_connection(device_manager: DeviceManager):
    """Test SSH connection to CPE device.

    This test verifies that we can connect to a CPE device via SSH
    and execute basic commands.
    """
    cpe = get_cpe_device(device_manager)
    logger.info(f"Got device: {cpe}")

    # Test basic command execution
    output = cpe.command("echo 'SSH CPE is connected'")
    assert "SSH CPE is connected" in output
    logger.info(f"Connection test passed: {output}")
```

### BDD with pytest-bdd

**Feature File:** `tests/features/ssh_cpe_connectivity.feature`
```gherkin
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
```

**Step Definitions:** `tests/test_ssh_cpe_bdd.py`
```python
@given('a CPE device is configured in the inventory')
def cpe_device_available(device_manager: DeviceManager, cpe_context):
    """Verify that a CPE device is available in the inventory."""
    cpe = get_cpe_device(device_manager)
    cpe_context['device'] = cpe
    logger.info(f"CPE device found: {cpe}")

@when('I connect to the CPE device via SSH')
def connect_to_cpe(cpe_context):
    """Connect to the CPE device via SSH (connection is automatic)."""
    cpe = cpe_context['device']
    logger.info(f"SSH connection established to: {cpe}")

@then('the connection should be successful')
def verify_connection(cpe_context):
    """Verify that the connection is successful."""
    cpe = cpe_context['device']
    output = cpe.command("echo 'SSH CPE is connected'")
    assert "SSH CPE is connected" in output
    logger.info("Connection verified successfully")

@then('I should be able to execute commands')
def verify_command_execution(cpe_context):
    """Verify that commands can be executed on the device."""
    cpe = cpe_context['device']
    output = cpe.command("echo 'test'")
    assert "test" in output
    logger.info("Command execution verified")
```

**Key Differences:**
- BDD separates the **what** (feature file) from the **how** (step definitions)
- BDD scenarios are readable by non-technical stakeholders
- BDD encourages reusable step definitions

---

## Example 2: System Information Retrieval

### Traditional Pytest
**File:** `tests/tests_ssh_cpe.py`

```python
def test_ssh_cpe_system_info(device_manager: DeviceManager):
    """Test retrieving system information from SSH CPE."""
    cpe = get_cpe_device(device_manager)

    # Get system hostname
    hostname = cpe.command("hostname")
    assert hostname, "Failed to get hostname"
    logger.info(f"Hostname: {hostname}")

    # Get kernel version
    kernel = cpe.command("uname -r")
    assert kernel, "Failed to get kernel version"
    logger.info(f"Kernel: {kernel}")

    # Get uptime
    uptime = cpe.command("uptime")
    assert uptime, "Failed to get uptime"
    logger.info(f"Uptime: {uptime}")
```

### BDD with pytest-bdd

**Feature File:** `tests/features/ssh_cpe_connectivity.feature`
```gherkin
Scenario: Retrieve system information from CPE
  When I connect to the CPE device via SSH
  And I query the system hostname
  Then I should receive a valid hostname
  When I query the kernel version
  Then I should receive a valid kernel version
  When I query the system uptime
  Then I should receive uptime information
```

**Step Definitions:** `tests/test_ssh_cpe_bdd.py`
```python
@when('I query the system hostname')
def query_hostname(cpe_context):
    cpe = cpe_context['device']
    cpe_context['output'] = cpe.command("hostname")
    logger.info(f"Hostname query result: {cpe_context['output']}")

@then('I should receive a valid hostname')
def verify_hostname(cpe_context):
    assert cpe_context['output'], "Hostname is empty"
    assert len(cpe_context['output'].strip()) > 0, "Hostname is invalid"
    logger.info(f"Valid hostname received: {cpe_context['output']}")

@when('I query the kernel version')
def query_kernel(cpe_context):
    cpe = cpe_context['device']
    cpe_context['output'] = cpe.command("uname -r")
    logger.info(f"Kernel version: {cpe_context['output']}")

@then('I should receive a valid kernel version')
def verify_kernel_version(cpe_context):
    assert cpe_context['output'], "Kernel version is empty"
    logger.info(f"Valid kernel version received: {cpe_context['output']}")

@when('I query the system uptime')
def query_uptime(cpe_context):
    cpe = cpe_context['device']
    cpe_context['output'] = cpe.command("uptime")
    logger.info(f"Uptime: {cpe_context['output']}")

@then('I should receive uptime information')
def verify_uptime(cpe_context):
    assert cpe_context['output'], "Uptime information is empty"
    logger.info(f"Uptime information received: {cpe_context['output']}")
```

**Key Differences:**
- BDD breaks down the test into smaller, reusable steps
- Each step can be reused in other scenarios
- The feature file reads like a specification document

---

## Example 3: File Operations

### Traditional Pytest
**File:** `tests/tests_ssh_cpe.py`

```python
def test_ssh_cpe_file_operations(device_manager: DeviceManager):
    """Test file operations on SSH CPE."""
    cpe = get_cpe_device(device_manager)

    # Create a test file
    test_file = "/tmp/boardfarm_test.txt"
    test_content = "Boardfarm SSH test"

    # Write to file
    cpe.command(f"echo '{test_content}' > {test_file}")

    # Read from file
    content = cpe.command(f"cat {test_file}")
    assert test_content in content, "File content mismatch"
    logger.info(f"File operation test passed: {content}")

    # Clean up
    cpe.command(f"rm -f {test_file}")
```

### BDD with pytest-bdd

**Feature File:** `tests/features/ssh_cpe_connectivity.feature`
```gherkin
Scenario: Perform file operations on CPE
  When I connect to the CPE device via SSH
  And I create a test file with content "Boardfarm SSH test"
  Then the file should be created successfully
  When I read the test file
  Then the content should match "Boardfarm SSH test"
  And I cleanup the test file
```

**Step Definitions:** `tests/test_ssh_cpe_bdd.py`
```python
@when(parsers.parse('I create a test file with content "{content}"'))
def create_test_file(cpe_context, content):
    """Create a test file with specified content."""
    cpe = cpe_context['device']
    test_file = cpe_context['test_file']
    cpe_context['test_content'] = content
    cpe.command(f"echo '{content}' > {test_file}")
    logger.info(f"Created test file: {test_file}")

@then('the file should be created successfully')
def verify_file_created(cpe_context):
    """Verify that the file was created successfully."""
    cpe = cpe_context['device']
    test_file = cpe_context['test_file']
    result = cpe.command(f"test -f {test_file} && echo 'exists' || echo 'not found'")
    assert 'exists' in result, "File was not created"
    logger.info("File created successfully")

@when('I read the test file')
def read_test_file(cpe_context):
    """Read the test file."""
    cpe = cpe_context['device']
    test_file = cpe_context['test_file']
    cpe_context['output'] = cpe.command(f"cat {test_file}")
    logger.info(f"Read test file content: {cpe_context['output']}")

@then(parsers.parse('the content should match "{expected_content}"'))
def verify_file_content(cpe_context, expected_content):
    """Verify that the file content matches the expected content."""
    assert cpe_context['output'], "File content is empty"
    assert expected_content in cpe_context['output'], "File content does not match"
    logger.info(f"File content matches: {expected_content}")

@then('I cleanup the test file')
def cleanup_test_file(cpe_context):
    """Clean up the test file."""
    cpe = cpe_context['device']
    test_file = cpe_context['test_file']
    cpe.command(f"rm -f {test_file}")
    logger.info("Test file cleaned up")
```

**Key Differences:**
- BDD uses parametrized steps with `parsers.parse()` for flexibility
- Each step is self-documenting
- The scenario describes the workflow clearly

---

## Example 4: DMCLI Integration Test

### Traditional Pytest
**File:** `tests/tests_ssh_cpe.py`

```python
@pytest.mark.slow
def test_ssh_rdk_cpe_dmcli_integration(device_manager: DeviceManager):
    """Test DMCLI integration with RDK CPE via SSH.

    This test verifies that DMCLI (TR-181 data model CLI) works
    over SSH connection to query device parameters.
    """
    devices = device_manager.get_devices_by_type(RdkCpeDevice)
    if not devices:
        pytest.skip("No RDK CPE devices found in inventory")

    cpe = list(devices.values())[0]

    # Check if dmcli is available
    dmcli_check = cpe.command("which dmcli")
    if "dmcli" not in dmcli_check:
        pytest.skip("dmcli not available on this device")

    try:
        # Get device model name via DMCLI
        model = cpe.get_device_model_name()
        logger.info(f"Device Model (via DMCLI): {model}")

        # Get device serial number via DMCLI
        serial = cpe.get_device_serial_number()
        logger.info(f"Device Serial (via DMCLI): {serial}")

        # Get software version via DMCLI
        version = cpe.get_device_software_version()
        logger.info(f"Software Version (via DMCLI): {version}")

    except Exception as e:
        logger.info(f"Warning: DMCLI operations failed: {e}")
        pytest.skip(f"DMCLI not fully functional: {e}")
```

### BDD with pytest-bdd

**Feature File:** `tests/features/rdk_cpe_advanced.feature`
```gherkin
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
```

**Step Definitions:** `tests/test_ssh_cpe_bdd.py`
```python
@given('I am connected to an RDK CPE device')
def connected_to_rdk_cpe(device_manager: DeviceManager, cpe_context):
    cpe = get_rdk_cpe_device(device_manager)
    cpe_context['device'] = cpe
    logger.info(f"Connected to RDK CPE: {cpe}")

@given('the DMCLI tool is available on the device')
def dmcli_available(cpe_context):
    cpe = cpe_context['device']
    dmcli_check = cpe.command("which dmcli")
    if "dmcli" not in dmcli_check:
        pytest.skip("dmcli not available on this device")
    logger.info("DMCLI tool is available")

@when('I query the device model name using DMCLI')
def query_model_dmcli(cpe_context):
    cpe = cpe_context['device']
    try:
        cpe_context['output'] = cpe.get_device_model_name()
        logger.info(f"Device model (DMCLI): {cpe_context['output']}")
    except Exception as e:
        logger.warning(f"DMCLI model query failed: {e}")
        cpe_context['output'] = None

@then('I should receive the device model information')
def verify_device_model(cpe_context):
    if cpe_context['output'] is None:
        pytest.skip("Device model not available via DMCLI")
    assert cpe_context['output'], "Device model is empty"
    logger.info(f"Device model received: {cpe_context['output']}")
```

**Key Differences:**
- BDD makes preconditions explicit in the Given steps
- Tags like `@slow` work seamlessly with pytest markers
- Error handling is cleaner with pytest.skip() in step definitions

---

## When to Use Each Approach?

### Use Traditional Pytest When:
- ✅ Writing quick unit tests
- ✅ Test is simple and straightforward
- ✅ Only developers will read the tests
- ✅ You need to iterate quickly

### Use BDD When:
- ✅ Testing user-facing features
- ✅ Tests need to be reviewed by non-developers (QA, Product, Business)
- ✅ Creating living documentation
- ✅ Testing complex workflows with multiple steps
- ✅ You want to encourage collaboration

### Hybrid Approach (Recommended):
Use **both** in the same project:
- **BDD** for integration tests and feature tests
- **Traditional pytest** for unit tests and quick checks

---

## Summary

| Aspect | Traditional Pytest | BDD with pytest-bdd |
|--------|-------------------|---------------------|
| **Readability** | Good for developers | Excellent for everyone |
| **Setup Time** | Fast | Moderate |
| **Maintenance** | Can become messy | Well-organized |
| **Documentation** | Docstrings | Living documentation |
| **Collaboration** | Developer-focused | Team-wide |
| **Step Reuse** | Manual | Built-in |
| **Learning Curve** | Low | Medium |
| **Best For** | Unit tests | Feature/Integration tests |

Both approaches are valid and can coexist in the same project. Choose based on your team's needs and the type of test you're writing.
