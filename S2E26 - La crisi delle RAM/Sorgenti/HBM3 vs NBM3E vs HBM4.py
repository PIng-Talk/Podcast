#################################################################################################
# Creating bar chart comparing HBM3, HBM3E, and HBM4 (estimated) for bandwidth and capacity     #
#                                                                                               #
# This script creates a bar chart to visually compare the bandwidth and capacity                #
# of HBM3, HBM3E, and HBM4 memory technologies.                                                 #
# Created by: Pietro Boccadoro                                                                  #
# Date: 28/02/2026                                                                              #
# email: pingtalkofficial[at]gmail[dot]com                                                      #
#                                                                                               #
# Note: Ensure you have matplotlib installed in your Python environment to run this script.     #
# The resulting chart will be saved as 'hbm3_3E_4_comparison_chart_case_A.png' in the current   #
# directory.                                                                                    #
# For any questions or issues, please contact the author.                                       #
#################################################################################################


# Import necessary libraries
import matplotlib.pyplot as plt # For plotting
import numpy as np # For numerical operations and array handling
import os # For file path handling

# Data for HBM3, HBM3E, and estimated HBM4
def case_A():
    # Data
    technologies = ['HBM3', 'HBM3E', 'HBM4 (est.)'] # Memory technologies
    bandwidth = [819.2, 1024, 1280]  # in GB/s
    capacity = [16, 16, 24]  # in GB

    x = np.arange(len(technologies))  # label locations
    width = 0.35  # width of the bars

    # Plotting
    # Use seaborn style for better aesthetics and create a figure and axis for the bar chart. The figure size is set to 10 inches by 6 inches.
    plt.style.use('seaborn-v0_8')
    # Create a figure and axis for the bar chart with the specified figure size. The bars for bandwidth and capacity are plotted with different colors and labels for the legend. 
    fig, ax = plt.subplots(figsize=(10, 6))
    # Plot bandwidth on the primary y-axis (ax) with a bar width and color steelblue. The bars are positioned to the left of the center (x - width/2).
    bars1 = ax.bar(x - width/2, bandwidth, width, label='Bandwidth (GB/s)', color='#1f77b4')
    # Plot capacity on the same axis (ax) with a bar width and color darkorange. The bars are positioned to the right of the center (x + width/2).
    bars2 = ax.bar(x + width/2, capacity, width, label='Capacity (GB)', color='#ff7f0e')

    # Labels and formatting
    # Set the y-axis label, title, x-axis ticks and labels, legend, and grid for better readability. The y-axis label is set to 'Value', and the title describes the comparison being made. The x-axis ticks are set to the positions defined in x, with labels corresponding to the technologies. A legend is added to differentiate between bandwidth and capacity bars, and a grid is added along the y-axis for easier value estimation.
    ax.set_ylabel('Value')
    # Set the title of the plot and the x-axis ticks and labels. The title is set to 'Comparison of HBM3, HBM3E, and HBM4 (Estimated - Conservative)', and the x-axis ticks are set to the positions defined in x, with labels corresponding to the technologies.
    ax.set_title('Comparison of HBM3, HBM3E, and HBM4 (Estimated - Conservative)')
    # Set x-axis ticks to the positions defined in x and label them with the corresponding technologies (HBM3, HBM3E, and HBM4 (est.)).
    ax.set_xticks(x)
    # Set the x-axis tick labels to the names of the technologies (HBM3, HBM3E, and HBM4 (est.)).
    ax.set_xticklabels(technologies)
    # Add a legend to differentiate between bandwidth and capacity bars, and add a grid along the y-axis for better readability.
    ax.legend()
    # Add a grid along the y-axis with dashed lines and a certain level of transparency for better readability.
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)

    # Annotate bars
    # Add annotations on top of the bars to display their values. The height of each bar is obtained, and an annotation is placed slightly above the bar with the corresponding value. The annotations are centered horizontally and positioned just above the top of the bars for better visibility.
    for bar in bars1 + bars2:
        # Get the height of the current bar to determine where to place the annotation.
        height = bar.get_height()
        # Annotate the bar with its height value. The annotation is placed at the center of the bar's width and slightly above the top of the bar (height) with a small offset (3 points). The text is horizontally centered and vertically aligned to the bottom of the annotation for better visibility.
        ax.annotate(f'{height}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

    # Save plot
    # Create the HBM subfolder if it does not exist
    hbm_folder = os.path.join(os.path.dirname(__file__), "../HBM")
    os.makedirs(hbm_folder, exist_ok=True)
    # Save the generated plot to a file named 'hbm3_3E_4_comparison_chart_case_A.png' in the current directory. The tight_layout() function is called to ensure that the layout of the plot is adjusted to prevent overlap of elements before saving.
    output_path = os.path.join(hbm_folder, "hbm3_3E_4_comparison_chart_case_A.png")
    # Adjust the layout to prevent overlap of elements and save the figure to the specified output path.
    plt.tight_layout()
    # Save the figure to the specified output path.
    plt.savefig(output_path)

    # Display the plot
    print("Generated chart for Case A (Conservative).")


# The following functions (case_B and case_C) are similar to case_A but with different data for bandwidth and capacity to represent aggressive and maximum estimates for HBM4. The structure of the code is the same, with adjustments to the data, titles, and output file names accordingly.
def case_B():
    # Stima aggressiva (roadmap industriali)
    technologies = ['HBM3', 'HBM3E', 'HBM4 (est. agg.)'] # Memory technologies
    bandwidth = [819.2, 1024, 1600]  # in GB/s
    capacity = [16, 16, 32]  # in GB

    # Create figure and axes, plot bars, set labels, title, legend, and grid. The bars for bandwidth and capacity are plotted with different colors and labels for the legend. Annotations are added on top of the bars to display their values. The layout is adjusted to prevent overlap of elements before saving the figure to a file named 'hbm3_3E_4_comparison_chart_case_B.png' in the current directory.
    x = np.arange(len(technologies)) # label locations
    width = 0.35 # width of the bars

    # Use seaborn style for better aesthetics and create a figure and axis for the bar chart. The figure size is set to 10 inches by 6 inches.
    plt.style.use('seaborn-v0_8')
    # Create a figure and axis for the bar chart with the specified figure size. The bars for bandwidth and capacity are plotted with different colors and labels for the legend.
    fig, ax = plt.subplots(figsize=(10, 6))
    # Plot bandwidth on the primary y-axis (ax) with a bar width and color steelblue. The bars are positioned to the left of the center (x - width/2). Plot capacity on the same axis (ax) with a bar width and color darkorange. The bars are positioned to the right of the center (x + width/2).
    bars1 = ax.bar(x - width/2, bandwidth, width, label='Bandwidth (GB/s)', color='#2ca02c')
    # Plot capacity on the same axis (ax) with a bar width and color darkorange. The bars are positioned to the right of the center (x + width/2).
    bars2 = ax.bar(x + width/2, capacity, width, label='Capacity (GB)', color='#98df8a')

    # Set the y-axis label, title, x-axis ticks and labels, legend, and grid for better readability. The y-axis label is set to 'Value', and the title describes the comparison being made. The x-axis ticks are set to the positions defined in x, with labels corresponding to the technologies. A legend is added to differentiate between bandwidth and capacity bars, and a grid is added along the y-axis for easier value estimation.
    ax.set_ylabel('Value')
    # Set the title of the plot and the x-axis ticks and labels. The title is set to 'Comparison of HBM3, HBM3E, and HBM4 (Estimated - Aggressive)', and the x-axis ticks are set to the positions defined in x, with labels corresponding to the technologies.
    ax.set_title('Comparison of HBM3, HBM3E, and HBM4 (Estimated - Aggressive)')
    # Set x-axis ticks to the positions defined in x and label them with the corresponding technologies (HBM3, HBM3E, and HBM4 (est. agg.)).
    ax.set_xticks(x)
    # Set the x-axis tick labels to the names of the technologies (HBM3, HBM3E, and HBM4 (est. agg.)).
    ax.set_xticklabels(technologies)
    # Add a legend to differentiate between bandwidth and capacity bars, and add a grid along the y-axis for better readability.
    ax.legend()
    # Add a grid along the y-axis with dashed lines and a certain level of transparency for better readability.
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)

    # Annotate bars
    for bar in bars1 + bars2:
        # Get the height of the current bar to determine where to place the annotation.
        height = bar.get_height()
        # Annotate the bar with its height value. The annotation is placed at the center of the bar's width and slightly above the top of the bar (height) with a small offset (3 points). The text is horizontally centered and vertically aligned to the bottom of the annotation for better visibility.
        ax.annotate(f'{height}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

    # Save plot
    # Create the HBM subfolder if it does not exist
    hbm_folder = os.path.join(os.path.dirname(__file__), "../HBM")
    os.makedirs(hbm_folder, exist_ok=True)

    # Modifica il percorso di output per salvare nella cartella di livello superiore
    # Save the generated plot to a file named 'hbm3_3E_4_comparison_chart_case_B.png' in the current directory. The tight_layout() function is called to ensure that the layout of the plot is adjusted to prevent overlap of elements before saving.
    output_path = os.path.join(os.path.dirname(__file__), hbm_folder, "hbm3_3E_4_comparison_chart_case_B.png")
    # Adjust the layout to prevent overlap of elements and save the figure to the specified output path.
    plt.tight_layout()
    # Save the figure to the specified output path.
    plt.savefig(output_path)

    # Display the plot
    print("Generated chart for Case B (Aggressive).")


# The following function (case_C) is similar to case_A and case_B but with different data for bandwidth and capacity to represent the maximum estimate for HBM4. The structure of the code is the same, with adjustments to the data, titles, legend labels, and output file name accordingly.
def case_C():
    # Maximum estimate (best-case scenario)
    technologies = ['HBM3', 'HBM3E', 'HBM4 (est. max)'] # Memory technologies
    bandwidth = [819.2, 1024, 2000]  # in GB/s
    capacity = [16, 16, 48]  # in GB

    # Create figure and axes, plot bars, set labels, title, legend, and grid. The bars for bandwidth and capacity are plotted with different colors and labels for the legend. Annotations are added on top of the bars to display their values. The layout is adjusted to prevent overlap of elements before saving the figure to a file named 'hbm3_3E_4_comparison_chart_case_C.png' in the current directory.
    x = np.arange(len(technologies))
    # Set the width of the bars for the bar chart.
    width = 0.35

    # Use seaborn style for better aesthetics and create a figure and axis for the bar chart. The figure size is set to 10 inches by 6 inches.
    plt.style.use('seaborn-v0_8')
    # Create a figure and axis for the bar chart with the specified figure size. The bars for bandwidth and capacity are plotted with different colors and labels for the legend.
    fig, ax = plt.subplots(figsize=(10, 6))
    # Plot bandwidth on the primary y-axis (ax) with a bar width and color steelblue. The bars are positioned to the left of the center (x - width/2). Plot capacity on the same axis (ax) with a bar width and color darkorange. The bars are positioned to the right of the center (x + width/2).
    bars1 = ax.bar(x - width/2, bandwidth, width, label='Bandwidth (GB/s)', color='#006400')
    # Plot capacity on the same axis (ax) with a bar width and color darkorange. The bars are positioned to the right of the center (x + width/2).
    bars2 = ax.bar(x + width/2, capacity, width, label='Capacity (GB)', color='#32cd32')

    # Set the y-axis label, title, x-axis ticks and labels, legend, and grid for better readability. The y-axis label is set to 'Value', and the title describes the comparison being made. The x-axis ticks are set to the positions defined in x, with labels corresponding to the technologies. A legend is added to differentiate between bandwidth and capacity bars, and a grid is added along the y-axis for easier value estimation.
    ax.set_ylabel('Value')
    # Set the title of the plot and the x-axis ticks and labels. The title is set to 'Comparison of HBM3, HBM3E, and HBM4 (Estimated - Maximum)', and the x-axis ticks are set to the positions defined in x, with labels corresponding to the technologies.
    ax.set_title('Comparison of HBM3, HBM3E, and HBM4 (Estimated - Maximum)')
    # Set x-axis ticks to the positions defined in x and label them with the corresponding technologies (HBM3, HBM3E, and HBM4 (est. max)).
    ax.set_xticks(x)
    # Set the x-axis tick labels to the names of the technologies (HBM3, HBM3E, and HBM4 (est. max)).
    ax.set_xticklabels(technologies)
    # Add a legend to differentiate between bandwidth and capacity bars, and add a grid along the y-axis for better readability.
    ax.legend()
    # Add a grid along the y-axis with dashed lines and a certain level of transparency for better readability.
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)

    # Annotate bars
    for bar in bars1 + bars2:
        # Get the height of the current bar to determine where to place the annotation.
        height = bar.get_height()
        # Annotate the bar with its height value. The annotation is placed at the center of the bar's width and slightly above the top of the bar (height) with a small offset (3 points). The text is horizontally centered and vertically aligned to the bottom of the annotation for better visibility.
        ax.annotate(f'{height}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

    # Save plot
    # Create the HBM subfolder if it does not exist
    hbm_folder = os.path.join(os.path.dirname(__file__), "../HBM")
    os.makedirs(hbm_folder, exist_ok=True)

    # Modify the output path to save in the parent directory
    output_path = os.path.join(os.path.dirname(__file__), hbm_folder, "hbm3_3E_4_comparison_chart_case_C.png")
    # Adjust the layout to prevent overlap of elements and save the figure to the specified output path.
    plt.tight_layout()
    # Save the figure to the specified output path.
    plt.savefig(output_path)

    # Display the plot
    print("Generated chart for Case C (Maximum).")

# Main function to execute the cases
def main():
    # Execute each case to generate the corresponding charts for HBM3, HBM3E, and HBM4 comparisons.
    # Each case represents a different estimation scenario for HBM4, allowing for a comprehensive comparison across conservative, aggressive, and maximum estimates.
    # The generated charts will be saved in the parent directory with distinct file names for each case.
    # The main function serves as the entry point for the script, orchestrating the execution of the different cases to produce the desired visual comparisons.
    # By running this script, users will obtain three separate bar charts that illustrate the differences in bandwidth and capacity among HBM3, HBM3E, and HBM4 under various estimation scenarios, providing valuable insights into the potential advancements in memory technology.
    
    # First case: Conservative estimate for HBM4, based on current trends and conservative projections from industry roadmaps. This case assumes a moderate improvement in bandwidth and capacity compared to HBM3E, reflecting a cautious outlook on the advancements in memory technology.
    case_A()
    # Second case: Aggressive estimate for HBM4, based on optimistic projections from industry roadmaps and potential breakthroughs in memory technology. This case assumes a significant improvement in bandwidth and capacity compared to HBM3E, reflecting an optimistic outlook on the advancements in memory technology.
    case_B()
    # Third case: Maximum estimate for HBM4, representing a best-case scenario where HBM4 achieves the highest possible improvements in bandwidth and capacity compared to HBM3E. This case assumes a substantial leap in memory technology, showcasing the potential maximum advancements that could be achieved with HBM4.
    case_C()

if __name__ == "__main__":
    main()