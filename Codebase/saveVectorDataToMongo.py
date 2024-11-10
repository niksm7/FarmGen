from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from intialize import embeddings_model_text, bedrock
import os
import base64
import json

def data_ingestion_text(data_directory, db_collection, index_name, chunk_size=10000, chunk_overlap=1000):

    loader=PyPDFDirectoryLoader(data_directory)
    documents=loader.load()

    text_splitter=RecursiveCharacterTextSplitter(chunk_size=chunk_size,
                                                 chunk_overlap=chunk_overlap,
                                                 separators=["\n\n", "\n", r"(?<=\. )", " "],
                                                 length_function=len)
    
    docs=text_splitter.split_documents(documents)
    print(f"Adding {len(docs)} documents to the MongoDB database")
    try:
        MongoDBAtlasVectorSearch.from_documents(
            docs, embeddings_model_text, collection=db_collection, index_name=index_name
        )
    except Exception as e:
        return "Exception Occured due to: " + str(e)

    return f"Successfully added: {len(docs)} documents to MongoDB Vector database collection!"

def get_multimodal_vector(input_image_base64=None, input_text=None):
    request_body = {}
    if input_text:
        request_body["inputText"] = input_text
    if input_image_base64:
        request_body["inputImage"] = input_image_base64
    request_body["embeddingConfig"] = {"outputEmbeddingLength": 384}
    body = json.dumps(request_body)
    response = bedrock.invoke_model(
        body=body, 
        modelId="amazon.titan-embed-image-v1", 
        accept="application/json", 
        contentType="application/json"
    )
    response_body = json.loads(response.get('body').read())
    embedding = response_body.get("embedding")
    return embedding


# creates a vector from an image file path
def get_vector_from_file(file_path):
    with open(file_path, "rb") as image_file:
        input_image_base64 = base64.b64encode(image_file.read()).decode('utf8')
    vector = get_multimodal_vector(input_image_base64 = input_image_base64)
    return vector


def data_ingestion_image(data_directory, db_collection):

    image_files = []

    for dir, _, files in os.walk(data_directory):
        for f in files:
            file_path = os.path.join(dir, f)
            image_files.append(file_path)

    for image_path in image_files:

        image_details = image_path.split("/")
        image_disease = image_details[3]
        image_name = image_details[4]
        
        img_embedding = get_vector_from_file(image_path)
        
        image_document = {
            'filename': image_name,
            'embedding': img_embedding,
            'disease': image_disease
        }

        db_collection.insert_one(image_document)
        print(f"Inserted: {image_name}")

    return "All images inserted into MongoDB."