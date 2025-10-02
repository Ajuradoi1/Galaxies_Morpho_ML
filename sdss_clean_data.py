import os
import pandas as pd
import matplotlib.pyplot as plt
from astropy.visualization import ZScaleInterval, ImageNormalize, LinearStretch
from astropy import units as u
from astroquery.skyview import SkyView
from astropy.io import fits
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

#path to clean data file
csv_path = "/Users/elisacamilleri/Documents/Masters/Statistics and Data Analysis/Computational Work/SDSS_filtered_data.csv"
df = pd.read_csv(csv_path)

#create output directory if it doesn't exist
out_dir = "images"
os.makedirs(out_dir, exist_ok=True)

#parameters
zoom = 0.03  # degrees across width/height
pixels = 500  # image pixels along each dimension
N_images = 10  # how many images to download (set small for testing)

def download_image(index, ra, dec, out_dir):
    filename = os.path.join(out_dir, f"object_{index}.fits")
    try:
        # Query SkyView for DSS survey with specified size in degrees
        images = SkyView.get_images(position=f"{ra} {dec}",
                                    survey=['DSS'],
                                    width=zoom * u.deg,
                                    height=zoom * u.deg,
                                    pixels=pixels)
        if images:
            hdu = images[0][0]
            hdu.writeto(filename, overwrite=True)
            print(f"[{index}] Downloaded image for RA: {ra}, Dec: {dec}")
            return filename
        else:
            print(f"[{index}] No image found for RA: {ra}, Dec: {dec}")
            return None
    except Exception as e:
        print(f"[{index}] Error downloading image for RA: {ra}, Dec: {dec}: {e}")
        return None

#parallel downloading
def download_all_images(df, n_download, out_dir):
    tasks = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        for i, row in df.iterrows():
            if i >= n_download:
                break
            ra, dec = row['ra'], row['dec']
            tasks.append(executor.submit(download_image, i, ra, dec, out_dir))
        # Collect results
        results = []
        for future in as_completed(tasks):
            result = future.result()
            results.append(result)
    return results

downloaded_files = download_all_images(df, N_images, out_dir)

#visualize downloaded images
zscale = ZScaleInterval()
for i in range(min(N_images, len(df))):
    filepath = os.path.join(out_dir, f"object_{i}.fits")
    if os.path.exists(filepath):
        data = fits.getdata(filepath)
        plt.figure()
        plt.imshow(zscale(data), cmap="gray", origin='lower')
        plt.title(f"Object {i}")
        plt.colorbar()
        plt.show()
    else:
        print(f"File not found for visualization: {filepath}")

#display special cases for spiral and elliptical galaxy
def plot_special_object(df, colname, out_dir, title, filename):
    idx = df[colname].idxmax()
    ra, dec = df.loc[idx, ['ra', 'dec']]
    filepath = os.path.join(out_dir, filename)
    download_image(idx, ra, dec, out_dir)
    if os.path.exists(filepath):
        data = fits.getdata(filepath)
        vmin, vmax = zscale.get_limits(data)
        norm = ImageNormalize(vmin=vmin, vmax=vmax, stretch=LinearStretch())
        plt.figure()
        plt.imshow(data, cmap="gray", origin='lower', norm=norm)
        plt.title(title)
        plt.colorbar()
        plt.show()
    else:
        print(f"File not found: {filepath}")

plot_special_object(df, 'p_cs_debiased', out_dir, "Spiral Galaxy", "spiral_galaxy.fits")
plot_special_object(df, 'p_el_debiased', out_dir, "Elliptical Galaxy", "elliptical_galaxy.fits")
