from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from bs4.filter import SoupStrainer


embed_func = HuggingFaceEmbeddings(
    model_name="ai-forever/sbert_large_nlu_ru",
    model_kwargs={"device": "cpu"}
)
strainer = SoupStrainer(class_=("post-title", "post-header", "post-content"))
loader = WebBaseLoader(
    web_path=("",),
    bs_kwargs={'parse_only': strainer}
)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 200,
    add_start_index = True
)
splitted_text = text_splitter.split_documents(documents=docs)

vector_db = Chroma(
    collection_name="Test",
    embedding_function=embed_func,
    persist_directory="/Chroma_db",
)
vector_db.add_documents(splitted_text)

def add_to_db(url):
    loader = WebBaseLoader(
    web_path=("",),
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
