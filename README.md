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

- The dataset
