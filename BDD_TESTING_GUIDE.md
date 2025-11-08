# BDD Testing Guide for Boardfarm

This guide explains how to use Behavior-Driven Development (BDD) testing in the Boardfarm project using pytest-bdd.

## What is BDD?

Behavior-Driven Development (BDD) is a testing approach that:
- Uses **natural language** (Gherkin) to describe test scenarios
- Makes tests **readable by non-technical stakeholders**
- Encourages **collaboration** between developers, QA, and business people
- Focuses on **behavior** rather than implementation

## Project Structure

```
boardfarm-demo/
├── tests/
│   ├── features/                          # Gherkin feature files
│   │   ├── ssh_cpe_connectivity.feature   # CPE connectivity scenarios
│   │   └── rdk_cpe_advanced.feature       # RDK CPE advanced scenarios
│   ├── test_ssh_cpe_bdd.py               # BDD step definitions
│   ├── tests_ssh_cpe.py                  # Traditional pytest tests (original)
│   └── ...
├── requirements.txt                       # Python dependencies
└── pytest.ini                            # Pytest configuration
```

## Components

### 1. Feature Files (.feature)

Feature files use **Gherkin syntax** to describe test scenarios in plain English.

**Location:** `tests/features/`

**Example:** [ssh_cpe_connectivity.feature](tests/features/ssh_cpe_connectivity.feature)

```gherkin
Feature: SSH CPE Device Connectivity
  As a network engineer
  I want to connect to CPE devices via SSH
  So that I can manage and monitor the devices remotely

  Scenario: Establish SSH connection to CPE device
    Given a CPE device is configured in the inventory
    When I connect to the CPE device via SSH
    Then the connection should be successful
    And I should be able to execute commands
```

### 2. Step Definitions (.py)

Step definitions are Python functions that implement the steps described in the feature files.

**Location:** `tests/test_ssh_cpe_bdd.py`

**Example:**

```python
from pytest_bdd import scenarios, given, when, then

# Load all scenarios from the feature file
scenarios('features/ssh_cpe_connectivity.feature')

@given('a CPE device is configured in the inventory')
def cpe_device_available(device_manager, cpe_context):
    cpe = get_cpe_device(device_manager)
    cpe_context['device'] = cpe

@when('I connect to the CPE device via SSH')
def connect_to_cpe(cpe_context):
    # Connection happens automatically
    logger.info(f"SSH connection established to: {cpe_context['device']}")

@then('the connection should be successful')
def verify_connection(cpe_context):
    cpe = cpe_context['device']
    output = cpe.command("echo 'SSH CPE is connected'")
    assert "SSH CPE is connected" in output
```

## Gherkin Syntax

### Keywords

- **Feature:** High-level description of a feature being tested
- **Scenario:** A specific test case
- **Background:** Steps that run before each scenario
- **Given:** Preconditions (setup)
- **When:** Actions performed
- **Then:** Expected outcomes (assertions)
- **And/But:** Additional steps

### Example Scenario

```gherkin
Scenario: Retrieve system information from CPE
  When I connect to the CPE device via SSH
  And I query the system hostname
  Then I should receive a valid hostname
  When I query the kernel version
  Then I should receive a valid kernel version
```

### Parametrized Steps

You can pass parameters to steps:

```gherkin
When I create a test file with content "Boardfarm SSH test"
Then the content should match "Boardfarm SSH test"
```

Implemented with `parsers.parse()`:

```python
from pytest_bdd import parsers

@when(parsers.parse('I create a test file with content "{content}"'))
def create_test_file(cpe_context, content):
    # content parameter is extracted from the step text
    cpe_context['test_content'] = content
```

## Running BDD Tests

### Run All Tests

```bash
pytest tests/test_ssh_cpe_bdd.py -v
```

### Run Specific Feature

```bash
pytest tests/test_ssh_cpe_bdd.py::test_ssh_cpe_connectivity -v
```

### Run Tests with Markers

```bash
# Run only slow tests
pytest tests/test_ssh_cpe_bdd.py -m slow -v

# Skip slow tests
pytest tests/test_ssh_cpe_bdd.py -m "not slow" -v
```

### Verbose Output

```bash
pytest tests/test_ssh_cpe_bdd.py -v --tb=short
```

### Run with Logging

```bash
pytest tests/test_ssh_cpe_bdd.py -v --log-cli-level=INFO
```

## BDD vs Traditional Pytest

### Traditional Pytest

```python
def test_ssh_cpe_connection(device_manager):
    """Test SSH connection to CPE device."""
    cpe = get_cpe_device(device_manager)
    output = cpe.command("echo 'SSH CPE is connected'")
    assert "SSH CPE is connected" in output
```

**Pros:**
- Quick to write
- Familiar to Python developers
- Less overhead

**Cons:**
- Test intent may not be clear to non-developers
- Harder to maintain as tests grow

### BDD with pytest-bdd

**Feature file:**
```gherkin
Scenario: Establish SSH connection to CPE device
  Given a CPE device is configured in the inventory
  When I connect to the CPE device via SSH
  Then the connection should be successful
```

**Step definitions:**
```python
@given('a CPE device is configured in the inventory')
def cpe_device_available(device_manager, cpe_context):
    cpe_context['device'] = get_cpe_device(device_manager)

@then('the connection should be successful')
def verify_connection(cpe_context):
    output = cpe_context['device'].command("echo 'SSH CPE is connected'")
    assert "SSH CPE is connected" in output
```

**Pros:**
- Business-readable scenarios
- Clear separation of "what" (feature) and "how" (steps)
- Better documentation
- Encourages thinking about behavior

**Cons:**
- More files to maintain
- Slight learning curve for Gherkin

## Best Practices

### 1. Write Declarative Scenarios

**Good:**
```gherkin
When I query the system hostname
Then I should receive a valid hostname
```

**Bad:**
```gherkin
When I execute "hostname" command
Then the output should not be empty
```

### 2. Use Background for Common Setup

```gherkin
Background:
  Given a CPE device is configured in the inventory
  And I am connected to the device

Scenario: Check hostname
  When I query the system hostname
  Then I should receive a valid hostname

Scenario: Check uptime
  When I query the system uptime
  Then I should receive uptime information
```

### 3. Keep Scenarios Focused

Each scenario should test **one specific behavior**.

### 4. Use Tags/Markers

```gherkin
@slow
Scenario: Retrieve hardware information from RDK CPE
  Given I am connected to an RDK CPE device
  When I query the device serial number
  Then I should receive a valid serial number
```

### 5. Reuse Step Definitions

Write generic, reusable steps that can be used across multiple scenarios.

## Integration with Boardfarm

### Device Manager Fixture

BDD tests work seamlessly with boardfarm's `device_manager` fixture:

```python
@given('a CPE device is configured in the inventory')
def cpe_device_available(device_manager: DeviceManager, cpe_context):
    devices = device_manager.get_devices_by_type(RdkCpeDevice)
    cpe_context['device'] = list(devices.values())[0]
```

### Context Sharing

Use a `cpe_context` fixture to share data between steps:

```python
@pytest.fixture
def cpe_context():
    """Context object to share data between steps in a scenario."""
    return {
        'device': None,
        'output': None,
        'test_file': '/tmp/boardfarm_test.txt'
    }
```

### Markers

pytest-bdd supports pytest markers:

```gherkin
@slow
Scenario: Long-running test
  ...
```

```python
# In pytest.ini
[pytest]
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
```

## Converting Existing Tests to BDD

### Step 1: Identify Test Behavior

Look at your existing test and identify:
- **Given:** What preconditions are needed?
- **When:** What action is performed?
- **Then:** What should be the result?

### Step 2: Write Feature File

```gherkin
Scenario: Test description
  Given precondition
  When action
  Then expected result
```

### Step 3: Implement Step Definitions

Map each step to a Python function using `@given`, `@when`, `@then`.

### Example Conversion

**Original pytest:**
```python
def test_ssh_cpe_system_info(device_manager):
    cpe = get_cpe_device(device_manager)
    hostname = cpe.command("hostname")
    assert hostname, "Failed to get hostname"
```

**BDD version:**

Feature file:
```gherkin
Scenario: Retrieve system information from CPE
  Given a CPE device is configured in the inventory
  When I query the system hostname
  Then I should receive a valid hostname
```

Step definitions:
```python
@when('I query the system hostname')
def query_hostname(cpe_context):
    cpe = cpe_context['device']
    cpe_context['output'] = cpe.command("hostname")

@then('I should receive a valid hostname')
def verify_hostname(cpe_context):
    assert cpe_context['output'], "Failed to get hostname"
```

## Hybrid Approach

You can **mix BDD and traditional pytest** in the same project:

```
tests/
├── features/              # BDD scenarios for high-level features
├── test_ssh_cpe_bdd.py   # BDD step definitions
├── tests_ssh_cpe.py      # Traditional pytest for quick tests
└── tests_basic.py        # Unit-style tests
```

**Use BDD for:**
- User-facing features
- Integration tests
- Tests that need to be understood by non-developers
- Complex workflows

**Use traditional pytest for:**
- Unit tests
- Quick smoke tests
- Developer-focused tests

## Running on Different Machines

The BDD tests work identically whether you run them:
- Locally on your Mac
- On your Linux test PC
- In CI/CD pipelines

Simply ensure `pytest-bdd` is installed:

```bash
pip3 install -r requirements.txt
```

Then run tests as usual:

```bash
pytest tests/test_ssh_cpe_bdd.py -v
```

## Troubleshooting

### Step Not Found

```
StepDefinitionNotFoundError: Step definition is not found
```

**Solution:** Ensure the step text in the feature file **exactly matches** the step definition decorator.

### Scenario Not Loaded

```
No tests collected
```

**Solution:** Check that you have `scenarios('features/your_file.feature')` in your test file.

### Import Errors

```
ModuleNotFoundError: No module named 'pytest_bdd'
```

**Solution:** Install pytest-bdd:
```bash
pip3 install pytest-bdd
```

## Resources

- **pytest-bdd documentation:** https://pytest-bdd.readthedocs.io/
- **Gherkin syntax:** https://cucumber.io/docs/gherkin/reference/
- **Example tests:** [test_ssh_cpe_bdd.py](tests/test_ssh_cpe_bdd.py)
- **Example features:** [features/](tests/features/)

## Next Steps

1. **Run the example BDD tests** to see them in action
2. **Convert one of your existing tests** to BDD
3. **Write new test scenarios** in Gherkin for upcoming features
4. **Share feature files** with your team for review

## Summary

BDD with pytest-bdd provides:
- ✅ **Readable scenarios** for everyone on the team
- ✅ **Better documentation** of system behavior
- ✅ **Seamless integration** with existing pytest tests
- ✅ **Reusable step definitions** across scenarios
- ✅ **Works with boardfarm fixtures** out of the box

Start by converting a few key tests to BDD, then gradually expand as you see the benefits!
