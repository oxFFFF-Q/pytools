import matplotlib.pyplot as plt
import numpy as np
import os


def log_time(label, time_elapsed):
    """
    Append timing data to a file.

    Parameters:
    - file_path: str, path to the log file.
    - label: str, description of the timing data.
    - time_elapsed: float, the elapsed time to log.
    """

    file_path = "/home/qiao/Projects/pytools/data/time_take/se3dif_grasp_timing_log.txt"
    with open(file_path, "a") as f:  # Open in append mode
        f.write(f"{label}: {time_elapsed}\n")  # Write timing data
    print("%" * 50, "saved timing data to", file_path)

import matplotlib.pyplot as plt
import numpy as np
import os

def plot_time_statistics(input_path, selected_labels=None, layout="horizontal"):
    """
    Reads timing data from a single text file or multiple text files in a directory,
    and plots average and cumulative timing statistics for selected time labels.

    Parameters:
    - input_path: str, the absolute path to a txt timing file or a directory containing multiple txt timing files.
    - selected_labels: list of str or None, specifies which timing labels to use; if None, all labels are used.
    - layout: str, "horizontal" for side-by-side subplots, "vertical" for top-bottom subplots.
    """
    # Get list of txt file paths
    if os.path.isdir(input_path):
        file_paths = [os.path.join(input_path, f) for f in os.listdir(input_path) if f.endswith(".txt")]
    elif os.path.isfile(input_path) and input_path.endswith(".txt"):
        file_paths = [input_path]
    else:
        raise ValueError("Invalid path. Please provide a path to a .txt file or a directory containing .txt files.")

    # Check selected_labels parameter
    if selected_labels is not None:
        if not isinstance(selected_labels, list) or not all(isinstance(label, str) for label in selected_labels):
            raise ValueError("selected_labels should be a list of strings or None.")

    # Initialize dictionary to store times for each category
    time_data = []
    model_names = []  # Store model names for legend

    # Read each file and populate time_data list
    min_length = float('inf')  # Track the minimum number of entries across files
    for file_path in file_paths:
        model_name = os.path.splitext(os.path.basename(file_path))[0]  # Use file name as model name
        model_names.append(model_name)

        with open(file_path, 'r') as f:
            lines = f.readlines()
            file_times = []  # Store timing data for each selected label in the current file
            for line in lines:
                label, time_str = line.strip().split(": ")
                time_value = float(time_str)

                # Only store labels that are in selected_labels or store all if selected_labels is None
                if selected_labels is None or label in selected_labels:
                    file_times.append(time_value)

            # Append each file's timing data and track minimum length
            time_data.append(np.array(file_times))
            min_length = min(min_length, len(file_times))

    # Trim each time series to the minimum length
    time_data = [times[:min_length] for times in time_data]

    # Set up subplots layout based on the layout parameter
    if layout == "horizontal":
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    elif layout == "vertical":
        fig, axes = plt.subplots(2, 1, figsize=(8, 10))
    else:
        raise ValueError("Invalid layout. Choose 'horizontal' or 'vertical'.")

    # Left (or top) plot: Average timing per iteration
    for i, times in enumerate(time_data):
        avg_times = np.cumsum(times) / np.arange(1, min_length + 1)
        axes[0].plot(avg_times, label=model_names[i], linewidth=2)
    axes[0].set_xlabel("Iteration", fontsize=12, fontweight='bold')
    axes[0].set_ylabel("Average Time (s)", fontsize=12, fontweight='bold')
    axes[0].set_title("Grasp Generation Time (Average)", fontsize=14, fontweight='bold')

    # Right (or bottom) plot: Cumulative timing
    for i, times in enumerate(time_data):
        cumulative_times = np.cumsum(times)
        axes[1].plot(cumulative_times, label=model_names[i], linewidth=2)
    axes[1].set_xlabel("Iteration", fontsize=12, fontweight='bold')
    axes[1].set_ylabel("Cumulative Time (s)", fontsize=12, fontweight='bold')
    axes[1].set_title("Grasp Generation Time (Cumulative)", fontsize=14, fontweight='bold')
    
    # Unified legend with bold and larger font size, position adjusted for layout
    if layout == "horizontal":
        axes[1].legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, frameon=False,
                       prop={'size': 11, 'weight': 'bold'})
    else:
        axes[1].legend(loc='upper center', bbox_to_anchor=(0.5, -0.25), ncol=2, frameon=False,
                       prop={'size': 11, 'weight': 'bold'})

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()




if __name__ == "__main__":
    input_path = "/home/qiao/Projects/pytools/data/time_take"
    selected_labels = ["t_grasp_generator_total"]
    lay_out = "vertical"
    plot_time_statistics(input_path, selected_labels, layout=lay_out)
