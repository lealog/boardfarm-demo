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

    def _ensure_speedtest_installed_locally(self) -> bool:
        """Ensure speedtest-cli is installed locally on the PC running boardfarm.

        Returns:
            bool: True if speedtest-cli is available, False otherwise
        """
        import shutil

        logger.info("Checking if speedtest-cli is installed locally...")

        # Check if speedtest-cli is already installed
        if shutil.which("speedtest-cli"):
            logger.info("✓ speedtest-cli is already installed locally")
            return True

        logger.error("speedtest-cli not found on local system")
        logger.info("Please install speedtest-cli using one of these methods:")
        logger.info("  - pip: pip install speedtest-cli")
        logger.info("  - pip3: pip3 install speedtest-cli")
        logger.info("  - apt: apt-get install speedtest-cli")
        return False

    def _convert_bps_to_human_readable(self, bits_per_second: float) -> str:
        """Convert bits per second to human readable format.

        Args:
            bits_per_second: Value in bits per second

        Returns:
            str: Human readable string (e.g., "127.89 Mbps")
        """
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
        """Test internet performance using speedtest-cli from LAN PC.

        This test measures real-world internet performance by running
        speedtest-cli locally on the PC (in LAN) against Ookla's speedtest servers.
        Traffic flows through the CPE to measure actual user experience.

        Traffic flow: LAN PC (running speedtest) → CPE → Internet (Speedtest servers)

        Reports:
        - Download speed (bytes/sec)
        - Upload speed (bytes/sec)
        - Ping latency (ms)
        - Server information (country, sponsor, host, name)
        - Client IP address

        The test uses --json flag to get structured output for easy parsing.
        """
        board = self._get_board(device_manager)

        logger.info("\n=== Speedtest-CLI Performance Test (LAN PC → CPE → Internet) ===")

        # Ensure speedtest-cli is installed locally
        if not self._ensure_speedtest_installed_locally():
            pytest.skip("speedtest-cli not available on local system. Install with: pip install speedtest-cli")
            return

        logger.info("Running speedtest-cli locally (this may take 30-60 seconds)...")

        try:
            import subprocess

            # Run speedtest with JSON output locally
            # Using a longer timeout as speedtest can take time
            result = subprocess.run(
                ["speedtest-cli", "--json"],
                capture_output=True,
                text=True,
                timeout=120
            )

            output = result.stdout

            # Parse JSON output
            try:
                speedtest_data = json.loads(output)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse speedtest JSON output: {e}")
                logger.error(f"Raw output: {output}")
                logger.error(f"Error output: {result.stderr}")
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
            download_readable = self._convert_bps_to_human_readable(download_bps)
            upload_readable = self._convert_bps_to_human_readable(upload_bps)

            # Log results
            logger.info("\n=== Speedtest Results (via CPE) ===")
            logger.info(f"Download: {download_bps:.0f} bits/sec ({download_readable})")
            logger.info(f"Upload: {upload_bps:.0f} bits/sec ({upload_readable})")
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

        except subprocess.TimeoutExpired:
            logger.error("Speedtest timed out after 120 seconds")
            pytest.fail("Speedtest execution timed out")
        except Exception as e:
            logger.error(f"Speedtest failed: {e}")
            pytest.fail(f"Speedtest execution failed: {e}")
