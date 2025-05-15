import ollama
import pandas as pd
from langchain_ollama.llms import OllamaLLM
from config import conf_models, NUM_GPU
from prompt import template


def prepare_models():
    for m in conf_models:
        try:
            ollama.show(m)
        except Exception as e:
            ollama.pull(m)
    

def get_chains():
    models = [
        OllamaLLM(model=m, temperature=0, num_gpu=NUM_GPU) 
        for m in conf_models
    ]
    chains = [(template | model) for model in models]
    for ch, m in zip(chains, conf_models):
        ch.name = m
    return chains


def get_csv_data(filename: str, title_col: str, abstract_col: str):
    df = pd.read_csv(filename)
    datas = df[[title_col, abstract_col]].to_numpy()
    return datas