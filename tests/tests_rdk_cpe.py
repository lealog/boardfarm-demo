"""Test cases for RDK CPE device using boardfarm3."""

import logging
import pytest
from boardfarm3.lib.device_manager import DeviceManager
from rdk_cpe_device import RdkCpeDevice

logger = logging.getLogger(__name__)


@pytest.mark.integration
def test_rdk_cpe_connection(device_manager: DeviceManager):
    """Test RDK CPE device connection."""
    logger.info("Testing RDK CPE connection")
    devices = device_manager.get_devices_by_type(RdkCpeDevice)
    assert len(devices) > 0, "No RDK CPE devices found"

    cpe = list(devices.values())[0]
    logger.info(f"Got CPE device: {cpe}")
    assert cpe is not None

    # Test basic command execution
    output = cpe.command("echo 'RDK CPE is connected'")
    logger.info(f"Command output: {output}")
    assert "RDK CPE is connected" in output
    logger.info("✓ RDK CPE connection test passed")


@pytest.mark.integration
def test_rdk_cpe_hardware_info(device_manager: DeviceManager):
    """Test RDK CPE hardware information retrieval."""
    logger.info("Testing RDK CPE hardware information")
    devices = device_manager.get_devices_by_type(RdkCpeDevice)
    cpe = list(devices.values())[0]

    # Check hardware properties
    assert cpe.hw is not None
    logger.info(f"WAN interface: {cpe.hw.wan_iface}")
    assert cpe.hw.wan_iface == "erouter0"  # Based on config

    # Test MAC address retrieval
    mac = cpe.hw.mac_address
    logger.info(f"MAC address: {mac}")
    assert mac is not None
    assert len(mac) == 17  # MAC address format XX:XX:XX:XX:XX:XX

    # Test serial number
    serial = cpe.hw.serial_number
    logger.info(f"Serial number: {serial}")
    assert serial is not None
    assert len(serial) > 0
    logger.info("✓ Hardware info test passed")


@pytest.mark.integration
def test_rdk_cpe_software_info(device_manager: DeviceManager):
    """Test RDK CPE software information retrieval."""
    logger.info("Testing RDK CPE software information")
    devices = device_manager.get_devices_by_type(RdkCpeDevice)
    cpe = list(devices.values())[0]

    # Check software properties
    assert cpe.sw is not None

    # Test version retrieval
    version = cpe.sw.version
    logger.info(f"Software version: {version}")
    assert version is not None
    assert len(version) > 0

    # Test interface names
    logger.info(f"eRouter interface: {cpe.sw.erouter_iface}")
    logger.info(f"LAN interface: {cpe.sw.lan_iface}")
    assert cpe.sw.erouter_iface == "erouter0"
    assert cpe.sw.lan_iface == "br0"

    # Test CPE ID
    cpe_id = cpe.sw.cpe_id
    logger.info(f"CPE ID: {cpe_id}")
    assert cpe_id is not None
    assert "-" in cpe_id  # Format: OUI-SERIAL
    logger.info("✓ Software info test passed")


@pytest.mark.integration
def test_rdk_cpe_network_interfaces(device_manager: DeviceManager):
    """Test RDK CPE network interface information."""
    logger.info("Testing RDK CPE network interfaces")
    devices = device_manager.get_devices_by_type(RdkCpeDevice)
    cpe = list(devices.values())[0]

    # Check WAN interface
    logger.info(f"Checking WAN interface: {cpe.hw.wan_iface}")
    output = cpe.command(f"ip addr show {cpe.hw.wan_iface}")
    assert cpe.hw.wan_iface in output

    # Check LAN interface
    logger.info(f"Checking LAN interface: {cpe.sw.lan_iface}")
    output = cpe.command(f"ip addr show {cpe.sw.lan_iface}")
    assert cpe.sw.lan_iface in output

    # Get LAN gateway IP
    lan_ip = cpe.sw.lan_gateway_ipv4
    logger.info(f"LAN gateway IP: {lan_ip}")
    assert lan_ip is not None
    assert str(lan_ip).startswith("192.168.") or str(lan_ip).startswith("10.")
    logger.info("✓ Network interfaces test passed")


@pytest.mark.integration
def test_rdk_cpe_system_commands(device_manager: DeviceManager):
    """Test RDK CPE system command execution."""
    logger.info("Testing RDK CPE system commands")
    devices = device_manager.get_devices_by_type(RdkCpeDevice)
    cpe = list(devices.values())[0]

    # Test hostname
    hostname = cpe.command("hostname").strip()
    logger.info(f"Hostname: {hostname}")
    assert hostname == cpe.hw.config.get("hostname", "RaspberryPi-Gateway")

    # Test kernel info
    kernel = cpe.command("uname -r").strip()
    logger.info(f"Kernel version: {kernel}")
    assert len(kernel) > 0

    # Test uptime
    uptime = cpe.command("uptime")
    logger.info(f"Uptime: {uptime.strip()}")
    assert "load average" in uptime

    # Test process list (BusyBox compatible)
    processes = cpe.command("ps aux | head -n 10")
    logger.info(f"Top processes:\n{processes}")
    assert "PID" in processes or "pid" in processes.lower()
    logger.info("✓ System commands test passed")


@pytest.mark.integration
@pytest.mark.slow
def test_rdk_cpe_provision_mode(device_manager: DeviceManager):
    """Test RDK CPE provisioning mode."""
    logger.info("Testing RDK CPE provisioning mode")
    devices = device_manager.get_devices_by_type(RdkCpeDevice)
    cpe = list(devices.values())[0]

    # Check provisioning mode
    mode = cpe.sw.get_provision_mode()
    logger.info(f"Provisioning mode: {mode}")
    assert mode in ["ipv4", "ipv6", "dual"]
    assert mode == "ipv4"  # Based on our config
    logger.info("✓ Provisioning mode test passed")


@pytest.mark.integration
def test_rdk_cpe_json_values(device_manager: DeviceManager):
    """Test RDK CPE JSON values retrieval."""
    logger.info("Testing RDK CPE JSON values")
    devices = device_manager.get_devices_by_type(RdkCpeDevice)
    cpe = list(devices.values())[0]

    # Get JSON values (device-specific config/status)
    json_values = cpe.sw.json_values
    logger.info(f"JSON values: {json_values}")
    assert isinstance(json_values, dict)
    assert len(json_values) > 0

    # Should have at least hostname and kernel
    if "hostname" in json_values:
        logger.info(f"Hostname from JSON: {json_values['hostname']}")
        assert json_values["hostname"] == cpe.hw.config.get("hostname", "RDK-RaspberryPi")
    logger.info("✓ JSON values test passed")


@pytest.mark.integration
def test_rdk_cpe_mtu_size(device_manager: DeviceManager):
    """Test RDK CPE interface MTU size retrieval."""
    logger.info("Testing RDK CPE MTU size")
    devices = device_manager.get_devices_by_type(RdkCpeDevice)
    cpe = list(devices.values())[0]

    # Check MTU size for WAN interface
    try:
        mtu = cpe.sw.get_interface_mtu_size(cpe.hw.wan_iface)
        logger.info(f"MTU size for {cpe.hw.wan_iface}: {mtu}")
        assert isinstance(mtu, int)
        assert 1000 <= mtu <= 9000  # Typical MTU range
        logger.info("✓ MTU size test passed")
    except ValueError:
        logger.warning(f"Interface {cpe.hw.wan_iface} not available")
        pytest.skip(f"Interface {cpe.hw.wan_iface} not available")


@pytest.mark.integration
def test_rdk_cpe_is_online(device_manager: DeviceManager):
    """Test if RDK CPE is online."""
    logger.info("Testing RDK CPE online status")
    devices = device_manager.get_devices_by_type(RdkCpeDevice)
    cpe = list(devices.values())[0]

    # Check if device is online
    is_online = cpe.sw.is_online()
    logger.info(f"Device online status: {is_online}")
    assert isinstance(is_online, bool)

    # If online, should be able to ping external host
    if is_online:
        logger.info("Testing internet connectivity with ping to 8.8.8.8")
        output = cpe.command("ping -c 1 8.8.8.8")
        logger.info(f"Ping result:\n{output}")
        assert "1 packets transmitted" in output or "1 packets received" in output
        logger.info("✓ Device is online and can reach internet")
    else:
        logger.info("ℹ Device is not online")
    logger.info("✓ Online status test passed")
