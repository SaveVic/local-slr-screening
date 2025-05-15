import pickle
from config import OUTPUT_DATA


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
    with open(OUTPUT_DATA, 'rb') as f:
        data = pickle.load(f)

    cleaned_data = []
    for row in data:
        r = clean_1(row)
        cleaned_data.append(r)
    
    with open(OUTPUT_DATA, 'wb') as f:
        pickle.dump(cleaned_data, f)
    print('Done cleaning')

if __name__ == "__main__":
    main()