import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

REQUIRED_COLUMNS = ["Company_ID", "Industry", "Annual_Revenue (M₺)"]

def load_and_clean_data(file):
    """
    Loads dataset from file path or uploaded file, validates required columns,
    cleans, and removes fuzzy duplicates by Company_Name.
    Returns cleaned DataFrame and removed duplicates DataFrame.
    """
    try:
        if isinstance(file, str):
            df = pd.read_csv(file)
        else:
            df = pd.read_csv(file)

        if df.empty or len(df.columns) == 0:
            raise ValueError("The uploaded file is empty or has no columns.")
    except pd.errors.EmptyDataError:
        raise ValueError("The uploaded file is empty.")
    except Exception as e:
        raise ValueError(f"Error reading the CSV file: {e}")

    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        raise ValueError(f"The dataset is missing required column(s): {', '.join(missing_cols)}")

    df = df.dropna(subset=REQUIRED_COLUMNS)
    df = df.fillna(0)

    numeric_cols = [
        "Annual_Revenue (M₺)",
        "Marketing_Spend (K₺)",
        "Leads_Generated",
        "Conversion_Rate (%)"
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    if "Company_Name" in df.columns:
        cleaned_df, removed_df = detect_and_remove_duplicates(df)
    else:
        cleaned_df = df
        removed_df = pd.DataFrame()

    return cleaned_df, removed_df


def detect_and_remove_duplicates(df, threshold=90):
    """
    Detects and removes fuzzy duplicate companies based on Company_Name.
    Keeps the most complete row from each group. Returns cleaned and removed duplicates.
    """
    df = df.copy()
    df["duplicate_group"] = -1
    key_field = "Company_Name"
    used_indices = set()
    group_id = 0

    for idx, row in df.iterrows():
        if idx in used_indices:
            continue

        name = row[key_field]
        matches = process.extract(name, df[key_field], scorer=fuzz.token_sort_ratio)

        similar_indices = [
            i for (matched_name, score, i) in matches
            if score >= threshold and i != idx and i not in used_indices
        ]

        if similar_indices:
            similar_indices.append(idx)
            used_indices.update(similar_indices)
            df.loc[similar_indices, "duplicate_group"] = group_id
            group_id += 1

    final_rows = []
    removed_rows = []

    for group in df["duplicate_group"].unique():
        if group == -1:
            final_rows.append(df[df["duplicate_group"] == -1])
        else:
            group_df = df[df["duplicate_group"] == group]
            group_df["non_zero_count"] = (group_df != 0).sum(axis=1)
            best_row = group_df.sort_values("non_zero_count", ascending=False).iloc[0:1]
            removed = group_df.drop(best_row.index)
            final_rows.append(best_row)
            removed_rows.append(removed)

    cleaned_df = pd.concat(final_rows, ignore_index=True)
    cleaned_df.drop(columns=["duplicate_group"], inplace=True)

    removed_df = pd.concat(removed_rows, ignore_index=True) if removed_rows else pd.DataFrame()

    # Cleanup
    for col in ["duplicate_group", "non_zero_count"]:
        if col in cleaned_df.columns:
            cleaned_df.drop(columns=[col], inplace=True)
        if col in removed_df.columns:
            removed_df.drop(columns=[col], inplace=True)

    return cleaned_df, removed_df
