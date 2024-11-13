import json
import numpy as np
import boto3
import requests
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.tools import Tool
from farmapp.intialize import *
from random import randint
from langchain.agents import initialize_agent
from farmapp.queryVectorData import queryTextData

location_coordinates = ""

def get_coordinates(*args, **kwargs):
    return location_coordinates

def get_climate_details(*args, **kwargs):
    coordinates = get_coordinates()
    lat,long = coordinates.split(" ")
    weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={long}&appid=2e8e57b6aadeffe86777fa7c2a261216")
    weather_data = weather_data.json()
    temperature = weather_data.get("main").get("temp") - 273.15
    humidity = weather_data.get("main").get("humidity")
    rainfall = weather_data.get("rain").get("1h") if weather_data.get("rain") else randint(100,200)
    return {"temperature" : temperature, "humidity": humidity, "rainfall": rainfall}

def get_crop_recommendation(*args, **kwargs):
    climate_data = get_climate_details()
    value_list = [climate_data["temperature"], climate_data["humidity"], climate_data["rainfall"]]
    payload = np.array(value_list).reshape(1,-1).astype(float).tolist()

    endpoint_name = "FarmGen-Crop-Recommendation-model"

    sm_runtime = boto3.client("runtime.sagemaker")
    response = sm_runtime.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType="application/json",
        Body=json.dumps(payload)
    )

    result = json.loads(response['Body'].read().decode())

    return f"recommended crop is {result}"

def get_best_farming_practices(*args, **kwargs):
    _, docs = queryTextData("best farming practices", farm_best_practices_collection, farm_best_practices_index)
    return docs[0].page_content

def intializeAgent():
    crop_recommendation_tool = Tool(
            name="CropRecommendation",
            func=get_crop_recommendation,
            description="Provides the recommendation for the crop to grow"
        )

    get_coordinates_tool = Tool(
        name="GetCoordinates",
        func=get_coordinates,
        description="Provides the location coordinates"
    )

    climate_details_tool = Tool(
        name="GetClimateDetails",
        func=get_climate_details,
        description="Provides the climate details based on the location coordinates"
    )

    climate_details_tool = Tool(
        name="GetBestFarmingPracices",
        func=get_best_farming_practices,
        description="Provides context for best practices to be used for farming"
    )

    tools = [crop_recommendation_tool, get_coordinates_tool, climate_details_tool]

    prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm_model, tools, prompt, stop_sequence=True)
    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        verbost=True,
        handle_parsing_errors=True
    )
    return agent_executor

def getAgentResponse(given_query, location_cords):
    global location_coordinates
    location_coordinates = location_cords
    # user_query = "Can you recommend me a crop to grow based on my climate conditions?"
    # user_query = "Can you suggest best practice to grow healthy crops?"
    agent = intializeAgent()
    response = agent.invoke({"input": given_query})
    return response.get("output")