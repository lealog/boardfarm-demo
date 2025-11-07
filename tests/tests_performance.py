"""Performance tests using speedtest-cli.

This module contains tests for measuring real-world internet performance
using speedtest-cli tool, which tests against Ookla's speedtest servers.
"""

import json
import logging
import pytest
from boardfarm3.lib.device_manager import DeviceManager
from rdk_cpe_device import RdkCpeDevice

logger = logging.getLogger(__name__)


class TestPerformance:
    """Performance tests using speedtest-cli."""

    def _get_board(self, device_manager: DeviceManager) -> RdkCpeDevice:
        """Get the RDK CPE device from device manager."""
        devices = device_manager.get_devices_by_type(RdkCpeDevice)
        assert len(devices) > 0, "No RDK CPE devices found"
        return list(devices.values())[0]

    def _ensure_speedtest_installed(self, board: RdkCpeDevice) -> bool:
        """Ensure speedtest-cli is installed on the device.

        Returns:
            bool: True if speedtest-cli is available, False otherwise
        """
        logger.info("Checking if speedtest-cli is installed...")

        try:
            # Check if speedtest-cli is already installed
            result = board.command("which speedtest-cli", timeout=10)
            if result.strip() and "speedtest-cli" in result:
                logger.info("✓ speedtest-cli is already installed")
                return True

            logger.info("speedtest-cli not found, attempting to install...")

            # Try pip installation (most common method)
            try:
                logger.info("Trying to install via pip...")
                board.command("pip install speedtest-cli", timeout=120)

                # Verify installation
                result = board.command("which speedtest-cli", timeout=10)
                if "speedtest-cli" in result:
                    logger.info("✓ speedtest-cli installed successfully via pip")
                    return True
            except Exception as e:
                logger.warning(f"pip installation failed: {e}")

            # Try pip3
            try:
                logger.info("Trying to install via pip3...")
                board.command("pip3 install speedtest-cli", timeout=120)

                # Verify installation
                result = board.command("which speedtest-cli", timeout=10)
                if "speedtest-cli" in result:
                    logger.info("✓ speedtest-cli installed successfully via pip3")
                    return True
            except Exception as e:
                logger.warning(f"pip3 installation failed: {e}")

            # Try apt-get (Debian/Ubuntu)
            try:
                logger.info("Trying to install via apt-get...")
                board.command("apt-get update && apt-get install -y speedtest-cli", timeout=180)

                # Verify installation
                result = board.command("which speedtest-cli", timeout=10)
                if "speedtest-cli" in result:
                    logger.info("✓ speedtest-cli installed successfully via apt-get")
                    return True
            except Exception as e:
                logger.warning(f"apt-get installation failed: {e}")

            logger.error("Failed to install speedtest-cli with any method")
            return False

        except Exception as e:
            logger.error(f"Error checking/installing speedtest-cli: {e}")
            return False

    def _convert_bytes_to_human_readable(self, bytes_value: float) -> str:
        """Convert bytes to human readable format.

        Args:
            bytes_value: Value in bytes

        Returns:
            str: Human readable string (e.g., "127.89 Mbps")
        """
        # Convert bytes per second to bits per second
        bits_per_second = bytes_value * 8

        if bits_per_second >= 1_000_000_000:
            return f"{bits_per_second / 1_000_000_000:.2f} Gbps"
        elif bits_per_second >= 1_000_000:
            return f"{bits_per_second / 1_000_000:.2f} Mbps"
        elif bits_per_second >= 1_000:
            return f"{bits_per_second / 1_000:.2f} Kbps"
        else:
            return f"{bits_per_second:.2f} bps"

    @pytest.mark.integration
    @pytest.mark.slow
    def test_speedtest_cli_performance(self, device_manager: DeviceManager):
        """Test internet performance using speedtest-cli.

        This test measures real-world internet performance by running
        speedtest-cli against Ookla's speedtest servers. It reports:
        - Download speed (bytes/sec)
        - Upload speed (bytes/sec)
        - Ping latency (ms)
        - Server information (country, sponsor, host, name)
        - Client IP address

        The test uses --json flag to get structured output for easy parsing.
        """
        board = self._get_board(device_manager)

        logger.info("\n=== Speedtest-CLI Performance Test ===")

        # Ensure speedtest-cli is installed
        if not self._ensure_speedtest_installed(board):
            pytest.skip("speedtest-cli not available and could not be installed")
            return

        logger.info("Running speedtest-cli (this may take 30-60 seconds)...")

        try:
            # Run speedtest with JSON output
            # Using a longer timeout as speedtest can take time
            result = board.command("speedtest-cli --json", timeout=120)

            # Parse JSON output
            try:
                speedtest_data = json.loads(result)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse speedtest JSON output: {e}")
                logger.error(f"Raw output: {result}")
                pytest.fail("Failed to parse speedtest-cli JSON output")
                return

            # Extract key metrics
            download_bps = speedtest_data.get("download", 0)
            upload_bps = speedtest_data.get("upload", 0)
            ping_ms = speedtest_data.get("ping", 0)

            # Server information
            server_info = speedtest_data.get("server", {})
            server_country = server_info.get("country", "Unknown")
            server_sponsor = server_info.get("sponsor", "Unknown")
            server_host = server_info.get("host", "Unknown")
            server_name = server_info.get("name", "Unknown")

            # Client information
            client_info = speedtest_data.get("client", {})
            client_ip = client_info.get("ip", "Unknown")
            client_country = client_info.get("country", "Unknown")
            client_isp = client_info.get("isp", "Unknown")

            # Convert to human readable
            download_readable = self._convert_bytes_to_human_readable(download_bps)
            upload_readable = self._convert_bytes_to_human_readable(upload_bps)

            # Log results
            logger.info("\n=== Speedtest Results ===")
            logger.info(f"Download: {download_bps:.0f} bytes/sec ({download_readable})")
            logger.info(f"Upload: {upload_bps:.0f} bytes/sec ({upload_readable})")
            logger.info(f"Ping: {ping_ms:.2f} ms")
            logger.info("\n--- Server Information ---")
            logger.info(f"Country: {server_country}")
            logger.info(f"Sponsor: {server_sponsor}")
            logger.info(f"Host: {server_host}")
            logger.info(f"Name: {server_name}")
            logger.info("\n--- Client Information ---")
            logger.info(f"IP: {client_ip}")
            logger.info(f"Country: {client_country}")
            logger.info(f"ISP: {client_isp}")
            logger.info("=========================\n")

            # Assertions to ensure we got valid data
            assert download_bps > 0, "Download speed should be greater than 0"
            assert upload_bps > 0, "Upload speed should be greater than 0"
            assert ping_ms > 0, "Ping should be greater than 0"
            assert server_country != "Unknown", "Server country should be detected"
            assert client_ip != "Unknown", "Client IP should be detected"

            logger.info("✅ Speedtest completed successfully!")

        except Exception as e:
            logger.error(f"Speedtest failed: {e}")
            pytest.fail(f"Speedtest execution failed: {e}")
