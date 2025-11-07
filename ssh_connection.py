"""SSH connection module for boardfarm devices."""

from __future__ import annotations

import logging
import time
from typing import Any

import pexpect
from pexpect import pxssh

from boardfarm3.exceptions import DeviceConnectionError
from boardfarm3.lib.boardfarm_pexpect import BoardfarmPexpect

logger = logging.getLogger(__name__)

_CONNECTION_ERROR_THRESHOLD = 2
_CONNECTION_FAILED_STR: str = "Connection failed to SSH device"
_SHELL_PROMPT_UNAVAILABLE_STR = "Shell prompt is not available"


class SSHConnection(BoardfarmPexpect):
    """Connect to a device via SSH."""

    def __init__(
        self,
        name: str,
        ip_addr: str,
        username: str = "root",
        password: str | None = None,
        port: int = 22,
        shell_prompt: list[str] | None = None,
        save_console_logs: str = "",
        timeout: int = 30,
        ssh_key: str | None = None,
        **kwargs: dict[str, Any],
    ) -> None:
        """Initialize SSH connection.

        :param name: connection name
        :type name: str
        :param ip_addr: IP address of the device
        :type ip_addr: str
        :param username: SSH username, defaults to "root"
        :type username: str
        :param password: SSH password, defaults to None
        :type password: str | None
        :param port: SSH port, defaults to 22
        :type port: int
        :param shell_prompt: shell prompt pattern, defaults to None
        :type shell_prompt: list[str] | None
        :param save_console_logs: save console logs to disk, defaults to ""
        :type save_console_logs: str
        :param timeout: connection timeout, defaults to 30
        :type timeout: int
        :param ssh_key: path to SSH private key file, defaults to None
        :type ssh_key: str | None
        :param kwargs: additional keyword args
        """
        self._ip_addr = ip_addr
        self._username = username
        self._password = password
        self._port = port
        self._shell_prompt = shell_prompt
        self._timeout = timeout
        self._ssh_key = ssh_key
        self._ssh_session = None

        # Create a pseudo-command for the parent pexpect class
        command = f"ssh {username}@{ip_addr}"
        super().__init__(name, command, save_console_logs, [])

    def login_to_server(self, password: str | None = None) -> None:
        """Login to SSH device.

        :param password: SSH password (can override init password)
        :raises DeviceConnectionError: if SSH connection fails
        :raises ValueError: if shell prompt is unavailable
        """
        if not self._shell_prompt:
            raise ValueError(_SHELL_PROMPT_UNAVAILABLE_STR)

        # Use provided password or fall back to init password
        login_password = password or self._password

        try:
            # Create SSH session
            self._ssh_session = pxssh.pxssh(
                timeout=self._timeout,
                encoding='utf-8',
                codec_errors='ignore'
            )

            # Set prompt pattern
            if self._shell_prompt:
                # Flatten shell_prompt if it's a list of lists, then join
                if isinstance(self._shell_prompt, list):
                    # Flatten any nested lists
                    flat_prompts = []
                    for item in self._shell_prompt:
                        if isinstance(item, list):
                            flat_prompts.extend(item)
                        else:
                            flat_prompts.append(item)
                    prompt_pattern = '|'.join(flat_prompts)
                else:
                    prompt_pattern = self._shell_prompt
                self._ssh_session.PROMPT = prompt_pattern

            # Connect to device
            logger.info(f"Connecting to {self._username}@{self._ip_addr}:{self._port}")

            login_kwargs = {
                'server': self._ip_addr,
                'username': self._username,
                'port': self._port,
                'auto_prompt_reset': False,
                'sync_multiplier': 1,
            }

            # Use SSH key if provided, otherwise use password
            if self._ssh_key:
                login_kwargs['ssh_key'] = self._ssh_key
            elif login_password:
                login_kwargs['password'] = login_password
            else:
                raise DeviceConnectionError("No authentication method provided (password or SSH key)")

            self._ssh_session.login(**login_kwargs)

            logger.info(f"Successfully connected to {self._ip_addr}")

        except pxssh.ExceptionPxssh as e:
            raise DeviceConnectionError(f"{_CONNECTION_FAILED_STR}: {e}") from e
        except Exception as e:
            raise DeviceConnectionError(f"SSH connection failed: {e}") from e

    def sendline(self, command: str = "") -> None:
        """Send a command line to the device (pexpect compatibility).

        :param command: command to send
        """
        if self._ssh_session:
            self._ssh_session.sendline(command)
        else:
            raise DeviceConnectionError("SSH session not established")

    def expect(self, patterns, timeout: int = 30):
        """Wait for expected pattern (pexpect compatibility).

        :param patterns: pattern(s) to match
        :param timeout: timeout in seconds
        :return: index of matched pattern
        """
        if self._ssh_session:
            try:
                return self._ssh_session.expect(patterns, timeout=timeout)
            except pexpect.TIMEOUT as e:
                raise DeviceConnectionError(f"Timeout waiting for pattern: {patterns}") from e
            except pexpect.EOF as e:
                raise DeviceConnectionError("SSH connection closed unexpectedly") from e
        else:
            raise DeviceConnectionError("SSH session not established")

    def expect_exact(self, pattern: str, timeout: int = 30):
        """Expect exact string match (pexpect compatibility).

        :param pattern: exact string to match
        :param timeout: timeout in seconds
        :return: index of matched pattern
        """
        if self._ssh_session:
            try:
                return self._ssh_session.expect_exact(pattern, timeout=timeout)
            except pexpect.TIMEOUT as e:
                raise DeviceConnectionError(f"Timeout waiting for pattern: {pattern}") from e
            except pexpect.EOF as e:
                raise DeviceConnectionError("SSH connection closed unexpectedly") from e
        else:
            raise DeviceConnectionError("SSH session not established")

    @property
    def before(self) -> str:
        """Get text before the match (pexpect compatibility)."""
        if self._ssh_session:
            return self._ssh_session.before or ""
        return getattr(self, '_before', "")

    @before.setter
    def before(self, value: str) -> None:
        """Set text before the match (pexpect compatibility)."""
        self._before = value

    @property
    def after(self) -> str:
        """Get text after the match (pexpect compatibility)."""
        if self._ssh_session:
            return self._ssh_session.after or ""
        return getattr(self, '_after', "")

    @after.setter
    def after(self, value: str) -> None:
        """Set text after the match (pexpect compatibility)."""
        self._after = value

    def execute_command(self, command: str, timeout: int = 30) -> str:
        """Execute a command via SSH.

        :param command: command to execute
        :type command: str
        :param timeout: timeout in seconds, defaults to 30
        :type timeout: int
        :return: command output
        :rtype: str
        :raises DeviceConnectionError: if command execution fails
        """
        if not self._ssh_session:
            raise DeviceConnectionError("SSH session not established")

        try:
            self.sendline(command)
            self.expect(self._shell_prompt, timeout=timeout)
            return self.before.strip()
        except Exception as e:
            raise DeviceConnectionError(f"Command execution failed: {e}") from e

    def logout(self) -> None:
        """Logout from SSH session."""
        if self._ssh_session:
            try:
                self._ssh_session.logout()
            except Exception as e:
                logger.warning(f"Error during logout: {e}")

    def close(self) -> None:
        """Close the SSH connection."""
        self.logout()
        if self._ssh_session:
            try:
                self._ssh_session.close()
            except Exception as e:
                logger.warning(f"Error closing SSH session: {e}")
        # Don't call super().close() as it tries to access ptyproc which doesn't exist in pxssh

    def __del__(self) -> None:
        """Cleanup on deletion."""
        try:
            self.close()
        except:
            pass

    def isalive(self) -> bool:
        """Check if SSH connection is alive.

        :return: True if connection is alive, False otherwise
        """
        if self._ssh_session:
            try:
                # pxssh doesn't have ptyproc, use its own isalive which checks the process
                return self._ssh_session.isalive()
            except (AttributeError, Exception):
                return False
        return False
