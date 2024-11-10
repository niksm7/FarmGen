from langchain.prompts import PromptTemplate

def getPromptForDiseaseCure():
    prompt_template = """

    Human: Use the following pieces of context to provide a concise answer to the question with a short summary in 4-5 lines and give relevant steps in 10 bullets. Understand that you are instructing a farmer about the curing of disease so be informative. If you don't know the answer, just say that you don't know, don't try to make up an answer.
    <context>
    {context}
    </context

    Question: {question}

    Assistant:"""

    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    return PROMPT

def getPromptForCropRecommendation():
    prompt_template = """

    Human: Use the following pieces of context to suggest the farmer about which crop should be grown under these conditions. Ignore the absence of other parameters and answer just with 'The recommended crop for your conditions is and the crop name'. If you don't know the answer, just say that you don't know, don't try to make up an answer.
    <context>
    {context}
    </context

    Question: {question}

    Assistant:"""

    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    return PROMPT