import numpy as np
import matplotlib.pyplot as plt
import glob


hist_files = glob.glob('Output/subhist_*.npy')
combined_hist = np.zeros(64)

for hist_file in hist_files:
    hist = np.load(hist_file)
    combined_hist += hist

if len(hist_files) > 0:
    combined_hist /= len(hist_files)

plt.figure(figsize=(10, 6))
plt.bar(range(64), combined_hist)
plt.title('Combined Hue Histogram')
plt.xlabel('Hue Bin')
plt.ylabel('Normalized Frequency')
plt.tight_layout()
plt.savefig('combined_histogram.png')
print(f"Combined {len(hist_files)} histograms and saved plot as combined_histogram.png")
