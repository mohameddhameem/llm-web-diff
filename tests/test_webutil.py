import pytest
from unittest.mock import patch, mock_open, MagicMock
from src.web.webutil import WebUtil
import os
import tempfile


# Test case for download_html_page function
@patch('src.web.webutil.requests.get')
@patch('src.web.webutil.os.path.exists', return_value=False)
@patch('src.web.webutil.BeautifulSoup')
def test_download_html_page(mock_bs, mock_exists, mock_get, monkeypatch):
    monkeypatch.setenv('TMPDIR', '/temp')  # set the TMPDIR environment variable
    os.environ['TMPDIR'] = '/temp'  # set the TMPDIR environment variable
    with tempfile.TemporaryDirectory() as tmpdirname:
        mock_exists.return_value = False
        mock_get.return_value.status_code = 200
        mock_bs.return_value.prettify.return_value = '<html></html>'
        WebUtil.download_html_page('http://example.com', tmpdirname)
        mock_get.assert_called_once_with('http://example.com')
        mock_bs.assert_called_once()


# Test case for list_form_elements function
@patch('src.web.webutil.os.path.exists')
@patch('src.web.webutil.BeautifulSoup')
@patch('src.web.webutil.json.dump')
def test_list_form_elements(mock_json_dump, mock_bs, mock_exists):
    os.environ['TMPDIR'] = '/temp'  # set the TMPDIR environment variable
    with tempfile.TemporaryDirectory() as tmpdirname:
        mock_exists.return_value = True
        mock_open_instance = mock_open(read_data='<html></html>').return_value
        with patch('src.web.webutil.open', mock_open_instance):
            mock_bs.return_value.find_all.side_effect = [[], [], []]
            WebUtil.list_form_elements(tmpdirname)
        assert mock_exists.call_count == 2
        mock_bs.assert_called_once()
        mock_json_dump.assert_called_once()
