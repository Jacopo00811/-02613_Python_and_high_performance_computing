import numpy as np
from PIL import Image
import sys 
import glob

def huehist(image):
    bins = np.linspace(0, 255, 64 + 1)
    hsv_image = np.asarray(Image.fromarray(image).convert('HSV'))
    hue_values = hsv_image[:, :, 0].reshape(-1)
    hue_hist = np.histogram(hue_values, bins)[0]
    return hue_hist

if __name__ == "__main__":
    DATA = '/dtu/projects/02613_2024/data/celeba/images'
    SAVE_PATH = 'Week_11/Exercise_6_7_8_9_10/Output'
    i = int(sys.argv[1])
    i -= 1 
    i = f"{i:03d}000"
    images = glob.glob(DATA + '/' + i + '/*.jpg')
    summed_hist = np.zeros(64)
    for image in images:
        img = Image.open(image)
        img = np.array(img)
        hist = huehist(img)
        summed_hist += hist
    summed_hist /= len(images)
    np.save(f'Output/subhist_{i}.npy', summed_hist)
