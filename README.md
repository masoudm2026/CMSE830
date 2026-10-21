# Used-Car Price Explorer

**Course:** CMSE 830 — Foundations of Data Science  
**Project:** Midterm Project  
**Author:** Masoud Moradi

## Project Overview

The Used-Car Price Explorer is an interactive Streamlit application for exploring relationships between automobile characteristics and prices. Users can filter vehicles by manufacturer, body style, fuel type, and price range, then examine summary statistics and interactive visualizations.

## Problem, Audience, and Research Question

**Intended audience:** Used-car buyers, students, and data science learners interested in exploring historical automobile data.

**Purpose:** To make it easier to investigate how recorded vehicle characteristics are associated with automobile prices.

**Research question:** What factors are associated with used-car prices?

The project focuses on exploratory data analysis rather than predicting current used-car prices.

## Dataset

The project uses the Automobile dataset from the UCI Machine Learning Repository.

- Dataset page: https://archive.ics.uci.edu/dataset/10/automobile
- Data file: https://archive.ics.uci.edu/ml/machine-learning-databases/autos/imports-85.data

Each row represents one automobile record. Variables include manufacturer, fuel type, body style, engine size, horsepower, curb weight, fuel economy, and price.

The app loads a supported local CSV file if available; otherwise, it downloads the dataset from UCI. An internet connection is needed when the local dataset is unavailable.

## Application Features

- Filter by manufacturer, body style, fuel type, and price range.
- View the number of selected cars, mean price, median price, and number of manufacturers.
- Explore interactive scatter plots for price versus horsepower, engine size, curb weight, and fuel economy.
- View Pearson correlation for the selected characteristic and price.
- Explore the distribution of automobile prices.
- Compare manufacturer mean and median prices.
- Review missing values, duplicate rows, and data limitations.
- Reset the filters.
- Download filtered records and the manufacturer summary as CSV files.

## Data Preparation and Quality

The application assigns descriptive column names to the source data and treats `?` as a missing value.

Numeric variables are converted to numeric types, and categorical variables are treated as text. Records without a price are excluded because they cannot be used in price comparisons.

Other missing values are retained in the dataset and omitted from analyses that require the missing variables. The application reports missing values and exact duplicate rows. It does not automatically impute missing values or remove duplicate rows.

## Exploratory Data Analysis

The application includes:

1. Summary statistics for the currently selected vehicles.
2. Interactive scatter plots comparing price with a selected vehicle characteristic.
3. Pearson correlation to summarize the linear association between the selected characteristic and price.
4. A histogram showing the price distribution.
5. A manufacturer comparison using mean and median prices.
6. Data-quality summaries and a discussion of limitations.

In the full-data view, horsepower and price show a positive association among records with the required values. The observed correlation can change when filters are applied.

Correlation describes association, not causation. Other vehicle characteristics and unmeasured factors may help explain price differences.

## Limitations

- The dataset contains historical automobile records and does not represent today's used-car market.
- Some variables contain missing observations.
- Manufacturers have different numbers of records, which affects how confidently their price summaries can be compared.
- Mileage, vehicle condition, accident history, maintenance, location, and current market demand are not represented.
- Correlation does not establish causation.
- Results should not be used as estimates of current used-car values.

## Requirements

- Python
- Streamlit
- pandas
- Plotly

## Installation and Setup

### 1. Open the project folder

Open a terminal in the project folder containing `app.py` and `requirements.txt`.

### 2. Install the required packages

Run this command:

```bash
python -m pip install -r requirements.txt
```

### 3. Start the application

Run this command:

```bash
python -m streamlit run app.py --server.port 8503
```

### 4. Open the application in your browser

While the application is running on your computer, open:

http://localhost:8503

**Note:** This is a local address that works on your own computer while the Streamlit application is running. It is not a public website link that other people can access over the internet.

To stop the app, press `Ctrl+C` in the terminal.

## Requirements File

The `requirements.txt` file should contain:

```text
streamlit
pandas
plotly
```

These are the Python packages required by the application. If you update the app to use additional packages, update this file accordingly.

## Project Files

- `app.py` — Streamlit application, data loading, analysis, and charts.
- `requirements.txt` — Python package dependencies.
- `README.md` — Project overview, methods, limitations, and setup instructions.
- `app_backup.py` — Local backup of the original application, kept for recovery.

The backup file is for local recovery and is not required to run the application.

## AI-Use Disclosure

Generative AI tools, including ChatGPT, assisted with code troubleshooting. 

This disclosure should be adjusted as needed to accurately reflect the assistance used and comply with course requirements.
