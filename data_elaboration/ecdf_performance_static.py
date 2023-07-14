import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.distributions.empirical_distribution import ECDF

alt_svc = pd.read_csv("./result/static-alt_svc-5-7-0.csv").loc[:, "request_time"]
alt_svc_ecdf = ECDF(alt_svc)

no_migration = pd.read_csv("./result/static-no_migration-5-7-0.csv").loc[:, "request_time"]
no_migration_ecdf = ECDF(no_migration)

dns60 = pd.read_csv("./result/static-dns60-5-7-0.csv").loc[:, "request_time"]
dns60_ecdf = ECDF(dns60)


dns1 = pd.read_csv("./result/static-dns1-5-7-0.csv").loc[:, "request_time"]
dns1_ecdf = ECDF(dns1)

plt.plot(alt_svc_ecdf.x, alt_svc_ecdf.y, label="Alt-Svc")
plt.plot(no_migration_ecdf.x, no_migration_ecdf.y, label="No migration")
plt.plot(dns1_ecdf.x, dns1_ecdf.y, label="DNS TTL 1s")
plt.plot(dns60_ecdf.x, dns60_ecdf.y, label="DNS TTL 60s")
plt.title("Static migration")

plt.legend()
plt.savefig("./img_plot/performance-static_migration-ecdf.svg", format="svg")
plt.show()
