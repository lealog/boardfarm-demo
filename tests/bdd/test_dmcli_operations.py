"""DMCLI Operations Tests

This file loads and runs all test scenarios from dmcli_operations.feature.
QA engineers should edit the .feature file to add/modify test scenarios.
"""

from pytest_bdd import scenarios

# Load all scenarios from the DMCLI operations feature file
scenarios('features/dmcli_operations.feature')
