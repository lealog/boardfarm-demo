"""Pytest configuration for boardfarm integration."""

import sys
import os
import re
from pathlib import Path
from datetime import datetime
from boardfarm3 import hookimpl

# Load environment variables from .env file if it exists
def load_env_file():
    """Load environment variables from .env file."""
    # Check multiple locations for .env file
    env_locations = [
        Path.home() / '.boardfarm.env',  # ~/.boardfarm.env
        Path.home() / '.env',             # ~/.env
        Path(__file__).parent / '.env'    # project/.env
    ]

    for env_file in env_locations:
        if env_file.exists():
            with open(env_file) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        key, _, value = line.partition('=')
                        if key and value:
                            os.environ[key.strip()] = value.strip().strip('"').strip("'")
            break

# Load .env file before anything else
load_env_file()

# Add current directory to Python path so our modules can be imported
sys.path.insert(0, os.path.dirname(__file__))

# Import our custom devices
from rpi_cpe_device import RpiCpeDevice
from rdk_cpe_device import RdkCpeDevice

# Import LXD connection
from lxd_connection import LXDConnection

# Import SSH connection
from ssh_connection import SSHConnection


@hookimpl
def boardfarm_add_devices():
    """Register custom devices with boardfarm."""
    return {
        "rpi_cpe": RpiCpeDevice,
        "rdk_cpe": RdkCpeDevice
    }


def register_custom_connections():
    """Register custom connection types (LXD and SSH) with boardfarm."""
    import sys
    from boardfarm3.lib import connection_factory
    from boardfarm3.exceptions import EnvConfigError

    # Store the original connection_factory function
    original_factory = connection_factory.connection_factory

    # Create a wrapper that adds LXD and SSH support
    def patched_connection_factory(connection_type, connection_name, **kwargs):
        if connection_type == "lxd":
            return LXDConnection(
                name=connection_name,
                container_name=kwargs.get("container_name", kwargs.get("hostname", "rdk-container")),
                lxd_endpoint=kwargs.get("lxd_endpoint", "https://127.0.0.1:8443"),
                shell_prompt=[kwargs.get("shell_prompt", "root@")],
                save_console_logs=kwargs.get("save_console_logs", False),
                cert_file=kwargs.get("cert_file"),
                key_file=kwargs.get("key_file"),
                trust_password=kwargs.get("trust_password"),
            )
        elif connection_type == "ssh":
            return SSHConnection(
                name=connection_name,
                ip_addr=kwargs.get("ip_addr", kwargs.get("hostname")),
                username=kwargs.get("username", "root"),
                password=kwargs.get("password"),
                port=int(kwargs.get("port", 22)),
                shell_prompt=[kwargs.get("shell_prompt", "root@")],
                save_console_logs=kwargs.get("save_console_logs", False),
                ssh_key=kwargs.get("ssh_key"),
            )
        else:
            # Fallback to original factory for other connection types
            return original_factory(connection_type, connection_name, **kwargs)
    
    # Replace the connection_factory function in the module
    connection_factory.connection_factory = patched_connection_factory
    
    # Also patch any modules that have already imported the function directly
    # This handles cases where modules do "from connection_factory import connection_factory"
    for module_name, module in sys.modules.items():
        if hasattr(module, 'connection_factory'):
            # Check if it's the function we want to replace (not the module)
            if callable(getattr(module, 'connection_factory')) and \
               getattr(module, 'connection_factory').__module__ == 'boardfarm3.lib.connection_factory':
                setattr(module, 'connection_factory', patched_connection_factory)


def substitute_env_vars(data):
    """Recursively substitute environment variables in data structures."""
    if isinstance(data, dict):
        return {key: substitute_env_vars(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [substitute_env_vars(item) for item in data]
    elif isinstance(data, str):
        # Replace ${VAR_NAME} with environment variable value
        pattern = r'\$\{([^}]+)\}'
        def replacer(match):
            var_name = match.group(1)
            return os.environ.get(var_name, match.group(0))  # Keep original if not found
        return re.sub(pattern, replacer, data)
    else:
        return data


@hookimpl
def boardfarm_parse_config(cmdline_args, inventory_config, env_config):
    """Hook to parse config and substitute environment variables in inventory."""
    from boardfarm3.lib.boardfarm_config import parse_boardfarm_config

    # Substitute environment variables in both inventory and env config
    processed_inventory = substitute_env_vars(inventory_config)
    processed_env_config = substitute_env_vars(env_config)

    # Use the standard parser with processed data
    return parse_boardfarm_config(processed_inventory, processed_env_config)


def pytest_addoption(parser):
    """Add pytest command line options for boardfarm."""
    # The boardfarm plugin will register its own options
    # We just ensure the hook is called
    pass


def pytest_load_initial_conftests(early_config, args):
    """Load boardfarm plugin early to ensure it's available."""
    from pytest_boardfarm3 import boardfarm_fixtures

    # Register boardfarm fixtures so they're available
    if not early_config.pluginmanager.has_plugin("boardfarm_fixtures"):
        early_config.pluginmanager.register(boardfarm_fixtures, "boardfarm_fixtures")


def pytest_configure(config):
    """Configure pytest and register custom devices."""
    from boardfarm3.main import get_plugin_manager

    # Set timestamped HTML report path if --html option was used
    if config.option.htmlpath and config.option.htmlpath == 'report.html':
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        config.option.htmlpath = f"reports/report_{timestamp}.html"

    pm = get_plugin_manager()

    # Register custom connection types (LXD and SSH)
    register_custom_connections()

    # Register this module as a plugin so the hook is discovered
    pm.register(sys.modules[__name__], name="custom_rpi_devices")
