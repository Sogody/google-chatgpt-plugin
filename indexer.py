import os
import json
from llama_index import (
    GPTSimpleVectorIndex,
    SimpleDirectoryReader,
    Document
)
from dotenv import load_dotenv

def load_environment_variables():
    load_dotenv()

def vector_index(results, query, max_tokens=4096):
    documents = []

    # for item in results:
    content = results[:max_tokens]
    document = Document(content)
    documents.append(document)

    index = GPTSimpleVectorIndex.from_documents(documents)

    response = index.query(query, response_mode="compact")

    return response
