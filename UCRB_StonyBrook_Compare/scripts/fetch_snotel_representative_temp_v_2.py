"""
Fetch daily SNOTEL air temperature for the same long-record UCRB station roster used
for the Lees Ferry SWE work, and pick one representative high-elevation station to show
alongside the NCEI basin-average temperature in the UCRB/Stony Brook comparison notebook.

DATA SOURCE
-----------
hf_hydrodata.get_point_data(dataset='snotel', variable='air_temp', temporal_resolution='daily',
                             aggregation='mean', ...)
SNOTEL air_temp is a separate variable from swe/soil_moisture in the catalog (confirmed via
hf.get_catalog_entries(dataset='snotel')), so a station having a long SWE record does NOT
guarantee a long air_temp record at that same station -- verified below rather than assumed.

STATION SELECTION
------------------
Reuses the 54-station roster already built for the Lees Ferry SWE work:
QUEST_2026/data/raw/SNOTEL_SWE/snotel_swe_station_roster_v_2.csv (HUC4 1401-1408, period of
record spanning <=1981-01-01 through >=2020-01-01, based on SWE data availability).
Fetches daily air_temp for all 54 for WY1981-2019, computes % non-NaN coverage per station,
and picks the single station with the highest coverage as "representative."

OUTPUTS (QUEST_2026/UCRB_StonyBrook_Compare/data/raw/)
--------------------------------------------------------
snotel_temp_candidates_daily_v_2.csv
    Daily air_temp (deg C) for all 54 candidate stations, WY1981-10-01 through WY2019-09-30,
    one column per site_id, index = date. Kept for provenance/QA, not used directly by the
    notebook.
snotel_representative_temp_monthly_climatology_v_2.csv
    Full Jan-Dec monthly climatology (mean by calendar month across the whole record) for the
    selected representative station only, in deg F, index = month (1-12). This is what the
    notebook plots.

Units: source is deg C (confirmed via catalog 'units': 'c'); climatology output converted to
deg F to match the existing ucrb_df_monthly/stonybrook_df_monthly convention in the notebook.
"""

import pandas as pd
import hf_hydrodata as hf

ROSTER_PATH = "/home/nj1079/PhD_Research/QUEST_2026/data/raw/SNOTEL_SWE/snotel_swe_station_roster_v_2.csv"
OUT_DIR = "/home/nj1079/PhD_Research/QUEST_2026/UCRB_StonyBrook_Compare/data/raw"

WY_START = "1980-10-01"  # start of WY1981, matches the SWE fetch window
WY_END = "2019-09-30"    # end of WY2019, matches this project's WY_START/WY_END


def fetch_daily_air_temp(site_ids):
    df = hf.get_point_data(
        dataset="snotel",
        variable="air_temp",
        temporal_resolution="daily",
        aggregation="mean",
        site_ids=list(site_ids),
        date_start=WY_START,
        date_end=WY_END,
    )
    return df


def main():
    roster = pd.read_csv(ROSTER_PATH)
    site_ids = roster["site_id"].tolist()
    print(f"querying air_temp for {len(site_ids)} candidate stations")

    daily = fetch_daily_air_temp(site_ids)
    date_col = "date" if "date" in daily.columns else daily.columns[0]
    daily[date_col] = pd.to_datetime(daily[date_col])
    daily = daily.set_index(date_col)

    full_index = pd.date_range(WY_START, WY_END, freq="D")
    daily = daily.reindex(full_index)
    daily.index.name = "date"

    present_sites = [s for s in site_ids if s in daily.columns]
    missing_sites = [s for s in site_ids if s not in daily.columns]
    for s in missing_sites:
        daily[s] = float("nan")
    daily = daily[site_ids]

    print(f"{len(present_sites)}/{len(site_ids)} stations returned any air_temp data")
    daily.to_csv(f"{OUT_DIR}/snotel_temp_candidates_daily_v_2.csv")

    coverage = daily.notna().mean().sort_values(ascending=False)
    print("top 5 stations by air_temp coverage:")
    print(coverage.head(5))

    best_site = coverage.index[0]
    best_coverage_pct = coverage.iloc[0] * 100
    site_meta = roster.set_index("site_id").loc[best_site]
    print(f"selected representative station: {best_site} ({site_meta['site_name']}), "
          f"{best_coverage_pct:.1f}% coverage, elevation {site_meta['usda_elevation']} ft, "
          f"HUC4 {site_meta['huc4']}")

    best_series = daily[best_site].dropna()
    monthly_climatology_c = best_series.groupby(best_series.index.month).mean()
    monthly_climatology_f = monthly_climatology_c * 9 / 5 + 32

    out = monthly_climatology_f.rename("air_temp_F").reset_index()
    out.columns = ["month", "air_temp_F"]
    out["site_id"] = best_site
    out["site_name"] = site_meta["site_name"]
    out["coverage_pct"] = round(best_coverage_pct, 1)
    out.to_csv(f"{OUT_DIR}/snotel_representative_temp_monthly_climatology_v_2.csv", index=False)

    print(f"wrote:")
    print(f"  {OUT_DIR}/snotel_temp_candidates_daily_v_2.csv "
          f"({daily.shape[0]} days x {daily.shape[1]} sites)")
    print(f"  {OUT_DIR}/snotel_representative_temp_monthly_climatology_v_2.csv (12 months)")


if __name__ == "__main__":
    main()
