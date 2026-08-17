# Canadian Corporate Financial Analysis

## Overview

**The Canadian Corporate Financial Analysis** is an end-to-end data analytics project that transforms corporate financial statement data into actionable financial insights.

The project builds a complete data pipeline that extracts, transforms, stores, cleans, and analyzes company financial information using Python, SQL, and PostgreSQL.

The final objective is to evaluate corporate financial performance, financial health, and business trends across multiple companies using standardized financial metrics.

---

# Business Problem

Companies generate large amounts of financial statement data through annual filings, but raw financial information is often difficult to analyze because it is:

- Distributed across different financial statements
- Reported using different accounting contexts
- Containing duplicate filings and restated information
- Difficult to compare across companies and time periods

This project addresses the following question:

> How can raw corporate financial statement data be transformed into a reliable analytical dataset that enables meaningful comparison of company performance and financial health?

---

# Project Objectives

The project aims to:

1. Build a structured financial database from SEC/API financial data.

2. Clean and standardize corporate financial statements.

3. Integrate income statements, balance sheets, and cash flow statements into a unified analytical dataset.

4. Develop financial metrics to evaluate:

   - Profitability
   - Liquidity
   - Solvency
   - Operational efficiency
   - Cash generation

5. Identify trends and differences in corporate financial performance over time.

---

# Data Scope

The project analyzes financial statement data from:

- 29 publicly listed companies

Current integrated dataset:

- About 300 company-period observations

Financial statements included:

## Income Statement

Examples: Revenue, Operating income and Net income.


## Balance Sheet

Examples: Assets, Liabilities, Equity, Cash and Debt.


## Cash Flow Statement

Examples: Operating cash flow, Investing cash flow, Financing cash flow, and Capital expenditure.

---

# Technical Architecture
```
            SEC/API Financial Reports
                     ↓
            Python (Data Extraction) 
                     ↓
              PostgreSQL Database
                     ↓
             Python (Data Cleaning) 
                     ↓
              SQL Analytics Views
                     ↓
              Power BI Dashboard
               
```

---

# Technology Stack

## Data Engineering

- PostgreSQL
- SQL
- SQL Views
- Window Functions

## Programming

- Python
- pandas
- SQLAlchemy

## Development

- VS Code
- Git/GitHub

## Visualization
- Power BI
---

# Analytical Questions

The analysis phase will answer questions such as:

## Profitability

- Which companies show consistent revenue growth?
- Which companies maintain strong profit margins?
- Which companies generate higher returns on assets and equity?


## Financial Health

- Which companies maintain strong liquidity?
- Which companies carry higher debt levels?
- How does financial structure differ across companies?


## Cash Generation

- Which companies generate strong operating cash flows?
- Are companies converting earnings into cash?
- How are companies allocating capital?


## Trends

- How has company performance changed over time?
- Which companies improved or deteriorated financially?

---

# Project Status

## Completed

✅ Database design  
✅ Data extraction  
✅ Data transformation  
✅ PostgreSQL loading  
✅ SQL cleaning layer  
✅ Financial data integration  
✅ Exploratory data analysis  
✅ Financial ratio calculation  
✅ Company comparison  
✅ Trend analysis  
✅ Visualization  
✅ Business insights    

---

# Project Deliverables

Final outputs will include:

- PostgreSQL database design
- SQL scripts
- Python analysis notebook
- Financial performance metrics
- Visualizations
- Analytical conclusions

---
## Key Findings
- The analysis covers **29 major Canadian public companies** across an unbalanced **2007–2025** financial panel. [See Dashboard](<power_bi/all_Sectors_power_bi/All_Canadia_ Companies.pdf>)

* The companies generated approximately **$3.09T in latest revenue**, **$561.59B in net income**, and held approximately **$63.03T in assets**. 

* **Toronto-Dominion Bank ($68B)** and **Royal Bank of Canada ($67B)** were the largest companies by latest revenue, followed by **Sun Life Financial**, **Bank of Nova Scotia**, and **Bank of Montreal**. [See Banking Sector](power_bi/all_Sectors_power_bi/Banking_Sector.pdf)

* Average revenue growth was approximately **14.2%**, while the latest year recorded approximately **$405.63B in revenue growth** across all companies.

* **Sun Life Financial** was the strongest growth performer at approximately **62.4%**, followed by **Fortis (33.5%)** and **Shopify (27.3%)**. [See Financial Services Sector](power_bi/all_Sectors_power_bi/Financial_Services_Sector.pdf)

* Revenue scale and profitability were not directly proportional; several smaller companies demonstrated strong profitability despite having substantially lower revenues than the largest firms.

* **Banking and Financial Services** represented the largest concentrations in the sector analysis, highlighting the importance of financial institutions to the analysis. [See Banking Sector](power_bi/all_Sectors_power_bi/Banking_Sector.pdf)

* Cash flow showed substantial historical volatility, reaching approximately **$0.52T in 2020** before declining considerably in subsequent years.

* Liabilities-to-assets varied across companies, highlighting differences in financial structure and leverage.

* Overall, the analysis demonstrates a portfolio characterized by **high financial scale, strong aggregate earnings, significant sector concentration, varied growth performance, and differing levels of financial risk**.


---

**Data Limitations:**
 - The dataset is an unbalanced panel of major Canadian public companies covering 2007–2025. Financial-statement coverage varies by company and metric because reporting availability differs across firms and years. Therefore, results should be interpreted as descriptive financial analytics based on available observations rather than investment advice or projected estimates.

---

# Repository Structure


```
canadian_corporate_financial_analysis/
├── csv_files
├── power_bi_dashboard/
├── .gitignore
├── README.md
└── requirements.txt
```


---

# Future Improvements

Potential improvements for this project include:

- Expand analysis to include additional companies

---

# Author

Christopher Ajayi