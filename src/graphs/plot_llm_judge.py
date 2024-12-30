import matplotlib.pyplot as plt
import numpy as np

# Data for the bar graph
groups = ['whisper-base.en', 'whisper-tiny.en', 'moonshine-base']
values_group1 = [9, 8, 6]  # First bar of each group
values_group2 = [2, 2, 4]  # Second bar of each group
values_group3 = [1, 2, 2]  # Third bar of each group

# Set up x-axis positions for the groups and width of the bars
x = np.arange(len(groups))  # Positions for the groups
bar_width = 0.25  # Width of each bar

# Create the plot
plt.bar(x - bar_width, values_group1, width=bar_width, label='Human', color='slateblue', edgecolor='black')  # First bar
plt.bar(x, values_group2, width=bar_width, label='Model', color='khaki', edgecolor='black')  # Second bar
plt.bar(x + bar_width, values_group3, width=bar_width, label='Equal', color='lightgreen', edgecolor='black')  # Third bar

# Add labels and title
plt.xlabel('Trials')
plt.ylabel('#Transcripts')
plt.title('gpt-4o-mini prefers Reference Transcripts over STT Transcripts')
plt.xticks(x, groups)  # Set x-axis ticks to group labels
plt.legend()  # Add a legend

# Show the plot
plt.tight_layout()
plt.show()
