from farmapp.intialize import llm_model
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.retrievers import ContextualCompressionRetriever
from langchain.prompts import PromptTemplate
from langchain.chains.retrieval_qa.base import RetrievalQA

def getBedrockResponse(given_query, vectorStore):
    compressor = LLMChainExtractor.from_llm(llm_model)

    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor,
        base_retriever=vectorStore.as_retriever()
    )

    print("\nAI Response:")
    print("-----------")
    try:
        compressed_docs = compression_retriever.invoke(given_query, k=1)
        print(compressed_docs)
        print("\n---------")
        for doc in compressed_docs:
            print(doc.metadata['source'])
            print(doc.page_content)
            print("\n-------")
        return compressed_docs
    except Exception as e:
        return e

def getBedrockResponseQA(given_query, vectorStore, prompt):

    qa = RetrievalQA.from_chain_type(
        llm=llm_model,
        chain_type="stuff",
        retriever=vectorStore.as_retriever(
            search_type="similarity", search_kwargs={"k": 3}
        ),
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )
    answer=qa({"query":given_query})
    return answer['result']