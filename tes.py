from src.prompt import RelevancePrompt
from src.client import LLMClient

# from src.setting import Settings
title = "Artificial intelligence in dentistry: insights and expectations from Swiss dental professionals"
abstract = """
Background: The goal of this study was to explore Swiss dentists' opinions on artificial intelligence (AI) and illustrate possible correlations to sex, age or professional background. Methods: An online questionnaire was designed and sent to 1121 Swiss dentists by e-mail. It included questions about current feelings, hopes and worries regarding the future of AI in dentistry and enquired habitual and professional use of AI tools. Results: After initial screening, 114 returned questionnaires were included in the final analysis of gathered data. This study revealed that 21.9% of respondents reported using AI in dentistry at least once a week. No significant differences were found between male and female participants regarding their perceptions of AI safety and utility (p = 0.823); however, a significant negative correlation was found between participants' age and their belief in AI's utility (p = 0.049). The belief that AI might replace jobs in the future correlated with lower perceived AI utility. Conclusions: The findings provide insight into AI's role in Swiss dentistry, highlighting areas for future research. Greater emphasis on digital medicine and AI in dental education is encouraged to advance the field and enhance oral health-related quality of life. © The Author(s) 2025.
"""

if __name__ == "__main__":
    client = LLMClient()
    client.inject_prompt(key=RelevancePrompt.key, prompt=RelevancePrompt.prompt)

    values = RelevancePrompt.build(title=title, abstract=abstract)
    results = client.run(values, "api", [1])
    print(results[1].usage)

    parsed_result = RelevancePrompt.parser(results[1].content)
    print(f"Relevance: {parsed_result.is_relevant}")
    print(f"Areas: {parsed_result.addressed_areas}")
    print(f"Reason: {parsed_result.justification}")
