# Boardfarm BDD Testing Framework

A comprehensive BDD (Behavior-Driven Development) testing framework for CPE devices using Gherkin syntax and pytest-bdd.

## 📁 Project Structure

```
boardfarm-demo/
├── tests/
│   ├── bdd/                              # BDD Test Suite
│   │   ├── features/                     # Gherkin scenarios (QA edits these)
│   │   │   ├── ssh_cpe_connectivity.feature      # SSH connectivity tests
│   │   │   ├── rdk_cpe_advanced.feature          # RDK advanced features
│   │   │   └── dmcli_operations.feature          # DMCLI GET/SET operations
│   │   ├── conftest.py                   # Step definitions (developers maintain)
│   │   ├── test_ssh_cpe_connectivity.py  # Loads SSH feature (template)
│   │   ├── test_rdk_cpe_advanced.py      # Loads RDK feature (template)
│   │   └── test_dmcli_operations.py      # Loads DMCLI feature (template)
│   └── [other test files]
├── docs/                                 # Documentation
│   ├── bdd/                             # BDD testing guides
│   ├── credentials/                     # Credential setup
│   └── setup/                           # Installation guides
├── inventory.json                        # Device inventory
├── env_config.json                       # Environment configuration
└── .env                                  # Credentials (not in git)
```

## 🚀 Quick Start

See [docs/bdd/](docs/bdd/) for complete documentation.

## ✍️ Writing New Tests (No Coding Required!)

Edit files in `tests/bdd/features/` - see [WRITING_BDD_TESTS.md](docs/bdd/WRITING_BDD_TESTS.md)

## 📚 Documentation

- [Writing BDD Tests](docs/bdd/WRITING_BDD_TESTS.md) - For QA engineers
- [Running Tests](docs/bdd/RUN_BDD_TESTS.md) - How to execute tests  
- [BDD Summary](docs/bdd/BDD_TESTING_SUMMARY.md) - Complete overview
- [Credentials Setup](docs/credentials/CREDENTIALS_SETUP.md) - Device setup

## 🎯 Current Tests: 19 Scenarios

- 6 SSH connectivity tests
- 3 RDK advanced tests
- 10 DMCLI GET/SET tests

Start writing tests in `tests/bdd/features/` - they'll appear in VSCode Test Explorer automatically!

## 📊 Test Reports

All test reports are automatically saved with timestamps in the `reports/` directory:

```
reports/report_20251110_170737.html
```

### Generate Report

```bash
# Run all BDD tests
pytest tests/bdd/ \
  --inventory-config=inventory.json \
  --env-config=env_config.json \
  --board-name=my_ssh_rdk_cpe \
  --skip-boot -v \
  --html=report.html \
  --self-contained-html

# Run specific feature tests
pytest tests/bdd/test_dmcli_operations.py \
  --inventory-config=inventory.json \
  --env-config=env_config.json \
  --board-name=my_ssh_rdk_cpe \
  --skip-boot -v \
  --html=report.html \
  --self-contained-html
```

See [Test Reports Documentation](docs/bdd/REPORTS.md) for details.
