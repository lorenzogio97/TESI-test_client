import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.distributions.empirical_distribution import ECDF

rtt = "122"
mig_period = "5"

alt_svc = pd.read_csv("./result-onDemandAllocation/dynamic-alt_svc-" + mig_period + "-" + rtt + "-1.csv").loc[:,
          "request_time"]
alt_svc_ecdf = ECDF(alt_svc)

alt_svc_pre = pd.read_csv("./result-preAllocated/dynamic-alt_svc-" + mig_period + "-" + rtt + "-1.csv").loc[:,
              "request_time"]
alt_svc_pre_ecdf = ECDF(alt_svc_pre)

no_migration = pd.read_csv(
    "./result-onDemandAllocation/dynamic-no_migration-" + mig_period + "-" + rtt + "-1.csv").loc[:,
               "request_time"]
no_migration_ecdf = ECDF(no_migration)

dns60 = pd.read_csv(
    "./result-onDemandAllocation/dynamic-dns60-" + mig_period + "-" + rtt + "-0.csv").loc[:,
        "request_time"]
dns60_ecdf = ECDF(dns60)

dns60_pre = pd.read_csv("./result-preAllocated/dynamic-dns60-" + mig_period + "-" + rtt + "-0.csv").loc[
            :, "request_time"]
dns60_pre_ecdf = ECDF(dns60_pre)

# dns40 = pd.read_csv("./result-onDemandAllocation/dynamic-dns40-5-26-1.csv").loc[:, "request_time"]
# dns40_ecdf = ECDF(dns40)
#
# dns20 = pd.read_csv("./result-onDemandAllocation/dynamic-dns20-5-26-0.csv").loc[:, "request_time"]
# dns20_ecdf = ECDF(dns20)


dns1 = pd.read_csv("./result-onDemandAllocation/dynamic-dns1-" + mig_period + "-" + rtt + "-0.csv").loc[
       :, "request_time"]
dns1_ecdf = ECDF(dns1)

dns1_pre = pd.read_csv("./result-preAllocated/dynamic-dns1-" + mig_period + "-" + rtt + "-1.csv").loc[:,
           "request_time"]
dns1_pre_ecdf = ECDF(dns1_pre)

plt.plot(alt_svc_ecdf.x, alt_svc_ecdf.y, label="Alt-Svc")
plt.plot(alt_svc_pre_ecdf.x, alt_svc_pre_ecdf.y, label="Alt-Svc (preallocated)")
plt.plot(no_migration_ecdf.x, no_migration_ecdf.y, label="No migration")
plt.plot(dns1_ecdf.x, dns1_ecdf.y, label="DNS TTL 1s")
plt.plot(dns1_pre_ecdf.x, dns1_pre_ecdf.y, label="DNS TTL 1s (preallocated)")
# plt.plot(dns20_ecdf.x, dns20_ecdf.y, label="DNS TTL 20s")
# plt.plot(dns40_ecdf.x, dns40_ecdf.y, label="DNS TTL 40s")
plt.plot(dns60_ecdf.x, dns60_ecdf.y, label="DNS TTL 60s")
plt.plot(dns60_pre_ecdf.x, dns60_pre_ecdf.y, label="DNS TTL 60s (preallocated)")

plt.xlabel("Response time (ms)")
plt.ylabel("Probability")
# plt.title("ECDF Response time - Typical, 5m migration period")

plt.legend()
plt.savefig("./img_plot-preallocated/performance-dynamic_migration-ecdf-" + rtt + "rtt-" + mig_period + "migfreq.svg",
            format="svg")
plt.show()
