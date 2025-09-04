import subprocess
import matplotlib.pyplot as plt
import re

# Input file path and array size
file_path = '/dtu/projects/02613_2025/data/mandelbrot/mandelbrot.raw'
array_size = 4000
step_sizes = [1, 2, 4, 8, 16]

# Function to extract runtime and memory usage from time command output
def parse_time_output(output):
    # Extract user time in seconds
    user_time_match = re.search(r'(\d+\.\d+)user', output)
    user_time = float(user_time_match.group(1)) if user_time_match else 0
    
    # Extract sys time in seconds
    sys_time_match = re.search(r'(\d+\.\d+)system', output)
    sys_time = float(sys_time_match.group(1)) if sys_time_match else 0
    
    # Extract memory in KB and convert to MB
    memory_match = re.search(r'(\d+)maxresident', output)
    memory_kb = int(memory_match.group(1)) if memory_match else 0
    memory_mb = memory_kb / 1024  # Convert KB to MB
    
    return user_time + sys_time, memory_mb

# Arrays to store results
runtimes = []
memory_usages = []

# Run the downsampling program for each step size
for step in step_sizes:
    print(f"Running with step size {step}...")
    # Create a unique output filename for each step size
    output_filename = f"downsampled_{step}.png"
    
    # Run the command with time and capture its output
    command = f"/usr/bin/time -v python code.py {file_path} {array_size} {step}"
    process = subprocess.run(command, shell=True, stderr=subprocess.PIPE, universal_newlines=True)
    
    # Parse the time output
    runtime, memory = parse_time_output(process.stderr)
    
    # Store results
    runtimes.append(runtime)
    memory_usages.append(memory)
    
    print(f"  Runtime: {runtime:.2f} seconds")
    print(f"  Memory: {memory:.2f} MB")

# Create a figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Plot runtime vs step size
ax1.plot(step_sizes, runtimes, 'o-', color='blue')
ax1.set_xlabel('Step Size (n)')
ax1.set_ylabel('Runtime (seconds)')
ax1.set_title('Runtime vs Step Size')
ax1.grid(True)
ax1.set_xticks(step_sizes)

# Plot memory usage vs step size
ax2.plot(step_sizes, memory_usages, 'o-', color='green')
ax2.set_xlabel('Step Size (n)')
ax2.set_ylabel('Peak Memory Usage (MB)')
ax2.set_title('Memory Usage vs Step Size')
ax2.grid(True)
ax2.set_xticks(step_sizes)

plt.tight_layout()
plt.savefig('performance_analysis.png')
plt.show()

print("Analysis complete. Results saved to 'performance_analysis.png'")