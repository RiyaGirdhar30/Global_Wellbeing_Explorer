# 🌍 Global Wellbeing Explorer

An interactive data analysis dashboard that explores global life evaluation scores, compares countries, examines historical wellbeing trends, and investigates factors associated with life evaluation using data from the World Happiness Report 2026.

## ✨ Features

- **Overview Dashboard:** View average life evaluation, the highest- and lowest-scoring countries, and the top 15 countries.
- **Country Explorer:** Compare countries and explore historical life evaluation trends.
- **Data Insights:** Explore correlations between life evaluation and explanatory components such as GDP per capita, social support, healthy life expectancy, and freedom to make life choices.
- **Country Rankings:** View top- and bottom-ranked countries for different reporting years.
- **Wellbeing Insights:** Examine yearly averages, highest and lowest scores, and the gap between them.
- **Data Quality Report:** Inspect missing values, duplicate rows, and country coverage by year.
- **CSV Exports:** Download ranking tables and missing-value reports.

## 🛠️ Technologies Used

- Python
- Pandas
- Streamlit
- Matplotlib
- Seaborn
- OpenPyXL
- Excel dataset

## 📊 Dataset

This project uses the World Happiness Report 2026 dataset for Figure 2.1, covering reporting years 2011–2025.

**Official source:** [World Happiness Report — Data Sharing](https://www.worldhappiness.report/data-sharing/)

The dataset includes life evaluation scores, rankings, confidence-interval bounds, and explanatory components.

**Note:** The available years and country coverage vary. Correlations are descriptive associations and should not be interpreted as proof of causation.

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/RiyaGirdhar30/Global_Wellbeing_Explorer.git
cd Global_Wellbeing_Explorer
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python -m streamlit run app.py
```

The application should open in your browser.

## 📁 Project Structure

```text
Global_Wellbeing_Explorer/
├── app.py
├── data_inspection.py
├── visualization.py
├── trend_analysis.py
├── correlation_analysis.py
├── statistical_analysis.py
├── requirements.txt
├── data/
│   └── WHR26_Data_Figure_2.1.xlsx
└── README.md
```

## 📈 Analysis Included

- Country ranking comparisons
- Historical life evaluation trends
- Correlation analysis
- Descriptive statistical analysis
- Outlier detection using the interquartile range (IQR)
- Missing-value and dataset-quality analysis

## ⚠️ Limitations

- The dashboard describes patterns in the available data; it does not establish causal relationships.
- Some explanatory components are unavailable for earlier reporting years.
- Results depend on the completeness and coverage of the source dataset.

## 👩‍💻 Author

**Riya Girdhar**

- GitHub: [RiyaGirdhar30](https://github.com/RiyaGirdhar30)
- LinkedIn: [Riya Girdhar](https://www.linkedin.com/in/riya-girdhar-a6074124a)
