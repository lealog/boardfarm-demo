"""RDK CPE Advanced Tests

This file loads and runs all test scenarios from rdk_cpe_advanced.feature.
QA engineers should edit the .feature file to add/modify test scenarios.
"""

from pytest_bdd import scenarios

# Load all scenarios from the RDK CPE advanced feature file
scenarios('features/rdk_cpe_advanced.feature')
