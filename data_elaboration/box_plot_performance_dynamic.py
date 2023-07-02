# Library Import (matplotlib)
import matplotlib.pyplot as plot
import pandas as pd

alt_svc = pd.read_csv("./result/dynamic-alt_svc-long_run.csv").loc[:, "request_time"]
no_migration = pd.read_csv("./result/dynamic-no_migration-long_run.csv").loc[:, "request_time"]
value_C = [25, 29, 19, 98, 52, 81, 21, 61, 65, 85, 12, 54, 12, 56, 36, 55, 35, 32, 22, 82]
value_D = [89, 75, 71, 19, 88, 66, 89, 99, 70, 80, 89, 78, 14, 29, 75, 86, 79, 91, 73, 90]
value_E = [90, 57, 76, 40, 18, 88, 65, 81, 58, 19, 47, 89, 32, 36, 43, 52, 18, 58, 19, 95]

box_plot_data = [alt_svc, no_migration]
plot.title("Response time in dynamic environment")
plot.boxplot(box_plot_data, patch_artist=True, whis=(20, 80), showfliers=False,
             labels=['Alt-Svc', 'No migration'])

plot.show()
