import pickle
import os
from tqdm import tqdm
from main import ResultData

resdir = "results/kimi"
in_total = 0
out_total = 0
num_failed = 0
rel = 0
irrel = 0
empty = 0
for fn in tqdm(os.listdir(resdir)):
    fp = os.path.join(resdir, fn)
    with open(fp, "rb") as f:
        d = pickle.load(f)
        res = ResultData.from_dict(d)
        in_total += res.usage.num_token_in
        out_total += res.usage.num_token_out
        if not res.success:
            num_failed += 1
        if res.result.is_relevant:
            rel += 1
        else:
            irrel += 1
        if len(res.result.justification.strip()) == 0:
            empty += 1

print(f"REL={rel}, IRREL={irrel}")
print(empty)
