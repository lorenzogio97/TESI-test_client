import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

number = pd.read_csv("./result_validation/validation-login_request_logout.csv").loc[:, "n"]

response_time = pd.read_csv("./result_validation/validation-login_request_logout.csv").loc[:, "request_time"]

plt.scatter(number, response_time)
plt.title("Login-Request-Logout")

plt.xlabel("Request number")
plt.ylabel("Response time")

plt.xticks(number)

plt.savefig("./img_plot/validation-login_request_logout.svg", format="svg")
plt.show()
