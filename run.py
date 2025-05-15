import os
from tqdm import tqdm
from preparation import prepare_models, get_chains, get_csv_data
from config import conf_sources


def extract_info(chain, title, abstract):
    result = chain.invoke({"title": title, "abstract": abstract })
    return result

in_dir = 'sources'
out_dir = 'outputs'

if __name__ == '__main__':
    prepare_models()
    chains = get_chains()
    for source in conf_sources:
        filename = source['filename']
        source_name = filename.split('.')[0]
        filepath = os.path.join(in_dir, filename)
        datas = get_csv_data(filepath, source['title_col'], source['abstract_col'])

        print(f'Extracting {source_name}')
        for chain in chains:
            model_name = chain.name
            raw_out_dir = os.path.join(out_dir, source_name, model_name)
            os.makedirs(raw_out_dir, exist_ok=True)

            print(f'Using {model_name}')
            start = len(os.listdir(raw_out_dir))
            chunk = datas[start:]
            progress = tqdm(enumerate(chunk), total=len(chunk), desc='Extracting')

            for i, [title, abstract] in progress:
                result = extract_info(chain, title, abstract)
                fn = os.path.join(raw_out_dir, f'{start+i}.txt')
                with open(fn, 'w', encoding='utf-8') as f:
                    f.write(result)