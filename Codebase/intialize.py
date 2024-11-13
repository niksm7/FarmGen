import os
import certifi
import boto3
from langchain_aws.embeddings import BedrockEmbeddings
from pymongo import MongoClient
from dotenv import load_dotenv
from langchain_aws import ChatBedrock

load_dotenv()

bedrock=boto3.client(service_name="bedrock-runtime")
embeddings_model_text=BedrockEmbeddings(model_id=os.getenv("BEDROCK_EMBEDDINGS_TEXT_MODEL_ID"),client=bedrock)
embeddings_model_image=BedrockEmbeddings(model_id=os.getenv("BEDROCK_EMBEDDINGS_IMAGE_MODEL_ID"),client=bedrock,)

llm_model = ChatBedrock(model_id=os.getenv("BEDROCK_LLM_MODEL_ID"),client=bedrock,
                model_kwargs={'max_tokens':1000})

client = MongoClient(os.getenv("MONGODB_CONN_STRING"), tlsCAFile=certifi.where())
disease_cure_collection = client[os.getenv("DISEASE_CURE_DB_NAME")][os.getenv("DISEASE_CURE_COLL_NAME")]
disease_detection_collection = client[os.getenv("DISEASE_DETECT_DB_NAME")][os.getenv("DISEASE_DETECT_COLL_NAME")]
farm_best_practices_collection = client[os.getenv("FARM_BEST_PRACTICES_DB_NAME")][os.getenv("FARM_BEST_PRACTICES_COLL_NAME")]

disease_cure_index = os.getenv("DISEASE_CURE_INDEX_NAME")
disease_detect_index = os.getenv("DISEASE_DETECT_INDEX_NAME")
farm_best_practices_index = os.getenv("FARM_BEST_PRACTICES_INDEX_NAME")