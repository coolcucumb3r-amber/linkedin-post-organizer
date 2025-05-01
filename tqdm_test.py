from tqdm import tqdm
import time

for i in tqdm(range(0, 10), desc="Progress Bar"):
    time.sleep(.2)