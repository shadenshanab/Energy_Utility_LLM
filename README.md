# Energy Utility Information Bot

## Overview

This Python project aims to enhance internal development and business processes for energy utility stakeholders. It fetches and stores Wikipedia articles on various utility topics, processes the content into manageable chunks, and uses a Large Language Model (LLM) to facilitate interaction and operational processes. This project is part of an initiative to assess the impact of integrating LLM technology into energy utility operations.

## Features

- **Article Fetching**: Automatically fetch articles from Wikipedia related to predefined energy utility topics.
- **Content Processing**: Split fetched articles into chunks suitable for analysis and storage.
- **Data Storage**: Store processed chunks in a Chroma database for efficient retrieval.
- **LLM Integration**: Utilize a pre-trained OpenAI model to respond to queries, enhancing the stakeholder interaction experience.

## Requirements

- Python 3.8+
- `requests`
- `unicodedata`, `re`
- `os`, `shutil`
- `dotenv` for environment management
- `langchain` library for document loading, text splitting, embedding, and storage

## Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/shadenshanab/Energy_Utility_LLM.git
   cd Energy_Utility_LLM
   
2. **Environment Variables**:
Set up your .env file at the root of the project with the following content:
   ```makefile
   OPENAI_API_KEY=YourOpenAIApiKeyHere

3. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
   
## Running the Application
Execute the main script to start the process:

   ```bash
   python main.py
   ```
### This will:

- Fetch articles on predefined utility topics.
- Process and store these articles in a format ready for querying.
- Allow querying the system using an integrated chat interface.

## Directory Structure
- **main.py**: The main script to run the processes.
- **chroma/**: Directory where the Chroma database files will be stored.
- **datasets/**: Directory where fetched articles are stored as markdown files.
