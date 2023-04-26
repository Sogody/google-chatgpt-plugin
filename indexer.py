import os
import json
import pinecone
from llama_index import (
    GPTSimpleVectorIndex,
    SimpleDirectoryReader,
    Document,
    GPTPineconeIndex
)
from dotenv import load_dotenv

def load_environment_variables():
    load_dotenv()
    return os.environ.get("PINECONE_INDEX_NAME"), os.environ.get("PINECONE_API_KEY")

PINECONE_INDEX_NAME, PINECONE_API_KEY = load_environment_variables()

def vector_index(results, query, max_tokens=4096):
    documents = []

    # for item in results:
    content = results[:max_tokens]
    document = Document(content)
    documents.append(document)

    index = GPTSimpleVectorIndex.from_documents(documents)

    # if PINECONE_INDEX_NAME != None and PINECONE_API_KEY != None:
        # pinecone.init(api_key=PINECONE_API_KEY, environment='northamerica-northeast1-gcp')
        # if not PINECONE_INDEX_NAME in pinecone.list_indexes():
        #     pinecone.create_index(index_name=PINECONE_INDEX_NAME, dimension=index.dimension, metric="cosine")

        # pinecone_index = pinecone.Index(index_name=PINECONE_INDEX_NAME)
        # Pinecone tbd
        # gpt_pinecone_index = GPTPineconeIndex(pinecone_index)

        # for doc in documents:
        #     gpt_pinecone_index.insert(doc)

    response = index.query(query, response_mode="compact")

    return response
