import pytest

from unittest.mock import Mock
from django.core.exceptions import ValidationError

from thumbnails.validators import validate_file_size


def test_file_size_within_limit():
    mock_file = Mock(size=4 * 1024 * 1024)
    assert validate_file_size(mock_file) == mock_file


def test_file_size_exceeds_limit():
    mock_file = Mock(size=6 * 1024 * 1024)
    with pytest.raises(ValidationError):
        validate_file_size(mock_file)
