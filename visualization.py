import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load the dataset
file_path = Path("data") / "WHR26_Data_Figure_2.1.xlsx"
df = pd.read_excel(file_path)

# Select the 2025 records
latest_year = df[df["Year"] == 2025]

# Get the top 10 countries
top_10 = latest_year.nsmallest(10, "Rank").copy()

# Sort by score for a horizontal bar chart
top_10 = top_10.sort_values(
    "Life evaluation (3-year average)"
)

# Create the chart
plt.figure(figsize=(10, 6))

plt.barh(
    top_10["Country name"],
    top_10["Life evaluation (3-year average)"]
)

plt.title("Top 10 Countries by Life Evaluation — 2025")
plt.xlabel("Life Evaluation Score")
plt.ylabel("Country")
plt.xlim(0, 10)

plt.tight_layout()

# Save the chart
output_path = Path("top_10_countries_2025.png")
plt.savefig(output_path, dpi=300, bbox_inches="tight")

plt.show()

print(f"Chart saved to: {output_path.resolve()}")
