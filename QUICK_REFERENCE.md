# Quick Reference Guide

## Directory Structure

```
tests/bdd/
├── features/                     ← Write test scenarios here (QA)
│   ├── ssh_cpe_connectivity.feature
│   ├── rdk_cpe_advanced.feature
│   └── dmcli_operations.feature
├── conftest.py                   ← Step definitions (Developers)
├── test_ssh_cpe_connectivity.py  ← Template (loads SSH feature)
├── test_rdk_cpe_advanced.py      ← Template (loads RDK feature)
└── test_dmcli_operations.py      ← Template (loads DMCLI feature)

reports/                          ← Timestamped HTML reports
docs/bdd/                        ← Documentation
```

## Running Tests

### Run All Tests
```bash
# Run all BDD tests (all 19 scenarios)
pytest tests/bdd/ \
  --inventory-config=inventory.json \
  --env-config=env_config.json \
  --board-name=my_ssh_rdk_cpe \
  --skip-boot -v \
  --html=report.html \
  --self-contained-html
```

### Run Specific Feature Tests
```bash
# Run SSH connectivity tests only (6 tests)
pytest tests/bdd/test_ssh_cpe_connectivity.py \
  --inventory-config=inventory.json \
  --env-config=env_config.json \
  --board-name=my_ssh_rdk_cpe \
  --skip-boot -v \
  --html=report.html \
  --self-contained-html

# Run DMCLI tests only (10 tests)
pytest tests/bdd/test_dmcli_operations.py \
  --inventory-config=inventory.json \
  --env-config=env_config.json \
  --board-name=my_ssh_rdk_cpe \
  --skip-boot -v \
  --html=report.html \
  --self-contained-html

# Run RDK advanced tests only (3 tests)
pytest tests/bdd/test_rdk_cpe_advanced.py \
  --inventory-config=inventory.json \
  --env-config=env_config.json \
  --board-name=my_ssh_rdk_cpe \
  --skip-boot -v \
  --html=report.html \
  --self-contained-html
```

### Run Specific Scenario
```bash
# Run specific scenario by name (use -k filter)
pytest tests/bdd/test_dmcli_operations.py \
  -k "Get a parameter value" \
  --inventory-config=inventory.json \
  --env-config=env_config.json \
  --board-name=my_ssh_rdk_cpe \
  --skip-boot -v \
  --html=report.html \
  --self-contained-html

# Run by exact function name
pytest tests/bdd/test_dmcli_operations.py::test_get_a_parameter_value_using_dmcli \
  --inventory-config=inventory.json \
  --env-config=env_config.json \
  --board-name=my_ssh_rdk_cpe \
  --skip-boot -v \
  --html=report.html \
  --self-contained-html
```

## Writing Tests (QA)

### 1. Open Feature File
```bash
# Edit existing or create new
vim tests/bdd/features/dmcli_operations.feature
```

### 2. Add Scenario
```gherkin
Scenario: Your test name here
  When I get the parameter "Device.DeviceInfo.ModelName" using DMCLI
  Then the DMCLI command should succeed
  And the parameter value should not be empty
```

### 3. Save and Run
- File saved → Test appears in VSCode automatically
- Click ▶️ to run

## Common Steps Reference

### DMCLI GET
```gherkin
When I get the parameter "Device.DeviceInfo.ModelName" using DMCLI
```

### DMCLI SET
```gherkin
When I set the parameter "Device.WiFi.Radio.1.Enable" to "true" using DMCLI
```

### Save & Restore
```gherkin
When I save the original value
# ... do testing ...
When I restore the parameter to its original value
```

### Verify
```gherkin
Then the DMCLI command should succeed
Then the parameter value should not be empty
Then the parameter value should be "expected_value"
Then the parameter value should be a valid IP address
Then the parameter value should be a boolean
```

## Reports

### View Latest Report
```bash
ls -lt reports/*.html | head -1
xdg-open $(ls -t reports/*.html | head -1)
```

### List All Reports
```bash
ls -lht reports/
```

### Clean Old Reports
```bash
# Delete reports older than 30 days
find reports/ -name "report_*.html" -mtime +30 -delete
```

## VSCode Integration

### Test Explorer
1. Click Testing icon (left sidebar)
2. Find tests grouped by feature file:
   - `test_ssh_cpe_connectivity.py` (6 tests)
   - `test_rdk_cpe_advanced.py` (3 tests)
   - `test_dmcli_operations.py` (10 tests)
3. Click ▶️ next to file to run all tests in that feature
4. Click ▶️ next to individual test to run single scenario

### Reload VSCode
```
Ctrl+Shift+P → "Developer: Reload Window"
```

## File Locations

| What | Where |
|------|-------|
| Test Scenarios (QA edits) | `tests/bdd/features/*.feature` |
| Step Definitions (Devs maintain) | `tests/bdd/conftest.py` |
| Test Files (Templates) | `tests/bdd/test_*.py` |
| Reports | `reports/report_YYYYMMDD_HHMMSS.html` |
| Documentation | `docs/bdd/` |
| Inventory | `inventory.json` |
| Credentials | `.env` |

## Common DMCLI Parameters

```gherkin
Device.DeviceInfo.Manufacturer
Device.DeviceInfo.ModelName
Device.DeviceInfo.SerialNumber
Device.DeviceInfo.SoftwareVersion
Device.WiFi.Radio.1.Enable
Device.WiFi.Radio.1.Channel
Device.WiFi.SSID.1.SSID
Device.IP.Interface.1.IPv4Address.1.IPAddress
```

## Test Statistics

- **Total Scenarios**: 19
- **SSH Tests**: 6
- **RDK Tests**: 3
- **DMCLI Tests**: 10

## Documentation

| Guide | Purpose |
|-------|---------|
| [GETTING_STARTED](docs/bdd/GETTING_STARTED.md) | Quick start for QA |
| [WRITING_BDD_TESTS](docs/bdd/WRITING_BDD_TESTS.md) | Complete writing guide |
| [RUN_BDD_TESTS](docs/bdd/RUN_BDD_TESTS.md) | How to run tests |
| [REPORTS](docs/bdd/REPORTS.md) | Report management |
| [PROJECT_STRUCTURE](docs/bdd/PROJECT_STRUCTURE.md) | Architecture |

## Troubleshooting

### Tests Not Found
```bash
# Reload VSCode
Ctrl+Shift+P → "Developer: Reload Window"
```

### Connection Failed
```bash
# Check credentials in .env
cat .env
```

### Report Not Generated
```bash
# Check pytest-html is installed
pip install pytest-html
```

## Quick Tips

1. ✅ **One step definitions file** - All steps in `conftest.py`
2. ✅ **Timestamped reports** - Never overwrite old reports
3. ✅ **No Python needed** - QA writes plain English in `.feature` files
4. ✅ **VSCode integration** - Click test file or scenario to run
5. ✅ **Organized by feature** - Tests grouped by feature file in GUI

## Need New Capability?

1. **QA**: Describe what you need to test
2. **Dev**: Add step to `conftest.py`
3. **QA**: Use new step in `.feature` files

## Example Workflow

```bash
# 1. Write test
vim tests/bdd/features/dmcli_operations.feature

# 2. Run test (from command line)
pytest tests/bdd/test_dmcli_operations.py --inventory-config=inventory.json --env-config=env_config.json --board-name=my_ssh_rdk_cpe --skip-boot -v --html=report.html --self-contained-html

# OR: Run from VSCode GUI (recommended)
# Open Test Explorer → Click ▶️ next to test_dmcli_operations.py

# 3. View report
xdg-open $(ls -t reports/*.html | head -1)

# 4. Commit changes
git add tests/bdd/features/dmcli_operations.feature
git commit -m "Add DMCLI test for..."
```

---

**For detailed documentation, see `docs/bdd/` directory**
