import numpy as np
import pandas as pd
import astroquery as aq
from astroquery.skyview import SkyView
from astropy.visualization import ZScaleInterval, ImageNormalize, LinearStretch
from astropy.io import fits
import matplotlib.pyplot as plt

import os

# Load the CSV file into a DataFrame

df = pd.read_csv("ZooSpecPhotoDR19_filtered.csv")

print(df.head())

# Create a directory to save images if it doesn't exist
if not os.path.exists("images"):
    os.makedirs("images")

#survey used: DSS, in the slides they ask for SDSS or hips2fits

def download_image(ra, dec, filename):
    try:
        images = SkyView.get_images(position=f"{ra} {dec}", survey=['DSS'], pixels=64)
        if images:
            hdu = images[0][0]
            hdu.writeto(filename, overwrite=True)
            print(f"Downloaded image for RA: {ra}, Dec: {dec}")
        else:
            print(f"No image found for RA: {ra}, Dec: {dec}")
    except Exception as e:
        print(f"Error downloading image for RA: {ra}, Dec: {dec}: {e}")

# Loop through the DataFrame and download images
for index, row in df.iterrows():
    ra = row['ra']
    dec = row['dec']
    filename = f"images/object_{index}.fits"
    download_image(ra, dec, filename)
    if index > 3:  # Limit to first 4 images for demonstration
        break

print("Image download process completed.")

#Plot images

for i in range(3):
    data = fits.getdata(f"images/object_{i}.fits")
    zscale = ZScaleInterval()
    plt.figure()
    plt.imshow(zscale(data), cmap="gray",origin='lower')
    plt.title(f"Object {i}")
    plt.colorbar()
    plt.show()

