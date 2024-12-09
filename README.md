# Typical Meteorological Year (TMY) Generator

This project provides a Python-based solution for generating a **Typical Meteorological Year (TMY)** dataset using solar radiation data. The TMY dataset identifies representative months for a year by comparing the absolute differences in cumulative distribution functions (CDFs) of solar radiation values across multiple years. The representative year for each month is determined based on the minimum Finkelstein-Schafer (FS) statistic.

## Features
- Processes raw solar radiation data for multiple years (e.g., 2019–2023) into a structured format.
- Computes the daily and long-term averages of solar radiation.
- Calculates cumulative distribution functions (CDFs) for each year and the long-term average.
- Identifies representative years for each month based on the minimum FS statistic.
- Outputs a monthly representative year dataset, including average solar radiation for each month.
- Saves the results to a CSV file, dynamically named based on the state data.

---

## How It Works

1. **Input**: The input is a CSV file containing hourly solar radiation data for multiple years.
2. **Processing**: The script:
   - Processes the raw data into a structured format with columns for Day, Hour, and solar radiation values for each year.
   - Calculates long-term averages, daily averages, and CDFs for each year and the long-term dataset.
3. **Representative Year Calculation**:
   - For each month, calculates the absolute difference between the long-term CDF and yearly CDFs.
   - Identifies the representative year for each month based on the minimum total absolute difference (FS statistic).
4. **Output**: A CSV file with the representative year and average solar radiation for each month, named dynamically based on the state name.

---

## Requirements

- Python 3.7 or higher
- Required Python libraries:
  - `pandas`

Install the required libraries using:
```bash
pip install pandas
