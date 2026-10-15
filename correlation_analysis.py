import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Load the dataset
file_path = Path("data") / "WHR26_Data_Figure_2.1.xlsx"
df = pd.read_excel(file_path)

# Select the variables for analysis
columns = [
    "Life evaluation (3-year average)",
    "Explained by: Log GDP per capita",
    "Explained by: Social support",
    "Explained by: Healthy life expectancy",
    "Explained by: Freedom to make life choices",
    "Explained by: Generosity",
    "Explained by: Perceptions of corruption",
]

analysis_data = df[columns].dropna()

print("Total records in original dataset:", len(df))
print("Complete records used:", len(analysis_data))

# Calculate correlations
correlation_matrix = analysis_data.corr(method="pearson")

print("\n--- CORRELATION WITH LIFE EVALUATION ---")

target = "Life evaluation (3-year average)"

correlations = correlation_matrix[target].drop(target)
correlations = correlations.sort_values(ascending=False)

print(correlations.round(3))

# Create a heatmap
plt.figure(figsize=(12, 8))

sns.heatmap(
    correlation_matrix,
    annot=True,
    cmap="coolwarm",
    vmin=-1,
    vmax=1,
    center=0,
    fmt=".2f"
)

plt.title("Correlation Between Life Evaluation and Its Reported Components")
plt.tight_layout()

# Save the chart
output_path = Path("correlation_heatmap.png")
plt.savefig(output_path, dpi=300, bbox_inches="tight")

plt.show()

print(f"\nChart saved to: {output_path.resolve()}")
