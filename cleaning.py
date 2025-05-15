import os
import pickle
from config import OUTPUT_DIR


def clean_1(row):
    val, out = row
    if out is None:
        return row
    res = out.split('\n')[0]
    if res == 'RELEVANT':
        val = 1
        out = None
    elif res == 'IRRELEVANT':
        val = 0
        out = None
    return (val, out)

def main():
    for fn in os.listdir(OUTPUT_DIR):
        _, source, model = fn.split('_')

        fp = os.path.join(OUTPUT_DIR, fn)
        with open(fp, 'rb') as f:
            data = pickle.load(f)

        print(f'Clean result data from {source}')
        cleaned_data = []
        cnt = [0, 0, 0]
        for row in data:
            r = clean_1(row)
            cnt[r[0]+1] += 1
            cleaned_data.append(r)
    
        with open(fp, 'wb') as f:
            pickle.dump(cleaned_data, f)
        print('Done cleaning')
        print(f'REL={cnt[2]}, IRREL={cnt[1]}, ERROR={cnt[0]}\n')

if __name__ == "__main__":
    main()