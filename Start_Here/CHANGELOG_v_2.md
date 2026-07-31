# Start_Here — Changelog

(Renamed from `UCRB_StonyBrook_Compare/` — see entry below. Earlier entries in this
file predate the rename and refer to the old name.)

Tracking edits from 2026-07-31 onward so we can revert cleanly if needed.

## 2026-07-31: renamed UCRB_StonyBrook_Compare/ to Start_Here/

- Plain filesystem `mv` (not `git mv`) — nothing auto-staged in git.
- Updated hardcoded absolute `OUT_DIR` paths (and matching header-comment mentions) in
  `scripts/fetch_snotel_representative_temp_v_2.py` and
  `scripts/fetch_snotel_representative_precip_v_2.py` from
  `.../UCRB_StonyBrook_Compare/data/raw` to `.../Start_Here/data/raw` — these were the
  only two files with an absolute (non-relative) dependency on the old folder name.
- `Notebook_1_Final.ipynb` needed no changes (uses relative paths only).
- Re-executed `notebooks/Notebook_1_Final.ipynb` from its new location — cell count
  unchanged (25 → 25), 0 errors.
- Note: `git status` will show the moved files as separate deletions (old path) +
  untracked `Start_Here/` (new path) until both sides are `git add`ed, at which point
  git detects it as a rename automatically. No data was lost — this is expected `mv`
  behavior, not a problem. Staging/committing this is left to the user.

## 2026-07-31: widen "Actual vs Predicted Monthly Flow" panel

- **File**: `scripts/nb01_helpers_v_2.py`, function `plot_mlr_results`
- **Before**: `fig, (ax_ts, ax_scatter) = plt.subplots(1, 2, figsize=(12, 5))`
- **After**: `fig, (ax_ts, ax_scatter) = plt.subplots(1, 2, figsize=(13, 5), gridspec_kw={"width_ratios": [1.3, 1]})`
- **Why**: left panel (time series) requested to be "a little longer"; scatter panel
  (right) intentionally left at its original proportions so the 1:1 reference line
  still reads as square/undistorted.
- **Notebook re-executed**: `notebooks/Notebook_1_Final.ipynb`, via
  `jupyter nbconvert --execute --inplace` (grace_processing_new env) — 0 errors.

### Note on cell count

`Notebook_1_Final.ipynb` had 28 cells right after it was first built (verified). After
this update it has 25 — the "MISC STUFF FOR NICK" markdown header, one scratch code
cell below it, and one blank code cell are no longer present. This did not happen
through any edit made on my end (I only touched the `plot_mlr_results` figsize) — the
notebook was open in your IDE between these two sessions, so this is most likely from
your own editing/cleanup in that window. Flagging it here in case it wasn't
intentional; the 3 missing cells are still present verbatim in the untouched
`01_dataframes_prefinal.ipynb` if you want them back.

**Update**: confirmed by user 2026-07-31 — intentional cleanup on their end, not a
side effect of any edit here.

## 2026-07-31: restructured "Actual vs Predicted" figure — stacked layout, wider

- **File**: `scripts/nb01_helpers_v_2.py`, function `plot_mlr_results`
- **Before**: 1x2 side-by-side layout, `figsize=(13, 5)`, `width_ratios=[1.3, 1]`
  (scatter on the right, same height as the time series).
- **After**: 2-row stacked layout via `GridSpec(2, 3)`, `figsize=(16, 10)`. Scatter
  ("Predicted vs Actual") moved to the top row, middle column only (`gs[0, 1]`) with
  `set_box_aspect(1)` so it stays square regardless of figure width. Time series
  ("Actual vs Predicted Monthly Flow") moved to the bottom row, spanning the full
  width (`gs[1, :]`) — now ~16" wide instead of ~7.3".
- **Why**: user wanted the time series panel "even longer"/wider, and asked for the
  scatter to sit on top (square) with the line plot on the bottom.
- **Notebook re-executed**: `notebooks/Notebook_1_Final.ipynb` — cell count unchanged
  (25 → 25), 0 errors.

## 2026-07-31: scatter bigger + moved left, added predictors-used text panel

- **File**: `scripts/nb01_helpers_v_2.py`, function `plot_mlr_results`
- **Before**: `GridSpec(2, 3)`, `figsize=(16, 11→10 previously)`, scatter in `gs[0, 1]`
  (middle third of top row), bottom row = time series only.
- **After**: `GridSpec(2, 2)`, `figsize=(16, 11)`. Scatter now `gs[0, 0]` (left half of
  top row, larger since it's a half instead of a third; still square via
  `set_box_aspect(1)`). New `gs[0, 1]` panel (right half of top row) is a
  `axis("off")` text box listing which predictors were used, built from `X.columns`
  via a new small helper `_describe_predictors()` — groups columns by predictor
  prefix (`P`/`T`/`SM`) and appends `(+ lag n, ...)` only when a lag >0 was toggled
  on. Bottom row unchanged (time series, full width).
- **Signature change**: `plot_mlr_results(activity_data, y, y_pred, r2_activity)` →
  `plot_mlr_results(X, activity_data, y, y_pred, r2_activity)` — needs `X.columns` for
  the predictor list. Updated the one call site,
  `notebooks/Notebook_1_Final.ipynb` cell `9093c06e`.
- **Notebook re-executed**: cell count unchanged (25 → 25), 0 errors.
