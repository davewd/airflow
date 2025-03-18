"""Tests for the dynamic_import_lib module."""
import sys
from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest

from ..dynamic_import_lib import MongoDBImporter, MongoDBModuleLoader


@pytest.fixture
def mock_mongo_client() -> Generator[MagicMock, None, None]:
    """Create a mock MongoDB client for testing.

    Returns:
        Generator yielding a mock collection object for testing MongoDB operations.
    """
    with patch('pymongo.MongoClient') as mock_client:
        mock_collection = MagicMock()
        mock_db = MagicMock()
        mock_db.__getitem__.return_value = mock_collection
        mock_client.return_value.__getitem__.return_value = mock_db
        yield mock_collection


@pytest.fixture
def module_loader(mock_mongo_client: MagicMock) -> MongoDBModuleLoader:
    """Create a MongoDBModuleLoader instance with mocked MongoDB client.

    Args:
        mock_mongo_client: Mocked MongoDB collection.

    Returns:
        Configured MongoDBModuleLoader instance.
    """
    with patch('pymongo.MongoClient'):
        loader = MongoDBModuleLoader()
        loader.collection = mock_mongo_client
        return loader


@pytest.fixture
def module_importer(module_loader: MongoDBModuleLoader) -> MongoDBImporter:
    """Create a MongoDBImporter instance with mocked loader.

    Args:
        module_loader: Mocked MongoDBModuleLoader instance.

    Returns:
        Configured MongoDBImporter instance.
    """
    importer = MongoDBImporter()
    importer.loader = module_loader
    return importer


def test_get_data_success(module_loader: MongoDBModuleLoader) -> None:
    """Test successful retrieval of module data from MongoDB."""
    expected_content = "def test_function(): return 'Hello'"
    module_loader.collection.find_one.return_value = {
        "_id": "test.module",
        "content": expected_content
    }

    result = module_loader.get_data("test.module")

    assert result == expected_content
    module_loader.collection.find_one.assert_called_once_with(
        {"_id": "test.module"},
        max_time_ms=1000
    )


def test_get_data_not_found(module_loader: MongoDBModuleLoader) -> None:
    """Test behavior when module data is not found in MongoDB."""
    module_loader.collection.find_one.return_value = None

    with pytest.raises(FileNotFoundError, match="Module test.module not found"):
        module_loader.get_data("test.module")


def test_get_sub_module_data(module_loader: MongoDBModuleLoader) -> None:
    """Test retrieval of submodule data from MongoDB."""
    mock_cursor = [
        {"_id": "jobs.market_data.ecb.fx_api"},
        {"_id": "jobs.market_data.ecb.utils"},
        {"_id": "jobs.market_data.ecb.constants"}
    ]
    module_loader.collection.find.return_value = mock_cursor

    result = module_loader.get_sub_module_data("jobs.market_data.ecb")

    assert 'fx_api' in result['content']
    assert 'utils' in result['content']
    assert 'constants' in result['content']
    module_loader.collection.find.assert_called_once()


def test_exec_module_with_code(module_loader: MongoDBModuleLoader) -> None:
    """Test execution of module code retrieved from MongoDB."""
    mock_module = MagicMock()
    mock_module.__name__ = "test.module"
    mock_module.__dict__ = {}

    test_code = "def test_func(): return 42"
    module_loader.get_data = MagicMock(return_value=test_code)

    with patch.dict(sys.modules, {}, clear=True):
        module_loader.exec_module(mock_module)

    assert "test_func" in mock_module.__dict__
    assert mock_module.__dict__["test_func"]() == 42


def test_find_spec_existing_module(module_importer: MongoDBImporter) -> None:
    """Test finding module spec for an existing module."""
    module_importer.loader.get_filename = MagicMock(return_value="test.module")

    spec = module_importer.find_spec("test.module")

    assert spec is not None
    assert spec.name == "test.module"
    assert spec.loader == module_importer.loader


def test_find_spec_nonexistent_module(module_importer: MongoDBImporter) -> None:
    """Test finding module spec for a non-existent module."""
    module_importer.loader.get_filename = MagicMock(side_effect=FileNotFoundError)

    spec = module_importer.find_spec("nonexistent.module")

    assert spec is None


def test_end_to_end_module_import(module_loader: MongoDBModuleLoader) -> None:
    """Test end-to-end module import process with MongoDB integration."""
    test_module_content = """
def get_data():
    return {'key': 'value'}

def process_data(data):
    return data['key'].upper()
"""
    module_loader.collection.find_one.return_value = {
        "_id": "test.data_module",
        "content": test_module_content
    }

    importer = MongoDBImporter()
    importer.loader = module_loader
    sys.meta_path.insert(0, importer)

    try:
        import test.data_module

        data = test.data_module.get_data()
        result = test.data_module.process_data(data)

        assert result == 'VALUE'
        module_loader.collection.find_one.assert_called_with(
            {"_id": "test.data_module"},
            max_time_ms=1000
        )
    finally:
        sys.meta_path.remove(importer)
        if 'test.data_module' in sys.modules:
            del sys.modules['test.data_module']
