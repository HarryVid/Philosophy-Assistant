from langchain.text_splitter import MarkdownTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.vectorstores import Chroma
from pathlib import Path


def vector_embedding_database():
	if not Path("./chroma_db").is_dir():
		MD_PATH = "./data/TextBooksMD/"
		loader = DirectoryLoader(MD_PATH, glob="*.md")
		documents = loader.load()
		embedding_function = HuggingFaceEmbeddings(model_name="all-mpnet-base-v2")
		text_splitter = MarkdownTextSplitter(chunk_size=1000, chunk_overlap=100, length_function = len)
		chunks = text_splitter.split_documents(documents)
		db = Chroma.from_documents(chunks, embedding_function, persist_directory="./chroma_db")
		print("Database Created Successfully!")
	else:
		print("Database Already Exists")


vector_embedding_database()
