# MyStreamlitapp


Global Literacy and Socioeconomic Dashboard

## Overview
The Global Literacy and Socioeconomic Dashboard is an interactive web application built with Python and Streamlit. This application allows users to explore, filter, and visualize global literacy rates across countries. It is designed to demonstrate data analysis, reactive state management, and data visualization principles using clean code architecture.

## Features
* **Interactive Controls:** Filter countries dynamically using a sidebar slider based on minimum literacy rate thresholds.
* **Data Visualizations:** Dynamic Plotly bar charts featuring customizable color scales, tooltips, and axis labels.
* **Summary Metrics:** Top-level KPI metrics calculating total records analyzed and average global literacy rates.
* **Raw Data Inspector:** An optional checkbox to toggle and view the underlying raw data table.

## Project Structure
```text
├── app.py                      # Main Streamlit application script
├── requirements.txt            # Python dependencies and package versions
├── cross-country-literacy-rates.csv # Local dataset containing global literacy metrics
└── README.md                   # Project documentation
