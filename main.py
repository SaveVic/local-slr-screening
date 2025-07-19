from dataclasses import dataclass
import pickle
import os
from tqdm import tqdm
import pandas as pd
from src.prompt import RelevanceData, RelevancePrompt
from src.client import LLMClient, LLMUsage


@dataclass
class ResultData:
    success: bool
    raw: str
    result: RelevanceData
    usage: LLMUsage

    @staticmethod
    def from_dict(data: dict):
        return ResultData(
            success=data.get("success", False),
            raw=data.get("raw", ""),
            result=RelevanceData.from_dict(data.get("result", {})),
            usage=LLMUsage.from_dict(data.get("usage", {})),
        )

    @property
    def to_dict(self):
        return {
            "success": self.success,
            "raw": self.raw,
            "result": self.result.to_dict,
            "usage": self.usage.to_dict,
        }


def process(dir: str, model_idx: int, idx: int, title: str, abstract: str):
    values = RelevancePrompt.build(title=title, abstract=abstract)
    results = client.run(values, "api", [model_idx])[model_idx]
    parsed_result = RelevancePrompt.parser(results.content)
    usage = results.usage
    data = ResultData(
        success=(parsed_result is not None),
        raw=results.content,
        result=(parsed_result or RelevanceData.from_dict({})),
        usage=usage,
    )
    filename = f"res-{idx}.pkl"
    filepath = os.path.join(dir, filename)
    with open(filepath, "wb") as f:
        pickle.dump(data.to_dict, f)


if __name__ == "__main__":
    # Prepare
    client = LLMClient()
    client.inject_prompt(key=RelevancePrompt.key, prompt=RelevancePrompt.prompt)

    # Data
    df = pd.read_csv("fix_merged.csv")
    cols = ["Title", "Abstract"]
    values = df[cols].values

    # Checkpoint
    res_dir = "results/kimi"
    os.makedirs(res_dir, exist_ok=True)
    num_done = len(os.listdir(res_dir))

    # Process
    model_idx = 0
    model_name = client.api_names[model_idx]
    print(f"Starting with {model_name}...")
    for i, (title, abstract) in tqdm(enumerate(values[num_done:])):
        process(res_dir, model_idx, i, title, abstract)
