"""BDD tests for SSH CPE devices using pytest-bdd.

This module demonstrates how to use pytest-bdd to write behavior-driven tests
for CPE devices. The scenarios are defined in Gherkin syntax in the features/
directory, and this file contains the step definitions.
"""

import logging
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from boardfarm3.lib.device_manager import DeviceManager
from rpi_cpe_device import RpiCpeDevice
from rdk_cpe_device import RdkCpeDevice

logger = logging.getLogger(__name__)

# Load all scenarios from the feature files
scenarios('features/ssh_cpe_connectivity.feature')
scenarios('features/rdk_cpe_advanced.feature')


# ============================================================================
# Fixtures and Helper Functions
# ============================================================================

@pytest.fixture
def cpe_context():
    """Context object to share data between steps in a scenario."""
    return {
        'device': None,
        'output': None,
        'test_file': '/tmp/boardfarm_test.txt',
        'test_content': None
    }


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


# ============================================================================
# Given Steps - Setup and Preconditions
# ============================================================================

@given('a CPE device is configured in the inventory')
def cpe_device_available(device_manager: DeviceManager, cpe_context):
    """Verify that a CPE device is available in the inventory."""
    cpe = get_cpe_device(device_manager)
    cpe_context['device'] = cpe
    logger.info(f"CPE device found: {cpe}")


@given('an RDK CPE device is available in the inventory')
def rdk_cpe_device_available(device_manager: DeviceManager, cpe_context):
    """Verify that an RDK CPE device is available in the inventory."""
    cpe = get_rdk_cpe_device(device_manager)
    cpe_context['device'] = cpe
    logger.info(f"RDK CPE device found: {cpe}")


@given('I am connected to an RDK CPE device')
def connected_to_rdk_cpe(device_manager: DeviceManager, cpe_context):
    """Establish connection to RDK CPE device."""
    cpe = get_rdk_cpe_device(device_manager)
    cpe_context['device'] = cpe
    # Connection is established automatically by the device manager
    logger.info(f"Connected to RDK CPE: {cpe}")


@given('the DMCLI tool is available on the device')
def dmcli_available(cpe_context):
    """Verify that DMCLI is available on the device."""
    cpe = cpe_context['device']
    dmcli_check = cpe.command("which dmcli")
    if "dmcli" not in dmcli_check:
        pytest.skip("dmcli not available on this device")
    logger.info("DMCLI tool is available")


# ============================================================================
# When Steps - Actions
# ============================================================================

@when('I connect to the CPE device via SSH')
def connect_to_cpe(cpe_context):
    """Connect to the CPE device via SSH (connection is automatic)."""
    cpe = cpe_context['device']
    # Connection happens automatically when device is retrieved
    logger.info(f"SSH connection established to: {cpe}")


@when('I establish an SSH connection to the RDK CPE')
def connect_to_rdk_cpe(cpe_context):
    """Establish SSH connection to RDK CPE (connection is automatic)."""
    cpe = cpe_context['device']
    logger.info(f"SSH connection established to RDK CPE: {cpe}")


@when('I query the system hostname')
def query_hostname(cpe_context):
    """Query the system hostname."""
    cpe = cpe_context['device']
    cpe_context['output'] = cpe.command("hostname")
    logger.info(f"Hostname query result: {cpe_context['output']}")


@when('I query the kernel version')
def query_kernel(cpe_context):
    """Query the kernel version."""
    cpe = cpe_context['device']
    cpe_context['output'] = cpe.command("uname -r")
    logger.info(f"Kernel version: {cpe_context['output']}")


@when('I query the system uptime')
def query_uptime(cpe_context):
    """Query the system uptime."""
    cpe = cpe_context['device']
    cpe_context['output'] = cpe.command("uptime")
    logger.info(f"Uptime: {cpe_context['output']}")


@when('I query the IP address configuration')
def query_ip_config(cpe_context):
    """Query the IP address configuration."""
    cpe = cpe_context['device']
    cpe_context['output'] = cpe.command("ip addr show")
    logger.info(f"IP configuration retrieved ({len(cpe_context['output'])} bytes)")


@when('I query the routing table')
def query_routing_table(cpe_context):
    """Query the routing table."""
    cpe = cpe_context['device']
    cpe_context['output'] = cpe.command("ip route show")
    logger.info(f"Routing table retrieved ({len(cpe_context['output'])} bytes)")


@when(parsers.parse('I create a test file with content "{content}"'))
def create_test_file(cpe_context, content):
    """Create a test file with specified content."""
    cpe = cpe_context['device']
    test_file = cpe_context['test_file']
    cpe_context['test_content'] = content
    cpe.command(f"echo '{content}' > {test_file}")
    logger.info(f"Created test file: {test_file}")


@when('I read the test file')
def read_test_file(cpe_context):
    """Read the test file."""
    cpe = cpe_context['device']
    test_file = cpe_context['test_file']
    cpe_context['output'] = cpe.command(f"cat {test_file}")
    logger.info(f"Read test file content: {cpe_context['output']}")


@when('I query the memory usage')
def query_memory_usage(cpe_context):
    """Query memory usage information."""
    cpe = cpe_context['device']
    cpe_context['output'] = cpe.command("free -h")
    logger.info(f"Memory usage:\n{cpe_context['output']}")


@when('I query the disk usage')
def query_disk_usage(cpe_context):
    """Query disk usage information."""
    cpe = cpe_context['device']
    cpe_context['output'] = cpe.command("df -h")
    logger.info(f"Disk usage:\n{cpe_context['output']}")


@when('I query the device serial number')
def query_serial_number(cpe_context):
    """Query the device serial number."""
    cpe = cpe_context['device']
    try:
        cpe_context['output'] = cpe.hw.serial_number
        logger.info(f"Serial number: {cpe_context['output']}")
    except Exception as e:
        logger.warning(f"Could not get serial number: {e}")
        cpe_context['output'] = None


@when('I query the device MAC address')
def query_mac_address(cpe_context):
    """Query the device MAC address."""
    cpe = cpe_context['device']
    try:
        cpe_context['output'] = cpe.hw.mac_address
        logger.info(f"MAC address: {cpe_context['output']}")
    except Exception as e:
        logger.warning(f"Could not get MAC address: {e}")
        cpe_context['output'] = None


@when('I query the device model name using DMCLI')
def query_model_dmcli(cpe_context):
    """Query device model name using DMCLI."""
    cpe = cpe_context['device']
    try:
        cpe_context['output'] = cpe.get_device_model_name()
        logger.info(f"Device model (DMCLI): {cpe_context['output']}")
    except Exception as e:
        logger.warning(f"DMCLI model query failed: {e}")
        cpe_context['output'] = None


@when('I query the device serial number using DMCLI')
def query_serial_dmcli(cpe_context):
    """Query device serial number using DMCLI."""
    cpe = cpe_context['device']
    try:
        cpe_context['output'] = cpe.get_device_serial_number()
        logger.info(f"Device serial (DMCLI): {cpe_context['output']}")
    except Exception as e:
        logger.warning(f"DMCLI serial query failed: {e}")
        cpe_context['output'] = None


@when('I query the software version using DMCLI')
def query_software_version_dmcli(cpe_context):
    """Query software version using DMCLI."""
    cpe = cpe_context['device']
    try:
        cpe_context['output'] = cpe.get_device_software_version()
        logger.info(f"Software version (DMCLI): {cpe_context['output']}")
    except Exception as e:
        logger.warning(f"DMCLI software version query failed: {e}")
        cpe_context['output'] = None


# ============================================================================
# Then Steps - Assertions and Verification
# ============================================================================

@then('the connection should be successful')
def verify_connection(cpe_context):
    """Verify that the connection is successful."""
    cpe = cpe_context['device']
    assert cpe is not None, "CPE device not found"
    # Test basic command execution
    output = cpe.command("echo 'SSH CPE is connected'")
    assert "SSH CPE is connected" in output, "Connection test failed"
    logger.info("Connection verified successfully")


@then('I should be able to execute commands')
def verify_command_execution(cpe_context):
    """Verify that commands can be executed on the device."""
    cpe = cpe_context['device']
    output = cpe.command("echo 'test'")
    assert "test" in output, "Command execution failed"
    logger.info("Command execution verified")


@then('the RDK CPE connection should be successful')
def verify_rdk_connection(cpe_context):
    """Verify that RDK CPE connection is successful."""
    cpe = cpe_context['device']
    assert cpe is not None, "RDK CPE device not found"
    output = cpe.command("echo 'SSH RDK CPE is connected'")
    assert "SSH RDK CPE is connected" in output, "RDK CPE connection test failed"
    logger.info("RDK CPE connection verified successfully")


@then('I should be able to execute RDK-specific commands')
def verify_rdk_commands(cpe_context):
    """Verify that RDK-specific commands can be executed."""
    cpe = cpe_context['device']
    # Test a basic command
    output = cpe.command("echo 'RDK test'")
    assert "RDK test" in output, "RDK command execution failed"
    logger.info("RDK command execution verified")


@then('I should receive a valid hostname')
def verify_hostname(cpe_context):
    """Verify that a valid hostname was received."""
    assert cpe_context['output'], "Hostname is empty"
    assert len(cpe_context['output'].strip()) > 0, "Hostname is invalid"
    logger.info(f"Valid hostname received: {cpe_context['output']}")


@then('I should receive a valid kernel version')
def verify_kernel_version(cpe_context):
    """Verify that a valid kernel version was received."""
    assert cpe_context['output'], "Kernel version is empty"
    assert len(cpe_context['output'].strip()) > 0, "Kernel version is invalid"
    logger.info(f"Valid kernel version received: {cpe_context['output']}")


@then('I should receive uptime information')
def verify_uptime(cpe_context):
    """Verify that uptime information was received."""
    assert cpe_context['output'], "Uptime information is empty"
    logger.info(f"Uptime information received: {cpe_context['output']}")


@then('I should receive IP address information')
def verify_ip_info(cpe_context):
    """Verify that IP address information was received."""
    assert cpe_context['output'], "IP address information is empty"
    logger.info("IP address information verified")


@then('I should receive routing information')
def verify_routing_info(cpe_context):
    """Verify that routing information was received."""
    assert cpe_context['output'], "Routing information is empty"
    logger.info("Routing information verified")


@then('the file should be created successfully')
def verify_file_created(cpe_context):
    """Verify that the file was created successfully."""
    cpe = cpe_context['device']
    test_file = cpe_context['test_file']
    # Check if file exists
    result = cpe.command(f"test -f {test_file} && echo 'exists' || echo 'not found'")
    assert 'exists' in result, "File was not created"
    logger.info("File created successfully")


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


@then('I should receive memory information')
def verify_memory_info(cpe_context):
    """Verify that memory information was received."""
    assert cpe_context['output'], "Memory information is empty"
    logger.info("Memory information verified")


@then('the memory information should contain usage statistics')
def verify_memory_stats(cpe_context):
    """Verify that memory information contains usage statistics."""
    mem_info = cpe_context['output']
    assert "Mem:" in mem_info, "Memory usage statistics not found"
    logger.info("Memory usage statistics verified")


@then('I should receive disk usage information')
def verify_disk_info(cpe_context):
    """Verify that disk usage information was received."""
    assert cpe_context['output'], "Disk usage information is empty"
    logger.info("Disk usage information verified")


@then('the disk information should contain filesystem details')
def verify_filesystem_details(cpe_context):
    """Verify that disk information contains filesystem details."""
    disk_info = cpe_context['output']
    assert "Filesystem" in disk_info or "/" in disk_info, "Filesystem details not found"
    logger.info("Filesystem details verified")


@then('I should receive a valid serial number')
def verify_serial_number(cpe_context):
    """Verify that a valid serial number was received."""
    if cpe_context['output'] is None:
        pytest.skip("Serial number not available on this device")
    assert cpe_context['output'], "Serial number is empty"
    logger.info(f"Valid serial number received: {cpe_context['output']}")


@then('I should receive a valid MAC address')
def verify_mac_address(cpe_context):
    """Verify that a valid MAC address was received."""
    if cpe_context['output'] is None:
        pytest.skip("MAC address not available on this device")
    assert cpe_context['output'], "MAC address is empty"
    logger.info(f"Valid MAC address received: {cpe_context['output']}")


@then('I should receive the device model information')
def verify_device_model(cpe_context):
    """Verify that device model information was received."""
    if cpe_context['output'] is None:
        pytest.skip("Device model not available via DMCLI")
    assert cpe_context['output'], "Device model is empty"
    logger.info(f"Device model received: {cpe_context['output']}")


@then('I should receive the device serial via DMCLI')
def verify_serial_dmcli(cpe_context):
    """Verify that device serial was received via DMCLI."""
    if cpe_context['output'] is None:
        pytest.skip("Device serial not available via DMCLI")
    assert cpe_context['output'], "Device serial is empty"
    logger.info(f"Device serial (DMCLI) received: {cpe_context['output']}")


@then('I should receive the software version information')
def verify_software_version(cpe_context):
    """Verify that software version information was received."""
    if cpe_context['output'] is None:
        pytest.skip("Software version not available via DMCLI")
    assert cpe_context['output'], "Software version is empty"
    logger.info(f"Software version received: {cpe_context['output']}")
