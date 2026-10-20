# Used-Car Price Explorer
**CMSE 830 Midterm Project**

## Project Overview
The Used-Car Price Explorer is an interactive Streamlit application that helps users explore relationships between automobile characteristics and prices. Users can filter vehicles by manufacturer, body style, fuel type, and price range, then examine summary statistics and visualizations.

## Problem, Audience, and Research Question
**Intended audience:** Students, data science learners, and people interested in exploring historical automobile data.

**Purpose:** To make it easier to explore how vehicle characteristics vary with automobile prices using interactive filters and visualizations.

**Research question:** Which recorded vehicle characteristics tend to be associated with automobile price?

This project focuses on exploratory data analysis rather than predicting current used-car prices.

## Dataset and Observation Unit
The project uses the Automobile dataset from the UCI Machine Learning Repository.

**Dataset source:** https://archive.ics.uci.edu/ml/machine-learning-databases/autos/imports-85.data

Each row represents one automobile record. Variables include manufacturer, fuel type, body style, engine size, horsepower, curb weight, fuel economy, and price.

The application downloads the dataset from the UCI source when no local copy is available. An internet connection is therefore needed to retrieve the data.

## Data Preparation and Quality
The application assigns descriptive column names to the source data and treats `?` values as missing. Numeric variables are converted to numeric types, and categorical variables are treated as text.

Records without a price are excluded because they cannot contribute to price comparisons. Missing values in other variables are retained and omitted from analyses that require those values.

The application also reports missing values and exact duplicate rows. It does not automatically impute missing values or remove duplicate rows. These choices avoid introducing unsupported replacement values or discarding observations without further justification.

## Exploratory Data Analysis
The application includes:

- Summary statistics, including the number of selected cars, mean price, and median price.
- A scatter plot comparing price with a user-selected characteristic, such as horsepower, engine size, curb weight, or fuel economy.
- Pearson correlation to summarize the linear association between the selected characteristic and price.
- A price distribution histogram.
- A manufacturer comparison using median and mean prices, with a minimum group-size filter.
- A data-quality summary and discussion of limitations.

## Interactive Features
Users can filter the dataset by manufacturer, body style, fuel type, and price range. The charts and summary statistics update based on the selected subset. Users can also download the filtered records as a CSV file.

## Key Findings
In the default full-data view, the application reports a positive association between horsepower and price. The observed correlation depends on the selected filters and available observations. Users can explore other characteristics and compare manufacturers interactively.

Correlation describes association, not causation. Differences in vehicle characteristics and other unmeasured factors may help explain price differences.

## Limitations
- The dataset is historical and does not represent current used-car listings or market prices.
- Some variables have missing observations.
- The number of records differs among manufacturers and vehicle categories.
- Variables such as mileage, vehicle condition, accident history, maintenance, location, and current market demand are not represented.
- Correlation does not establish causation.
- Results should not be used as estimates of current used-car values.

## Installation and Setup

### Requirements
- Python 3.9 or a compatible newer version
- Internet connection for downloading the dataset when no local copy is available

### Install dependencies
Open a terminal in the project folder and run:

```bash
python -m pip install -r requirements.txt
```

### Run the application
Run:

```bash
python -m streamlit run app.py
```

Streamlit will provide a local web address, usually `http://localhost:8501`, where the application can be viewed in a browser.

Press `Ctrl+C` in the terminal to stop the application.

## Project Files
- `app.py` — Streamlit application, data loading, analysis, and visualizations.
- `requirements.txt` — Python package dependencies.
- `README.md` — Project overview, methods, limitations, and setup instructions.

## AI-Use Disclosure
Adapt this statement to accurately reflect your work and your course policy:

AI tools, including ChatGPT, were used to assist with code troubleshooting and/or project documentation. I reviewed and tested the application and am responsible for the final project, analysis, interpretation, and submission.

## Author
CMSE 830 Midterm Project
