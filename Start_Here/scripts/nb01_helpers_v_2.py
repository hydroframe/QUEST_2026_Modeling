"""
Helper functions for Notebook_1_Final.ipynb (UCRB vs Stony Brook streamflow comparison).

These are the "claude look here" cells pulled out of the notebook so the teaching
notebook shows one function call instead of the full plotting/math code. Each
function's body is the same code that used to live directly in the notebook cell
(same variable names, same logic) -- nothing here was rewritten or optimized, so it
can be read/debugged the same way the original cell was.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def water_year(date):
    return date.year if date.month < 10 else date.year + 1


# standardized-coefficient MLR: no intercept term needed since z-scoring centers
# both X and y at 0; beta values are directly comparable "beta weights"
def fit_mlr(X, y):
    X_mean, X_std = X.mean(), X.std()
    y_mean, y_std = y.mean(), y.std()

    Xz = (X - X_mean) / X_std
    yz = (y - y_mean) / y_std

    beta, *_ = np.linalg.lstsq(Xz.values, yz.values, rcond=None)
    y_pred_z = Xz.values @ beta
    r2 = np.corrcoef(y_pred_z, yz.values)[0, 1] ** 2
    y_pred = y_pred_z * y_std + y_mean

    return beta, r2, y_pred


def plot_climatology_comparison(stonybrook_df_monthly, ucrb_df_monthly, snotel_temp, snotel_precip):
    """
    PLOTTING!
    """
    TITLE_FONTSIZE = 15
    LABEL_FONTSIZE = 13
    TICK_FONTSIZE = 11

    fig = plt.figure(figsize=(11, 9))

    plt.suptitle('CLIMATOLOGY AND FLOW COMPARISON\n(Precip, Temp, Flow)\n', fontsize=TITLE_FONTSIZE)

    ###########
    ax_sb_p = plt.subplot(3, 2, 1)
    ax_sb_p.plot(stonybrook_df_monthly.index, stonybrook_df_monthly["precip_in"])
    ax_sb_p.set_title("Stony Brook: Monthly Precipitation", fontsize=TITLE_FONTSIZE)
    ax_sb_p.set_xlabel("Month", fontsize=LABEL_FONTSIZE)
    ax_sb_p.set_ylabel("Precip (in/month)", fontsize=LABEL_FONTSIZE)
    ax_sb_p.set_ylim(0.5, 6)
    ax_sb_p.tick_params(labelsize=TICK_FONTSIZE)
    ax_sb_p.grid()

    ax_ucrb_p = plt.subplot(3, 2, 2)
    ax_ucrb_p.plot(ucrb_df_monthly.index, ucrb_df_monthly["precip_in"], label="Basin avg (NCEI)")
    ax_ucrb_p.plot(
        snotel_precip.index,
        snotel_precip.values,
        linestyle="--",
        color="blue",
        label="Red Mountain Pass SNOTEL (~11,100 ft)",
    )
    ax_ucrb_p.set_title("UCRB: Monthly Precipitation", fontsize=TITLE_FONTSIZE)
    ax_ucrb_p.set_xlabel("Month", fontsize=LABEL_FONTSIZE)
    ax_ucrb_p.set_ylabel("Precip (in/month)", fontsize=LABEL_FONTSIZE)
    ax_ucrb_p.set_ylim(0.5, 6)
    ax_ucrb_p.tick_params(labelsize=TICK_FONTSIZE)
    ax_ucrb_p.legend(fontsize=9, loc="upper left")
    ax_ucrb_p.grid()
    ############

    ############
    ax_sb_t = plt.subplot(3, 2, 3)
    ax_sb_t.plot(stonybrook_df_monthly.index, stonybrook_df_monthly["temp_F"])
    ax_sb_t.set_title("Stony Brook: Monthly Temperature", fontsize=TITLE_FONTSIZE)
    ax_sb_t.set_xlabel("Month", fontsize=LABEL_FONTSIZE)
    ax_sb_t.set_ylabel("Temp (F)", fontsize=LABEL_FONTSIZE)
    ax_sb_t.set_ylim(0, 80)
    ax_sb_t.tick_params(labelsize=TICK_FONTSIZE)
    ax_sb_t.axhline(y=32, linestyle=':', label='Freezing', c='black')
    ax_sb_t.legend(fontsize=9, loc="upper left")
    ax_sb_t.grid()

    ax_ucrb_t = plt.subplot(3, 2, 4)
    ax_ucrb_t.plot(ucrb_df_monthly.index, ucrb_df_monthly["temp_F"], label="Basin avg (NCEI)")
    ax_ucrb_t.plot(
        snotel_temp.index,
        snotel_temp.values,
        linestyle="--",
        color="blue",
        label="Red Mountain Pass SNOTEL (~11,100 ft)",
    )
    ax_ucrb_t.set_title("UCRB: Monthly Temperature", fontsize=TITLE_FONTSIZE)
    ax_ucrb_t.set_xlabel("Month", fontsize=LABEL_FONTSIZE)
    ax_ucrb_t.set_ylabel("Temp (F)", fontsize=LABEL_FONTSIZE)
    ax_ucrb_t.set_ylim(0, 80)
    ax_ucrb_t.tick_params(labelsize=TICK_FONTSIZE)
    ax_ucrb_t.axhline(y=32, linestyle=':', c='black')
    ax_ucrb_t.legend(fontsize=9, loc="upper left")
    ax_ucrb_t.grid()
    ############

    ############
    ax_sb_q = plt.subplot(3, 2, 5)
    ax_sb_q.plot(stonybrook_df_monthly.index, stonybrook_df_monthly["flow_af"])
    ax_sb_q.set_title("Stony Brook: Monthly Streamflow", fontsize=TITLE_FONTSIZE)
    ax_sb_q.set_ylabel("Flow (AF/Month)", fontsize=LABEL_FONTSIZE)
    ax_sb_q.set_xlabel("Month", fontsize=LABEL_FONTSIZE)
    ax_sb_q.tick_params(labelsize=TICK_FONTSIZE)
    ax_sb_q.grid()

    ax_ucrb_q = plt.subplot(3, 2, 6)
    ax_ucrb_q.plot(ucrb_df_monthly.index, ucrb_df_monthly["flow_af"])
    ax_ucrb_q.set_title("UCRB: Monthly Streamflow", fontsize=TITLE_FONTSIZE)
    ax_ucrb_q.set_xlabel("Month", fontsize=LABEL_FONTSIZE)
    ax_ucrb_q.set_ylabel("Flow (AF/Month)", fontsize=LABEL_FONTSIZE)
    ax_ucrb_q.tick_params(labelsize=TICK_FONTSIZE)
    ax_ucrb_q.grid()
    ############

    plt.tight_layout()
    plt.show()


def plot_precip_temp_vs_flow(stonybrook_df, ucrb_df):
    TITLE_FONTSIZE = 14
    LABEL_FONTSIZE = 13
    TICK_FONTSIZE = 11

    fig = plt.figure(figsize=(11, 9))

    ############
    x = stonybrook_df["precip_in"]
    y = stonybrook_df["flow_af"]
    slope_sb_p, intercept_sb_p = np.polyfit(x, y, 1)
    r_sb_p = np.corrcoef(x, y)[0, 1]
    r2_sb_p = r_sb_p ** 2

    ax_sb_p = plt.subplot(2, 2, 1)
    ax_sb_p.scatter(x, y, s=10)
    ax_sb_p.plot(x, slope_sb_p * x + intercept_sb_p, color="red")
    ax_sb_p.set_title("Stony Brook: Monthly Precipitation vs Flow", fontsize=TITLE_FONTSIZE)
    ax_sb_p.set_xlabel("Precip (in)", fontsize=LABEL_FONTSIZE)
    ax_sb_p.set_ylabel("Flow (AF)", fontsize=LABEL_FONTSIZE)
    ax_sb_p.tick_params(labelsize=TICK_FONTSIZE)
    ax_sb_p.text(
        0.05, 0.95, f"R² = {r2_sb_p:.2f}\nR = {r_sb_p:.2f}",
        transform=ax_sb_p.transAxes, fontsize=12, va="top",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
    )
    ax_sb_p.grid()
    ############

    ############
    x = ucrb_df["precip_in"]
    y = ucrb_df["flow_af"]
    slope_ucrb_p, intercept_ucrb_p = np.polyfit(x, y, 1)
    r_ucrb_p = np.corrcoef(x, y)[0, 1]
    r2_ucrb_p = r_ucrb_p ** 2

    ax_ucrb_p = plt.subplot(2, 2, 2)
    ax_ucrb_p.scatter(x, y, s=10)
    ax_ucrb_p.plot(x, slope_ucrb_p * x + intercept_ucrb_p, color="red")
    ax_ucrb_p.set_title("UCRB: Monthly Precipitation vs Flow", fontsize=TITLE_FONTSIZE)
    ax_ucrb_p.set_xlabel("Precip (in)", fontsize=LABEL_FONTSIZE)
    ax_ucrb_p.set_ylabel("Flow (AF)", fontsize=LABEL_FONTSIZE)
    ax_ucrb_p.tick_params(labelsize=TICK_FONTSIZE)
    ax_ucrb_p.text(
        0.05, 0.95, f"R² = {r2_ucrb_p:.2f}\nR = {r_ucrb_p:.2f}",
        transform=ax_ucrb_p.transAxes, fontsize=12, va="top",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
    )
    ax_ucrb_p.grid()
    ############

    ############
    x = stonybrook_df["temp_F"]
    y = stonybrook_df["flow_af"]
    slope_sb_t, intercept_sb_t = np.polyfit(x, y, 1)
    r_sb_t = np.corrcoef(x, y)[0, 1]
    r2_sb_t = r_sb_t ** 2

    ax_sb_t = plt.subplot(2, 2, 3)
    ax_sb_t.scatter(x, y, s=10)
    ax_sb_t.plot(x, slope_sb_t * x + intercept_sb_t, color="red")
    ax_sb_t.set_title("Stony Brook: Monthly Temperature vs Flow", fontsize=TITLE_FONTSIZE)
    ax_sb_t.set_xlabel("Temp (F)", fontsize=LABEL_FONTSIZE)
    ax_sb_t.set_ylabel("Flow (AF)", fontsize=LABEL_FONTSIZE)
    ax_sb_t.tick_params(labelsize=TICK_FONTSIZE)
    ax_sb_t.text(
        0.05, 0.95, f"R² = {r2_sb_t:.2f}\nR = {r_sb_t:.2f}",
        transform=ax_sb_t.transAxes, fontsize=12, va="top",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
    )
    ax_sb_t.grid()
    ############

    ############
    x = ucrb_df["temp_F"]
    y = ucrb_df["flow_af"]
    slope_ucrb_t, intercept_ucrb_t = np.polyfit(x, y, 1)
    r_ucrb_t = np.corrcoef(x, y)[0, 1]
    r2_ucrb_t = r_ucrb_t ** 2

    ax_ucrb_t = plt.subplot(2, 2, 4)
    ax_ucrb_t.scatter(x, y, s=10)
    ax_ucrb_t.plot(x, slope_ucrb_t * x + intercept_ucrb_t, color="red")
    ax_ucrb_t.set_title("UCRB: Monthly Temperature vs Flow", fontsize=TITLE_FONTSIZE)
    ax_ucrb_t.set_xlabel("Temp (F)", fontsize=LABEL_FONTSIZE)
    ax_ucrb_t.set_ylabel("Flow (AF)", fontsize=LABEL_FONTSIZE)
    ax_ucrb_t.tick_params(labelsize=TICK_FONTSIZE)
    ax_ucrb_t.text(
        0.05, 0.95, f"R² = {r2_ucrb_t:.2f}\nR = {r_ucrb_t:.2f}",
        transform=ax_ucrb_t.transAxes, fontsize=12, va="top",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
    )
    ax_ucrb_t.grid()
    ############

    plt.tight_layout()
    plt.show()


def run_mlr_activity(stonybrook_df, use_p, use_t, use_sm, p_lags, t_lags, sm_lags):
    """
    Build the lagged monthly design matrix from the notebook's toggles, fit the MLR,
    and return everything plot_mlr_results() needs.
    """
    features = {}
    if use_p:
        for lag in p_lags:
            features[f"P_lag{lag}"] = stonybrook_df["precip_in"].shift(lag)
    if use_t:
        for lag in t_lags:
            features[f"T_lag{lag}"] = stonybrook_df["temp_F"].shift(lag)
    if use_sm:
        for lag in sm_lags:
            features[f"SM_lag{lag}"] = stonybrook_df["sm_anom_in"].shift(lag)

    X_full = pd.DataFrame(features)
    y_full = stonybrook_df["flow_af"]

    activity_data = pd.concat([X_full, y_full], axis=1).dropna()
    X = activity_data[X_full.columns]
    y = activity_data["flow_af"]

    beta, r2_activity, y_pred = fit_mlr(X, y)

    return X, y, activity_data, beta, r2_activity, y_pred


def _describe_predictors(columns):
    """
    Turn design-matrix column names like "P_lag0", "T_lag1" into readable labels,
    e.g. "Precipitation (P)" or "Temperature (T) (+ lag 1, 2)".
    """
    predictor_names = {"P": "Precipitation (P)", "T": "Temperature (T)", "SM": "Soil Moisture (SM)"}

    lags_by_predictor = {}
    for col in columns:
        prefix, lag_str = col.rsplit("_lag", 1)
        lags_by_predictor.setdefault(prefix, []).append(int(lag_str))

    labels = []
    for prefix, lags in lags_by_predictor.items():
        label = predictor_names.get(prefix, prefix)
        extra_lags = sorted(lag for lag in lags if lag > 0)
        if extra_lags:
            label += " (+ lag " + ", ".join(str(lag) for lag in extra_lags) + ")"
        labels.append(label)

    return labels


def plot_mlr_results(X, activity_data, y, y_pred, r2_activity):
    fig = plt.figure(figsize=(16, 11))
    gs = fig.add_gridspec(2, 2, height_ratios=[1, 1], hspace=0.4, wspace=0.3)

    ax_scatter = fig.add_subplot(gs[0, 0])
    ax_text = fig.add_subplot(gs[0, 1])
    ax_ts = fig.add_subplot(gs[1, :])

    ax_scatter.scatter(y_pred, y, s=12)
    lims = [min(y.min(), y_pred.min()), max(y.max(), y_pred.max())]
    ax_scatter.plot(lims, lims, color="red", linestyle="--", label='1:1 line')
    ax_scatter.set_ylabel("Actual Flow (AF)", fontsize=13)
    ax_scatter.set_xlabel("Predicted Flow (AF)", fontsize=13)
    ax_scatter.set_title("Predicted vs Actual", fontsize=14)
    ax_scatter.tick_params(labelsize=11)
    ax_scatter.text(
        0.05, 0.95, f"R² = {r2_activity:.2f}",
        transform=ax_scatter.transAxes, fontsize=12, va="top",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
    )
    ax_scatter.grid()
    ax_scatter.set_ylim(0, 28000)
    ax_scatter.set_xlim(0, 28000)
    ax_scatter.legend(loc='lower right')
    ax_scatter.set_box_aspect(1)

    predictor_labels = _describe_predictors(X.columns)
    predictor_text = "Predictors used:\n\n" + "\n".join(f"• {label}" for label in predictor_labels)
    ax_text.text(0.05, 0.95, predictor_text, transform=ax_text.transAxes, fontsize=13, va="top", ha="left")
    ax_text.axis("off")

    ax_ts.plot(activity_data.index, y, label="Actual", marker="o", markersize=3)
    ax_ts.plot(activity_data.index, y_pred, label="Predicted", marker="o", markersize=3)
    ax_ts.set_title("Actual vs Predicted Monthly Flow", fontsize=14)
    ax_ts.set_ylabel("Flow (AF)", fontsize=13)
    ax_ts.legend(fontsize=10)
    ax_ts.tick_params(labelsize=11)
    ax_ts.grid()

    plt.tight_layout()
    plt.show()
