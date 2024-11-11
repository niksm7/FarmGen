from farmapp.saveVectorDataToMongo import get_vector_from_file
from langchain_mongodb import MongoDBAtlasVectorSearch
from farmapp.intialize import disease_detect_index, disease_detection_collection, embeddings_model_text

def queryDiseaseDetectionImage(query_image):

    query_embedding = get_vector_from_file(query_image)

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

    lowest_score = 0

    for doc in documents:
        image_file = doc['filename']
        image_disease = doc['disease']
        image_score = doc['score']
        print("Current Doc: ", [image_file, image_disease, image_score])
        if lowest_score == 0:
            detected_images_information[image_score] = [image_file, image_disease, image_score]
            lowest_score = image_score
        elif len(detected_images_information) < 3:
            detected_images_information[image_score] = [image_file, image_disease, image_score]
            lowest_score = image_score if image_score < lowest_score else lowest_score
        elif len(detected_images_information) == 3:
            if image_score > lowest_score:
                detected_images_information[image_score] = [image_file, image_disease, image_score]
                del detected_images_information[lowest_score]
    return detected_images_information


def queryTextData(given_query, collection_db, index_name):
    vectorStore = MongoDBAtlasVectorSearch(
        collection_db, embeddings_model_text, index_name=index_name
    )

    docs = vectorStore.max_marginal_relevance_search(given_query, K=1)
    return vectorStore,docs
