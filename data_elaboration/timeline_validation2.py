import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

dataframe = pd.read_csv("./result_validation/validation-login_request_migrate_request_logout.csv")

number = dataframe.loc[:, "n"]

response_time = dataframe.loc[:, "request_time"]
edge = dataframe.loc[:, "edge"]
edge_color = []
for item in edge:
    if item == "edge1":
        edge_color.append("green")
    if item == "edge2":
        edge_color.append("blue")
    if item == "edge3":
        edge_color.append("orange")

plt.figure(figsize=(8.4, 4.8))
plt.scatter(number, response_time, c=edge_color)
plt.title("Login-Request-Migrate-Request-Logout")

plt.xlabel("Request number")
plt.ylabel("Response time (ms)")

plt.xticks(number)
# only one line may be specified; full height
plt.axvline(x=9.1, color='red', label='Migration request')
plt.axvline(x=10.1, color='blue', label='Alt-Svc learned')

plt.legend()
plt.savefig("./img_plot/validation-login_request_migrate_request_logout.svg", format="svg")
plt.show()
