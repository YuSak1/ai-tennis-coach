from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import os
import tqdm

dir = "Transcripts"
texts = []
for filename in tqdm.tqdm(os.listdir(dir)):
    if filename.endswith(".txt"):
        with open(os.path.join(dir, filename), "r", encoding="utf-8") as f:
            texts.append(Document(page_content=f.read()))

splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=80)
split_docs = splitter.split_documents(texts)

# Save FAISS
embedding = OpenAIEmbeddings()
db = FAISS.from_documents(split_docs, embedding)
db.save_local("faiss_index_fore")
