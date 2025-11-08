# Test Changelog - Boardfarm Demo

This file tracks changes to test files, test coverage, and test implementations.

For framework and infrastructure changes, see [FRAMEWORK_CHANGELOG.md](FRAMEWORK_CHANGELOG.md).

---

## [Unreleased]

### 2025-11-08 - BDD Test Implementation

#### Added

**New Test Files**
- `tests/test_ssh_cpe_bdd.py` - BDD implementation of SSH CPE tests
  - 40+ step definitions (Given/When/Then)
  - Covers all scenarios from `tests_ssh_cpe.py`
  - 100% compatible with existing pytest infrastructure
  - Lines of code: ~400

**New Feature Files**
- `tests/features/ssh_cpe_connectivity.feature` - CPE connectivity scenarios
  - 6 complete scenarios
  - Background section for common setup
  - Covers: connection, system info, network info, file operations, memory, disk

- `tests/features/rdk_cpe_advanced.feature` - RDK CPE advanced features
  - 3 scenarios (1 basic, 2 marked as @slow)
  - Covers: RDK connection, hardware info, DMCLI integration

#### Test Coverage

**BDD Scenarios (9 total)**

1. **SSH CPE Connectivity** (6 scenarios)
   - Establish SSH connection to CPE device
   - Retrieve system information from CPE
   - Retrieve network information from CPE
   - Perform file operations on CPE
   - Retrieve memory information from CPE
   - Retrieve disk usage from CPE

2. **RDK CPE Advanced** (3 scenarios)
   - Connect to RDK CPE via SSH
   - Retrieve hardware information from RDK CPE (@slow)
   - Access DMCLI interface on RDK CPE (@slow)

#### Test Execution
```bash
# Run all BDD tests
pytest tests/test_ssh_cpe_bdd.py -v

# Run with markers
pytest tests/test_ssh_cpe_bdd.py -m slow -v
pytest tests/test_ssh_cpe_bdd.py -m "not slow" -v

# Run specific scenario
pytest tests/test_ssh_cpe_bdd.py::test_establish_ssh_connection_to_cpe_device -v
```

---

## Recent Releases

### Recent - Performance Testing Enhancements

#### Modified
- `tests/tests_performance.py` - Speedtest-cli improvements
  - Added HTTP 403 error handling
  - Changed speed units from bytes/sec to bits/sec
  - Added installation verification checks
  - Enhanced logging for debugging
  - Improved error messages

#### Test Updates
- Speed unit conversion for accurate reporting
- Better error handling for speedtest-cli failures
- More descriptive test output

---

### Recent - iPerf Testing Implementation

#### Modified
- `tests/tests_rdk_cpe_use_cases.py` - iPerf integration
  - Added iPerf3 throughput testing (IPv4 and IPv6)
  - Implemented retry mechanism (up to 3 attempts)
  - Added local and remote iPerf3 availability checks
  - Enhanced connectivity validation through CPE
  - Improved regex patterns for bandwidth parsing
  - Added UDP packet loss extraction
  - Enhanced logging with full iPerf3 output preview
  - Individual test result reporting for IPv4/IPv6

#### New Tests
- `test_iperf_throughput_ipv4` - IPv4 throughput testing
- `test_iperf_throughput_ipv6` - IPv6 throughput testing
- Retry logic for improved reliability

#### Configuration Required
```json
"iperf_server_ipv4": "ping.online.net",
"iperf_server_ipv6": "ping6.online.net",
"iperf_ports_ipv4": [5200, 5201, 5202, 5203, 5204],
"iperf_ports_ipv6": [5205, 5206, 5207, 5208, 5209],
"iperf_test_duration_ipv4": 10,
"iperf_test_duration_ipv6": 10
```

---

### Recent - DMCLI Integration Tests

#### Added
- `tests/test_rdk_cpe_dmcli_integration.py` - Complete DMCLI test suite
  - 15+ integration tests
  - Device information tests (serial, model, software version)
  - Uptime and status queries
  - Network interface queries
  - WiFi status checks
  - Parameter get/set operations
  - Error handling and retry logic
  - Lines of code: ~235

#### Test Coverage
- Device information retrieval via DMCLI
- Software version and uptime queries
- Network interface parameter access
- WiFi radio status and SSID configuration
- Generic parameter get/set operations
- Error handling for missing parameters

#### Test Classes
- `TestRdkCpeDmcliIntegration` - Integration test suite

---

### Recent - System Monitoring Tests

#### Modified
- Multiple test files - System monitoring additions
  - 1-minute load average retrieval tests
  - CPU usage monitoring tests
  - Memory usage tracking tests
  - Error handling for load average parsing

#### New Tests
- Load average monitoring
- System health checks combining CPU, memory, and uptime

---

### Recent - Logging Improvements

#### Modified
- `tests/tests_ssh_cpe.py` - Logger integration
  - Replaced all `print()` with `logger.info()`
  - Added structured logging for test steps
  - Improved debug output

- `tests/tests_rdk_cpe.py` - Logger integration
  - Consistent logging patterns
  - Better test output formatting

- `tests/tests_rdk_cpe_use_cases.py` - Logger integration
  - Comprehensive logging for use cases
  - Better traceability

- `tests/tests_performance.py` - Logger integration
  - Performance test logging
  - Result formatting

---

### Recent - Test Organization Improvements

#### Modified
- `tests/tests_ssh_cpe.py` - Refactored device retrieval
  - Consolidated device retrieval logic into `get_cpe_device()` helper
  - Improved code readability and maintainability
  - Reduced code duplication

#### Benefits
- Single source of truth for device retrieval
- Easier to maintain and update
- Consistent error handling

---

### Initial - Core Test Suite

#### Test Files Created

**Basic Tests**
- `tests/tests_basic.py` - pytest fundamentals
  - Sample data fixture
  - Parametrized tests
  - Marked tests (slow, integration)
  - Lines: 70

**RPI CPE Tests**
- `tests/tests_rpi_cpe.py` - Simple RPI device tests
  - Basic connection test
  - Command execution test
  - Lines: 73

**RDK CPE Tests**
- `tests/tests_rdk_cpe.py` - Advanced RDK device tests
  - Hardware information tests
  - Software information tests
  - Network interface tests
  - System command tests
  - Provisioning mode checks
  - JSON values retrieval
  - MTU size and online status
  - Lines: 215

**SSH CPE Tests**
- `tests/tests_ssh_cpe.py` - SSH connectivity tests
  - SSH connection tests (RPI and RDK)
  - System information retrieval
  - Network information gathering
  - File operations
  - Process listing
  - Memory and disk usage
  - Hardware info via SSH
  - DMCLI integration via SSH
  - Lines: 204

**Performance Tests**
- `tests/tests_performance.py` - Performance validation
  - Speedtest-cli integration
  - Download/upload speed tests
  - JSON result parsing
  - Human-readable output formatting
  - Lines: 172

**Use Case Tests**
- `tests/tests_rdk_cpe_use_cases.py` - Real-world scenarios
  - CPU usage monitoring
  - Memory usage monitoring
  - System uptime tracking
  - Provisioning mode checks
  - NTP synchronization
  - Ping connectivity tests
  - iPerf throughput tests (IPv4/IPv6)
  - Combined system health checks
  - Error scenario handling
  - Lines: 1,045

**DMCLI Library Tests**
- `tests/test_dmcli.py` - DMCLI library unit tests
  - GPV (Get Parameter Value) tests
  - SPV (Set Parameter Value) tests
  - AddObject tests
  - DelObject tests
  - Error handling tests
  - Mock-based testing
  - 17 unit tests

- `tests/test_dmcli_integration_basic.py` - Structure validation
  - Method signature verification
  - Integration structure checks

#### Total Test Count (Initial)
- **56 test functions** across all test files
- **6 test files** (excluding BDD)
- **23 integration tests** requiring device access
- **6 slow tests** marked for optional execution

---

## Test Organization

### Test Categories

#### Unit Tests
- `tests/tests_basic.py` - Framework verification
- `tests/test_dmcli.py` - Library unit tests

#### Integration Tests (@integration marker)
- Most tests in `tests_ssh_cpe.py`
- All tests in `tests_rdk_cpe.py`
- DMCLI integration tests
- Performance tests

#### Slow Tests (@slow marker)
- Hardware information retrieval
- DMCLI operations
- Performance measurements

#### Network Tests (@ipv4, @ipv6 markers)
- iPerf throughput tests
- IPv4/IPv6 specific validations

### Test Classes

#### TestRdkCpeDmcliIntegration
- DMCLI integration test suite
- 15+ test methods
- Device information, network, WiFi tests

#### TestPerformance
- Performance testing suite
- Speedtest-cli based tests
- Download/upload measurements

#### TestRdkCpeUseCases
- Use case demonstration suite
- System health monitoring
- Network performance
- Real-world scenarios

---

## Test Execution Patterns

### Fixture Usage
- **device_manager**: Primary fixture from pytest-boardfarm3
  - Used in 50+ tests
  - Provides access to configured devices
  - Automatic cleanup

- **sample_data**: Custom fixture in tests_basic.py
  - Demonstrates custom fixture creation

- **cpe_context**: BDD context fixture
  - Shares data between BDD steps

### Helper Methods

#### get_cpe_device(device_manager)
- Location: `tests_ssh_cpe.py`, `test_ssh_cpe_bdd.py`
- Purpose: Retrieve any CPE device (RDK or RPI)
- Returns first available device or skips test

#### get_rdk_cpe_device(device_manager)
- Location: `test_ssh_cpe_bdd.py`
- Purpose: Retrieve specifically RDK CPE device
- Returns RDK device or skips test

#### _get_board(device_manager)
- Location: Test classes
- Purpose: Class-specific device retrieval
- Consistent pattern across test classes

---

## Test Markers

### Defined Markers (pytest.ini)
```ini
[pytest]
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    ipv4: IPv4-specific tests
    ipv6: IPv6-specific tests
```

### Usage Examples
```bash
# Run only integration tests
pytest -m integration -v

# Skip slow tests
pytest -m "not slow" -v

# Run IPv4 tests only
pytest -m ipv4 -v

# Combine markers
pytest -m "integration and not slow" -v
```

---

## Test Coverage Summary

### Device Types Tested
- ✅ RPI CPE (ser2net, LXD, SSH)
- ✅ RDK CPE (ser2net, LXD, SSH)

### Connection Types Tested
- ✅ ser2net (physical devices)
- ✅ LXD (containers)
- ✅ SSH (direct connection)

### Feature Coverage
- ✅ Basic connectivity
- ✅ Command execution
- ✅ System information retrieval
- ✅ Hardware information (serial, MAC)
- ✅ Software information (version, uptime)
- ✅ Network configuration
- ✅ File operations
- ✅ DMCLI integration (TR-181)
- ✅ Performance testing (speedtest, iPerf)
- ✅ Use case demonstrations
- ✅ Error handling
- ✅ BDD scenarios

---

## Test Maintenance

### Adding New Tests

#### Traditional pytest
1. Create test file: `tests/test_<feature>.py`
2. Import required fixtures and devices
3. Write test functions with `test_` prefix
4. Add appropriate markers (@pytest.mark.slow, etc.)
5. Update this TEST_CHANGELOG.md
6. Add examples to README if user-facing

#### BDD Tests
1. Create feature file: `tests/features/<feature>.feature`
2. Write scenarios in Gherkin syntax
3. Add/reuse step definitions in appropriate test file
4. Load scenarios: `scenarios('features/<feature>.feature')`
5. Update this TEST_CHANGELOG.md
6. Add to BDD_TESTING_GUIDE.md if new patterns

### Modifying Existing Tests
1. Document change in this TEST_CHANGELOG.md
2. Update related feature files if BDD
3. Ensure backward compatibility if possible
4. Update examples in documentation if behavior changes
5. Consider impact on CI/CD

### Deleting Tests
1. Document deletion in this TEST_CHANGELOG.md
2. Explain reason for deletion
3. Provide migration path if replacement exists
4. Remove from documentation

---

## Test Execution Commands

### All Tests
```bash
# Traditional pytest tests
pytest --board-name=rdk_cpe_1 --env-config=env_config.json --inventory-config=inventory.json tests/ -v

# BDD tests only
pytest tests/test_ssh_cpe_bdd.py -v

# All tests including BDD
pytest --board-name=rdk_cpe_1 --env-config=env_config.json --inventory-config=inventory.json tests/ -v
```

### Specific Test Files
```bash
# Basic tests
pytest tests/tests_basic.py -v

# RPI CPE tests
pytest --board-name=rpi_cpe_1 ... tests/tests_rpi_cpe.py -v

# RDK CPE tests
pytest --board-name=rdk_cpe_1 ... tests/tests_rdk_cpe.py -v

# SSH tests
pytest --board-name=my_ssh_cpe ... tests/tests_ssh_cpe.py -v

# Performance tests
pytest --board-name=rdk_cpe_1 ... tests/tests_performance.py -v

# Use case tests
pytest --board-name=rdk_cpe_1 ... tests/tests_rdk_cpe_use_cases.py -v

# DMCLI integration
pytest --board-name=rdk_cpe_1 ... tests/test_rdk_cpe_dmcli_integration.py -v

# BDD tests
pytest tests/test_ssh_cpe_bdd.py -v
```

### With Filters
```bash
# Run tests matching pattern
pytest -k "network" -v

# Run specific test
pytest tests/tests_rdk_cpe.py::test_rdk_cpe_hardware_info -v

# Run with markers
pytest -m "not slow" -v
pytest -m integration -v
pytest -m ipv4 -v
```

---

## Future Test Enhancements

### Planned
- BDD scenarios for performance tests
- BDD scenarios for DMCLI operations
- WiFi configuration test suite
- Firmware upgrade test scenarios
- Security testing (firewall, ports)
- QoS testing
- Stability/stress tests

### Under Consideration
- Scenario outlines for parametrized BDD tests
- Shared step library across multiple features
- Test data generators
- Visual test reporting
- Test execution time optimization

---

## References

- [FRAMEWORK_CHANGELOG.md](FRAMEWORK_CHANGELOG.md) - Framework changes
- [BDD_TESTING_GUIDE.md](BDD_TESTING_GUIDE.md) - BDD testing guide
- [BDD_COMPARISON.md](BDD_COMPARISON.md) - Test approach comparison
- [README.md](README.md) - Main documentation
