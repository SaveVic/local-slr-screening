from langchain_core.prompts import ChatPromptTemplate

human_instruction = """
Analyze the following academic paper to determine its relevance to the topic: Large Language Models (LLMs) in Education.  
The response contain this information:
    1. Relevance: YES/NO  
    2. Explanation: (1-2 sentences)  
    3. If relevance is YES:
        - Use Case: (How the paper applies LLMs in education, e.g., "automated essay scoring")  
        - Technical Discussion: YES/NO (Does it cover model architecture, training, or fine-tuning?)  

Please answer it using this structure:
```
relevance=False
explanation=str
```
or
```
relevance=True
explanation=str
use_cases=list[str]
tech_discussion=True/False
```

Dont add any explanation or additional text other than that format.
"""

human_input = """
Title: {title}
Abstract: {abstract}
"""

template = ChatPromptTemplate([
    ("system", "You are an expert researcher in computer science."),
    ("human", human_instruction),
    ("ai", "Sure, I can do that! Please provide the title and abstract for analysis."),
    ("human", human_input)
])