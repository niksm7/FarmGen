from langchain.prompts import PromptTemplate

def getPromptForDiseaseCure(given_language="English"):
    human_string = f"Human: Use the following pieces of context to answer the question directly without mentioning the context. Provide concise answer to the question with a with a short summary in 4-5 lines and give relevant steps in 10 bullets. Understand that you are instructing a farmer about the curing of disease so be informative, clear, and practical. If you don't know the answer, simply respond that you don't know without any further explanation. Give the output in language {given_language}"

    prompt_template = human_string + """
    <context>
    {context}
    </context

    Question: {question}

    Assistant:"""

    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    return PROMPT