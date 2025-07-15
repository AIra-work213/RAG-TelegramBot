from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_huggingface import HuggingFaceEmbeddings
from bs4.filter import SoupStrainer
import logging

logging.basicConfig(level=logging.INFO)
logging.info("Успешный импорт")

embed_func = HuggingFaceEmbeddings(
    model_name="ai-forever/sbert_large_nlu_ru",
    model_kwargs={"device": "cpu"}
)
logging.info("Успешный импорт модели сбера")
# Стрейнер для всех параграфов, заголовков и списков
strainer = SoupStrainer(['article', 'main', 'section', 'div', 'p', 'h1', 'h2', 'h3', 'li'])
loader = WebBaseLoader(
    web_path=("https://habr.com/ru/companies/tochka/articles/927386/","https://habr.com/ru/companies/onlinepatent/articles/927834/"),
    bs_kwargs={'parse_only': strainer}
)
docs = loader.load()
print(f"Загружено документов: {len(docs)}")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 200,
    add_start_index = True
)
splitted_text = text_splitter.split_documents(documents=docs)

vector_db = Chroma(
    collection_name="pages",
    embedding_function=embed_func,
    persist_directory="/Chroma_db",
)
vector_db.add_documents(splitted_text)

def add_to_db(url):
    loader = WebBaseLoader(
    web_path=(url,),
    bs_kwargs={'parse_only': strainer}
    )
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200,
        add_start_index = True
    )
    splitted_text = text_splitter.split_documents(documents=docs)
    vector_db.add_documents(splitted_text)
    return "Успешно!"
