# Friendly Multi Store — Sales & Marketing Analysis Dashboard

A Python dashboard built with **Streamlit, Pandas and Plotly**, styled to match the internship dashboard screenshots.

## Features
- Date-range and product filters
- Sales overview KPI cards
- Daily purchase trend calculated from the uploaded transaction data
- Product revenue and contribution analysis
- Business insight cards
- Monthly revenue chart
- Expandable source transaction table and CSV download

## Project structure
```text
Friendly_Multi_Store_Dashboard/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   ├── campaign_transactions.csv
│   ├── reported_product_revenue.csv
│   └── reported_dashboard_kpis.json
└── assets/
    └── reference_screenshots/
```

## Run locally
1. Install Python 3.10 or later.
2. Open a terminal in this project folder.
3. Create and activate a virtual environment (recommended).
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Start the dashboard:
   ```bash
   streamlit run app.py
   ```
6. Open the local URL printed in the terminal (usually `http://localhost:8501`).

## Data and reporting note
The source transaction PDF contains 35 records from 1–17 June 2026, with columns for order ID, date, product, category and purchase quantity. Those records total **200 purchase units**:
- Free Fire Diamonds: 168
- PUBG UC: 31
- Mobile Legends: 1

The separate revenue and overview figures (NPR 128,550 total sales, NPR 62,100 Free Fire revenue, 78 orders, 402 units, 56 customers, etc.) are transcribed from the dashboard screenshots supplied with the internship materials. They are not present in the transaction PDF and cannot be recalculated from its quantity-only rows. The app labels these as reported dashboard figures and keeps them separate from metrics calculated from the CSV.

## GitHub upload
```bash
git init
git add .
git commit -m "Build Friendly Multi Store analytics dashboard"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/friendly-multistore-dashboard.git
git push -u origin main
```

Replace the remote URL with your own GitHub repository URL.
