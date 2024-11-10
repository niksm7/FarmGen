from saveVectorDataToMongo import data_ingestion_text, data_ingestion_image
from queryVectorData import queryDiseaseDetectionImage,queryTextData
from getLLMResponse import getBedrockResponse,getBedrockResponseQA
from intialize import *
from promptsCollection import *
import os
import time

knowledge_base_dir = "../KnowledgeBase"
disease_detection_image_dir = "DiseaseDetectionImageDataset"
disease_detection_pdf_dir = "DiseaseDetectionPdfs"

## Save cure pdf vector data to mongo

# res = data_ingestion_text(knowledge_base_dir + "/DiseaseDetectionPdfs", disease_cure_collection, disease_cure_index)
# print(res)

# res = data_ingestion_text(knowledge_base_dir + "/AdditionalKnowledge", disease_cure_collection, disease_cure_index)
# print(res)

# res = data_ingestion_text(knowledge_base_dir + "/CropRecommendationKnowledge", crop_recommendation_collection, crop_recommendation_index, chunk_size=1000, chunk_overlap=30)
# print(res)

## Save disease detection vector data to mongo

# count_for_calls = 0
# for dir in os.listdir(knowledge_base_dir + "/" + disease_detection_image_dir):
#     if count_for_calls == 4:
#         count_for_calls = 0
#         print("Sleeping for 60 seconds")
#         time.sleep(60)
#         print("Sleep completed so resuming...")
#     res = data_ingestion_image(knowledge_base_dir + "/" + disease_detection_image_dir + "/" + dir, disease_detection_collection)
#     count_for_calls += 1
#     print(res + f" for {dir}")


# Query vector for image detection
# detected_information = queryDiseaseDetectionImage("./test.JPG")
# print(detected_information)

# # Query vector for disease cure
# query = "How to control tomato leaf mold?"
# vectorStore, page = queryTextData(query, disease_cure_collection, disease_cure_index)
# print("\nQuery Response:")
# print("---------------")
# print(page[0].metadata['source'],page[0].page_content)

# res = getBedrockResponse(query, vectorStore)
# print("\nAI Response:")
# print("-----------")
# print(res)

# res = getBedrockResponseQA(query, vectorStore, getPromptForDiseaseCure())
# print("\nAI Response:")
# print("-----------")
# print(res)

query = "For temperature somewhere around 35.644753°C having somewhat 36.76766% humidity and 136.777777mm rainfall suggest me crop"
vectorStore, page = queryTextData(query, crop_recommendation_collection, crop_recommendation_index)


res = getBedrockResponseQA(query, vectorStore,getPromptForCropRecommendation())
print("\nAI Response:")
print("-----------")
print(res)