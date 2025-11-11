"""SSH CPE Connectivity Tests

This file loads and runs all test scenarios from ssh_cpe_connectivity.feature.
QA engineers should edit the .feature file to add/modify test scenarios.
"""

from pytest_bdd import scenarios

# Load all scenarios from the SSH CPE connectivity feature file
scenarios('features/ssh_cpe_connectivity.feature')
