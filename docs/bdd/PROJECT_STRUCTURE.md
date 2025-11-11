# BDD Testing Project Structure

## Overview

The BDD testing framework is organized to **separate test cases from test implementation**, making it easy for non-developers to write tests while developers maintain the step definitions.

## Directory Structure

```
boardfarm-demo/
├── tests/bdd/                           # BDD Test Suite Root
│   ├── features/                        # ✍️ QA ENGINEERS WORK HERE
│   │   ├── ssh_cpe_connectivity.feature      # SSH connection tests (6 scenarios)
│   │   ├── rdk_cpe_advanced.feature          # RDK advanced tests (3 scenarios)
│   │   └── dmcli_operations.feature          # DMCLI GET/SET tests (10 scenarios)
│   │
│   ├── conftest.py                      # 👨‍💻 Step definitions (developers maintain)
│   ├── test_ssh_cpe_connectivity.py     # Template: loads SSH feature
│   ├── test_rdk_cpe_advanced.py         # Template: loads RDK feature
│   └── test_dmcli_operations.py         # Template: loads DMCLI feature
│
├── docs/                                # Documentation
│   ├── bdd/                            # BDD-specific documentation
│   │   ├── WRITING_BDD_TESTS.md        # Guide for writing tests (QA)
│   │   ├── RUN_BDD_TESTS.md            # Guide for running tests
│   │   ├── BDD_TESTING_SUMMARY.md      # Complete overview
│   │   └── PROJECT_STRUCTURE.md        # This file
│   │
│   ├── credentials/                    # Authentication documentation
│   │   └── CREDENTIALS_SETUP.md        # Device credential setup
│   │
│   └── setup/                          # Installation guides (future)
│
├── inventory.json                       # Device inventory configuration
├── env_config.json                      # Environment configuration
├── .env                                 # Device credentials (NOT in git)
└── .env.example                         # Credential template
```

## Key Design Principles

### 1. Single Source of Truth
- **ONE master step definitions file**: `tests/bdd/conftest.py`
- All reusable steps are defined here
- No duplication across multiple files
- Easy to maintain and extend

### 2. Separation of Concerns

#### QA Engineers (`tests/bdd/features/`)
- Write test scenarios in plain English (Gherkin)
- No Python knowledge required
- Create unlimited `.feature` files
- Focus on **WHAT to test**

#### Developers (`tests/bdd/conftest.py`)
- Implement step definitions once
- Write Python code
- Maintain test infrastructure
- Focus on **HOW to test**

### 3. Organized by Feature
- Each test file (`test_*.py`) loads one feature file
- Tests appear grouped by feature in VSCode Test Explorer
- QA can click on a feature group to run all its tests
- Easy to see which tests belong to which feature

### 3. Standardization
- All tests use the same step definitions
- Consistent test patterns across the project
- Easy to review and understand

## How It Works

### 1. QA Creates Test Scenario

File: `tests/bdd/features/my_test.feature`
```gherkin
Scenario: Check WiFi status
  When I get the parameter "Device.WiFi.Radio.1.Enable" using DMCLI
  Then the DMCLI command should succeed
  And the parameter value should be "true"
```

### 2. pytest-bdd Magic
- Reads the `.feature` file
- Matches steps to definitions in `test_bdd_steps.py`
- Executes the Python code
- Reports results

### 3. Template Files
- Simple Python template files (`test_*.py`) load feature files
- QA focuses on `.feature` files
- All step definitions are automatically available
- For new features, developer creates simple 2-line template file

## Adding New Test Capabilities

### Scenario: QA needs a new test capability

**Example**: "I need to verify a parameter is within a range"

### Step 1: QA Requests
QA describes what they need:
> "I want to verify that `Device.WiFi.Radio.1.Channel` is between 1 and 11"

### Step 2: Developer Adds to Master File
Developer adds to `tests/bdd/conftest.py`:

```python
@then(parsers.parse('the parameter value should be between {min_val} and {max_val}'))
def verify_value_in_range(test_context, min_val, max_val):
    """Verify parameter value is within a range."""
    value = int(test_context['parameter_value'])
    assert int(min_val) <= value <= int(max_val), \
        f"Value {value} not in range [{min_val}, {max_val}]"
    logger.info(f"Value {value} is within range [{min_val}, {max_val}]")
```

### Step 3: QA Uses Immediately
QA can now use in ANY `.feature` file:

```gherkin
Scenario: Verify WiFi channel is valid
  When I get the parameter "Device.WiFi.Radio.1.Channel" using DMCLI
  Then the DMCLI command should succeed
  And the parameter value should be between 1 and 11
```

## Benefits of This Structure

### ✅ For QA Team
- Write tests without coding
- Unlimited test scenarios
- Fast test development
- Easy to understand and review

### ✅ For Development Team
- Maintain code in one place
- No code duplication
- Easy to add new capabilities
- Clear separation of concerns

### ✅ For Management
- Faster time-to-market
- Lower training costs
- Scalable test development
- Living documentation

## File Naming Conventions

### Feature Files (`tests/bdd/features/`)
- Format: `<feature_area>.feature`
- Examples:
  - `dmcli_operations.feature` - DMCLI GET/SET tests
  - `wifi_configuration.feature` - WiFi settings tests
  - `network_diagnostics.feature` - Network diagnostic tests

### Step Definitions (`tests/bdd/step_defs/`)
- **Single file**: `test_bdd_steps.py`
- Contains ALL step definitions
- Organized by sections (Given, When, Then)

## Current Test Coverage

### tests/bdd/features/ssh_cpe_connectivity.feature (6 scenarios)
1. Establish SSH connection to CPE device
2. Retrieve system information from CPE
3. Retrieve network information from CPE
4. Perform file operations on CPE
5. Retrieve memory information from CPE
6. Retrieve disk usage from CPE

### tests/bdd/features/rdk_cpe_advanced.feature (3 scenarios)
1. Connect to RDK CPE via SSH
2. Retrieve hardware information from RDK CPE
3. Access DMCLI interface on RDK CPE

### tests/bdd/features/dmcli_operations.feature (10 scenarios)
1. Get a parameter value using DMCLI
2. Set and verify a parameter using DMCLI
3. Get device hardware information via DMCLI
4. Get device software version via DMCLI
5. Get network interface information via DMCLI
6. Verify read-only parameter cannot be set
7. Get multiple related parameters
8. Set a numeric parameter
9. Verify parameter data type
10. Set a boolean parameter

**Total: 19 automated test scenarios**

## Running Tests

### From VSCode
1. Reload window (`Ctrl+Shift+P` → "Developer: Reload Window")
2. Open Test Explorer (Testing icon in sidebar)
3. All tests appear under `test_bdd_steps.py`
4. Click ▶️ to run any test

### From Command Line
```bash
# Run all BDD tests
pytest tests/bdd/step_defs/test_bdd_steps.py \
  --inventory-config=inventory.json \
  --env-config=env_config.json \
  --board-name=my_ssh_rdk_cpe \
  --skip-boot -v

# Run specific feature
pytest tests/bdd/step_defs/test_bdd_steps.py -k "dmcli" \
  --inventory-config=inventory.json \
  --env-config=env_config.json \
  --board-name=my_ssh_rdk_cpe \
  --skip-boot -v
```

## Next Steps

1. **QA Team**: Start adding test scenarios in `tests/bdd/features/`
2. **Developers**: Add new step definitions as needed in `test_bdd_steps.py`
3. **Everyone**: Run tests from VSCode Test Explorer!

See [WRITING_BDD_TESTS.md](WRITING_BDD_TESTS.md) for detailed guide on writing tests.
