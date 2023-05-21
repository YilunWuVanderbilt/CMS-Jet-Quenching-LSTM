import numpy as np
import matplotlib.pyplot as plt
from TrkEff2018PbPb import*

trkEff = TrkEff2018PbPb("general", "", False, "./Table/")
#eta_values = [0, 0.3, 0.6, 0.9, 1.2, 1.5, 1.8, 2.1]
eta_values = [2.1, 1.8, 1.5, 1.2, 0.9, 0.6, 0.3, 0]
centrality_values = [0, 10, 20, 30, 40, 50, 60, 70]

# Create a 2D array to store the data for the heat map
data = np.zeros((8, 8))
i = 0
for eta in eta_values: 
    j = 0
    for cent in centrality_values:
        #correction = trkEff.getCorrection(1.0, eta+0.15, (cent+5)*2)
        data[i, j] =trkEff.getEfficiency(1.0, eta+0.15, (cent+5)*2)
        # print(trkEff.getEfficiency(1.0, eta, hiBin*2))
        j = j+1
    i = i+1

# Define the number of bins for eta and hiBin
eta_bins = np.linspace(0.15, 2.25, 8)  # 8 bins for eta
hiBin_bins = np.linspace(5, 75, 8)  # 8 bins for hiBin

# Create a figure and axis
fig, ax = plt.subplots()

# Create the heat map
heatmap = ax.imshow(data, cmap='pink', extent=[0, 80, 0, 2.4])

ax.set_aspect('auto')

# Add a colorbar
cbar = plt.colorbar(heatmap)

# Add numbers to each square
for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        # Add the value as text at the center of each square
        ax.text(hiBin_bins[j], eta_bins[7-i], f'{data[i, j]:.2f}', 
                ha='center', va='center', color='black')

# Show the plot
plt.savefig('PbPbEfficiency.png')
