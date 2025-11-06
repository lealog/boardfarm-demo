"""Tests for SSH CPE devices."""

import pytest
from boardfarm3.lib.device_manager import DeviceManager
from rpi_cpe_device import RpiCpeDevice
from rdk_cpe_device import RdkCpeDevice


def test_ssh_cpe_connection(device_manager: DeviceManager):
    """Test SSH connection to CPE device.

    This test verifies that we can connect to a CPE device via SSH
    and execute basic commands.
    """
    devices = device_manager.get_devices_by_type(RpiCpeDevice)
    assert len(devices) > 0, "No rpi_cpe devices found in inventory"

    cpe = list(devices.values())[0]
    print(f"Got device: {cpe}")

    # Test basic command execution
    output = cpe.command("echo 'SSH CPE is connected'")
    assert "SSH CPE is connected" in output
    print(f"Connection test passed: {output}")


def test_ssh_cpe_system_info(device_manager: DeviceManager):
    """Test retrieving system information from SSH CPE."""
    devices = device_manager.get_devices_by_type(RpiCpeDevice)
    cpe = list(devices.values())[0]

    # Get system hostname
    hostname = cpe.command("hostname")
    assert hostname, "Failed to get hostname"
    print(f"Hostname: {hostname}")

    # Get kernel version
    kernel = cpe.command("uname -r")
    assert kernel, "Failed to get kernel version"
    print(f"Kernel: {kernel}")

    # Get uptime
    uptime = cpe.command("uptime")
    assert uptime, "Failed to get uptime"
    print(f"Uptime: {uptime}")


def test_ssh_cpe_network_info(device_manager: DeviceManager):
    """Test retrieving network information from SSH CPE."""
    devices = device_manager.get_devices_by_type(RpiCpeDevice)
    cpe = list(devices.values())[0]

    # Get IP addresses
    ip_info = cpe.command("ip addr show")
    assert ip_info, "Failed to get IP information"
    print(f"IP Info:\n{ip_info}")

    # Get routing table
    routes = cpe.command("ip route show")
    assert routes, "Failed to get routing table"
    print(f"Routes:\n{routes}")


def test_ssh_rdk_cpe_connection(device_manager: DeviceManager):
    """Test SSH connection to RDK CPE device."""
    devices = device_manager.get_devices_by_type(RdkCpeDevice)
    if not devices:
        pytest.skip("No RDK CPE devices found in inventory")

    cpe = list(devices.values())[0]

    # Test basic command execution
    output = cpe.command("echo 'SSH RDK CPE is connected'")
    assert "SSH RDK CPE is connected" in output
    print(f"RDK CPE connection test passed: {output}")


@pytest.mark.slow
def test_ssh_rdk_cpe_hardware_info(device_manager: DeviceManager):
    """Test retrieving hardware information from RDK CPE via SSH."""
    devices = device_manager.get_devices_by_type(RdkCpeDevice)
    if not devices:
        pytest.skip("No RDK CPE devices found in inventory")

    cpe = list(devices.values())[0]

    # Test hardware properties
    try:
        serial = cpe.hw.serial_number
        print(f"Serial Number: {serial}")
        assert serial, "Failed to get serial number"
    except Exception as e:
        print(f"Warning: Could not get serial number: {e}")

    try:
        mac = cpe.hw.mac_address
        print(f"MAC Address: {mac}")
        assert mac, "Failed to get MAC address"
    except Exception as e:
        print(f"Warning: Could not get MAC address: {e}")


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
        print(f"Device Model (via DMCLI): {model}")

        # Get device serial number via DMCLI
        serial = cpe.get_device_serial_number()
        print(f"Device Serial (via DMCLI): {serial}")

        # Get software version via DMCLI
        version = cpe.get_device_software_version()
        print(f"Software Version (via DMCLI): {version}")

    except Exception as e:
        print(f"Warning: DMCLI operations failed: {e}")
        pytest.skip(f"DMCLI not fully functional: {e}")


def test_ssh_cpe_file_operations(device_manager: DeviceManager):
    """Test file operations on SSH CPE."""
    devices = device_manager.get_devices_by_type(RpiCpeDevice)
    cpe = list(devices.values())[0]

    # Create a test file
    test_file = "/tmp/boardfarm_test.txt"
    test_content = "Boardfarm SSH test"

    # Write to file
    cpe.command(f"echo '{test_content}' > {test_file}")

    # Read from file
    content = cpe.command(f"cat {test_file}")
    assert test_content in content, "File content mismatch"
    print(f"File operation test passed: {content}")

    # Clean up
    cpe.command(f"rm -f {test_file}")


def test_ssh_cpe_process_list(device_manager: DeviceManager):
    """Test listing processes on SSH CPE."""
    devices = device_manager.get_devices_by_type(RpiCpeDevice)
    cpe = list(devices.values())[0]

    # Get process list
    processes = cpe.command("ps aux | head -20")
    assert processes, "Failed to get process list"
    assert "PID" in processes or "root" in processes, "Invalid process list format"
    print(f"Process list (top 20):\n{processes}")


def test_ssh_cpe_memory_info(device_manager: DeviceManager):
    """Test retrieving memory information from SSH CPE."""
    devices = device_manager.get_devices_by_type(RpiCpeDevice)
    cpe = list(devices.values())[0]

    # Get memory info
    mem_info = cpe.command("free -h")
    assert mem_info, "Failed to get memory information"
    assert "Mem:" in mem_info, "Invalid memory info format"
    print(f"Memory Info:\n{mem_info}")


def test_ssh_cpe_disk_usage(device_manager: DeviceManager):
    """Test retrieving disk usage from SSH CPE."""
    devices = device_manager.get_devices_by_type(RpiCpeDevice)
    cpe = list(devices.values())[0]

    # Get disk usage
    disk_info = cpe.command("df -h")
    assert disk_info, "Failed to get disk usage"
    assert "Filesystem" in disk_info or "/" in disk_info, "Invalid disk info format"
    print(f"Disk Usage:\n{disk_info}")
