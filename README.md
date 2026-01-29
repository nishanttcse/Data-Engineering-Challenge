# Slooze Data Engineering Challenge

## 📌 Overview
This repository contains an end-to-end data engineering solution designed to scrape, clean, and analyze B2B product data from **IndiaMART**. The project demonstrates a robust ETL pipeline followed by Exploratory Data Analysis (EDA) to uncover market insights regarding pricing trends and supplier hubs.

## 📂 Project Structure

```text
Slooze_Challenge/
│
├── Slooze_Challenge.ipynb   # Main Jupyter Notebook (Source Code)
├── indiamart_raw.csv        # Snapshot of collected data (Backup)
├── requirements.txt         # List of dependencies
└── README.md                # Project documentation
⚙️ Prerequisites
Python 3.8+

Jupyter Notebook or JupyterLab

🚀 Setup & Installation
Unzip the submission file.

Install dependencies: Open your terminal/command prompt in the project folder and run:

Bash
pip install -r requirements.txt
(Note: If you do not have requirements.txt, you can install manually using: pip install requests beautifulsoup4 pandas matplotlib seaborn fake-useragent tqdm)

🏃‍♂️ How to Run
Launch Jupyter Notebook:

Bash
jupyter notebook
Open Slooze_Challenge.ipynb.

Run all cells sequentially (Kernel > Restart & Run All).

Execution Flow:
Part A (Data Collection): The scraper initializes and targets the "Industrial Valves" category (or utilizes the pre-loaded sample dataset if the site blocks requests).

Part B (EDA): The notebook automatically cleans the price data, handles outliers, and generates visualizations for:

Supplier Regional Distribution (Hub Identification)

Price Distribution Histograms

📊 Methodology
1. Data Collection (Scraping)
Strategy: Used requests and BeautifulSoup with header rotation (fake_useragent) to mimic organic traffic.

Robustness: Implemented error handling (try-except) to skip malformed HTML cards without crashing the crawler.

Politeness: Added random sleep intervals (2-5 seconds) between requests to respect server load.

2. Exploratory Data Analysis (EDA)
Cleaning: Created a regex-based parser to convert unstructured strings (e.g., "₹ 4,500 / Unit") into float values.

Insights:

Identified major supplier hubs (e.g., Mumbai, Ahmedabad).

Analyzed market transparency by calculating the ratio of "Ask for Price" vs. displayed prices.

👤 Author
Nishant Srivastava


---

### **Bonus: `requirements.txt`**

```text
requests
beautifulsoup4
pandas
matplotlib
seaborn
fake-useragent
tqdm
