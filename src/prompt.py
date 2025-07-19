from dataclasses import dataclass
import json
from langchain_core.prompts import ChatPromptTemplate

_system = """
You are expert in assisting with a systematic literature review on Privacy Aware in Electronic Health Record.
"""

_definition = """
Based on this provided title and abstract, evaluate the research paper's relevance for a 
Systematic Literature Review on privacy in Electronic Health Record (EHR) systems.
The review investigates the following research questions:
1. What are the fundamental privacy challenges in electronic health record systems?
2. What privacy requirements must be satisfied in modern electronic health records?
3. How can technology enhance privacy protection in electronic health records?
"""

_in_format = """
Given the title:
\"{title}\"
and the abstract:
\"\"\"
{abstract}
\"\"\"
"""

_out_format = """
Your response must be a single, valid JSON object. 
Do not include any text or formatting outside of the JSON structure.
The JSON object should strictly conform to the following schema:
- `is_relevant`: A boolean (`true` or `false`).
- `addressed_areas`: An array of strings. If `is_relevant` is `true`, populate this array with one or more of the following values based on the paper's focus:
  - "Privacy Challenges"
  - "Privacy Requirements"
  - "Technological Solutions"
  If `is_relevant` is `false`, this should be an empty array `[]`.
- `justification`: A string providing a concise explanation for your relevance decision.
"""


@dataclass
class RelevanceData:
    is_relevant: bool
    addressed_areas: list[str]
    justification: str

    @staticmethod
    def from_dict(data: dict):
        return RelevanceData(
            is_relevant=data.get("is_relevant", False),
            addressed_areas=data.get("addressed_areas", []),
            justification=data.get("justification", ""),
        )

    @property
    def to_dict(self):
        return {
            "is_relevant": self.is_relevant,
            "addressed_areas": self.addressed_areas,
            "justification": self.justification,
        }


class RelevancePrompt:
    key = "relevance"
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", _system),
            ("user", f"{_definition}\n{_in_format}\n{_out_format}"),
        ]
    )

    @staticmethod
    def build(title: str, abstract: str):
        return {"title": title, "abstract": abstract}

    @staticmethod
    def parser(result: str):
        raw_str = result.replace("```", "").replace("json\n", "")
        raw_json = json.loads(raw_str)
        if not isinstance(raw_json, dict):
            return None

        return RelevanceData.from_dict(raw_json)
