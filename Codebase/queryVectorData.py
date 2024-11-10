from saveVectorDataToMongo import get_vector_from_file
from langchain_mongodb import MongoDBAtlasVectorSearch
from intialize import disease_detect_index, disease_detection_collection, embeddings_model_text

def queryDiseaseDetectionImage(query_image_path):

    query_embedding = get_vector_from_file(query_image_path)

    documents = disease_detection_collection.aggregate([
    {"$vectorSearch": {
        "index": disease_detect_index,
        "path": "embedding",
        "queryVector": query_embedding,
        "numCandidates": 100,
        "limit": 5,
        }},
        {
            "$project": {
            "filename": 1,
            "data": 1,
            "embedding": 1,
            "disease": 1, 
            "score": { "$meta": "vectorSearchScore" }
            }
        }
    ])

    documents = list(documents)

    detected_images_information = {}

    for doc in documents:
        image_file = doc['filename']
        image_disease = doc['disease']
        image_score = doc['score']
        if not detected_images_information.get(image_disease):
            detected_images_information[image_disease] = []
        detected_images_information[image_disease].append([image_file, image_score])
    return detected_images_information


def queryTextData(given_query, collection_db, index_name):
    vectorStore = MongoDBAtlasVectorSearch(
        collection_db, embeddings_model_text, index_name=index_name
    )

    docs = vectorStore.max_marginal_relevance_search(given_query, K=1)
    return vectorStore,docs
