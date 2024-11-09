# import matplotlib.pyplot as plt
# from matplotlib.patches import Ellipse
# import numpy as np

# # CAT10 data
# methods = ['GroundTruth', 'SE3Diffusion (Baseline)', 'VAE', 'GDN(Our)']
# emd_mean = [0.108, 0.168, 0.145, 0.144]  # EMD Mean values
# emd_std = [0.023, 0.054, 0.037, 0.036]  # EMD Std values
# success_rate_mean = [0.857, 0.717, 0.672, 0.726]  # Success Rate Mean values
# success_rate_std = [0.195, 0.268, 0.209, 0.223]  # Success Rate Std values

# # Apply a scaling factor to std deviations to control the ellipse sizes
# std_scaling_factor = 0.1  # Adjust this to control the ellipse size relative to the axis

# # Scale down std values
# scaled_emd_std = [s * std_scaling_factor for s in emd_std]
# scaled_success_rate_std = [s * std_scaling_factor for s in success_rate_std]

# # Create the figure
# plt.figure(figsize=(8, 6))

# # Define colors and markers for each method
# colors = ['blue', 'red', 'green', 'purple']

# # Plot each method with an ellipse representing the std deviation as an approximation of a circular region
# for i, method in enumerate(methods):
#     # Create an ellipse for each method
#     ellipse = Ellipse(
#         (emd_mean[i], success_rate_mean[i]),  # Center at the mean values
#         width=2 * scaled_emd_std[i],  # Scaled EMD standard deviation determines width
#         height=2 * scaled_success_rate_std[i],  # Scaled Success rate standard deviation determines height
#         color=colors[i], alpha=0.4, label=method
#     )
#     plt.gca().add_patch(ellipse)  # Add ellipse to the plot

# # Labels with larger and bold font
# plt.xlabel('EMD', fontsize=14, fontweight='bold')
# plt.ylabel('Success Rate', fontsize=14, fontweight='bold')

# # Dynamically adjust the axis limits based on the range of data and ellipse sizes
# plt.xlim(min(emd_mean) - max(scaled_emd_std) * 2, max(emd_mean) + max(scaled_emd_std) * 2)
# plt.ylim(min(success_rate_mean) - max(scaled_success_rate_std) * 2, 
#          max(success_rate_mean) + max(scaled_success_rate_std) * 2)

# # Set major ticks for better visibility and adjust spacing for clarity
# plt.xticks(np.arange(0.03, 0.23, 0.02))
# plt.yticks(np.arange(0.55, 1.05, 0.05))

# # Add a legend to differentiate between methods, bolden method names in the legend
# legend = plt.legend(loc='upper left', fontsize=12)
# for text in legend.get_texts():
#     text.set_fontweight('bold')

# # Display the plot with ellipses
# plt.show()


import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import numpy as np

# CAT10 data
methods = ['GroundTruth', 'SE3Diffusion (Baseline)', 'VAE', 'GDN(Our)']
emd_mean = [0.108, 0.162, 0.144, 0.145]  # EMD Mean values
emd_std = [0.023, 0.051, 0.039, 0.042]  # EMD Std values
success_rate_mean = [0.857, 0.721, 0.703, 0.755]  # Success Rate Mean values
success_rate_std = [0.195, 0.244, 0.197, 0.225]  # Success Rate Std values

# Apply a scaling factor to std deviations to control the ellipse sizes
std_scaling_factor = 0.1  # Adjust this to control the ellipse size relative to the axis

# Scale down std values
scaled_emd_std = [s * std_scaling_factor for s in emd_std]
scaled_success_rate_std = [s * std_scaling_factor for s in success_rate_std]

# Create the figure
plt.figure(figsize=(8, 6))

# Define colors and markers for each method
colors = ['blue', 'red', 'green', 'purple']

# Plot each method with an ellipse representing the std deviation as an approximation of a circular region
for i, method in enumerate(methods):
    # Create an ellipse for each method
    ellipse = Ellipse(
        (emd_mean[i], success_rate_mean[i]),  # Center at the mean values
        width=2 * scaled_emd_std[i],  # Scaled EMD standard deviation determines width
        height=2 * scaled_success_rate_std[i],  # Scaled Success rate standard deviation determines height
        color=colors[i], alpha=0.4, label=method
    )
    plt.gca().add_patch(ellipse)  # Add ellipse to the plot

# Labels with larger and bold font
plt.xlabel('EMD', fontsize=14, fontweight='bold')
plt.ylabel('Success Rate', fontsize=14, fontweight='bold')

# Dynamically adjust the axis limits based on the range of data and ellipse sizes
plt.xlim(min(emd_mean) - max(scaled_emd_std) * 2, max(emd_mean) + max(scaled_emd_std) * 2)
plt.ylim(min(success_rate_mean) - max(scaled_success_rate_std) * 2, 
         max(success_rate_mean) + max(scaled_success_rate_std) * 2)

# Set major ticks for better visibility and adjust spacing for clarity
plt.xticks(np.arange(0.03, 0.23, 0.02))
plt.yticks(np.arange(0.55, 1.05, 0.05))

# Add a legend to differentiate between methods, bolden method names in the legend
legend = plt.legend(loc='upper left', fontsize=12)
for text in legend.get_texts():
    text.set_fontweight('bold')

# Display the plot with ellipses
plt.show()
