# Release Notes - Boardfarm Demo

**High-level release notes and project changelog.**

This file provides a summary of major releases and changes to the Boardfarm Demo project.

For detailed tracking:
- **Framework & Infrastructure Changes**: See [FRAMEWORK_CHANGELOG.md](FRAMEWORK_CHANGELOG.md)
- **Test Changes**: See [TEST_CHANGELOG.md](TEST_CHANGELOG.md)

---

## [Unreleased] - 2025-11-08

### BDD Testing Framework

**Major Addition**: Complete Behavior-Driven Development (BDD) testing capability using pytest-bdd.

#### What's New
- 🎯 **Gherkin Syntax Support**: Write human-readable test scenarios
- 🔄 **Hybrid Approach**: Mix BDD and traditional pytest tests
- 📚 **Living Documentation**: Feature files serve as up-to-date documentation
- 🧩 **Reusable Steps**: 40+ step definitions for common test operations
- ✅ **Seamless Integration**: Works with existing pytest infrastructure

#### Key Features
- Business-readable test scenarios in plain English
- Clear separation of test intent (feature files) and implementation (step definitions)
- Compatible with boardfarm3 device_manager fixture
- Support for pytest markers (@slow, @integration, etc.)
- Cross-platform compatibility (Mac, Linux, CI/CD)

#### Test Coverage
- 9 BDD scenarios covering SSH CPE connectivity and RDK advanced features
- Complete conversion of `tests_ssh_cpe.py` to BDD format
- All existing tests still functional (hybrid approach)

#### Documentation
- **BDD_TESTING_GUIDE.md**: Comprehensive 11KB guide covering BDD concepts, syntax, and best practices
- **BDD_COMPARISON.md**: 13KB side-by-side comparison of traditional pytest vs BDD with examples
- **FRAMEWORK_CHANGELOG.md**: Framework and infrastructure changes tracking
- **TEST_CHANGELOG.md**: Test-specific changes tracking

#### Dependencies
```bash
pip install pytest-bdd>=6.0.0
```

#### Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Run BDD tests
pytest tests/test_ssh_cpe_bdd.py -v

# Run specific scenario
pytest tests/test_ssh_cpe_bdd.py::test_establish_ssh_connection_to_cpe_device -v
```

**Learn More**: [BDD_TESTING_GUIDE.md](BDD_TESTING_GUIDE.md)

---

## Recent Releases

### Performance Testing Enhancements

#### Speedtest-cli Integration
- HTTP 403 error handling for reliability
- Speed unit conversion to bits/sec for industry standards
- Installation verification checks
- Enhanced error logging

**Modified**: `tests/tests_performance.py`

#### iPerf Throughput Testing
- IPv4 and IPv6 throughput testing
- Automatic retry mechanism (up to 3 attempts)
- Local and remote iPerf3 availability checks
- Comprehensive connectivity validation
- UDP packet loss reporting
- Enhanced bandwidth parsing with improved regex

**Modified**: `tests/tests_rdk_cpe_use_cases.py`
**Configuration**: Added iPerf server settings to inventory.json

---

### DMCLI Library Integration

Complete TR-181 data model CLI interface library with structured parameter access.

#### Features
- **DMCLI Library** (`shared/lib/dmcli.py`): Clean Python interface for TR-181 parameters
- **RdkCpeDevice Integration**: Built-in helper methods for common operations
- **Type Safety**: Automatic parameter type handling (string/int/bool)
- **Error Resilience**: Graceful handling of missing or read-only parameters

#### Device Methods
```python
board.get_device_serial_number()
board.get_device_model_name()
board.get_device_software_version()
board.is_wifi_radio_enabled()
board.get_wifi_ssid() / board.set_wifi_ssid()
```

#### Test Coverage
- 17 unit tests for DMCLI library
- 15+ integration tests with real devices
- Structure validation tests

**Added**:
- `shared/lib/dmcli.py`
- `tests/test_dmcli.py`
- `tests/test_rdk_cpe_dmcli_integration.py`

**Modified**: `rdk_cpe_device.py`

---

### System Monitoring & Logging

#### System Monitoring
- 1-minute load average retrieval from `/proc/loadavg`
- CPU usage monitoring
- Memory usage tracking
- Combined system health checks

#### Logging Improvements
- Replaced all `print()` statements with Python `logging` module
- Standardized log levels (INFO, WARNING, ERROR)
- Better traceability and debugging capabilities
- Professional logging output

**Modified**: All test files and device implementations

---

### Infrastructure Improvements

#### SSH Connection Enhancements
- Improved shell prompt handling after login
- Better connection reliability
- Consistent pxssh settings
- Enhanced session management

**Modified**:
- `shared/lib/ssh_connection.py`
- `rdk_cpe_device.py`

#### Test Organization
- Consolidated device retrieval logic into helper functions
- Improved code readability and maintainability
- Reduced code duplication

**Modified**: `tests/tests_ssh_cpe.py`

---

## Initial Release

### Core Features

#### Device Implementations
- **RpiCpeDevice**: Simple Raspberry Pi device for basic command execution
- **RdkCpeDevice**: Advanced RDK CPE with hardware/software separation
  - TR-181 data model access
  - Network interface management
  - DMCLI integration
  - Use case support

#### Connection Types
- **ser2net**: Physical device serial console access
- **LXD**: Container-based testing via LXD REST API
- **SSH**: Direct SSH connectivity

#### Test Framework
- pytest-boardfarm3 integration
- Device manager fixture support
- Custom device registration hooks
- Automatic device discovery
- Pytest markers (slow, integration, ipv4, ipv6)

#### Test Suite
- **56 test functions** across 6 test files
- Basic connectivity tests
- System and hardware information tests
- Network configuration tests
- DMCLI integration tests
- Performance tests (speedtest, iPerf)
- Use case demonstrations

#### Configuration
- JSON-based inventory management (`inventory.json`)
- Environment configuration (`env_config.json`)
- Flexible device parameters
- Multiple board configurations

#### Documentation
- Comprehensive README (21KB)
- Quick start guide
- Connection setup instructions (ser2net, LXD, SSH)
- Test execution examples
- Use cases documentation
- Known issues and solutions

---

## Installation

### Requirements
```bash
# Core dependencies
pip install pytest
pip install git+https://github.com/lgirdk/boardfarm.git@boardfarm3
pip install git+https://github.com/lgirdk/pytest-boardfarm.git@boardfarm3

# BDD testing
pip install pytest-bdd

# Or install all from requirements file
pip install -r requirements.txt
```

---

## Testing

### Traditional pytest Tests
```bash
# All tests
pytest --board-name=rdk_cpe_1 --env-config=env_config.json --inventory-config=inventory.json tests/ -v

# Specific test file
pytest --board-name=rdk_cpe_1 ... tests/tests_rdk_cpe.py -v

# With filters
pytest -k "network" -v
pytest -m "not slow" -v
```

### BDD Tests
```bash
# All BDD tests
pytest tests/test_ssh_cpe_bdd.py -v

# Specific scenario
pytest tests/test_ssh_cpe_bdd.py::test_establish_ssh_connection_to_cpe_device -v

# With markers
pytest tests/test_ssh_cpe_bdd.py -m slow -v
```

### Hybrid (All Tests)
```bash
# Run everything (traditional + BDD)
pytest --board-name=rdk_cpe_1 --env-config=env_config.json --inventory-config=inventory.json tests/ -v
```

---

## Project Structure

```
boardfarm-demo/
├── tests/
│   ├── features/                    # BDD Gherkin feature files
│   │   ├── ssh_cpe_connectivity.feature
│   │   └── rdk_cpe_advanced.feature
│   ├── test_ssh_cpe_bdd.py         # BDD step definitions
│   ├── tests_basic.py              # Basic pytest tests
│   ├── tests_rpi_cpe.py            # RPI CPE tests
│   ├── tests_rdk_cpe.py            # RDK CPE tests
│   ├── tests_ssh_cpe.py            # SSH connectivity tests
│   ├── tests_performance.py        # Performance tests
│   ├── tests_rdk_cpe_use_cases.py  # Use case tests
│   └── test_rdk_cpe_dmcli_integration.py  # DMCLI tests
├── shared/
│   └── lib/
│       ├── dmcli.py                # DMCLI library
│       ├── ssh_connection.py       # SSH connection
│       ├── ser2net_connection.py   # Serial connection
│       └── lxd_connection.py       # LXD connection
├── rpi_cpe_device.py               # Simple RPI device
├── rdk_cpe_device.py               # Advanced RDK device
├── conftest.py                     # pytest configuration
├── pytest.ini                      # pytest settings
├── inventory.json                  # Device inventory
├── env_config.json                 # Environment config
├── requirements.txt                # Python dependencies
├── README.md                       # Main documentation
├── BDD_TESTING_GUIDE.md            # BDD guide
├── BDD_COMPARISON.md               # BDD vs pytest comparison
├── RELEASE_NOTES.md                # This file
├── FRAMEWORK_CHANGELOG.md          # Framework changes
└── TEST_CHANGELOG.md               # Test changes
```

---

## Documentation

### Main Documentation
- **[README.md](README.md)** - Complete project documentation
  - Quick start guide
  - Device implementations
  - Connection types
  - Test execution
  - Use cases
  - Known issues

### BDD Documentation
- **[BDD_TESTING_GUIDE.md](BDD_TESTING_GUIDE.md)** - Complete BDD guide
  - BDD concepts and benefits
  - Gherkin syntax
  - Running BDD tests
  - Best practices
  - Converting tests to BDD

- **[BDD_COMPARISON.md](BDD_COMPARISON.md)** - Comparison guide
  - Side-by-side examples
  - When to use each approach
  - Pros and cons

### Changelogs
- **[FRAMEWORK_CHANGELOG.md](FRAMEWORK_CHANGELOG.md)** - Infrastructure changes
  - Framework components
  - Libraries and tools
  - Connection types
  - Device implementations
  - Dependencies

- **[TEST_CHANGELOG.md](TEST_CHANGELOG.md)** - Test changes
  - Test files added/modified/deleted
  - Test coverage
  - Test execution commands
  - Test organization

---

## Migration Guides

### Adopting BDD Testing
1. Review [BDD_TESTING_GUIDE.md](BDD_TESTING_GUIDE.md)
2. Install `pytest-bdd`: `pip install pytest-bdd`
3. Start with 1-2 feature files
4. Write step definitions or reuse existing ones
5. Run tests: `pytest tests/test_ssh_cpe_bdd.py -v`
6. Gradually expand BDD coverage
7. Maintain hybrid approach (BDD + traditional pytest)

### Upgrading from Previous Versions
- All existing tests remain functional
- BDD is additive, not replacing existing tests
- No breaking changes to core framework
- Install new dependencies: `pip install -r requirements.txt`

---

## Known Issues

### ps Command Compatibility
- Different container environments may have varying `ps` implementations
- **Solution**: RdkCpeDevice includes overridden methods for compatibility
- See README "Known Issues and Solutions" for details

### HTTP Request Logging
- httpx library logs HTTP requests at INFO level by default
- **Solution**: Set to WARNING in `lxd_connection.py`
- Adjust for debugging as needed

---

## Future Roadmap

### Planned Features
- Additional BDD scenarios for performance and DMCLI tests
- Extended use case library
- CI/CD integration examples
- Docker container testing support
- Additional device type implementations

### Under Consideration
- Scenario outlines for parametrized BDD tests
- BDD reporting plugins (HTML, Allure)
- Feature file templates
- Web UI for test execution
- Real-time device monitoring dashboard

---

## Contributing

### When Adding Features
1. Update appropriate changelog:
   - Framework changes → [FRAMEWORK_CHANGELOG.md](FRAMEWORK_CHANGELOG.md)
   - Test changes → [TEST_CHANGELOG.md](TEST_CHANGELOG.md)
2. Add corresponding tests (traditional and/or BDD)
3. Update [README.md](README.md) for user-facing changes
4. Follow existing code patterns
5. Add logging for debugging
6. Update this [RELEASE_NOTES.md](RELEASE_NOTES.md) for major releases

### Changelog Sections
- **Added**: New features, files, capabilities
- **Changed**: Changes to existing functionality
- **Enhanced**: Improvements to existing features
- **Fixed**: Bug fixes
- **Removed**: Removed features or files
- **Deprecated**: Features marked for future removal
- **Security**: Security-related changes

---

## References

### Internal Documentation
- [README.md](README.md)
- [BDD_TESTING_GUIDE.md](BDD_TESTING_GUIDE.md)
- [BDD_COMPARISON.md](BDD_COMPARISON.md)
- [FRAMEWORK_CHANGELOG.md](FRAMEWORK_CHANGELOG.md)
- [TEST_CHANGELOG.md](TEST_CHANGELOG.md)

### External Resources
- [Boardfarm3 Repository](https://github.com/lgirdk/boardfarm)
- [pytest-boardfarm3 Repository](https://github.com/lgirdk/pytest-boardfarm)
- [pytest Documentation](https://docs.pytest.org/)
- [pytest-bdd Documentation](https://pytest-bdd.readthedocs.io/)
- [Gherkin Syntax Reference](https://cucumber.io/docs/gherkin/reference/)

---

## Version History

### Unreleased
- BDD Testing Framework
- Performance testing enhancements
- DMCLI library integration
- System monitoring and logging improvements

### Initial Release
- Core device implementations (RPI, RDK)
- Multiple connection types (ser2net, LXD, SSH)
- Complete test suite (56 tests)
- Comprehensive documentation

---

*For detailed changes, see [FRAMEWORK_CHANGELOG.md](FRAMEWORK_CHANGELOG.md) and [TEST_CHANGELOG.md](TEST_CHANGELOG.md)*
