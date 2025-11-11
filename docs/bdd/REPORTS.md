# Test Reports

## Overview

All test reports are automatically saved in the `reports/` directory with timestamps in the format:

```
reports/report_YYYYMMDD_HHMMSS.html
```

Example: `reports/report_20251110_170737.html`

## Automatic Timestamped Reports

The test framework automatically generates timestamped HTML reports. When you run tests with `--html=report.html`, the actual report is saved with a timestamp.

### How It Works

The `conftest.py` automatically intercepts the `--html=report.html` option and converts it to:

```python
--html=reports/report_20251110_170737.html
```

This means:
- ✅ All reports are saved in the `reports/` directory
- ✅ Each report has a unique timestamp
- ✅ Old reports are never overwritten
- ✅ You can track test history over time

## Running Tests with Reports

### Using pytest

```bash
# Run all BDD tests
pytest tests/bdd/step_defs/test_bdd_steps.py \
  --inventory-config=inventory.json \
  --env-config=env_config.json \
  --board-name=my_ssh_rdk_cpe \
  --skip-boot -v \
  --html=report.html \
  --self-contained-html

# The report will be automatically saved as:
# reports/report_20251110_170737.html
```

### From VSCode

When running tests from VSCode Test Explorer, reports are also automatically timestamped.

The report location is configured in `.vscode/settings.json`:

```json
{
  "python.testing.pytestArgs": [
    "tests/bdd",
    "-v",
    "--inventory-config=inventory.json",
    "--env-config=env_config.json",
    "--board-name=my_ssh_rdk_cpe",
    "--skip-boot",
    "--log-cli-level=INFO",
    "--html=report.html",
    "--self-contained-html"
  ]
}
```

## Report Features

### What's Included in Reports

1. **Test Summary**
   - Total tests run
   - Pass/Fail counts
   - Test duration

2. **Detailed Results**
   - Each test scenario
   - Gherkin steps executed
   - Pass/Fail status
   - Error messages (if any)
   - Logs and output

3. **Environment Info**
   - Python version
   - Pytest version
   - Test configuration
   - Device information

4. **Self-Contained**
   - All CSS and JavaScript embedded
   - No external dependencies
   - Easy to share via email

## Managing Reports

### Viewing Recent Reports

```bash
# List all reports (newest first)
ls -lt reports/*.html

# List last 5 reports
ls -lt reports/*.html | head -5

# Open most recent report in browser
xdg-open $(ls -t reports/*.html | head -1)
```

### Cleaning Old Reports

```bash
# Keep last 10 reports, delete older ones
cd reports/
ls -t report_*.html | tail -n +11 | xargs rm -f

# Delete reports older than 30 days
find reports/ -name "report_*.html" -mtime +30 -delete
```

### Finding Specific Reports

```bash
# Find reports from a specific date
ls reports/report_20251110_*.html

# Find reports from a specific hour
ls reports/report_20251110_17*.html

# Search for reports containing specific test results
grep -l "test_dmcli" reports/*.html
```

## Report Organization

### Directory Structure

```
reports/
├── .gitignore              # Ignores HTML files (not committed to git)
├── .gitkeep                # Keeps directory in git
└── report_YYYYMMDD_HHMMSS.html  # Timestamped reports
```

### Timestamp Format

- `YYYY` - 4-digit year (2025)
- `MM` - 2-digit month (01-12)
- `DD` - 2-digit day (01-31)
- `HH` - 2-digit hour, 24-hour format (00-23)
- `MM` - 2-digit minute (00-59)
- `SS` - 2-digit second (00-59)

Example: `report_20251110_170737.html`
- Date: November 10, 2025
- Time: 17:07:37 (5:07:37 PM)

## Sharing Reports

### Email
Reports are self-contained HTML files that can be attached to emails.

### Network Share
```bash
# Copy to shared network location
cp reports/report_*.html /path/to/shared/folder/
```

### CI/CD Integration
```bash
# Archive reports in Jenkins/GitLab CI
- uses: actions/upload-artifact@v2
  with:
    name: test-reports
    path: reports/*.html
```

## Report Examples

### Successful Test Run
```
✅ tests/bdd/step_defs/test_bdd_steps.py::test_get_a_parameter_value_using_dmcli PASSED
✅ tests/bdd/step_defs/test_bdd_steps.py::test_set_and_verify_a_parameter_using_dmcli PASSED
✅ tests/bdd/step_defs/test_bdd_steps.py::test_get_device_hardware_information_via_dmcli PASSED

19 passed in 45.23s
```

### Failed Test Run
```
✅ tests/bdd/step_defs/test_bdd_steps.py::test_get_a_parameter_value_using_dmcli PASSED
❌ tests/bdd/step_defs/test_bdd_steps.py::test_set_and_verify_a_parameter_using_dmcli FAILED
   DMCLI command failed: Parameter not found

17 passed, 2 failed in 42.15s
```

## Troubleshooting

### Reports Not Being Created

**Issue**: No report file generated

**Solution**: Check that pytest-html is installed:
```bash
pip install pytest-html
```

### Reports in Wrong Location

**Issue**: Report saved as `report.html` in current directory

**Solution**: Make sure you're using the conftest.py that has the timestamp logic

### Old Reports Filling Disk

**Issue**: Too many old reports

**Solution**: Set up a cleanup cron job:
```bash
# Add to crontab (daily cleanup of reports older than 30 days)
0 2 * * * find /path/to/boardfarm-demo/reports -name "report_*.html" -mtime +30 -delete
```

## Best Practices

1. **Keep Recent Reports** - Don't delete reports from the last 30 days
2. **Archive Important Runs** - Copy significant test runs to a permanent location
3. **Review Failed Tests** - Always check the report when tests fail
4. **Share With Team** - Email reports to stakeholders after major test runs
5. **Track Trends** - Compare reports over time to spot patterns

## Quick Reference

```bash
# Run tests and generate report

# Run specific test category

# View most recent report
xdg-open $(ls -t reports/*.html | head -1)

# List all reports
ls -lht reports/*.html

# Clean reports older than 30 days
find reports/ -name "report_*.html" -mtime +30 -delete
```

## Next Steps

- Run tests to generate your first report
- Share report with your team
- Set up automated cleanup of old reports
- Integrate reports into your CI/CD pipeline
