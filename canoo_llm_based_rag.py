from langchain_community.document_loaders import CSVLoader
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import HuggingFaceHub
from langchain.memory import VectorStoreRetrieverMemory
from langchain.chains import LLMChain,RetrievalQA,ConversationalRetrievalChain,RetrievalQAWithSourcesChain
import os

os.environ['HUGGINGFACEHUB_API_TOKEN'] = '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'                          #Hugging Faces access token

csv_data = CSVLoader('Canoo EV.csv',source_column = 'Website Content',encoding='utf-8')         #Loading the CSV file and only using 1 column which contains all the information

csv_content = csv_data.load()

chunker = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=30)
csv_chunking = chunker.split_documents(csv_content)

embeddings = HuggingFaceEmbeddings(model_name = 'sentence-transformers/all-MiniLM-L6-v2')
vectorstore = FAISS.from_documents(csv_chunking,embeddings)

vectorstore.save_local("./lizmotors/vector_embeddings", index_name="base_and_adjacent")
vectorstore  =   FAISS.load_local("lizmotors/vector_embeddings", embeddings, index_name="base_and_adjacent")
retriever = vectorstore.as_retriever(search_type = 'mmr',search_kwargs={'k':5})
memory = VectorStoreRetrieverMemory(retriever=retriever)

model = HuggingFaceHub(repo_id = 'HuggingFaceH4/zephyr-7b-alpha',model_kwargs={'tempreature':0.5,'max_new_tokens':1500,'max_length':100})

text = """ You are an AI assistant for Canoo. You have to answer the queries asked to you by the user.
You have to answer the queries in detail.

Instructions to the assistant:
a) Explain in form pointers in detail and include only those pointers which matches the query asked by the user.
b) If you answer in points, explain the point in detail again, considering the important points from previous detailed explaination.
c) Only answer user query.DO not explain any other points asked in the query and do not use follow up questions by your own.
d) Keep your responses in form pointers.

User : {query}
Assistant :
"""

prompt = PromptTemplate(input_variables=["query"],template = text)

chain = ConversationalRetrievalChain.from_llm(llm=model,retriever = retriever)

def LLM(query):
  chat_history = []
  result = chain.invoke({"question": query,
                  "chat_history":chat_history})
  return result['answer'].split('Helpful Answer:')[-1]

list_of_questions = ["""Identify the industry in which Canoo operates, along with its size, growth rate, trends, and key players.""",
                     """Analyze Canoo's main competitors, including their market share, products or services offered, pricing strategies, and marketing efforts.""",
                     """Identify key trends in the market, including changes in consumer behavior, technological advancements, and shifts in the competitive landscape.""",
                     """Gather information on Canoo's financial performance, including its revenue, profit margins, return on investment, and expense structure."""]

for query in list_of_questions:
  response = LLM(query)
  print("User : ",query,"\nAssistant : ",response)
  print("\n\n")
