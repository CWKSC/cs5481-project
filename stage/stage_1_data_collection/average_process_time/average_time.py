import re
import pathlib
import matplotlib.pyplot as plt

def extract_floats_from_file(file_path):
    current_folder = pathlib.Path(__file__).parent
    file_path = current_folder / file_path
    floats = []
    pattern = r'in\s+([-+]?[0-9]*\.?[0-9]+)'

    with open(file_path, 'r') as file:
        for line in file:
            matches = re.findall(pattern, line)
            for match in matches:
                floats.append(float(match))

    return floats

# Define file paths
file_paths = {
    'Intern VL2-8B': 'intern_vl_2_process.log',
    'Llama 3.2-11B': 'llama3_2_process.log'
}

# Extract times and calculate averages
averages = {}
for label, file_path in file_paths.items():
    times = extract_floats_from_file(file_path)
    if times:  # Check if the list is not empty
        averages[label] = sum(times) / len(times)
    else:
        averages[label] = 0

# Create a horizontal bar chart
labels = list(averages.keys())
average_times = list(averages.values())

plt.figure(figsize=(10, 6))
bars = plt.barh(labels, average_times, color='skyblue', height=0.4)  # Adjust height for thinner bars
plt.xlabel('Average Time (seconds)')
plt.title('Average Processing Times Per Prompt')
plt.xlim(0, max(average_times) + 1)  # Adjust x-axis limit for better visualization
plt.grid(axis='x')

# Annotate bars with average values
for bar in bars:
    plt.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, 
             f'{bar.get_width():.2f}', 
             va='center', ha='left', color='black')

# Show plot
plt.tight_layout()
plt.savefig('average_processing_times.png')