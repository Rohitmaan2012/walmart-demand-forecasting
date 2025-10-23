# Data Directory

This directory contains the raw data files for the Walmart MLOps pipeline.

## Required Data

### Walmart.csv
The main dataset should be placed here as `Walmart.csv`. This file should contain:

- **Date**: Date in DD-MM-YYYY format
- **Store**: Store ID (integer)
- **Weekly_Sales**: Weekly sales amount (float)
- **Holiday_Flag**: Holiday indicator (0 or 1)
- **Temperature**: Temperature in Fahrenheit (float)
- **Fuel_Price**: Fuel price (float)
- **CPI**: Consumer Price Index (float)
- **Unemployment**: Unemployment rate (float)

### Sample Data Format
```csv
Date,Store,Weekly_Sales,Holiday_Flag,Temperature,Fuel_Price,CPI,Unemployment
05-02-2010,1,24924.50,0,42.31,2.572,211.0963582,8.106
12-02-2010,1,46039.49,1,38.51,2.548,211.2421698,8.106
```

## Data Sources

- **Kaggle**: [Walmart Store Sales Forecasting](https://www.kaggle.com/c/walmart-recruiting-store-sales-forecasting)
- **Alternative**: Any retail sales data with similar schema

## Data Requirements

- **Minimum rows**: 1000+ for meaningful training
- **Time span**: At least 6 months of data
- **Stores**: Multiple store locations
- **Format**: CSV with header row

## Notes

- The pipeline automatically handles data cleaning and feature engineering
- Missing values are handled gracefully
- Date format is automatically detected and converted
- Economic indicators are optional but recommended for better predictions
