import os

source_dir = 'sources'
output_dir = 'outputs'

INPUT_CSV = os.path.join(source_dir, 'scopus.csv')
INPUT_COLS = {'title': 'Tittle', 'abstract': 'Abstrak'}

NUM_GPU = None
OLLAMA_MODEL = 'phi4-mini'  # or 'mistral', 'phi3', etc.
OUTPUT_DATA = os.path.join(output_dir, f'result_scopus_{OLLAMA_MODEL}.pkl')
BATCH_SIZE = 5