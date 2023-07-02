import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.distributions.empirical_distribution import ECDF

alt_svc = pd.read_csv("./result/dynamic-alt_svc-long_run.csv").loc[:, "request_time"]
alt_svc_ecdf = ECDF(alt_svc)

no_migration = pd.read_csv("./result/dynamic-no_migration-long_run.csv").loc[:, "request_time"]
no_migration_ecdf = ECDF(no_migration)

plt.plot(alt_svc_ecdf.x, alt_svc_ecdf.y, label="Alt-Svc")
plt.plot(no_migration_ecdf.x, no_migration_ecdf.y, label="No migration")

plt.legend()
plt.savefig("test.svg", format="svg")
plt.show()
