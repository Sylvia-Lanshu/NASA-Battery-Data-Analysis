import scipy.io
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# --- 1. configuration path (in accordance with your request) ---
# input file path
MAT_FILE_PATH = r'______'

# out put file path (the generated CSV file will be saved here)
OUTPUT_DIR = r'_______'
OUTPUT_CSV_NAME = 'B0005_Cleaned.csv'
OUTPUT_PATH = os.path.join(OUTPUT_DIR, OUTPUT_CSV_NAME)


# peeling onions，locate the core data layer
battery_data = data['B0005'][0][0][0][0]

# --- 3. prepare the storage list ---
cleaned_data = []
RATED_CAPACITY = 2.0  # rated capacity in Ah


# --- 4. perform each operation in a loop ---
for i, cycle in enumerate(battery_data):
    operation_type = cycle[0][0]
    
    if operation_type == 'discharge':
        # extract metadata
        # ambient_temp = cycle[1][0][0]
        # date_time = cycle[2][0]
        
        # extract the core measurement data
        measurements = cycle[3][0][0]
        
        # obtain the sequences of voltage,current,time and temperature
        voltage_seq = measurements['Voltage_measured'][0]
        current_seq = measurements['Current_measured'][0]
        time_seq = measurements['Time'][0]
        temp_seq = measurements['Temperature_measured'][0]
        
        # NASA :Ground Truth
        try:
            nasa_capacity = measurements['Capacity'][0][0]
        except:
            nasa_capacity = 0
            
      
        calculated_capacity = np.trapezoid(np.abs(current_seq), time_seq) / 3600.0
        
        # --- calculate SOH ---
        soh = (nasa_capacity / RATED_CAPACITY) * 100
        
        # --- add to the list ---
        cleaned_data.append({
            'Cycle_Index': i + 1, # original cycyle index
            'SOH': soh,
            'Capacity_NASA': nasa_capacity,
            'Capacity_Calculated': calculated_capacity,
            'Error_Diff': nasa_capacity - calculated_capacity, # error difference
            'Temp_Avg': np.mean(temp_seq),
            'Voltage_End': voltage_seq[-1], # cut off voltage
            'Time_End': time_seq[-1]
        })

# --- 5.transform into   DataFrame  ---
df_clean = pd.DataFrame(cleaned_data)

# filter out the invalid test data 
df_clean = df_clean[df_clean['Capacity_NASA'] > 0.1]

#regenerate the cycle index after filtering
df_clean['Cycle'] = range(1, len(df_clean) + 1)

# --- 6.save as  CSV ---
try:
    df_clean.to_csv(OUTPUT_PATH, index=False)
except Exception as e:
# --- 7. draw a graph to verify ---
plt.figure(figsize=(12, 6))

plt.plot(df_clean['Cycle'], df_clean['Capacity_NASA'], 
         'b-', label='NASA Ground Truth (Lab)', linewidth=2, alpha=0.7)

plt.plot(df_clean['Cycle'], df_clean['Capacity_Calculated'], 
         'r--', label='My Algorithm (Coulomb Counting)', linewidth=2)

plt.title('Validation: My Code vs NASA Data')
plt.xlabel('Cycle Number')
plt.ylabel('Capacity (Ah)')
plt.legend()
plt.grid(True)
plt.show()
