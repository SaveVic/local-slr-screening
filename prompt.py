import ollama

from config import NUM_GPU, OLLAMA_MODEL


SCREENING_PROMPT = """
You are assisting with a systematic literature review on Large Language Models (LLMs) for Education.
Evaluate whether this paper is relevant based on its title and abstract, considering these research questions:

1. What architectural designs and model variants of LLMs are most effective for educational applications?
2. Which prompting techniques and fine-tuning methods optimize LLM performance in educational contexts?
3. What evaluation frameworks, metrics, and benchmarks are used to assess LLM efficacy in education?
4. How are domain-specific educational datasets being developed and utilized for LLM training and evaluation?
5. What technical challenges and computational constraints exist in deploying LLMs in educational environments?

Instructions:
- Respond ONLY with "RELEVANT" or "IRRELEVANT" based on whether the paper addresses any of these questions.
- Be inclusive - if the paper might be relevant to any aspect, mark it RELEVANT.
- Focus on LLM applications in education, not general educational technology.

Paper Title: {title}
Abstract: {abstract}

Decision: 
"""

def screen_paper(title: str, abstract: str):
    """Use Ollama to screen a single paper"""
    prompt = SCREENING_PROMPT.format(title=title, abstract=abstract)
    
    d = 'Error'
    try:
        response = ollama.generate(
            model=OLLAMA_MODEL,
            prompt=prompt,
            options={'temperature': 0.0, 'num_gpu': NUM_GPU}  # Minimize randomness
        )
        out = response['response'].strip().upper()
        d = out
        if out == 'RELEVANT':
            return 1, None
        elif out == 'IRRELEVANT':
            return 0, None
        else:
            return -1, out
    except Exception as e:
        # print(f"Error screening paper '{title}': {str(e)}")
        return -1, d