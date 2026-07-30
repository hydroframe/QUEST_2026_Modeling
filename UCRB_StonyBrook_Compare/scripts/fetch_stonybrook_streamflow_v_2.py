"""Stony Brook (USGS 01401000) monthly streamflow volume, acre-feet.
Source: USGS NWIS daily values service, parameter 00060 (discharge, cfs).
1 cfs-day = 1.983471 acre-feet.
Output: ../data/raw/stonybrook_streamflow_monthly_v_2.csv
"""
import pandas as pd
import requests

SITE = "01401000"
START, END = "1979-01-01", "2025-12-31"
CFS_DAY_TO_AF = 1.983471

url = (
    "https://waterservices.usgs.gov/nwis/dv/"
    f"?format=json&sites={SITE}&parameterCd=00060&statCd=00003"
    f"&startDT={START}&endDT={END}"
)
r = requests.get(url, timeout=60)
r.raise_for_status()
values = r.json()["value"]["timeSeries"][0]["values"][0]["value"]

df = pd.DataFrame(values)[["dateTime", "value"]]
df["dateTime"] = pd.to_datetime(df["dateTime"]).dt.tz_localize(None)
df["value"] = df["value"].astype(float)

monthly = (
    df.set_index("dateTime")["value"]
    .resample("MS").sum()
    .mul(CFS_DAY_TO_AF)
    .rename("flow_af")
    .reset_index()
    .rename(columns={"dateTime": "date"})
)
monthly.to_csv("../data/raw/stonybrook_streamflow_monthly_v_2.csv", index=False)
print(f"Saved {len(monthly)} monthly records.")
