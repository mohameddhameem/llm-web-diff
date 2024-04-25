import pytest
import yaml
from unittest.mock import patch, mock_open
from main import read_config_and_process


@patch('builtins.open', new_callable=mock_open,
       read_data="websites:\n  - url: 'http://example.com'\n    subpages: ['/subpage1', '/subpage2']")
@patch('main.WebUtil.download_html_page')
def test_read_config_and_process(mock_download_html_page, mock_open):
    """
    Test the read_config_and_process function.

    This function tests the read_config_and_process function from the main module.

    Args:
        mock_download_html_page (Mock): Mock object for the download_html_page function.
        mock_open (Mock): Mock object for the built-in open function.

    Returns:
        None
    """
    # Arrange
    yaml_file = 'config.yaml'
    folder = 'html_pages'

    # Act
    read_config_and_process(yaml_file, folder)

    # Assert
    mock_download_html_page.assert_any_call('http://example.com/subpage1', folder)
    mock_download_html_page.assert_any_call('http://example.com/subpage2', folder)
