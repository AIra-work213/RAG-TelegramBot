'''
Подбор наиболее релевантных фрагментов текста по запросу в векторной БД, для последующей передачи клиенту.
'''

from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from fastapi import FastAPI
from uvicorn import run
from chroma import add_to_db
import logging

logging.basicConfig(level=logging.INFO)
logging.info("Успешный импорт")

"""Часть для работы с векторной БД"""
'''
llm = HuggingFacePipeline.from_model_id(
    model_id="sberbank-ai/rugpt3large_based_on_gpt2",
    task="text-generation"
)
logging.info("Успешный импорт LLM сбера")
'''
embed_func = HuggingFaceEmbeddings(
    model_name="ai-forever/sbert_large_nlu_ru",
    model_kwargs={"device": "cpu"}
)
logging.info("Успешный импорт эмбед модели сбера")
vector_db = Chroma(
    collection_name='pages',
    persist_directory='/Chroma_db',
    embedding_function=embed_func
)

def query_db(user_query):
    user_vector = embed_func.embed_query(user_query)
    docs = vector_db.similarity_search_by_vector(user_vector, k=5)
    return [doc.page_content for doc in docs]
    
logging.info("Подготовка к запуску сервера")
"""Серверная часть"""
app = FastAPI()

@app.get("/search")
def search(query: str):
    return query_db(query)

@app.post("/add")
def add(url: str):
    return add_to_db(url)


if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8000)