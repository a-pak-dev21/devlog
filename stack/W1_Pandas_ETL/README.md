Here’s a ready-to-drop README.md (English) that consolidates your W1 (L1) + W1 (L2) theory, clarifications, and a practical Accessors Cheat Sheet (.str, .dt, .cat) with their most used methods.

⸻

Pandas ETL — W1 (L1 + L2) Notes

This doc is a compact but practical reference for the ETL blocks we covered:
• L1: filtering, selection, grouping, sorting, exporting, basic IO & paths
• L2: robust joins/merges, transform vs agg, wide/long reshape, categorical dtype, datetime parsing, de-duplication, memory optimization
• Accessors Cheat Sheet: .str, .dt, .cat (what they are, when they work, most useful methods)

All examples assume import pandas as pd and typical dataframes like df (facts) and dim (lookup).

⸻

0. Mindset / ETL Contract
   • Input → Normalize → Validate → Transform → Output.
   • Keep a simple contract: what changes, why, and how to reproduce it.
   • Prefer vectorized operations; avoid row-wise .apply(axis=1) unless truly needed.

⸻

1. Selection & Filtering (L1)

Boolean filters (&, |, ~)
• & = AND, | = OR, ~ = NOT
• Wrap each condition in parentheses.

adults = df[(df["age"] >= 18) & (df["city"] == "Prague")]
non_prague = df[~(df["city"] == "Prague")]

.loc vs .iloc
• df.loc[row_selector, col_selector] — label-based (values/index names).
• df.iloc[row_idx, col_idx] — position-based (integers).

df.loc[df["reps"] > 10, ["user_id", "reps"]]
df.iloc[:5, :3]

⸻

2. Sorting & Export (L1)

out = df.sort_values(["city", "weight_kg"], ascending=[True, False])
out.to_excel("solutions/L1_sorted.xlsx", index=False) # index usually False in reports

⸻

3. Groupby & Aggregation (L1 → L2 refinement)
   • groupby(...).agg({...}) returns one row per group.
   • Strings like "mean", "sum", "nunique" map to built-in reductions.

summary = (
df.groupby("city")
.agg({"weight_kg": "mean", "reps": "sum", "user_id": "nunique"})
.reset_index()
)

transform vs agg (L2)
• agg collapses groups → shorter result.
• transform returns a Series same length as df → can attach per-row group metrics.

df["avg_weight_city"] = df.groupby("city")["weight_kg"].transform("mean")

# Per-row compare (vectorized is best; row-wise apply is slower)

df["is_above_avg"] = df["weight_kg"] >= df["avg_weight_city"]

⸻

4. Merging / Joining (L2)

Use merge with validation and indicator for safe joins.

# Normalize join keys first (strip spaces, consistent dtype)

for d in (df, dim):
d["city"] = d["city"].astype("string").str.strip()

res = df.merge(
dim,
on="city",
how="left",
validate="m:1", # many-to-one (facts → lookup)
indicator=True, # adds \_merge: left_only/right_only/both
suffixes=("\_fact", "\_dim")
)

    •	validate values: "1:1", "1:m", "m:1", "m:m" (raises MergeError on violation).
    •	indicator=True surfaces mismatches (left_only are missing keys in lookup).

Common cleanup:

left_only = res.loc[res["_merge"] == "left_only", "city"]

# Replace missing keys, then either re-merge or fill right fields:

res.loc[res["_merge"] == "left_only", "city"] = "Unknown"
res = res.drop(columns=["_merge"], errors="ignore")

# Optionally: fill missing right columns if no "Unknown" row exists in dim:

res[["country","region"]] = res[["country","region"]].fillna("Unknown")

⸻

5. Wide ↔ Long Reshaping (L2)

Use cases:
• Long is great for aggregations/visualizations (one value column, one key column).
• Wide is great for presentation/export or model input formats.

# Wide → Long: columns like day1_reps, day2_reps, ... → rows

value_cols = [c for c in df.columns if c.endswith("_reps")]
df_long = df.melt(id_vars=["user_id"], value_vars=value_cols,
var_name="day", value_name="reps")

# Long → Wide (pivot)

wide = df_long.pivot_table(index="user_id", columns="day",
values="reps", aggfunc="sum", fill_value=0)

⸻

6. Datetime Parsing (L2)
   • format= defines input pattern; final dtype is datetime64[ns] (ISO when printed).
   • dayfirst/yearfirst help with ambiguous numeric formats.
   • Mixed formats → cascade or use dateparser (optional).

# Single consistent format (fast & reliable)

df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d", errors="coerce")

# Extract parts

df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["day"] = df["date"].dt.day

⸻

7. Categorical dtype (L2)

Why use it:
• Huge memory savings when few unique values.
• Custom ordering (non-alphabetical) for sorting/logic.
• Faster groupby/comparisons; convenient data validation.

df["body_part"] = pd.Categorical(
df["body_part"],
categories=["cardio", "legs", "back", "chest"],
ordered=True
)

# Sorting respects your category order:

df = df.sort_values("body_part")

# Codes and categories:

codes = df["body_part"].cat.codes # int codes (0..n)
cats = df["body_part"].cat.categories # category index

If categories don’t include some values from the column, those values become NaN.
Use this intentionally to flag unexpected data.

⸻

8. De-duplication (L2)

# Business key duplicates

clean = df.drop_duplicates(subset=["user_id", "exercise"], keep="first")

# Or: sort by weight/reps then drop_duplicates(keep="first")

⸻

9. Memory Optimization (L2)
   • Convert textual columns to string or category.
   • Downcast numerics where safe (Int16, float32).
   • Compare memory before/after:

before = df.memory_usage(deep=True).sum()
df["city"] = df["city"].astype("category")
df["reps"] = df["reps"].astype("Int16")
df["weight_kg"] = df["weight_kg"].astype("float32")
after = df.memory_usage(deep=True).sum()
print(f"Memory: {before/1e6:.2f}MB → {after/1e6:.2f}MB")

⸻

10. Path & Export Hygiene

Use pathlib.Path, build safe paths, ensure directories exist, and prefer index=False for report files.

from pathlib import Path

root = Path.cwd().parent
def out_path(folder: str, filename: str) -> Path:
d = root / folder
d.mkdir(exist_ok=True)
return d / filename

df.to_excel(out_path("solutions", "report.xlsx"), index=False)

⸻

11. Common Pitfalls Checklist
    • Forgetting parentheses in boolean filters → ValueError: ambiguous truth value.
    • Calling .dt/.str on wrong dtype → always convert (to_datetime, astype("string"), etc.).
    • Destroying NaN by astype(str) → prefer astype("string") to retain missing values (<NA>).
    • Merging unnormalized keys (trailing spaces/case issues) → .astype("string").str.strip().
    • Not validating joins → always add validate and inspect \_merge.

⸻

Accessors Cheat Sheet (.str, .dt, .cat)

Accessors activate type-specific method sets on a Series. They work only if the underlying dtype is compatible.

Convert first, then use accessor:
• Strings: s = s.astype("string") → s.str...
• Datetimes: s = pd.to_datetime(s) → s.dt...
• Categoricals: s = s.astype("category") → s.cat...

⸻

.str — String Accessor (on string or string-like object)

When: text cleanup, parsing, flags, extraction.

s.str.lower() # lowercase
s.str.upper() # uppercase
s.str.strip() # trim both sides
s.str.contains("rx", case=False, na=False) # boolean mask
s.str.replace(r"\s+", " ", regex=True) # regex replace
s.str.len() # string length
s.str.extract(r"(\d{4})") # first group as new Series
s.str.split("-", expand=True) # split into columns (if expand=True)
s.str.startswith("pre"), s.str.endswith("x")
s.str.zfill(3) # pad with zeros to width 3

Tips:
• Always set na=False in .contains if you want a clean mask without NaNs.
• Prefer regex=True explicitly in .replace when using patterns (pandas 2.x behavior).

⸻

.dt — Datetime Accessor (on datetime64[ns])

When: extracting parts, time logic, calendar features.

s.dt.year, s.dt.month, s.dt.day
s.dt.hour, s.dt.minute, s.dt.second
s.dt.dayofweek, s.dt.day_name() # 0=Mon ... 6=Sun
s.dt.is_month_start, s.dt.is_month_end
s.dt.normalize() # strip time part to midnight
s.dt.tz_localize("UTC").dt.tz_convert("Europe/Prague")
s.dt.strftime("%Y-%m-%d") # format back to string

Tips:
• Ensure s is datetime: s = pd.to_datetime(s, errors="coerce", ...).
• Use errors="coerce" to avoid crashes on dirty rows (NaT for bad parses).

⸻

.cat — Categorical Accessor (on category)

When: memory saving, custom order, validation, fast groupby/sort.

s.cat.categories # Index of categories
s.cat.codes # int codes (−1 for NaN)
s.cat.add_categories(["new"])
s.cat.remove_unused_categories()

# Define order at creation for meaningful sort:

s = pd.Categorical(s, categories=["low","med","high"], ordered=True)
df = df.sort_values("priority") # respects category order

Tips:
• Values not in categories become NaN → use this to validate inputs.
• Good for reports/plots that must follow business order (not alphabetical).

⸻

Bonus: A few other useful Series tools

(Not accessors, but frequently paired.)

s.fillna("Unknown") # fill missing text/category
s.astype("Int16") # nullable integer dtype
s.clip(lower=0) # clamp values
s.where(cond, other=np.nan) # conditional assignment (vectorized)

⸻

Mini Templates

Robust LEFT merge with validation & report

for t in (df, dim):
t["city"] = t["city"].astype("string").str.strip()

res = df.merge(dim, on="city", how="left", validate="m:1", indicator=True)

left_only = res.loc[res["_merge"]=="left_only", "city"]
if not left_only.empty:
(left_only.value_counts()
.rename_axis("city").reset_index(name="count")
).to_excel(out_path("solutions", "L2_missing_cities.xlsx"), index=False)

res.loc[res["_merge"]=="left_only","city"] = "Unknown"
res = res.drop(columns=["_merge"], errors="ignore")
res[["country","region"]] = res[["country","region"]].fillna("Unknown")
res.to_excel(out_path("solutions","L2_joined.xlsx"), index=False)

Wide → Long → Aggregate → (Optional) Pivot back

value_cols = [c for c in df.columns if c.endswith("_reps")]
long = df.melt(id_vars=["user_id"], value_vars=value_cols,
var_name="day", value_name="reps")

avg = (long.groupby("user_id", as_index=False)["reps"]
.mean().rename(columns={"reps":"avg_reps"}))

wide = long.pivot_table(index="user_id", columns="day",
values="reps", aggfunc="sum", fill_value=0)

Datetime parse + parts

df["date"] = pd.to_datetime(df["date"], errors="coerce", dayfirst=True)
df["year"], df["month"], df["day"] = df["date"].dt.year, df["date"].dt.month, df["date"].dt.day

Categorical with explicit order

df["body_part"] = pd.Categorical(
df["body_part"],
categories=["cardio","legs","back","chest"],
ordered=True
)
df = df.sort_values("body_part")

⸻

Quality Checklist Before Shipping
• Keys normalized before merge (strip, dtype).
• validate and (optionally) indicator used in joins.
• Accessors used only on correct dtypes (.str/.dt/.cat).
• Exports use index=False (unless index meaningful).
• Memory optimizations applied where reasonable (string→category, Int16/float32).
• README updated with data contract and examples.

⸻

If you want this saved as an actual file in your repo (e.g., notebooks/W1/README.md or docs/W1_Pandas_ETL.md), say where to place it and I’ll format the path lines accordingly.
