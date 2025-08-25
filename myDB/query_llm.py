'''
Подбор наиболее релевантных фрагментов текста по запросу в векторной БД, для последующей передачи клиенту.
'''
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from fastapi import FastAPI
from uvicorn import run
from chroma import add_to_db
import logging
from langchain_huggingface import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain_core.prompts import ChatPromptTemplate
logging.basicConfig(level=logging.INFO)


template = """
Ты чат-бот отвечающий на вопросы пользователя на основе переданного тебе контекста, твоя задача отвечать четко и понятно.
Если ответ отсутствует в переданном контексте, скажи что не способен ответить на вопрос. Не выдумывай.
Контекст: {context}
Вопрос: {question}
"""
prompt = ChatPromptTemplate.from_template(template=template)

tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B")
model = AutoModelForCausalLM.from_pretrained("deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B")

pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=256
)

llm = HuggingFacePipeline(pipeline=pipe)

logging.info("Успешный импорт llm")


"""Часть для работы с векторной БД"""
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

chain = prompt | llm
def query_db(user_query):
    docs = vector_db.similarity_search(user_query, k=3)
    answer = "\n".join([doc.page_content for doc in docs])
    return answer
    
    
"""Серверная часть"""
logging.info("Подготовка к запуску сервера")
app = FastAPI()

@app.get("/search")
def search(query: str):
    response = query_db(query)
    return chain.invoke({"question": query, "context": response})
@app.post("/add")
def add(url: str):
    return add_to_db(url)


if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8000)