"""Test Feature

This file loads and runs all test scenarios from test.feature.
QA engineers should edit the .feature file to add/modify test scenarios.
"""

from pytest_bdd import scenarios

# Load all scenarios from the test feature file
scenarios('features/test.feature')
