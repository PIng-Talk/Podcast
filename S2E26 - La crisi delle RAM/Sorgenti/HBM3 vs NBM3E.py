#################################################################################################
# Generating bar chart comparing HBM3 and HBM3E bandwidth and capacities                        #
#                                                                                               #
# This script creates a bar chart to visually compare the bandwidth and capacity                #
# of HBM3 and HBM3E memory technologies.                                                        #
# Created by: Pietro Boccadoro                                                                  #
# Date: 28/02/2026                                                                              #
# email: pingtalkofficial[at]gmail[dot]com                                                      #
#                                                                                               #
# Note: Ensure you have matplotlib installed in your Python environment to run this script.     #
# The resulting chart will be saved as 'hbm3_3E_comparison.png' in the current directory.       #
# For any questions or issues, please contact the author.                                       #
#################################################################################################

# Import necessary libraries
import matplotlib.pyplot as plt # For plotting
import os # For file path handling

# Data
technologies = ['HBM3', 'HBM3E'] # Memory technologies
bandwidth = [819.2, 1024]  # in GB/s
capacity = [16, 16]        # in GB

# Create figure and axes
fig, ax1 = plt.subplots(figsize=(8, 5)) # Set figure size
plt.style.use('seaborn-v0_8') # Use seaborn style for better aesthetics

# Bar width and positions
bar_width = 0.35 # Width of the bars
x = range(len(technologies)) # X-axis positions for the bars

# Plot bandwidth
# The first set of bars (bandwidth) is plotted on the primary y-axis (ax1) and colored steelblue.
ax1.bar([i - bar_width/2 for i in x], bandwidth, width=bar_width, label='Bandwidth (GB/s)', color='steelblue')
# Set the y-axis label for bandwidth and color it steelblue to match the bars. Also, set the tick parameters to color the y-axis labels accordingly.
ax1.set_ylabel('Bandwidth (GB/s)', color='steelblue')
# Set the tick parameters for the y-axis to color the labels in steelblue, matching the bandwidth bars.
ax1.tick_params(axis='y', labelcolor='steelblue')

# Create second y-axis for capacity
# The second set of bars (capacity) is plotted on a secondary y-axis (ax2) that shares the same x-axis. The bars are colored darkorange.
ax2 = ax1.twinx()
# Plot capacity on the secondary y-axis (ax2) with a bar width and color darkorange. The bars are positioned to the right of the bandwidth bars.
ax2.bar([i + bar_width/2 for i in x], capacity, width=bar_width, label='Capacity (GB)', color='darkorange')
# Set the y-axis label for capacity and color it darkorange to match the bars. Also, set the tick parameters to color the y-axis labels accordingly.
ax2.set_ylabel('Capacity (GB)', color='darkorange')
# Set the tick parameters for the y-axis to color the labels in darkorange, matching the capacity bars.
ax2.tick_params(axis='y', labelcolor='darkorange')

# Titles and labels
# Set the title of the plot and the x-axis ticks and labels. The title is set to 'Comparison of HBM3 vs HBM3E', and the x-axis ticks are set to the positions defined in x, with labels corresponding to the technologies.
plt.title('Comparison of HBM3 vs HBM3E')
# Set x-axis ticks to the positions defined in x and label them with the corresponding technologies (HBM3 and HBM3E).
ax1.set_xticks(x)
# Set the x-axis tick labels to the names of the technologies (HBM3 and HBM3E).
ax1.set_xticklabels(technologies)

# Save plot
# Create the HBM subfolder if it does not exist
hbm_folder = os.path.join(os.path.dirname(__file__), "../HBM")
os.makedirs(hbm_folder, exist_ok=True)

# Save the generated plot inside the HBM subfolder
output_path = os.path.join(hbm_folder, "hbm3_3E_comparison.png")

# Adjust layout and save the figure
plt.tight_layout()
plt.savefig(output_path)


# Display the plot
print("Created bar chart comparing HBM3 and HBM3E bandwidth and capacity, saved as hbm_comparison.png")