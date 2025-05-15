import json
import os
import pickle
import tqdm

raw_out_dir = os.path.join('outputs', 'raw')
parsed_out_dir = os.path.join('outputs', 'parsed')

def parse_from_txt(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
        data = {}
        for line in lines:
            tmp = line.split('\n')[0].split('=')
            k = tmp[0]
            v = '='.join(tmp[1:])
            data[k] = v
    return data

if __name__ == '__main__':
    for par, dirs, files in os.walk(raw_out_dir):
        if len(files) > 0:
            p, model_name = os.path.split(par)
            p, source_name = os.path.split(p)
            d = os.path.join(parsed_out_dir, source_name, model_name)
            os.makedirs(d, exist_ok=True)
            failed = []
            progress = tqdm.tqdm(files, total=len(files), desc='Parsing')
            for ft in progress:
                fpkl = ft.split('.')[0] + '.pkl'
                fp = os.path.join(d, fpkl)
                if os.path.exists(fp):
                    continue
                fs = os.path.join(par, ft)
                result = parse_from_txt(fs)
                if result is not None:
                    with open(fp, 'wb') as f:
                        pickle.dump(result, f)
                else:
                    failed.append(fs)
                progress.set_postfix({'failed': len(failed)})