"""
Fetch daily SNOTEL precipitation for the same representative UCRB station already selected
for air temperature (Red Mountain Pass, 713:CO:SNTL -- see fetch_snotel_representative_temp_v_2.py),
so the notebook's SNOTEL temperature and precipitation lines come from one consistent site.

DATA SOURCE
-----------
hf_hydrodata.get_point_data(dataset='snotel', variable='precipitation', temporal_resolution='daily',
                             aggregation='sum', ...)
Confirmed via hf.get_catalog_entries(dataset='snotel') that 'precipitation'/'daily'/'sum' (mm) is a
distinct catalog entry from air_temp -- a station having good air_temp coverage does NOT guarantee
good precipitation coverage at that same station, so coverage is checked here rather than assumed.

OUTPUT (QUEST_2026/UCRB_StonyBrook_Compare/data/raw/)
--------------------------------------------------------
snotel_representative_precip_monthly_climatology_v_2.csv
    Monthly precipitation climatology (mean of each calendar month's total across the whole
    WY1981-2019 record) for the representative station, in inches, index = month (1-12).

Units: source is daily sum in mm; monthly totals summed from daily, then averaged across years
per calendar month, then converted mm -> in to match ucrb_df_monthly's precip_in convention.
"""

import pandas as pd
import hf_hydrodata as hf

SITE_ID = "713:CO:SNTL"  # Red Mountain Pass -- same station used for representative SNOTEL temp
OUT_DIR = "/home/nj1079/PhD_Research/QUEST_2026/UCRB_StonyBrook_Compare/data/raw"

WY_START = "1980-10-01"  # start of WY1981, matches the temp/SWE fetch window
WY_END = "2019-09-30"    # end of WY2019, matches this project's WY_START/WY_END


def main():
    daily = hf.get_point_data(
        dataset="snotel",
        variable="precipitation",
        temporal_resolution="daily",
        aggregation="sum",
        site_ids=[SITE_ID],
        date_start=WY_START,
        date_end=WY_END,
    )
    date_col = "date" if "date" in daily.columns else daily.columns[0]
    daily[date_col] = pd.to_datetime(daily[date_col])
    daily = daily.set_index(date_col)

    full_index = pd.date_range(WY_START, WY_END, freq="D")
    daily = daily.reindex(full_index)
    daily.index.name = "date"

    series = daily[SITE_ID] if SITE_ID in daily.columns else daily.iloc[:, 0]
    coverage_pct = series.notna().mean() * 100
    print(f"{SITE_ID} precipitation coverage: {coverage_pct:.1f}% of {len(series)} days")

    monthly_total_mm = series.resample("MS").sum(min_count=1)
    monthly_climatology_mm = monthly_total_mm.groupby(monthly_total_mm.index.month).mean()
    monthly_climatology_in = monthly_climatology_mm / 25.4

    out = monthly_climatology_in.rename("precip_in").reset_index()
    out.columns = ["month", "precip_in"]
    out["site_id"] = SITE_ID
    out["site_name"] = "Red Mountain Pass"
    out["coverage_pct"] = round(coverage_pct, 1)
    out.to_csv(f"{OUT_DIR}/snotel_representative_precip_monthly_climatology_v_2.csv", index=False)

    print(f"wrote {OUT_DIR}/snotel_representative_precip_monthly_climatology_v_2.csv (12 months)")


if __name__ == "__main__":
    main()
