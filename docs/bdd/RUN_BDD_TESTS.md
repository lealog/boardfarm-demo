# Running BDD Tests with Visual Studio Code

## Overview

Your BDD/Gherkin tests are organized by feature file for easy GUI execution:
- `tests/bdd/conftest.py` - Step definitions (all reusable steps)
- `tests/bdd/features/` - Gherkin scenarios (QA edits these)
  - `ssh_cpe_connectivity.feature` - 6 SSH connectivity scenarios
  - `rdk_cpe_advanced.feature` - 3 RDK advanced scenarios
  - `dmcli_operations.feature` - 10 DMCLI GET/SET scenarios
- `tests/bdd/test_*.py` - Test files (load feature files)

**Total: 19 test scenarios organized in 3 feature groups**

## Running from Command Line

To run the BDD tests, you need to provide boardfarm configuration:

```bash
# Run all BDD tests (all 19 scenarios)
pytest tests/bdd/ \
  --inventory-config=inventory.json \
  --env-config=env_config.json \
  --board-name=my_ssh_rdk_cpe \
  --skip-boot -v \
  --html=report.html \
  --self-contained-html

# Run SSH tests only (6 scenarios)
pytest tests/bdd/test_ssh_cpe_connectivity.py \
  --inventory-config=inventory.json \
  --env-config=env_config.json \
  --board-name=my_ssh_rdk_cpe \
  --skip-boot -v \
  --html=report.html \
  --self-contained-html

# Run DMCLI tests only (10 scenarios)
pytest tests/bdd/test_dmcli_operations.py \
  --inventory-config=inventory.json \
  --env-config=env_config.json \
  --board-name=my_ssh_rdk_cpe \
  --skip-boot -v \
  --html=report.html \
  --self-contained-html

# Run a specific scenario by function name
pytest tests/bdd/test_ssh_cpe_connectivity.py::test_establish_ssh_connection_to_cpe_device \
  --inventory-config=inventory.json \
  --env-config=env_config.json \
  --board-name=my_ssh_rdk_cpe \
  --skip-boot -v \
  --html=report.html \
  --self-contained-html
```

**Note**: Reports are automatically timestamped in the `reports/` directory (e.g., `reports/report_20251110_170737.html`)

## Running from VSCode Test Explorer

### Option 1: Configure VSCode Settings (Recommended)

Update `.vscode/settings.json` to include the required arguments:

```json
{
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,
  "python.testing.pytestArgs": [
    "tests/bdd",
    "-v",
    "--inventory-config=inventory.json",
    "--env-config=env_config.json",
    "--board-name=my_ssh_rdk_cpe",
    "--skip-boot",
    "--html=report.html",
    "--self-contained-html"
  ]
}
```

After updating the settings:
1. Reload VSCode (`Ctrl+Shift+P` → "Developer: Reload Window")
2. Open Test Explorer (Testing icon in left sidebar)
3. Click the play button next to any test to run it

### Option 2: Use pytest.ini defaults

Add to `pytest.ini`:

```ini
[pytest]
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests

# Boardfarm default configuration
addopts = --inventory-config=inventory.json --env-config=env_config.json --board-name=my_ssh_rdk_cpe --skip-boot
```

## Available Environments

Your `inventory.json` contains these environments:
- `my_ssh_cpe` - SSH connection to RPI CPE
- `my_ssh_rdk_cpe` - SSH connection to RDK CPE (default)
- `rdk_cpe_lxd` - LXD container with RDK CPE
- `rpi_cpe_lxd` - LXD container with RPI CPE

## Environment Variables

Make sure your `.env` file contains the required credentials:

```bash
CPE_USERNAME=root
CPE_PASSWORD=your_password_here
CPE_SHELL_PROMPT=root@.*#
CPE_GUI_PASSWORD=password
```

## Test Organization

```
tests/bdd/
├── features/                          # Gherkin scenarios (QA edits these)
│   ├── ssh_cpe_connectivity.feature   # 6 SSH scenarios
│   ├── rdk_cpe_advanced.feature       # 3 RDK scenarios
│   └── dmcli_operations.feature       # 10 DMCLI scenarios
├── conftest.py                        # Step definitions (developers maintain)
├── test_ssh_cpe_connectivity.py       # Loads SSH feature
├── test_rdk_cpe_advanced.py           # Loads RDK feature
└── test_dmcli_operations.py           # Loads DMCLI feature
```

**Key Architecture:**
- **Single Source of Truth**: All step definitions in `conftest.py`
- **Grouped by Feature**: Each test file loads one feature file
- **VSCode GUI Friendly**: Tests organized by feature in Test Explorer
- **QA-Friendly**: QA team writes plain English in `.feature` files, no Python knowledge needed
