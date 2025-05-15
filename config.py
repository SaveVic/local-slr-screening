import os

# Change this
NUM_GPU = 0
FILENAME = 'scopus.csv'
INPUT_COLS = {'title': 'Tittle', 'abstract': 'Abstrak'}
OLLAMA_MODEL = 'phi4-mini'  # or 'mistral', 'phi3', etc.
BATCH_SIZE = 5

# Fix
SOURCE_DIR = 'sources'
OUTPUT_DIR = 'outputs'
INPUT_CSV = os.path.join(SOURCE_DIR, FILENAME)
SOURCE_NAME = FILENAME.split('.')[0]
OUTPUT_DATA = os.path.join(OUTPUT_DIR, f'result_{SOURCE_NAME}_{OLLAMA_MODEL}.pkl')