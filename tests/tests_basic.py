import logging
import pytest

logger = logging.getLogger(__name__)


def test_simple_addition():
    logger.info("Testing simple addition: 2 + 2")
    result = 2 + 2
    logger.info(f"Result: {result}")
    assert result == 4
    logger.info("✓ Addition test passed")


def test_string_operations():
    name = "boardfarm"
    logger.info(f"Testing string operations on: '{name}'")

    upper_result = name.upper()
    logger.info(f"Uppercase: {upper_result}")
    assert upper_result == "BOARDFARM"

    length = len(name)
    logger.info(f"Length: {length}")
    assert length == 9

    logger.info("✓ String operations test passed")


@pytest.fixture
def sample_data():
    """Provides test data to tests"""
    logger.info("Creating sample data fixture")
    return {"username": "admin", "password": "secret"}


def test_login(sample_data):
    # Test uses the fixture data
    logger.info(f"Testing login with username: {sample_data['username']}")
    assert sample_data["username"] == "admin"
    logger.info("✓ Login test passed")


@pytest.mark.parametrize("input,expected", [
    (3, 9),
    (4, 16),
    (5, 25)
])
def test_square(input, expected):
    logger.info(f"Testing square: {input}² = {expected}")
    result = input ** 2
    logger.info(f"Calculated: {input}² = {result}")
    assert result == expected
    logger.info(f"✓ Square test passed for {input}")


@pytest.mark.slow
def test_performance():
    # This test takes a long time
    logger.info("Running performance test (slow)")
    import time
    time.sleep(0.1)
    logger.info("✓ Performance test completed")


@pytest.mark.integration
def test_database_connection():
    # Integration test
    logger.info("Testing database connection (integration test)")
    logger.info("✓ Database connection test passed")
