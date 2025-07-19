import pickle
import os
from tqdm import tqdm
from main import ResultData

resdir = "results"
in_total = 0
out_total = 0
for fn in tqdm(os.listdir(resdir)):
    fp = os.path.join(resdir, fn)
    with open(fp, "rb") as f:
        d = pickle.load(f)
        res = ResultData.from_dict(d)
        in_total += res.usage.num_token_in
        out_total += res.usage.num_token_out

print(in_total)
print(out_total)
