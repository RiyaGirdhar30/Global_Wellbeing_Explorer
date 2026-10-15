import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load the dataset
file_path = Path("data") / "WHR26_Data_Figure_2.1.xlsx"
df = pd.read_excel(file_path)

# Countries we want to compare
countries = [
    "Finland",
    "Denmark",
    "India",
    "United States",
    "Afghanistan"
]

# Filter the dataset
trend_data = df[df["Country name"].isin(countries)].copy()

# Sort records chronologically
trend_data = trend_data.sort_values("Year")

# Check which countries were found
found_countries = trend_data["Country name"].unique()
missing_countries = set(countries) - set(found_countries)

print("Countries included:", sorted(found_countries))

if missing_countries:
    print("Countries not found:", sorted(missing_countries))

# Plot life-evaluation trends
plt.figure(figsize=(12, 7))

for country in found_countries:
    country_data = trend_data[
        trend_data["Country name"] == country
    ]

    plt.plot(
        country_data["Year"],
        country_data["Life evaluation (3-year average)"],
        marker="o",
        label=country
    )

plt.title("Life Evaluation Trends Across Countries")
plt.xlabel("Year")
plt.ylabel("Life Evaluation Score")
plt.xticks(sorted(df["Year"].unique()), rotation=45)
plt.ylim(0, 10)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

# Save the chart
output_path = Path("life_evaluation_trends.png")
plt.savefig(output_path, dpi=300, bbox_inches="tight")

plt.show()

print(f"\nChart saved to: {output_path.resolve()}")
