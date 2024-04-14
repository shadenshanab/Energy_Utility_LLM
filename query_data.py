import os
from dotenv import load_dotenv
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
chroma_path = "chroma"
conversation_history = ""


def fetch_response(query_text):
    """Fetches a response from the chat model based on user input and stored document data."""
    global conversation_history
    openai_api_key = os.getenv("OPENAI_API_KEY")
    chroma_path = "chroma"
    embedding_function = OpenAIEmbeddings(openai_api_key=openai_api_key)
    db = Chroma(persist_directory=chroma_path, embedding_function=embedding_function)

    # Update conversation history
    if conversation_history:
        conversation_history += "\n---\n"
    conversation_history += "User: " + query_text

    # Search the DB
    results = db.similarity_search_with_relevance_scores(query_text, k=3)
    if len(results) == 0 or results[0][1] < 0.7:
        conversation_history += "\nBot: Unable to find matching results."
        return "Unable to find matching results."

    # Format the context
    context_text = conversation_history + "\n\n---\n\n" + "\n\n---\n\n".join(
        [doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template("""
    Hello! I'm here to assist you as your Energy Utility Assistant. Users can ask me about energy utilities, and I will answer your questions based on the provided documents. Please note that my responses are based on the specific documents provided, so I will do my best to offer you the most accurate information available. If your question relates to topics not covered by these documents, I might not be able to provide a complete answer, but I'll try to help as much as I can.

    Documents:
    {context}

    ---

    Your question: {question}

    If your inquiry is a general greeting or small talk, such as 'hi' or 'how are you', feel free to ask more detailed questions about our services or information you need assistance with!
    """)

    prompt = prompt_template.format(context=context_text, question=query_text)

    # Get the response
    """ During testing, use this function to retrieve the response as it returns the source too to make sure the model is not hallucinating. 
    
    model = ChatOpenAI(openai_api_key=openai_api_key)
    response_text = model.predict(prompt)
    conversation_history += "\nBot: " + response_text
    sources = [doc.metadata.get("source", None) for doc, _score in results]
    formatted_response = f"{response_text}\n\nSources: {sources}"
    return formatted_response
    """
    model = ChatOpenAI(openai_api_key=openai_api_key)
    response_text = model.predict(prompt)
    conversation_history += response_text
    return response_text
