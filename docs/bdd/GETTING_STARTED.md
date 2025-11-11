# Getting Started with BDD Testing

## Quick Start for QA Engineers

### 1. Understanding the Structure

```
tests/bdd/
├── features/          ← YOU WRITE TESTS HERE (plain English)
└── step_defs/        ← Developers maintain this (Python)
```

**You only work in `features/` directory!**

### 2. Write Your First Test

1. Open `tests/bdd/features/dmcli_operations.feature`
2. Add a new scenario:

```gherkin
Scenario: Check device manufacturer
  When I get the parameter "Device.DeviceInfo.Manufacturer" using DMCLI
  Then the DMCLI command should succeed
  And the parameter value should not be empty
```

3. Save the file
4. Done! ✅

### 3. Run Your Test

#### In VSCode:
1. Reload VSCode (`Ctrl+Shift+P` → "Developer: Reload Window")
2. Click Testing icon (left sidebar)
3. Find your test under `test_bdd_steps.py`
4. Click ▶️ button

#### From Terminal:
```bash
pytest tests/bdd/step_defs/test_bdd_steps.py -k "manufacturer" \
  --inventory-config=inventory.json \
  --env-config=env_config.json \
  --board-name=my_ssh_rdk_cpe \
  --skip-boot -v
```

## Available Steps Reference Card

### Get a DMCLI Parameter
```gherkin
When I get the parameter "Device.DeviceInfo.ModelName" using DMCLI
```

### Set a DMCLI Parameter
```gherkin
When I set the parameter "Device.WiFi.Radio.1.Enable" to "true" using DMCLI
```

### Save & Restore Values
```gherkin
When I save the original value
# ... make changes ...
When I restore the parameter to its original value
```

### Verify Success
```gherkin
Then the DMCLI command should succeed
Then the parameter value should not be empty
Then the parameter value should be "expected_value"
```

### Verify Data Types
```gherkin
Then the parameter value should be a valid IP address
Then the parameter value should be a boolean
```

## Common Test Patterns

### Pattern 1: Simple GET
```gherkin
Scenario: Get device model
  When I get the parameter "Device.DeviceInfo.ModelName" using DMCLI
  Then the DMCLI command should succeed
  And the parameter value should not be empty
```

### Pattern 2: SET and Verify
```gherkin
Scenario: Enable WiFi radio
  When I get the parameter "Device.WiFi.Radio.1.Enable" using DMCLI
  And I save the original value
  When I set the parameter "Device.WiFi.Radio.1.Enable" to "true" using DMCLI
  Then the DMCLI command should succeed
  When I get the parameter "Device.WiFi.Radio.1.Enable" using DMCLI
  Then the parameter value should be "true"
  When I restore the parameter to its original value
```

### Pattern 3: Verify Read-Only
```gherkin
Scenario: Serial number is read-only
  When I attempt to set the parameter "Device.DeviceInfo.SerialNumber" to "TEST" using DMCLI
  Then the DMCLI command should fail
  And the error message should contain "read-only" or "not writable"
```

## Next Steps

1. Read [WRITING_BDD_TESTS.md](WRITING_BDD_TESTS.md) for complete guide
2. Look at existing scenarios in `tests/bdd/features/` for examples
3. Start adding your own tests!

## Need Help?

- **How to write tests**: See [WRITING_BDD_TESTS.md](WRITING_BDD_TESTS.md)
- **How to run tests**: See [RUN_BDD_TESTS.md](RUN_BDD_TESTS.md)
- **Project structure**: See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
- **Complete overview**: See [BDD_TESTING_SUMMARY.md](BDD_TESTING_SUMMARY.md)
