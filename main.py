from tqdm import tqdm
import os
import pickle
from config import BATCH_SIZE, INPUT_COLS, INPUT_CSV, OUTPUT_DATA
from utils import load_papers, process_batch

def main():
    # Load papers
    title_col = INPUT_COLS['title']
    abs_col = INPUT_COLS['abstract']
    all_papers = load_papers(INPUT_CSV, title_col, abs_col)
    print(f"Loaded {len(all_papers)} papers for screening")
    
    # Initialize output and check for existing progress
    output_data: list = []
    if os.path.exists(OUTPUT_DATA):
        with open(OUTPUT_DATA, 'rb') as f:
            output_data = pickle.load(f)
    else:
        with open(OUTPUT_DATA, 'wb') as f:
            pickle.dump(output_data, f)
    
    # Determine which papers need processing
    processed_papers_num = len(output_data)
    papers_to_process = all_papers[processed_papers_num:]

    # Counter
    counter = [0, 0, 0]
    for v,_ in output_data:
        counter[v+1] += 1
    
    n = len(papers_to_process)
    if n == 0:
        print("All papers have already been processed.")
        return
    
    print(f"Found {n} papers remaining to screen")
    
    # Process in batches
    progress = tqdm(range(0, n, BATCH_SIZE), desc="Screening papers")
    progress.set_postfix({
        'REL': counter[2],
        'IRR': counter[1],
        'ERR': counter[0],
    })
    for i in progress:
        batch = papers_to_process[i:min(i+BATCH_SIZE, n)]
        result = process_batch(batch, output_data)

        output_data.extend(result)
        with open(OUTPUT_DATA, 'wb') as f:
            pickle.dump(output_data, f)
        
        for v,_ in result:
            counter[v+1] += 1
        progress.set_postfix({
            'REL': counter[2],
            'IRR': counter[1],
            'ERR': counter[0],
        })
    

if __name__ == "__main__":
    main()