import time
import numpy as np
import pandas as pd
from prompt import screen_paper


def load_papers(file_path: str, title_col: str, abstract_col: str):
    """Load papers from CSV file"""
    df = pd.read_csv(file_path)
    return df[[title_col, abstract_col]].to_numpy()

def process_batch(papers_batch: np.ndarray, output_data: list[int]):
    """Screen all papers with progress tracking"""
    results = []
    for title, abstract in papers_batch:
        decision, out = screen_paper(title, abstract)
        results.append((decision, out))
        time.sleep(0.5)  # Rate limiting to avoid overwhelming Ollama
        
    return results