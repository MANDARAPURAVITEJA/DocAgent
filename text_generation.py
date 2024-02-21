from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core import ServiceContext
from llama_index.llms.openai import OpenAI
# from llama_index.llms.huggingface import HuggingFaceInferenceAPI
import os
from dotenv import load_dotenv
load_dotenv()


def create_storage_embeddings():
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    llm = OpenAI(model_name="gpt-3.5-turbo", token=os.environ["OPENAI_API_KEY"])
    docs = SimpleDirectoryReader("data").load_data()
    service_context = ServiceContext.from_defaults(llm=llm, embed_model="local",chunk_size=2048)

    index = VectorStoreIndex.from_documents(docs)

    query_engine = index.as_query_engine()

    return query_engine

def text_generator(query_engine, query):
    answer = query_engine.query(query)
    if answer:
        return answer.response.strip()

    else:
        return "Sorry I can't help you with that. Try rephrasing your question."