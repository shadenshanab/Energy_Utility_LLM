from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores.chroma import Chroma
import os
import shutil
import requests
import unicodedata
import re
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
CHROMA_PATH = "chroma"
DATA_PATH = "datasets"
os.makedirs(CHROMA_PATH, exist_ok=True)
os.makedirs(DATA_PATH, exist_ok=True)


def main():
    """Main function to initiate the fetching and processing of articles."""
    topics = [
        "electricity utilities", "water supply utilities", "telecommunications utilities",
        "natural gas utilities", "renewable energy utilities", "nuclear energy utilities",
        "thermal power utilities", "energy storage utilities", "energy distribution utilities",
        "energy efficiency utilities"
    ]

    for topic in topics:
        print("Downloading " + topic + " articles.")
        fetch_and_save_wikipedia_articles(topic, DATA_PATH)

    print("generating data store")
    generate_data_store()


def safe_file_name(page_title):
    """Converts a page title into a filesystem-safe name by normalizing and removing unsafe characters."""
    normalized_title = unicodedata.normalize('NFKD', page_title)
    safe_title = re.sub(r'[^\w\s-]', '_', normalized_title)
    safe_title = re.sub(r'[-\s]+', '_', safe_title).strip()
    return safe_title


def fetch_and_save_wikipedia_articles(topic, directory):
    """Fetches articles from Wikipedia for a specified topic and saves them in the specified directory."""
    session = requests.Session()
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": topic,
        "srlimit": 100
    }

    response = session.get(url=url, params=params)
    data = response.json()

    if not os.path.exists(directory):
        os.makedirs(directory)

    for i, item in enumerate(data["query"]["search"]):
        page_title = item["title"]
        page_content = get_wikipedia_page_content(page_title)
        safe_title = safe_file_name(page_title)
        file_path = os.path.join(directory, f"{safe_title}.md")
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(f"# {page_title}\n\n{page_content}")


def get_wikipedia_page_content(page_title):
    """Retrieves the full content of a Wikipedia page given its title."""
    session = requests.Session()
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "parse",
        "page": page_title,
        "format": "json",
        "prop": "text"
    }
    response = session.get(url=url, params=params)
    data = response.json()
    return data["parse"]["text"]["*"]


def generate_data_store():
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)


def load_documents():
    loader = DirectoryLoader(DATA_PATH, glob="*.md")
    documents = loader.load()
    return documents


def split_text(documents: list[Document]):
    """Splits documents into chunks for easier processing and storage."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    document = chunks[10]
    print(document.page_content)
    print(document.metadata)

    return chunks


def save_to_chroma(chunks: list[Document]):
    """Saves processed document chunks into the Chroma vector store for later retrieval."""
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    db = Chroma.from_documents(
        chunks, OpenAIEmbeddings(openai_api_key=openai_api_key), persist_directory=CHROMA_PATH
    )
    db.persist()
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")


if __name__ == "__main__":
    main()
