import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt
#input your path here
path = '     '
mat = sio.loadmat(path)
print(mat.keys())
battery = mat['B0005']
cycles = battery['cycle'][0][0][0]
discharge_cycles = []
capacities = []

for cycle in cycles:
    cycle_type = cycle['type'][0]
    
    if cycle_type == 'discharge':
        data = cycle['data'][0][0]
        capacity = data['Capacity'][0][0]
        
        discharge_cycles.append(data)
        capacities.append(capacity)
        cycle_index = np.arange(1, len(capacities) + 1)

plt.figure()
plt.plot(cycle_index, capacities)
plt.xlabel('Cycle number')
plt.ylabel('Discharge Capacity (Ah)')
plt.title('Capacity Degradation of Battery B0005')
plt.grid(True)
plt.show()