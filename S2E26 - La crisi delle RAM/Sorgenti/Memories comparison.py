#################################################################################################
# Generating graphs to compare different memories usign relevan KPIs                            #
#                                                                                               #
# This script creates a series of graphs to visually compare the bandwidth, capacity, latency,  #
# and cost of various memory technologies, including DDR4, DDR5, HBM3, and HBM4. The script     #
# also generates a radar chart to provide a comprehensive comparison across multiple metrics.   #
# Additionally, it includes a specific cost comparison for HBM generations.                     #
# All generated charts are saved as PNG files in a designated folder, and metadata about the    #
# charts is exported as a JSON file for reference.                                              #
#                                                                                               #
# Created by: Pietro Boccadoro                                                                  #
# Date: 25/03/2026                                                                              #
# email: pingtalkofficial[at]gmail[dot]com                                                      #
#                                                                                               #
# Note: Ensure you have matplotlib installed in your Python environment to run this script.     #
# The resulting graphs will be saved in the 'Memories comparison - charts/' folder, and         #
# metadata will be saved as 'memories_comparison_metadata.json' within the same folder.         #
# For any questions or issues, please contact the author.                                       #
#################################################################################################


# ============================================================
# LIBRARIES IMPORT
# ============================================================

import pandas as pd                     # Used for creating and manipulating DataFrames
import matplotlib.pyplot as plt         # Base plotting library
import seaborn as sns                   # High-level plotting library built on Matplotlib
import numpy as np                      # Used for numerical operations (needed for radar chart)
import json                             # Used to export metadata as JSON
import os                               # Used for directory and file handling

sns.set(style="whitegrid")              # Set a clean visual style for all charts


# ============================================================
# DATA CREATION FUNCTIONS
# ============================================================

def create_main_dataframe():
    """
    Creates the main dataset for DDR4, DDR5, HBM3 and HBM4.
    Latency values:
    - DDR4 / DDR5: derived from official JEDEC/vendor timing (tCK * CL)
    - HBM3 / HBM4: estimated values (explicitly marked as estimates)
    """
    data = {                                            # Create a dictionary containing all metrics
        "Technology": ["DDR4", "DDR5", "HBM3", "HBM4"], # Names of memory technologies
        "Generation": ["DDR4", "DDR5", "HBM3", "HBM4_est"],  # Labels including "est" for estimated values
        "Bandwidth_GBs": [28, 70, 900, 1800],           # Bandwidth per unit in GB/s
        "Capacity_GB": [32, 64, 24, 48],                # Capacity per unit in GB
        "Latency_ns": [                                 # Latency in nanoseconds
            13.75,  # DDR4-3200: official timing (tCK=0.625ns, CL=22)
            15.0,   # DDR5-4800: official timing (tCK=0.417ns, CL=36)
            30.0,   # HBM3: estimated (no JEDEC official ns value)
            28.0    # HBM4: estimated roadmap value
        ],
        "Cost_per_MB_index": [1.0, 1.1, 7.0, 9.0]       # Cost index (not monetary)
    }
    return pd.DataFrame(data)                           # Convert dictionary to DataFrame and return it


def create_hbm_cost_dataframe():
    """
    Creates a dataset with real monetary cost per GB (USD) for HBM generations.
    Based on structured market analysis data (not vendor list prices).
    """
    data = {                                            # Create dictionary with HBM cost data
        "Technology": ["HBM2e", "HBM3", "HBM3E", "HBM4_est"],  # HBM generations
        "Capacity_GB": [16, 24, 36, 48],                # Capacity per stack
        "Stack_cost_USD": [120, 200, 300, 500],         # Cost per stack in USD
        "Cost_per_GB_USD": [7.50, 8.33, 8.33, 10.42]    # Cost per GB in USD
    }
    return pd.DataFrame(data)                           # Convert dictionary to DataFrame and return it


# ============================================================
# FILE SAVING + METADATA EXPORT
# ============================================================

def save_png(fig, base_name):
    """
    Saves a PNG file with the naming convention:
    'Memories comparison - <metric>.png'
    """
    if not os.path.exists("Memories comparison - charts"):                    # Check if output folder exists
        os.makedirs("Memories comparison - charts")                           # Create folder if missing

    final_name = f"Memories comparison - {base_name}.png"  # Build final filename
    fig.savefig(f"Memories comparison - charts/{final_name}", dpi=300, bbox_inches="tight")  # Save figure as PNG
    return final_name                                   # Return filename for metadata storage


def save_metadata(metadata_dict):
    """
    Saves a JSON file containing metadata for all generated charts.
    """
    if not os.path.exists("Memories comparison - charts"):                    # Ensure output folder exists
        os.makedirs("Memories comparison - charts")

    with open("Memories comparison - charts/memories_comparison_metadata.json", "w") as f:  # Open JSON file for writing
        json.dump(metadata_dict, f, indent=4)           # Write metadata dictionary to JSON file


# ============================================================
# GENERIC BAR CHART FUNCTION
# ============================================================

def bar_chart(df, column, title, ylabel, palette, filename):
    fig, ax = plt.subplots(figsize=(7, 5))              # Create a figure and axis

    sns.barplot(                                        # Draw a bar chart
        data=df,
        x="Technology",
        y=column,
        palette=palette,
        ax=ax
    )

    ax.set_title(title)                                 # Set chart title
    ax.set_xlabel("Technology")                         # Label X-axis
    ax.set_ylabel(ylabel)                               # Label Y-axis

    for p in ax.patches:                                # Loop through bars to add labels
        value = p.get_height()                          # Get bar height
        label = f"{value:.2f}" if value < 10 else f"{value:.0f}"  # Format label
        ax.annotate(                                     # Add label above bar
            label,
            (p.get_x() + p.get_width() / 2, value),
            ha="center",
            va="bottom",
            fontsize=9
        )

    saved_file = save_png(fig, filename)                # Save chart as PNG
    plt.close(fig)                                      # Close figure to free memory
    return saved_file                                   # Return filename for metadata


# ============================================================
# LATENCY CHART (NANOSECONDS)
# ============================================================

def latency_chart(df):
    """
    Latency chart in nanoseconds.
    DDR4/DDR5 = official timing-derived values
    HBM3/HBM4 = estimates (annotated)
    """
    fig, ax = plt.subplots(figsize=(7, 5))              # Create figure and axis

    sns.barplot(                                        # Draw bar chart
        data=df,
        x="Technology",
        y="Latency_ns",
        palette="Oranges",
        ax=ax
    )

    ax.set_title("Memory Access Latency (ns)\nDDR4/DDR5: official timing • HBM3/HBM4: estimates")  
    ax.set_xlabel("Technology")                         # Label X-axis
    ax.set_ylabel("Latency [ns]")                       # Label Y-axis

    for p, tech in zip(ax.patches, df["Technology"]):   # Loop through bars and tech names
        value = p.get_height()                          # Get bar height
        label = f"{value:.2f} ns"                       # Base label
        if tech.startswith("HBM"):                      # Mark estimated values
            label += " (est.)"
        ax.annotate(                                    # Add label above bar
            label,
            (p.get_x() + p.get_width() / 2, value),
            ha="center",
            va="bottom",
            fontsize=9
        )

    saved_file = save_png(fig, "latency_ns")            # Save chart
    plt.close(fig)                                      # Close figure
    return saved_file                                   # Return filename


# ============================================================
# RADAR CHART
# ============================================================

def radar_chart(df):
    """
    Radar chart using normalized metrics:
    - Bandwidth
    - Capacity
    - Inverted latency
    - Inverted cost index
    """
    df_norm = pd.DataFrame()                            # Create new DataFrame for normalized values
    df_norm["Technology"] = df["Technology"]            # Copy technology names

    df_norm["Bandwidth_norm"] = df["Bandwidth_GBs"] / df["Bandwidth_GBs"].max()  # Normalize bandwidth
    df_norm["Capacity_norm"] = df["Capacity_GB"] / df["Capacity_GB"].max()       # Normalize capacity
    df_norm["Latency_inv"] = 1 / df["Latency_ns"]                                 # Invert latency
    df_norm["Cost_inv"] = 1 / df["Cost_per_MB_index"]                             # Invert cost index

    metrics = ["Bandwidth_norm", "Capacity_norm", "Latency_inv", "Cost_inv"]      # Metrics for radar
    N = len(metrics)                                      # Number of metrics
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()  # Compute angles
    angles += angles[:1]                                  # Close the radar loop

    fig = plt.figure(figsize=(7, 7))                      # Create figure
    ax = plt.subplot(111, polar=True)                     # Create polar axis

    for _, row in df_norm.iterrows():                     # Loop through each technology
        values = row[metrics].tolist()                    # Extract metric values
        values += values[:1]                              # Close the loop
        ax.plot(angles, values, linewidth=2, label=row["Technology"])  # Draw line
        ax.fill(angles, values, alpha=0.15)               # Fill area

    ax.set_xticks(angles[:-1])                            # Set axis labels
    ax.set_xticklabels(["Bandwidth", "Capacity", "Latency (inv.)", "Cost (inv.)"])

    ax.set_title("Normalized Memory Metrics Radar Chart", fontsize=14)  # Title
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))             # Legend

    saved_file = save_png(fig, "radar_chart")             # Save chart
    plt.close(fig)                                        # Close figure
    return saved_file                                     # Return filename


# ============================================================
# HBM COST CHART (USD/GB)
# ============================================================

def hbm_cost_chart(df_hbm):
    """
    Real monetary cost chart for HBM generations (USD/GB).
    """
    fig, ax = plt.subplots(figsize=(7, 5))                # Create figure and axis

    sns.barplot(                                          # Draw bar chart
        data=df_hbm,
        x="Technology",
        y="Cost_per_GB_USD",
        palette="Reds",
        ax=ax
    )

    ax.set_title("HBM Cost per GB (USD)")                 # Title
    ax.set_xlabel("HBM Technology")                       # X-axis label
    ax.set_ylabel("Cost [USD/GB]")                        # Y-axis label

    for p in ax.patches:                                  # Loop through bars
        value = p.get_height()                            # Get bar height
        ax.annotate(                                      # Add label above bar
            f"{value:.2f} $/GB",
            (p.get_x() + p.get_width() / 2, value),
            ha="center",
            va="bottom",
            fontsize=9
        )

    saved_file = save_png(fig, "cost_hbm_usd")            # Save chart
    plt.close(fig)                                        # Close figure
    return saved_file                                     # Return filename


# ============================================================
# MAIN EXECUTION
# ============================================================

def main():
    df = create_main_dataframe()                          # Load main dataset
    df_hbm = create_hbm_cost_dataframe()                  # Load HBM cost dataset

    metadata = {}                                         # Initialize metadata dictionary

    metadata["bandwidth_chart"] = bar_chart(              # Generate bandwidth chart
        df, "Bandwidth_GBs", "Bandwidth per Unit (GB/s)", "GB/s", "Blues", "bandwidth"
    )

    metadata["capacity_chart"] = bar_chart(               # Generate capacity chart
        df, "Capacity_GB", "Capacity per Unit (GB)", "GB", "Greens", "capacity"
    )

    metadata["latency_chart"] = latency_chart(df)         # Generate latency chart

    metadata["radar_chart"] = radar_chart(df)             # Generate radar chart

    metadata["hbm_cost_chart"] = hbm_cost_chart(df_hbm)   # Generate HBM cost chart

    save_metadata(metadata)                               # Save metadata JSON

    print("All charts and metadata have been saved in the 'Memories comparison - charts/' folder.")  # Console message


if __name__ == "__main__":                                # Entry point check
    main()                                                # Run main()