import pandas as pd
from pathlib import Path

# Load the dataset
file_path = Path("data") / "WHR26_Data_Figure_2.1.xlsx"
df = pd.read_excel(file_path)

# Select 2025 country scores
latest_year = df[df["Year"] == 2025].copy()
scores = latest_year["Life evaluation (3-year average)"]

# Descriptive statistics
print("--- 2025 DESCRIPTIVE STATISTICS ---")
print(scores.describe().round(3))

print("\nMean:", round(scores.mean(), 3))
print("Median:", round(scores.median(), 3))
print("Standard deviation:", round(scores.std(), 3))
print("Range:", round(scores.max() - scores.min(), 3))

# Calculate quartiles and IQR
q1 = scores.quantile(0.25)
q3 = scores.quantile(0.75)
iqr = q3 - q1

lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

print("\n--- IQR OUTLIER CHECK ---")
print("Q1:", round(q1, 3))
print("Q3:", round(q3, 3))
print("IQR:", round(iqr, 3))
print("Lower bound:", round(lower_bound, 3))
print("Upper bound:", round(upper_bound, 3))

outliers = latest_year[
    (scores < lower_bound) | (scores > upper_bound)
][["Country name", "Life evaluation (3-year average)"]]

print("\nPotential outliers:")
if outliers.empty:
    print("No potential outliers identified by the IQR rule.")
else:
    print(outliers.to_string(index=False))



import matplotlib.pyplot as plt

# Visualize the distribution of 2025 scores
plt.figure(figsize=(9, 5))

plt.boxplot(
    scores,
    orientation="horizontal",
    patch_artist=True
)

plt.title("Distribution of Life Evaluation Scores — 2025")
plt.xlabel("Life Evaluation Score")
plt.yticks([1], ["Countries"])
plt.xlim(0, 10)
plt.grid(axis="x", alpha=0.3)
plt.tight_layout()

plt.savefig(
    "life_evaluation_boxplot_2025.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
