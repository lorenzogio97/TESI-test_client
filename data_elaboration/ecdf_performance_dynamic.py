import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.distributions.empirical_distribution import ECDF

alt_svc = pd.read_csv("./result/dynamic-alt_svc-5-26-1.csv").loc[:, "request_time"]
alt_svc_ecdf = ECDF(alt_svc)

no_migration = pd.read_csv("./result/dynamic-no_migration-5-26-0.csv").loc[:, "request_time"]
no_migration_ecdf = ECDF(no_migration)

dns60 = pd.read_csv("./result/dynamic-dns60-5-26-0.csv").loc[:, "request_time"]
dns60_ecdf = ECDF(dns60)

dns40 = pd.read_csv("./result/dynamic-dns40-5-26-1.csv").loc[:, "request_time"]
dns40_ecdf = ECDF(dns40)

dns20 = pd.read_csv("./result/dynamic-dns20-5-26-0.csv").loc[:, "request_time"]
dns20_ecdf = ECDF(dns20)

dns1 = pd.read_csv("./result/dynamic-dns1-5-26-0.csv").loc[:, "request_time"]
dns1_ecdf = ECDF(dns1)

plt.plot(alt_svc_ecdf.x, alt_svc_ecdf.y, label="Alt-Svc")
plt.plot(no_migration_ecdf.x, no_migration_ecdf.y, label="No migration")
plt.plot(dns1_ecdf.x, dns1_ecdf.y, label="DNS TTL 1s")
plt.plot(dns20_ecdf.x, dns20_ecdf.y, label="DNS TTL 20s")
plt.plot(dns40_ecdf.x, dns40_ecdf.y, label="DNS TTL 40s")
plt.plot(dns60_ecdf.x, dns60_ecdf.y, label="DNS TTL 60s")

plt.xlabel("Response time (ms)")
plt.ylabel("Probability")

plt.legend()
plt.savefig("./img_plot/performance-dynamic_migration-ecdf-26rtt-5migfreq.svg", format="svg")
plt.show()
