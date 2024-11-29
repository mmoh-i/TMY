import pandas as pd
import matplotlib.pyplot as plt

def process_solar_data(input_file, output_file):
    """
    Process solar radiation data, converting the date and hour columns
    into a unified datetime format, handling February 29, and splitting
    the date into independent columns.
    """
    data = pd.read_csv(input_file)
    
    processed_data = []
    current_date = None

    def is_leap_year(year):
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    
    for idx, row in data.iterrows():
        if isinstance(row.iloc[0], str) and '-' in row.iloc[0]:
            current_date = row.iloc[0]
        else:
            hour = int(row.iloc[0])
            for year, value in zip(range(2019, 2024), row.iloc[1:]):
                try:
                    full_date = pd.to_datetime(f"{current_date} {year}", format="%d-%b %Y") + pd.to_timedelta(hour, unit='h')
                    
                    if not is_leap_year(year) and full_date.strftime('%m-%d') == '02-29':
                        value = 0
                    
                    processed_row = {
                        'Year': year,
                        'Month': full_date.month,
                        'Day': full_date.day,
                        'Hour': full_date.hour,
                        'Solar Radiation': value
                    }
                    processed_data.append(processed_row)
                except ValueError:
                    print(f"Invalid date detected: {current_date} for year {year}. Skipping...")
                    continue
    
    processed_df = pd.DataFrame(processed_data)
    processed_df.to_csv(output_file, index=False)
    print(f"Processed data saved as {output_file}")
    
    return processed_df

def calculate_tmm(processed_data):
    """
    Calculate the Typical Meteorological Month (TMM) using improved 
    Finkelstein-Schafer statistics.
    """
    tmm_results = []

    for month in range(1, 13):
        month_data = processed_data[processed_data['Month'] == month]
        years = [2019, 2020, 2021, 2022, 2023]
        
        long_term_hourly_avg = month_data.groupby('Hour')['Solar Radiation'].mean()
        
        fs_statistics = {}
        
        for year in years:
            year_data = month_data[month_data['Year'] == year]
            year_hourly_avg = year_data.groupby('Hour')['Solar Radiation'].mean()
            
            cdf_diff = abs(
                (long_term_hourly_avg.values - year_hourly_avg.values) / 
                (long_term_hourly_avg.values.max() - long_term_hourly_avg.values.min() + 1e-10)  # Prevent division by zero
            )
            
            fs_stat = sum(cdf_diff)
            fs_statistics[year] = fs_stat
        
        representative_year = min(fs_statistics, key=fs_statistics.get)
        
        representative_data = month_data[month_data['Year'] == representative_year]
        avg_solar_radiation = representative_data['Solar Radiation'].mean()

        tmm_results.append({
            'Month': month,
            # '': [i for i in ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")],
            'Representative Year': representative_year,
            'Average Solar Radiation (MJ/m²)': round(avg_solar_radiation, 2)
        })

    tmm_data = pd.DataFrame(tmm_results)
    return tmm_data

def calculate_tmy(tmm_data, processed_data):
    """
     Typical Meteorological Year (TMY) by combining TMM data.
    """
    tmy_data_list = []

    for _, row in tmm_data.iterrows():
        month = row['Month']
        year = row['Representative Year']
        
        month_data = processed_data[
            (processed_data['Month'] == month) & 
            (processed_data['Year'] == year)
        ]
        tmy_data_list.append(month_data)
    
    tmy_data = pd.concat(tmy_data_list, ignore_index=True)
    return tmy_data

def visualize_tmy_comparison(processed_data, tmy_data):
    """
    Visualize the comparison between original data and TMY
    """
    plt.figure(figsize=(15, 10))
    
    # Plot original data monthly averages
    original_monthly_avg = processed_data.groupby(['Month', 'Year'])['Solar Radiation'].mean().reset_index()
    
    # Plot TMY monthly averages
    tmy_monthly_avg = tmy_data.groupby('Month')['Solar Radiation'].mean()
    
    # Scatter plot for original data
    for year in range(2019, 2024):
        year_data = original_monthly_avg[original_monthly_avg['Year'] == year]
        plt.scatter(year_data['Month'], year_data['Solar Radiation'], 
                    label=f'Original {year}', alpha=0.7)
    
    # Line plot for TMY
    plt.plot(tmy_monthly_avg.index, tmy_monthly_avg.values, 
             color='red', linewidth=3, label='TMY')
    
    plt.title('Monthly Solar Radiation: Original vs Typical Meteorological Year')
    plt.xlabel('Month')
    plt.ylabel('Average Solar Radiation')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Main execution
state_name = "Abuja"
input_file = "Abuja Solar Radiation Data.csv"  
processed_output_file = f"processed_{state_name}_solar_data.csv"
tmm_output_file = f"tmm_results_{state_name}.csv"
tmy_output_file = f"tmy_{state_name}.csv"

# Step 1: Process Solar Data
processed_data = process_solar_data(input_file, processed_output_file)

# Step 2: Calculate Typical Meteorological Month (TMM)
tmm_data = calculate_tmm(processed_data)
print("Typical Meteorological Month (TMM) Results:")
print(tmm_data)
tmm_data.to_csv(tmm_output_file, index=False)

# Step 3: Generate Typical Meteorological Year (TMY)
tmy_data = calculate_tmy(tmm_data, processed_data)
tmy_data.to_csv(tmy_output_file, index=False)

# Visualization
# visualize_tmy_comparison(processed_data, tmy_data)

# Additional Debugging: Print detailed monthly comparisons
# def debug_year_comparison(processed_data):
#     """
#     Debug function to compare yearly solar radiation distributions
#     """
#     for month in range(1, 13):
#         month_data = processed_data[processed_data['Month'] == month]
#         print(f"\nMonth {month} Yearly Comparisons:")
#         for year in [2019, 2020, 2021, 2022, 2023]:
#             year_data = month_data[month_data['Year'] == year]
#             print(f"Year {year}:")
#             print(f"  Mean Solar Radiation: {year_data['Solar Radiation'].mean():.2f}")
#             print(f"  Std Dev: {year_data['Solar Radiation'].std():.2f}")

# # debugging function
# debug_year_comparison(processed_data)