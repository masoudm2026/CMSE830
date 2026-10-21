
# Used-Car Price Explorer

**Course:** CMSE 830 — Foundations of Data Science  
**Project question:** What factors are associated with used-car prices?

## Project overview

This Streamlit application explores associations between automobile prices
and recorded vehicle characteristics, including horsepower, engine size,
curb weight, fuel economy, and manufacturer.

Users can filter the dataset and interact with charts and summary statistics.

## Dataset

Source: UCI Machine Learning Repository — Automobile dataset  
https://archive.ics.uci.edu/ml/machine-learning-databases/autos/imports-85.data

The dataset contains historical automobile records and should not be treated
as a source of current used-car valuations.

## Requirements

- Python
- Streamlit
- pandas
- Plotly

## Run the application

Install the required packages:

```bash
python -m pip install -r requirements.txt
```

Start the app:

```bash
python -m streamlit run app.py --server.port 8503
```

Open http://localhost:8503 in your browser.

## Data preparation

- The dataset is loaded from the UCI source unless a supported local CSV
  file is available.
- The `?` symbol is interpreted as a missing value.
- Numeric columns are converted to numeric types.
- Records without a price are excluded from the price analysis.
- Other missing values are not automatically imputed.

## Limitations

The data are historical and may not represent today's used-car market.
Some variables contain missing values, manufacturer groups differ in size,
and important factors such as mileage, vehicle condition, and accident
history are not represented. Associations do not establish causation.


