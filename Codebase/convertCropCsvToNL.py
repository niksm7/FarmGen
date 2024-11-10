file_location = "../KnowledgeBase/CropRecommendationKnowledge/Crop_recommendation.csv"
dest_file_location = "../KnowledgeBase/CropRecommendationKnowledge/Crop_recommendation.txt"

source_file = open(file_location, "r")
dest_file = open(dest_file_location, "w")

for line in source_file:
    data = line.split(",")
    nl_data = f"For temperature somewhere around {data[3]}°C having somewhat {data[4]}% humidity and {data[6]}mm rainfall then the recommended or suggested crop is {data[7]}"
    dest_file.write(nl_data)