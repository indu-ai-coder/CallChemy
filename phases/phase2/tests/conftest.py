"""Pytest configuration for Phase 2 tests"""
import pytest

def pytest_configure(config):
    """Register custom marks"""
    config.addinivalue_line(
        "markers",
        "performance: mark test as a performance test"
    )
