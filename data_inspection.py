import pandas as pd
from pathlib import Path

# Locate the Excel dataset
file_path = Path("data") / "WHR26_Data_Figure_2.1.xlsx"

# Load the Excel file
df = pd.read_excel(file_path)

# Display basic information
print("\n--- DATASET SHAPE ---")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\n--- COLUMN NAMES ---")
print(df.columns.tolist())

print("\n--- FIRST FIVE ROWS ---")
print(df.head())

print("\n--- DATA TYPES AND MISSING VALUES ---")
df.info()
print("\nMissing values per column:")
print(df.isnull().sum())


print("\n--- ROWS WITH MISSING VALUES ---")
rows_with_missing = df.isnull().any(axis=1).sum()
print("Rows containing at least one missing value:", rows_with_missing)

print("\n--- MISSING VALUE PERCENTAGES ---")
missing_percentage = (df.isnull().mean() * 100).round(2)
print(missing_percentage)

print("\n--- DUPLICATE ROWS ---")
print("Duplicate rows:", df.duplicated().sum())

print("\n--- YEAR COVERAGE ---")
print("Years available:", sorted(df["Year"].unique()))

print("\n--- RECORDS PER YEAR ---")
print(df["Year"].value_counts().sort_index())

print("\n--- MISSING VALUES BY YEAR ---")
missing_by_year = df.groupby("Year").apply(
    lambda group: group.isnull().any(axis=1).sum()
)
print(missing_by_year)


print("\n--- MISSING VALUES BY YEAR AND COLUMN ---")

missing_by_year_column = df.groupby("Year").apply(
    lambda group: group.isnull().sum()
)

print(missing_by_year_column.to_string())

print("\n--- COMPLETE ROWS BY YEAR ---")

complete_rows_by_year = df.groupby("Year").apply(
    lambda group: group.notnull().all(axis=1).sum()
)

print(complete_rows_by_year)


print("\n--- 2025 DATA PREVIEW ---")

latest_year = df[df["Year"] == 2025]

print(latest_year.head(10).to_string(index=False))

print("\n--- 2025 MISSING VALUES ---")

print(latest_year.isnull().sum())

print("\n--- 2025 LIFE EVALUATION SUMMARY ---")

print(latest_year["Life evaluation (3-year average)"].describe())


print("\n--- TOP 10 COUNTRIES IN 2025 ---")

top_10 = latest_year.nsmallest(
    10, "Rank"
)[["Rank", "Country name", "Life evaluation (3-year average)"]]

print(top_10.to_string(index=False))

print("\n--- BOTTOM 10 COUNTRIES IN 2025 ---")

bottom_10 = latest_year.nlargest(
    10, "Rank"
)[["Rank", "Country name", "Life evaluation (3-year average)"]]

print(bottom_10.to_string(index=False))
