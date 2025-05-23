import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
from datetime import datetime

# Database path
db_path = "local_database_1.db"

# Connect to SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Query to get CMS_RUN data
cms_run_query = """
    SELECT number, start, end FROM CMS_RUN
"""
cms_run_df = pd.read_sql_query(cms_run_query, conn)

# Query to get WORKFLOW_FILE data
workflow_file_query = """
    SELECT run, workflow, uploaded FROM WORKFLOW_FILE
"""
workflow_file_df = pd.read_sql_query(workflow_file_query, conn)

# Close database connection
conn.close()

# Convert date columns to datetime format
cms_run_df["end"] = pd.to_datetime(cms_run_df["end"], errors='coerce')
workflow_file_df["uploaded"] = pd.to_datetime(workflow_file_df["uploaded"], errors='coerce')

# Merge the dataframes on run number
merged_df = workflow_file_df.merge(cms_run_df, left_on="run", right_on="number", how="inner")

# Calculate time difference
diff_df = merged_df.dropna().copy()
diff_df["time_difference"] = (diff_df["uploaded"] - diff_df["end"]).dt.total_seconds() / 3600  # Convert to hours

# Create output directory
output_dir = "workflow_plots"
os.makedirs(output_dir, exist_ok=True)

# Define bins (0 to 60 hours in 30-minute intervals)
bins = np.arange(0, 60.5, 0.5)

# Generate plots per workflow
for workflow, data in diff_df.groupby("workflow"):
    # Compute statistics
    mean_diff = data["time_difference"].mean()
    rms_diff = np.sqrt(((data["time_difference"] - mean_diff) ** 2).mean())

    plt.figure(figsize=(10, 5))
    plt.hist(data["time_difference"], bins=bins, edgecolor='black', alpha=0.7)
    plt.xlabel("Time Difference (hours)")
    plt.ylabel("Frequency")
    plt.title(f"Time Difference Between Run End and Upload for {workflow}")
    plt.grid(True)

    # Print statistics on the plot
    plt.axvline(mean_diff, color='r', linestyle='dashed', linewidth=1, label=f'Mean: {mean_diff:.2f}h')
    plt.axvline(mean_diff + rms_diff, color='g', linestyle='dashed', linewidth=1, label=f'RMS: {rms_diff:.2f}h')
    plt.axvline(mean_diff - rms_diff, color='g', linestyle='dashed', linewidth=1)
    plt.legend()
    
    plt.savefig(os.path.join(output_dir, f"{workflow}_time_diff.png"))
    plt.close()

print(f"Plots saved in {output_dir}/")
