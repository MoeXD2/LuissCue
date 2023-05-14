from langchain.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI


def process_user_query(query, text_file): 
   try:
      loader = TextLoader(text_file)
      data = loader.load()
   except UnicodeDecodeError:
      loader = PyPDFLoader(text_file)
      data = loader.load()

   # splitting the document into chunks
   text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 0)
   texts = text_splitter.split_documents(data)

   # Creating embeddings of the documents
   embeddings = OpenAIEmbeddings(openai_api_key = "YOUR_KEY")
   model = OpenAI(model_name = "gpt-3.5-turbo", openai_api_key = "YOUR_KEY")
   # starting chroma
   docsearch = Chroma.from_texts([t.page_content for t in texts], embeddings)

   # querying the docs
   qa = RetrievalQA.from_chain_type(llm = model, chain_type = "stuff", 
                                       retriever = docsearch.as_retriever(search_kwargs = {"k": 5}))

   return qa.run(query)


if __name__ == '__main__':
   pass