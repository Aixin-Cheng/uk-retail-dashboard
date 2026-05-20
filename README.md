# 🛒 UK Retail Sales Dashboard

An interactive sales intelligence dashboard built with **Python**, **Streamlit**, and **Plotly**, powered by the UCI Online Retail II dataset.

---

## 📌 Overview

This dashboard provides a comprehensive view of UK retail sales data, enabling businesses to explore revenue trends, top products, customer behaviour, and international market performance — all in a clean, dark-themed UI.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📊 KPI Cards | Revenue, Orders, Customers, Products, Avg Order Value |
| 📈 Monthly Trend | Area chart of revenue over time |
| 🏆 Top Products | Best selling products by units sold (adjustable N) |
| 🌍 Country Markets | Top 10 international markets by revenue |
| 📅 Day of Week | Revenue breakdown by weekday |
| 🕐 Hour Analysis | Revenue by hour of day |
| 👤 Top Customers | Most valuable customers by total spend |
| 💡 Key Insights | Auto-generated business recommendations |
| 🔍 Raw Data Explorer | Browse and download the cleaned dataset as CSV |

---

## 🛠️ Tech Stack

- **Python** 3.10+
- **Streamlit** — Web app framework
- **Plotly** — Interactive charts
- **Pandas** — Data manipulation
- **NumPy** — Numerical operations

---

## 📁 Project Structure
uk-retail-dashboard/
│
├── app.py                  # Main Streamlit application
├── online_retail_II.csv    # Dataset (download separately)
├── requirements.txt        # Python dependencies
└── README.md               # This file

---

## 📦 Dataset

- **Name:** Online Retail II
- **Source:** UCI Machine Learning Repository
- **Link:** https://archive.ics.uci.edu/dataset/502/online+retail+ii
- **File:** `online_retail_II.csv`
- **Records:** ~1 million transactions (2009–2011)
- **Fields:** Invoice, StockCode, Description, Quantity, InvoiceDate, Price, Customer ID, Country

> ⚠️ The dataset is **not included** in this repo due to file size. Download it manually from the link above and place it in the project root.

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/Aixin-Cheng/uk-retail-dashboard.git
cd uk-retail-dashboard
```

### 2. Create a virtual environment
```bash
python -m venv .venv
```

### 3. Activate the virtual environment
```bash
# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Download the dataset
Visit the link above and place `online_retail_II.csv` in the project root folder.

### 6. Run the app
```bash
streamlit run app.py
```

### 7. Open in browser
[http://localhost:8501](https://uk-retail-dashboard-exvvvdkytozapkp4neda8y.streamlit.app)

---

## 🎛️ Sidebar Filters

- **Year(s)** — Filter data by one or more years
- **Country(ies)** — Filter by country (default: United Kingdom)
- **Top N** — Adjust how many top products are displayed (5–20)

---

## 🧹 Data Cleaning Applied

- Removed rows with missing Customer ID
- Removed cancelled invoices (prefix `C`)
- Removed rows where Quantity or Price `<= 0`
- Parsed InvoiceDate to datetime
- Engineered features: `TotalPrice`, `Year`, `Month`, `Day_of_Week`, `Hour`

---

## ⚠️ Known Issues

- The **Top International Market** insight shows `N/A` if only United Kingdom is selected
- Dataset must be downloaded manually (not included in repo)
- Tested on Windows 11 with Python 3.11

---

## 👤 Author

- **Name:** Htet Htet Wint
- **GitHub:** https://github.com/Aixin-Cheng
- **LinkedIn:** https://linkedin.com/in/htet-htet-wint/

---

## 📄 License

This project is open source and available under the **MIT License**.  
Dataset provided by [UCI Machine Learning Repository](https://archive.ics.uci.edu).
