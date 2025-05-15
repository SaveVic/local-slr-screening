### Preparation
Install dependencies
```
pip install ollama pandas tqdm
```
Insert the csv file into `sources` directory.
Then change the configuration in the `config.py`
```py
NUM_GPU = None
FILENAME = 'scopus.csv'
INPUT_COLS = {'title': 'Tittle', 'abstract': 'Abstrak'}
OLLAMA_MODEL = 'phi4-mini'  # or 'mistral', 'phi3', etc.
BATCH_SIZE = 5
```