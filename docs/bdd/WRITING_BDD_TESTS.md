# Writing BDD Test Cases for Non-Developers

This guide helps QA engineers write new test cases using Gherkin syntax without needing to write Python code.

## What is Gherkin?

Gherkin is a plain-English syntax for writing test scenarios. It uses keywords like:
- **Feature**: Describes what you're testing
- **Scenario**: A specific test case
- **Given**: The starting conditions
- **When**: Actions to perform
- **Then**: Expected results

## Quick Start

### 1. Create or Edit a `.feature` File

Feature files are located in `tests/features/`. You can either:
- Edit an existing file (e.g., `dmcli_operations.feature`)
- Create a new file (e.g., `my_new_tests.feature`)

### 2. Write Your Test Scenario

```gherkin
Feature: Your feature name here
  As a QA engineer
  I want to test something
  So that I can verify it works

  Background:
    Given an RDK CPE device is available in the inventory
    And I am connected to an RDK CPE device
    And the DMCLI tool is available on the device

  Scenario: Your test scenario name
    When I get the parameter "Device.DeviceInfo.ModelName" using DMCLI
    Then the DMCLI command should succeed
    And the parameter value should not be empty
```

## Available Step Definitions for DMCLI Testing

### Setup Steps (Given)
```gherkin
Given an RDK CPE device is available in the inventory
Given I am connected to an RDK CPE device
Given the DMCLI tool is available on the device
```

### Action Steps (When)

#### Get a Parameter
```gherkin
When I get the parameter "Device.DeviceInfo.ModelName" using DMCLI
```

#### Set a Parameter
```gherkin
When I set the parameter "Device.WiFi.Radio.1.Enable" to "true" using DMCLI
When I set the parameter "Device.WiFi.Radio.1.Channel" to "6" using DMCLI
```

#### Save and Restore Values
```gherkin
When I get the parameter "Device.WiFi.Radio.1.Channel" using DMCLI
And I save the original value
When I set the parameter "Device.WiFi.Radio.1.Channel" to "11" using DMCLI
# ... do more tests ...
When I restore the parameter to its original value
```

#### Get Multiple Parameters
```gherkin
When I get the following parameters using DMCLI:
  | Parameter                          |
  | Device.DeviceInfo.Manufacturer     |
  | Device.DeviceInfo.ModelName        |
  | Device.DeviceInfo.SoftwareVersion  |
```

#### Attempt a SET (that might fail)
```gherkin
When I attempt to set the parameter "Device.DeviceInfo.SerialNumber" to "TEST" using DMCLI
```

### Verification Steps (Then)

#### Check Command Success/Failure
```gherkin
Then the DMCLI command should succeed
Then the DMCLI command should fail
```

#### Check Parameter Values
```gherkin
Then the parameter value should not be empty
Then the parameter value should be "true"
Then the parameter value should be "6"
```

#### Check Value Format
```gherkin
Then the parameter value should be a valid IP address
Then the parameter value should be a boolean
Then the parameter value should match the pattern ".*[0-9]+.*"
```

#### Check Error Messages
```gherkin
Then the error message should contain "read-only" or "not writable"
```

#### Check Multiple Results
```gherkin
Then all DMCLI commands should succeed
Then all parameter values should not be empty
```

## Example Test Scenarios

### Example 1: Simple GET Test
```gherkin
Scenario: Get device model name
  When I get the parameter "Device.DeviceInfo.ModelName" using DMCLI
  Then the DMCLI command should succeed
  And the parameter value should not be empty
```

### Example 2: SET and Verify Test
```gherkin
Scenario: Change WiFi channel
  When I get the parameter "Device.WiFi.Radio.1.Channel" using DMCLI
  And I save the original value
  When I set the parameter "Device.WiFi.Radio.1.Channel" to "11" using DMCLI
  Then the DMCLI command should succeed
  When I get the parameter "Device.WiFi.Radio.1.Channel" using DMCLI
  Then the parameter value should be "11"
  When I restore the parameter to its original value
```

### Example 3: Verify Read-Only Parameter
```gherkin
Scenario: Verify serial number is read-only
  When I attempt to set the parameter "Device.DeviceInfo.SerialNumber" to "FAKE123" using DMCLI
  Then the DMCLI command should fail
  And the error message should contain "read-only" or "not writable"
```

### Example 4: Get Multiple Parameters
```gherkin
Scenario: Get all device information
  When I get the following parameters using DMCLI:
    | Parameter                               |
    | Device.DeviceInfo.Manufacturer          |
    | Device.DeviceInfo.ModelName             |
    | Device.DeviceInfo.HardwareVersion       |
    | Device.DeviceInfo.SoftwareVersion       |
    | Device.DeviceInfo.SerialNumber          |
  Then all DMCLI commands should succeed
  And all parameter values should not be empty
```

## Common DMCLI Parameters to Test

### Device Information
- `Device.DeviceInfo.Manufacturer`
- `Device.DeviceInfo.ModelName`
- `Device.DeviceInfo.SerialNumber`
- `Device.DeviceInfo.HardwareVersion`
- `Device.DeviceInfo.SoftwareVersion`
- `Device.DeviceInfo.UpTime`

### WiFi Parameters
- `Device.WiFi.Radio.1.Enable` (boolean)
- `Device.WiFi.Radio.1.Channel` (number)
- `Device.WiFi.Radio.1.OperatingFrequencyBand` (string)
- `Device.WiFi.SSID.1.Enable` (boolean)
- `Device.WiFi.SSID.1.SSID` (string)

### Network Parameters
- `Device.IP.Interface.1.IPv4Address.1.IPAddress`
- `Device.Ethernet.Interface.1.MACAddress`
- `Device.Routing.Router.1.Enable`

### System Parameters
- `Device.Time.CurrentLocalTime`
- `Device.UserInterface.X_CISCO_COM_AdvancedSecurity`

## Tips for Writing Good Test Scenarios

1. **Be Specific**: Use clear, descriptive scenario names
   - ✅ Good: "Verify WiFi radio can be enabled and disabled"
   - ❌ Bad: "Test WiFi"

2. **One Test Per Scenario**: Each scenario should test one thing
   - ✅ Good: Separate scenarios for GET and SET
   - ❌ Bad: One scenario that tests 10 different parameters

3. **Always Clean Up**: If you change a value, restore it
   ```gherkin
   When I save the original value
   # ... test steps ...
   When I restore the parameter to its original value
   ```

4. **Use Background**: Put common setup steps in the Background section
   ```gherkin
   Background:
     Given an RDK CPE device is available in the inventory
     And I am connected to an RDK CPE device
   ```

5. **Add Tags for Organization**: Use `@tags` to categorize tests
   ```gherkin
   @smoke @wifi
   Scenario: Quick WiFi radio check
     ...

   @slow @network
   Scenario: Full network configuration test
     ...
   ```

## Running Your Tests

### From Command Line
```bash
# Run all DMCLI tests
pytest tests/test_dmcli_operations_bdd.py --inventory-config=inventory.json --env-config=env_config.json --board-name=my_ssh_rdk_cpe --skip-boot -v

# Run a specific scenario
pytest tests/test_dmcli_operations_bdd.py::test_get_device_model_name --inventory-config=inventory.json --env-config=env_config.json --board-name=my_ssh_rdk_cpe --skip-boot -v

# Run with HTML report
pytest tests/test_dmcli_operations_bdd.py --inventory-config=inventory.json --env-config=env_config.json --board-name=my_ssh_rdk_cpe --skip-boot -v --html=report.html --self-contained-html
```

### From VSCode
1. Open Test Explorer (Testing icon in left sidebar)
2. Find your test under `test_dmcli_operations_bdd.py`
3. Click the ▶️ play button next to any scenario

## Need More Step Definitions?

If you need to test something that isn't covered by the existing steps, ask a developer to add new step definitions to `tests/test_dmcli_operations_bdd.py`.

For example, if you need to:
- Check if a value is within a range
- Parse complex output formats
- Perform calculations on values
- Test timing/performance

The developer can add new `@when` and `@then` step definitions that you can then use in your `.feature` files!

## Common Issues and Solutions

### Issue: Test fails with "step not found"
**Solution**: Make sure you're using the exact step text from the "Available Step Definitions" section above. Even small differences (like missing quotes or different wording) will cause the step not to match.

### Issue: Parameter not found
**Solution**: Verify the parameter name is correct for your device. You can test it manually first:
```bash
ssh root@your-device-ip
dmcli eRT getv Device.DeviceInfo.ModelName
```

### Issue: Test times out
**Solution**: Some parameters take longer to query. You can mark slow tests with `@slow` tag:
```gherkin
@slow
Scenario: Long-running test
  ...
```

Then skip them in quick test runs:
```bash
pytest -m "not slow"
```
