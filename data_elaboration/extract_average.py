import pandas as pd
for run in range(2):
    values = pd.read_csv("./result-preAllocated/dynamic-alt_svc-20-122-"+str(run)+".csv").loc[:, "request_time"]
    print(values.mean())
