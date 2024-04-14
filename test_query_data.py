import pytest
from unittest.mock import patch, Mock
from query_data import fetch_response


@pytest.fixture
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "testkey123")


@pytest.fixture
def mock_chroma(monkeypatch):
    mock_chroma = Mock()
    monkeypatch.setattr("query_data.Chroma", Mock(return_value=mock_chroma))
    return mock_chroma


@pytest.fixture
def mock_openai_embeddings(monkeypatch):
    mock_embeddings = Mock()
    monkeypatch.setattr("query_data.OpenAIEmbeddings", Mock(return_value=mock_embeddings))
    return mock_embeddings


def test_fetch_response_no_results(mock_env_vars, mock_chroma, mock_openai_embeddings):
    mock_chroma.similarity_search_with_relevance_scores.return_value = []
    response = fetch_response("test query")
    assert response == "Unable to find matching results."


def test_fetch_response_with_low_relevance(mock_env_vars, mock_chroma, mock_openai_embeddings):
    mock_chroma.similarity_search_with_relevance_scores.return_value = [(Mock(page_content="Relevant content"), 0.5)]
    response = fetch_response("test query")
    assert response == "Unable to find matching results."


def test_fetch_response_with_high_relevance(mock_env_vars, mock_chroma, mock_openai_embeddings, monkeypatch):
    mock_chroma.similarity_search_with_relevance_scores.return_value = [
        (Mock(page_content="High relevance content"), 0.8)]
    mock_model = Mock()
    mock_model.predict.return_value = "Here is your response"
    monkeypatch.setattr("query_data.ChatOpenAI", Mock(return_value=mock_model))

    response = fetch_response("test query")
    assert "Here is your response" in response

