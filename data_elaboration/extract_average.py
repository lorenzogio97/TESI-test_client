import pandas as pd

values = pd.read_csv("./result/static-no_migration-5-7-1.csv").loc[:, "request_time"]

print(values.mean())
