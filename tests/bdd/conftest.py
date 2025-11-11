"""Shared BDD step definitions and fixtures for all test scenarios.

This module contains ALL reusable step definitions that can be used across
any .feature file. QA engineers can create new .feature files without needing
to write any Python code - all the steps they need are defined here.

To add support for new test types, developers add new step definitions to this
file, and they become immediately available in all .feature files.
"""

import logging
import re
import pytest
from pytest_bdd import given, when, then, parsers
from boardfarm3.lib.device_manager import DeviceManager
from rpi_cpe_device import RpiCpeDevice
from rdk_cpe_device import RdkCpeDevice

logger = logging.getLogger(__name__)


# ============================================================================
# Shared Fixtures
# ============================================================================

@pytest.fixture
def test_context():
    """Universal context object to share data between steps.

    This context can be used by any test scenario to store and retrieve data.
    """
    return {
        # Device references
        'device': None,
        'cpe': None,

        # Command execution
        'last_output': None,
        'last_command': None,
        'last_error': None,
        'success': False,

        # DMCLI specific
        'parameter_value': None,
        'saved_values': {},  # Store original values for restoration
        'multiple_results': [],  # Store results from multiple parameter queries

        # File operations
        'test_file': '/tmp/boardfarm_test.txt',
        'test_content': None,

        # General output storage
        'output': None,
    }


# Alias for backward compatibility
@pytest.fixture
def cpe_context(test_context):
    """Alias for test_context for backward compatibility."""
    return test_context


@pytest.fixture
def dmcli_context(test_context):
    """Alias for test_context for DMCLI tests."""
    return test_context


# ============================================================================
# Helper Functions
# ============================================================================

def get_cpe_device(device_manager: DeviceManager):
    """Get either RPI or RDK CPE device from device manager."""
    # Try RDK CPE first
    devices = device_manager.get_devices_by_type(RdkCpeDevice)
    if devices:
        return list(devices.values())[0]

    # Fall back to RPI CPE
    devices = device_manager.get_devices_by_type(RpiCpeDevice)
    if devices:
        return list(devices.values())[0]

    pytest.skip("No CPE devices found in inventory")


def get_rdk_cpe_device(device_manager: DeviceManager):
    """Get RDK CPE device from device manager."""
    devices = device_manager.get_devices_by_type(RdkCpeDevice)
    if not devices:
        pytest.skip("No RDK CPE devices found in inventory")
    return list(devices.values())[0]


def parse_dmcli_output(output: str) -> tuple:
    """Parse DMCLI output to extract parameter value.

    Returns:
        tuple: (success: bool, value: str, error: str)
    """
    # Check for common error patterns
    error_patterns = [
        r"Invalid parameter",
        r"not found",
        r"read-only",
        r"not writable",
        r"Permission denied",
        r"CCSP_ERR",
        r"Execution fail"
    ]

    for pattern in error_patterns:
        if re.search(pattern, output, re.IGNORECASE):
            return False, None, output

    # Try to extract value from different DMCLI output formats
    # Format 1: "value: <value>"
    match = re.search(r'value:\s*(.+?)(?:\n|$)', output, re.IGNORECASE)
    if match:
        value = match.group(1).strip()
        return True, value, None

    # Format 2: "Parameter value = <value>"
    match = re.search(r'Parameter value\s*=\s*(.+?)(?:\n|$)', output, re.IGNORECASE)
    if match:
        value = match.group(1).strip()
        return True, value, None

    # Format 3: Direct value output
    lines = [line.strip() for line in output.split('\n') if line.strip()]
    if lines and not any(error in lines[-1].lower() for error in ['error', 'fail', 'invalid']):
        return True, lines[-1], None

    return False, None, "Could not parse DMCLI output"


# ============================================================================
# GIVEN Steps - Setup and Preconditions
# ============================================================================

@given('a CPE device is configured in the inventory')
def cpe_device_available(device_manager: DeviceManager, test_context):
    """Verify that a CPE device is available in the inventory."""
    cpe = get_cpe_device(device_manager)
    test_context['device'] = cpe
    test_context['cpe'] = cpe
    logger.info(f"CPE device found: {cpe}")


@given('an RDK CPE device is available in the inventory')
def rdk_cpe_device_available(device_manager: DeviceManager, test_context):
    """Verify that an RDK CPE device is available in the inventory."""
    cpe = get_rdk_cpe_device(device_manager)
    test_context['device'] = cpe
    test_context['cpe'] = cpe
    logger.info(f"RDK CPE device found: {cpe}")


@given('I am connected to an RDK CPE device')
def connected_to_rdk_cpe(device_manager: DeviceManager, test_context):
    """Establish connection to RDK CPE device."""
    if test_context['device'] is None:
        cpe = get_rdk_cpe_device(device_manager)
        test_context['device'] = cpe
        test_context['cpe'] = cpe
    logger.info(f"Connected to RDK CPE: {test_context['device']}")


@given('the DMCLI tool is available on the device')
def dmcli_available(test_context):
    """Verify that DMCLI is available on the device."""
    cpe = test_context['device']
    dmcli_check = cpe.command("which dmcli")
    if "dmcli" not in dmcli_check:
        pytest.skip("dmcli not available on this device")
    logger.info("DMCLI tool is available")


# ============================================================================
# WHEN Steps - Actions
# ============================================================================

# --- Connection Actions ---

@when('I connect to the CPE device via SSH')
def connect_to_cpe(test_context):
    """Connect to the CPE device via SSH (connection is automatic)."""
    cpe = test_context['device']
    logger.info(f"SSH connection established to: {cpe}")


@when('I establish an SSH connection to the RDK CPE')
def connect_to_rdk_cpe(test_context):
    """Establish SSH connection to RDK CPE (connection is automatic)."""
    cpe = test_context['device']
    logger.info(f"SSH connection established to RDK CPE: {cpe}")


# --- System Information Queries ---

@when('I query the system hostname')
def query_hostname(test_context):
    """Query the system hostname."""
    cpe = test_context['device']
    test_context['output'] = cpe.command("hostname")
    logger.info(f"Hostname query result: {test_context['output']}")


@when('I query the kernel version')
def query_kernel(test_context):
    """Query the kernel version."""
    cpe = test_context['device']
    test_context['output'] = cpe.command("uname -r")
    logger.info(f"Kernel version: {test_context['output']}")


@when('I query the system uptime')
def query_uptime(test_context):
    """Query the system uptime."""
    cpe = test_context['device']
    test_context['output'] = cpe.command("uptime")
    logger.info(f"Uptime: {test_context['output']}")


# --- Network Information Queries ---

@when('I query the IP address configuration')
def query_ip_config(test_context):
    """Query the IP address configuration."""
    cpe = test_context['device']
    test_context['output'] = cpe.command("ip addr show")
    logger.info(f"IP configuration retrieved ({len(test_context['output'])} bytes)")


@when('I query the routing table')
def query_routing_table(test_context):
    """Query the routing table."""
    cpe = test_context['device']
    test_context['output'] = cpe.command("ip route show")
    logger.info(f"Routing table retrieved ({len(test_context['output'])} bytes)")


# --- Memory and Storage Queries ---

@when('I query the memory usage')
def query_memory_usage(test_context):
    """Query memory usage information."""
    cpe = test_context['device']
    test_context['output'] = cpe.command("free -h")
    logger.info(f"Memory usage:\n{test_context['output']}")


@when('I query the disk usage')
def query_disk_usage(test_context):
    """Query disk usage information."""
    cpe = test_context['device']
    test_context['output'] = cpe.command("df -h")
    logger.info(f"Disk usage:\n{test_context['output']}")


# --- Hardware Information Queries ---

@when('I query the device serial number')
def query_serial_number(test_context):
    """Query the device serial number."""
    cpe = test_context['device']
    try:
        test_context['output'] = cpe.hw.serial_number
        logger.info(f"Serial number: {test_context['output']}")
    except Exception as e:
        logger.warning(f"Could not get serial number: {e}")
        test_context['output'] = None


@when('I query the device MAC address')
def query_mac_address(test_context):
    """Query the device MAC address."""
    cpe = test_context['device']
    try:
        test_context['output'] = cpe.hw.mac_address
        logger.info(f"MAC address: {test_context['output']}")
    except Exception as e:
        logger.warning(f"Could not get MAC address: {e}")
        test_context['output'] = None


# --- File Operations ---

@when(parsers.parse('I create a test file with content "{content}"'))
def create_test_file(test_context, content):
    """Create a test file with specified content."""
    cpe = test_context['device']
    test_file = test_context['test_file']
    test_context['test_content'] = content
    cpe.command(f"echo '{content}' > {test_file}")
    logger.info(f"Created test file: {test_file}")


@when('I read the test file')
def read_test_file(test_context):
    """Read the test file."""
    cpe = test_context['device']
    test_file = test_context['test_file']
    test_context['output'] = cpe.command(f"cat {test_file}")
    logger.info(f"Read test file content: {test_context['output']}")


# --- DMCLI Operations ---

@when(parsers.parse('I get the parameter "{parameter}" using DMCLI'))
def get_parameter_dmcli(test_context, parameter):
    """Get a parameter value using DMCLI."""
    cpe = test_context['device']
    command = f"dmcli eRT getv {parameter}"
    test_context['last_command'] = command

    try:
        output = cpe.command(command)
        test_context['last_output'] = output
        success, value, error = parse_dmcli_output(output)
        test_context['success'] = success
        test_context['parameter_value'] = value
        test_context['last_error'] = error
        test_context['output'] = value  # Also store in output for compatibility
        logger.info(f"DMCLI GET {parameter}: success={success}, value={value}")
    except Exception as e:
        test_context['success'] = False
        test_context['last_error'] = str(e)
        logger.error(f"DMCLI GET failed: {e}")


@when('I save the original value')
def save_original_value(test_context):
    """Save the current parameter value for later restoration."""
    if test_context['success'] and test_context['parameter_value']:
        # Extract parameter name from the last command
        match = re.search(r'getv\s+(\S+)', test_context['last_command'])
        if match:
            param_name = match.group(1)
            test_context['saved_values'][param_name] = test_context['parameter_value']
            logger.info(f"Saved original value for {param_name}: {test_context['parameter_value']}")


@when(parsers.parse('I set the parameter "{parameter}" to "{value}" using DMCLI'))
def set_parameter_dmcli(test_context, parameter, value):
    """Set a parameter value using DMCLI."""
    cpe = test_context['device']

    # Determine the parameter type based on the value
    if value.lower() in ['true', 'false']:
        param_type = 'bool'
    elif value.isdigit():
        param_type = 'int'
    else:
        param_type = 'string'

    command = f"dmcli eRT setv {parameter} {param_type} {value}"
    test_context['last_command'] = command

    try:
        output = cpe.command(command)
        test_context['last_output'] = output

        # Check if set was successful
        success = 'Execution succeed' in output or 'CR_SUCCESS' in output
        if not success:
            test_context['success'] = False
            test_context['last_error'] = output
        else:
            test_context['success'] = True
            test_context['last_error'] = None

        logger.info(f"DMCLI SET {parameter}={value}: success={success}")
    except Exception as e:
        test_context['success'] = False
        test_context['last_error'] = str(e)
        logger.error(f"DMCLI SET failed: {e}")


@when(parsers.parse('I attempt to set the parameter "{parameter}" to "{value}" using DMCLI'))
def attempt_set_parameter_dmcli(test_context, parameter, value):
    """Attempt to set a parameter (expecting it might fail)."""
    set_parameter_dmcli(test_context, parameter, value)


@when('I restore the parameter to its original value')
def restore_parameter(test_context):
    """Restore a parameter to its saved original value."""
    match = re.search(r'setv\s+(\S+)', test_context['last_command'])
    if match:
        param_name = match.group(1)
        if param_name in test_context['saved_values']:
            original_value = test_context['saved_values'][param_name]
            set_parameter_dmcli(test_context, param_name, original_value)
            logger.info(f"Restored {param_name} to {original_value}")


@when('I get the following parameters using DMCLI:')
def get_multiple_parameters(test_context, datatable):
    """Get multiple parameters using DMCLI."""
    test_context['multiple_results'] = []

    for row in datatable:
        parameter = row['Parameter']
        get_parameter_dmcli(test_context, parameter)
        test_context['multiple_results'].append({
            'parameter': parameter,
            'success': test_context['success'],
            'value': test_context['parameter_value'],
            'error': test_context['last_error']
        })


# --- DMCLI via Device Methods ---

@when('I query the device model name using DMCLI')
def query_model_dmcli(test_context):
    """Query device model name using DMCLI."""
    cpe = test_context['device']
    try:
        test_context['output'] = cpe.get_device_model_name()
        logger.info(f"Device model (DMCLI): {test_context['output']}")
    except Exception as e:
        logger.warning(f"DMCLI model query failed: {e}")
        test_context['output'] = None


@when('I query the device serial number using DMCLI')
def query_serial_dmcli(test_context):
    """Query device serial number using DMCLI."""
    cpe = test_context['device']
    try:
        test_context['output'] = cpe.get_device_serial_number()
        logger.info(f"Device serial (DMCLI): {test_context['output']}")
    except Exception as e:
        logger.warning(f"DMCLI serial query failed: {e}")
        test_context['output'] = None


@when('I query the software version using DMCLI')
def query_software_version_dmcli(test_context):
    """Query software version using DMCLI."""
    cpe = test_context['device']
    try:
        test_context['output'] = cpe.get_device_software_version()
        logger.info(f"Software version (DMCLI): {test_context['output']}")
    except Exception as e:
        logger.warning(f"DMCLI software version query failed: {e}")
        test_context['output'] = None


# ============================================================================
# THEN Steps - Assertions and Verification
# ============================================================================

# --- Connection Verification ---

@then('the connection should be successful')
def verify_connection(test_context):
    """Verify that the connection is successful."""
    cpe = test_context['device']
    assert cpe is not None, "CPE device not found"
    output = cpe.command("echo 'SSH CPE is connected'")
    assert "SSH CPE is connected" in output, "Connection test failed"
    logger.info("Connection verified successfully")


@then('I should be able to execute commands')
def verify_command_execution(test_context):
    """Verify that commands can be executed on the device."""
    cpe = test_context['device']
    output = cpe.command("echo 'test'")
    assert "test" in output, "Command execution failed"
    logger.info("Command execution verified")


@then('the RDK CPE connection should be successful')
def verify_rdk_connection(test_context):
    """Verify that RDK CPE connection is successful."""
    cpe = test_context['device']
    assert cpe is not None, "RDK CPE device not found"
    output = cpe.command("echo 'SSH RDK CPE is connected'")
    assert "SSH RDK CPE is connected" in output, "RDK CPE connection test failed"
    logger.info("RDK CPE connection verified successfully")


@then('I should be able to execute RDK-specific commands')
def verify_rdk_commands(test_context):
    """Verify that RDK-specific commands can be executed."""
    cpe = test_context['device']
    output = cpe.command("echo 'RDK test'")
    assert "RDK test" in output, "RDK command execution failed"
    logger.info("RDK command execution verified")


# --- System Information Verification ---

@then('I should receive a valid hostname')
def verify_hostname(test_context):
    """Verify that a valid hostname was received."""
    assert test_context['output'], "Hostname is empty"
    assert len(test_context['output'].strip()) > 0, "Hostname is invalid"
    logger.info(f"Valid hostname received: {test_context['output']}")


@then('I should receive a valid kernel version')
def verify_kernel_version(test_context):
    """Verify that a valid kernel version was received."""
    assert test_context['output'], "Kernel version is empty"
    assert len(test_context['output'].strip()) > 0, "Kernel version is invalid"
    logger.info(f"Valid kernel version received: {test_context['output']}")


@then('I should receive uptime information')
def verify_uptime(test_context):
    """Verify that uptime information was received."""
    assert test_context['output'], "Uptime information is empty"
    logger.info(f"Uptime information received: {test_context['output']}")


@then('I should receive IP address information')
def verify_ip_info(test_context):
    """Verify that IP address information was received."""
    assert test_context['output'], "IP address information is empty"
    logger.info("IP address information verified")


@then('I should receive routing information')
def verify_routing_info(test_context):
    """Verify that routing information was received."""
    assert test_context['output'], "Routing information is empty"
    logger.info("Routing information verified")


# --- Memory and Storage Verification ---

@then('I should receive memory information')
def verify_memory_info(test_context):
    """Verify that memory information was received."""
    assert test_context['output'], "Memory information is empty"
    logger.info("Memory information verified")


@then('the memory information should contain usage statistics')
def verify_memory_stats(test_context):
    """Verify that memory information contains usage statistics."""
    mem_info = test_context['output']
    assert "Mem:" in mem_info, "Memory usage statistics not found"
    logger.info("Memory usage statistics verified")


@then('I should receive disk usage information')
def verify_disk_info(test_context):
    """Verify that disk usage information was received."""
    assert test_context['output'], "Disk usage information is empty"
    logger.info("Disk usage information verified")


@then('the disk information should contain filesystem details')
def verify_filesystem_details(test_context):
    """Verify that disk information contains filesystem details."""
    disk_info = test_context['output']
    assert "Filesystem" in disk_info or "/" in disk_info, "Filesystem details not found"
    logger.info("Filesystem details verified")


# --- Hardware Information Verification ---

@then('I should receive a valid serial number')
def verify_serial_number(test_context):
    """Verify that a valid serial number was received."""
    if test_context['output'] is None:
        pytest.skip("Serial number not available on this device")
    assert test_context['output'], "Serial number is empty"
    logger.info(f"Valid serial number received: {test_context['output']}")


@then('I should receive a valid MAC address')
def verify_mac_address(test_context):
    """Verify that a valid MAC address was received."""
    if test_context['output'] is None:
        pytest.skip("MAC address not available on this device")
    assert test_context['output'], "MAC address is empty"
    logger.info(f"Valid MAC address received: {test_context['output']}")


# --- File Operations Verification ---

@then('the file should be created successfully')
def verify_file_created(test_context):
    """Verify that the file was created successfully."""
    cpe = test_context['device']
    test_file = test_context['test_file']
    result = cpe.command(f"test -f {test_file} && echo 'exists' || echo 'not found'")
    assert 'exists' in result, "File was not created"
    logger.info("File created successfully")


@then(parsers.parse('the content should match "{expected_content}"'))
def verify_file_content(test_context, expected_content):
    """Verify that the file content matches the expected content."""
    assert test_context['output'], "File content is empty"
    assert expected_content in test_context['output'], "File content does not match"
    logger.info(f"File content matches: {expected_content}")


@then('I cleanup the test file')
def cleanup_test_file(test_context):
    """Clean up the test file."""
    cpe = test_context['device']
    test_file = test_context['test_file']
    cpe.command(f"rm -f {test_file}")
    logger.info("Test file cleaned up")


# --- DMCLI Verification ---

@then('the DMCLI command should succeed')
def verify_dmcli_success(test_context):
    """Verify that the DMCLI command succeeded."""
    assert test_context['success'], \
        f"DMCLI command failed: {test_context['last_error']}\nOutput: {test_context['last_output']}"
    logger.info("DMCLI command succeeded")


@then('the DMCLI command should fail')
def verify_dmcli_failure(test_context):
    """Verify that the DMCLI command failed (as expected)."""
    assert not test_context['success'], \
        f"DMCLI command was expected to fail but succeeded"
    logger.info("DMCLI command failed as expected")


@then('the parameter value should not be empty')
def verify_value_not_empty(test_context):
    """Verify that the parameter value is not empty."""
    value = test_context.get('parameter_value') or test_context.get('output')
    assert value, "Parameter value is empty"
    assert len(str(value).strip()) > 0, "Parameter value is empty after stripping whitespace"
    logger.info(f"Parameter value is not empty: {value}")


@then(parsers.parse('the parameter value should be "{expected_value}"'))
def verify_parameter_value(test_context, expected_value):
    """Verify that the parameter value matches the expected value."""
    actual_value = test_context.get('parameter_value') or test_context.get('output')
    assert str(actual_value) == expected_value, \
        f"Parameter value mismatch: expected '{expected_value}', got '{actual_value}'"
    logger.info(f"Parameter value matches: {expected_value}")


@then(parsers.parse('the parameter value should match the pattern "{pattern}"'))
def verify_value_matches_pattern(test_context, pattern):
    """Verify that the parameter value matches a regex pattern."""
    value = test_context.get('parameter_value') or test_context.get('output')
    assert re.match(pattern, str(value)), \
        f"Parameter value '{value}' does not match pattern '{pattern}'"
    logger.info(f"Parameter value matches pattern: {pattern}")


@then('the parameter value should be a valid IP address')
def verify_value_is_ip(test_context):
    """Verify that the parameter value is a valid IP address."""
    value = test_context.get('parameter_value') or test_context.get('output')
    ip_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
    assert re.match(ip_pattern, str(value)), \
        f"Parameter value '{value}' is not a valid IP address"
    logger.info(f"Parameter value is a valid IP address: {value}")


@then('the parameter value should be a boolean')
def verify_value_is_boolean(test_context):
    """Verify that the parameter value is a boolean."""
    value = str(test_context.get('parameter_value') or test_context.get('output')).lower()
    assert value in ['true', 'false', '0', '1'], \
        f"Parameter value '{value}' is not a boolean"
    logger.info(f"Parameter value is a boolean: {value}")


@then(parsers.parse('the error message should contain "{text1}" or "{text2}"'))
def verify_error_contains_text(test_context, text1, text2):
    """Verify that the error message contains specific text."""
    error = test_context['last_error'] or test_context['last_output']
    assert error, "No error message found"
    assert text1.lower() in error.lower() or text2.lower() in error.lower(), \
        f"Error message does not contain '{text1}' or '{text2}': {error}"
    logger.info(f"Error message contains expected text")


@then('all DMCLI commands should succeed')
def verify_all_commands_succeed(test_context):
    """Verify that all DMCLI commands in the batch succeeded."""
    failures = [r for r in test_context['multiple_results'] if not r['success']]
    assert len(failures) == 0, \
        f"Some DMCLI commands failed: {failures}"
    logger.info("All DMCLI commands succeeded")


@then('all parameter values should not be empty')
def verify_all_values_not_empty(test_context):
    """Verify that all parameter values are not empty."""
    empty_values = [r for r in test_context['multiple_results']
                   if not r['value'] or len(str(r['value']).strip()) == 0]
    assert len(empty_values) == 0, \
        f"Some parameter values are empty: {empty_values}"
    logger.info("All parameter values are not empty")


# --- Device Model/Serial/Version Verification ---

@then('I should receive the device model information')
def verify_device_model(test_context):
    """Verify that device model information was received."""
    if test_context['output'] is None:
        pytest.skip("Device model not available via DMCLI")
    assert test_context['output'], "Device model is empty"
    logger.info(f"Device model received: {test_context['output']}")


@then('I should receive the device serial via DMCLI')
def verify_serial_dmcli(test_context):
    """Verify that device serial was received via DMCLI."""
    if test_context['output'] is None:
        pytest.skip("Device serial not available via DMCLI")
    assert test_context['output'], "Device serial is empty"
    logger.info(f"Device serial (DMCLI) received: {test_context['output']}")


@then('I should receive the software version information')
def verify_software_version(test_context):
    """Verify that software version information was received."""
    if test_context['output'] is None:
        pytest.skip("Software version not available via DMCLI")
    assert test_context['output'], "Software version is empty"
    logger.info(f"Software version received: {test_context['output']}")
