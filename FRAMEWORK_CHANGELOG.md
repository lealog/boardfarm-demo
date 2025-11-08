# Framework Changelog - Boardfarm Demo

This file tracks changes to the testing framework, infrastructure, libraries, and tooling.

For test-specific changes (test files added/modified/deleted), see [TEST_CHANGELOG.md](TEST_CHANGELOG.md).

---

## [Unreleased]

### 2025-11-08 - BDD Testing Framework

#### Added
- **pytest-bdd Integration**: Complete BDD testing capability
  - pytest-bdd >= 6.0.0 dependency
  - Gherkin syntax support for human-readable scenarios
  - Seamless integration with existing pytest infrastructure
  - Compatible with boardfarm3 device_manager fixture

#### New Files
- `requirements.txt` - Python package dependencies
- `tests/features/` - Directory for Gherkin feature files
- `BDD_TESTING_GUIDE.md` - Comprehensive BDD testing guide (11KB)
- `BDD_COMPARISON.md` - Traditional pytest vs BDD comparison (13KB)
- `FRAMEWORK_CHANGELOG.md` - This file
- `TEST_CHANGELOG.md` - Test-specific changes tracking

#### Framework Features
- **Step Definitions**: Reusable Given/When/Then step decorators
- **Context Sharing**: Custom `cpe_context` fixture for data sharing between steps
- **Marker Support**: BDD scenarios support pytest markers (@slow, @integration, etc.)
- **Parametrized Steps**: Support for dynamic step parameters using `parsers.parse()`
- **Cross-Platform**: Works on Mac, Linux, and CI/CD environments

#### Benefits
- Business-readable test scenarios
- Clear separation of test intent (feature files) and implementation (step definitions)
- Reusable step definitions across multiple scenarios
- Living documentation through feature files
- No disruption to existing test infrastructure
- Gradual adoption possible (hybrid approach)

---

## Previous Releases

### Recent - Logging Infrastructure Improvements

#### Changed
- **Standardized Logging**: Replaced all `print()` statements with Python `logging` module
  - Consistent log levels (INFO, WARNING, ERROR)
  - Better traceability and debugging
  - Standardized logger instantiation pattern: `logger = logging.getLogger(__name__)`

#### Files Modified
- `tests/tests_ssh_cpe.py` - Logging integration
- `tests/tests_rdk_cpe.py` - Logging integration
- `tests/tests_rdk_cpe_use_cases.py` - Logging integration
- `tests/tests_performance.py` - Logging integration
- Multiple device implementation files

#### Benefits
- Configurable log levels
- Better integration with pytest's log capture
- Easier debugging and troubleshooting
- Professional logging output

---

### Recent - SSH Connection Infrastructure

#### Enhanced
- **SSHConnection Class Improvements**
  - Shell prompt handling after login
  - Connection parameter adjustments for reliability
  - Consistency with pxssh settings
  - Better session management

#### Files Modified
- `shared/lib/ssh_connection.py` - SSHConnection class refactoring
- `rdk_cpe_device.py` - RdkRpiHW class updates

#### Benefits
- More reliable SSH connections
- Consistent shell prompt detection
- Better handling of edge cases

---

### Recent - DMCLI Library Integration

#### Added
- **Complete DMCLI Library**: TR-181 data model CLI interface
  - `shared/lib/dmcli.py` - DMCLI library implementation
  - Structured parameter access (Get/Set/Add/Delete)
  - Type-safe parameter handling (string/int/bool)
  - Comprehensive error handling with logging
  - Lazy initialization pattern

#### DMCLI API Features
- **GPV**: Get Parameter Value
- **SPV**: Set Parameter Value
- **AddObject**: Create data model objects
- **DelObject**: Delete data model objects
- **Type Handling**: Automatic string/bool/int conversion
- **Error Resilience**: Graceful handling of missing or read-only parameters

#### Integration
- RdkCpeDevice class includes built-in DMCLI helper methods
- Automatic DMCLI API instance creation
- Console safety during device registration
- Warning logs for failed operations

#### Benefits
- Clean Python interface to TR-181 data model
- No manual parsing of dmcli command output
- Production-ready with error handling
- Reusable across device implementations

---

### Initial - Core Framework Components

#### Device Implementations
- **RpiCpeDevice**: Simple Raspberry Pi device
  - Basic command execution
  - Minimal configuration required
  - Perfect for learning boardfarm fundamentals

- **RdkCpeDevice**: Advanced RDK CPE template
  - Hardware/Software separation pattern (RdkRpiHW, RdkSW classes)
  - TR-181 data model access
  - Network interface management
  - DMCLI integration
  - Use case support

#### Connection Types
- **ser2net Connection**: Physical device serial console access
  - `shared/lib/ser2net_connection.py`
  - Serial-to-network proxy support
  - Telnet-based communication

- **LXD Connection**: Container-based testing
  - `shared/lib/lxd_connection.py`
  - LXD REST API integration
  - Certificate-based authentication
  - httpx library for HTTP requests
  - Reduced HTTP logging verbosity

- **SSH Connection**: Direct SSH connectivity
  - `shared/lib/ssh_connection.py`
  - pxssh-based implementation
  - Shell prompt detection

#### pytest-boardfarm Integration
- **conftest.py**: Custom configuration
  - Device registration hooks
  - Connection factory patching
  - Custom device type registration (RpiCpeDevice, RdkCpeDevice)
  - Automatic plugin registration

- **pytest.ini**: Test markers
  - `slow`: Long-running tests
  - `integration`: Integration tests requiring device access
  - `ipv4`: IPv4-specific tests
  - `ipv6`: IPv6-specific tests

#### Device Manager
- Automatic device discovery from inventory
- Type-based device filtering
- Fixture injection into tests
- Support for multiple devices

#### Configuration Management
- **inventory.json**: Device inventory
  - JSON-based device definitions
  - Multiple connection types support
  - Flexible device parameters
  - Board configurations

- **env_config.json**: Environment configuration
  - Environment-specific settings

#### Hardware Abstraction
- **RdkRpiHW**: Hardware layer for RDK CPE
  - Serial number retrieval from /proc/cpuinfo
  - MAC address retrieval from network interfaces
  - Power cycle/reboot capabilities
  - Console connection management

#### Software Abstraction
- **RdkSW**: Software layer for RDK CPE
  - Device information via dmcli
  - Management server configuration (TR-069/CWMP)
  - Network interface properties
  - Software version retrieval

#### Shared Libraries
- **dmcli.py**: TR-181 data model CLI interface
- **ssh_connection.py**: SSH connection implementation
- **ser2net_connection.py**: Serial console connection
- **lxd_connection.py**: LXD container connection

---

## Framework Architecture

### Layer Structure
```
Tests Layer
    ├── BDD Tests (test_ssh_cpe_bdd.py)
    ├── Traditional pytest Tests (tests_*.py)
    └── Feature Files (features/*.feature)

Framework Layer
    ├── Device Manager (pytest-boardfarm3)
    ├── Custom Devices (RpiCpeDevice, RdkCpeDevice)
    └── Test Fixtures (conftest.py)

Device Layer
    ├── Hardware Abstraction (RdkRpiHW)
    ├── Software Abstraction (RdkSW)
    └── Device Templates (CPETemplate)

Connection Layer
    ├── SSH (ssh_connection.py)
    ├── ser2net (ser2net_connection.py)
    └── LXD (lxd_connection.py)

Library Layer
    ├── DMCLI (dmcli.py)
    └── Use Cases (boardfarm3.use_cases)

Configuration Layer
    ├── inventory.json
    ├── env_config.json
    └── pytest.ini
```

---

## Dependencies

### Core Dependencies
```
pytest >= 7.0.0
boardfarm3 (git+https://github.com/lgirdk/boardfarm.git@boardfarm3)
pytest-boardfarm3 (git+https://github.com/lgirdk/pytest-boardfarm.git@boardfarm3)
```

### BDD Testing
```
pytest-bdd >= 6.0.0
parse >= 1.20.0
parse-type >= 0.6.0
gherkin-official >= 29.0.0
```

### Connection Libraries
```
pexpect (for SSH via pxssh)
httpx (for LXD REST API)
```

---

## Configuration Files

### pytest.ini
- Test markers definition
- pytest configuration options

### conftest.py
- Custom device registration
- Connection factory patching
- Fixture definitions
- Plugin registration

### requirements.txt
- Python package dependencies
- Version specifications

---

## Known Issues

### ps Command Compatibility
- **Issue**: Different container environments have varying `ps` implementations
- **Solution**: RdkCpeDevice overrides `start_traffic_receiver` and `start_traffic_sender` methods
- **Impact**: Ensures compatibility across LXD, Docker, and physical devices

### HTTP Request Logging
- **Issue**: httpx library logs all HTTP requests at INFO level by default
- **Solution**: Set to WARNING level in `lxd_connection.py`
- **Impact**: Reduced log verbosity for LXD operations

---

## Future Enhancements

### Planned
- Docker container connection support
- Additional device type templates
- Enhanced error handling and retry mechanisms
- Performance monitoring hooks
- CI/CD integration examples

### Under Consideration
- Web UI for test execution and reporting
- Real-time device monitoring dashboard
- Automated test generation from device specs
- Plugin system for custom use cases

---

## Best Practices

### Adding New Connection Types
1. Create connection class in `shared/lib/`
2. Implement required interface methods
3. Register in `conftest.py` connection_factory
4. Add configuration example to README
5. Update this changelog

### Adding New Device Types
1. Create device class inheriting from appropriate template
2. Implement hardware/software separation if applicable
3. Register device type in `conftest.py`
4. Add inventory.json configuration example
5. Create sample tests
6. Update documentation

### Framework Modifications
1. Update this FRAMEWORK_CHANGELOG.md
2. Consider backward compatibility
3. Update relevant documentation
4. Add/update tests if applicable
5. Consider impact on existing tests

---

## References

### Documentation
- [README.md](README.md) - Main project documentation
- [BDD_TESTING_GUIDE.md](BDD_TESTING_GUIDE.md) - BDD testing guide
- [BDD_COMPARISON.md](BDD_COMPARISON.md) - Traditional vs BDD comparison
- [TEST_CHANGELOG.md](TEST_CHANGELOG.md) - Test-specific changes

### External Resources
- [Boardfarm3](https://github.com/lgirdk/boardfarm)
- [pytest-boardfarm3](https://github.com/lgirdk/pytest-boardfarm)
- [pytest Documentation](https://docs.pytest.org/)
- [pytest-bdd Documentation](https://pytest-bdd.readthedocs.io/)
