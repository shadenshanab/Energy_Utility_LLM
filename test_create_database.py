import os
import pytest
from unittest.mock import patch, mock_open
from create_database import fetch_and_save_wikipedia_articles, safe_file_name, get_wikipedia_page_content

def test_safe_file_name():
    assert safe_file_name("Test/Page Title?*") == "Test_Page_Title__"

@patch("create_database.requests.Session")
def test_get_wikipedia_page_content(mock_session):
    mock_session.return_value.get.return_value.json.return_value = {
        "parse": {
            "text": {"*": "Some content"}
        }
    }
    assert get_wikipedia_page_content("test") == "Some content"


@patch("create_database.get_wikipedia_page_content", return_value="Detailed content")
@patch("create_database.os.path.exists", return_value=False)
@patch("create_database.os.makedirs")
@patch("create_database.open", new_callable=mock_open, create=True)
@patch("create_database.requests.Session")
def test_fetch_and_save_wikipedia_articles(mock_session, mock_open_file, mock_makedirs, mock_exists, mock_get_content):
    mock_session.return_value.get.return_value.json.return_value = {
        "query": {
            "search": [
                {"title": "Test Article", "pageid": 123}
            ]
        }
    }
    expected_path = os.path.join("test_dir", "Test_Article.md")
    fetch_and_save_wikipedia_articles("test topic", "test_dir")
    mock_open_file.assert_called_with(expected_path, 'w', encoding='utf-8')