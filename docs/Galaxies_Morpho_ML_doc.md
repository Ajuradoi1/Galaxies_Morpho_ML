
# Notebook Documentation: Galaxy Image Retrieval and Filtering

This document explains the code logic and supporting functions used for galaxy image retrieval,
filtering, and downloading from Galaxy Zoo and SDSS databases. It includes a description of all
functions defined in the module file.

---

## 1. Data Retrieval and Filtering

The notebook retrieves and filters galaxy data. It connects to the TAP service to obtain SDSS and Galaxy Zoo
data, saves it locally, and filters it based on photometric quality and classification criteria (spiral or elliptical).
Filtered data are then stored in compressed CSV files for subsequent use.

---

## 2. Image Downloading Process

The notebook automates downloading of galaxy images using the Hips2Fits service.
It parallelizes downloads using ThreadPoolExecutor and saves batches of 1000 images in TAR archives.
A metadata CSV keeps track of successfully downloaded images for future reference.

---

## 3. Module Functions Overview

The module file supports the main notebook with several key functions and configurations.
These handle safe data conversions, Hips2Fits URL creation, TAR saving, and retry mechanisms for downloads.

### 3.1 `safe_to_numeric(col)`

Attempts to convert a pandas DataFrame column to numeric values.
If conversion fails (e.g., non-numeric data), the original column is returned unchanged.
This ensures the notebook doesn't crash on mixed-type columns.

### 3.2 `Hips2Fits_access(ra, dec, petroR90_r, width=64, height=64, hips='CDS/P/SDSS9/color')`

Generates a Hips2Fits query URL for a specific galaxy.
It calculates the Field of View (FOV) in degrees using the Petrosian radius and a margin of 25%.
The function returns a complete URL for requesting the galaxy image in JPG format.

### 3.3 `save_images_to_TAR(TAR_path, contents)`

Saves a collection of images into a TAR archive.
Each image (stored as bytes) is wrapped in an in-memory file-like object using io.BytesIO.
The TAR file is created or overwritten, ensuring all images are properly added with metadata (size, name).

### 3.4 `download_with_retries(ra, dec, petroR90_r, max_retries=5, delay=2)`

Downloads a galaxy image from Hips2Fits using retry logic.
It repeatedly attempts to fetch the image up to a maximum number of retries in case of connection issues.
If the download succeeds (HTTP 200), the raw bytes are returned.
Otherwise, errors are logged and failed URLs are skipped after all retries.

### 3.5 `session = requests.Session()`

Defines a reusable HTTP session to speed up repeated image downloads.
Using a single session maintains persistent connections and reduces overhead.

---

## 4. Summary of Function Roles

- **safe_to_numeric**: Converts mixed-type columns safely to numeric.  
- **Hips2Fits_access**: Builds a Hips2Fits API request URL for a given galaxy.  
- **save_images_to_TAR**: Efficiently stores downloaded images in compressed archives.  
- **download_with_retries**: Robustly downloads galaxy images with retry handling.  
- **session**: Shared connection object for efficient HTTP communication.

---

## 5. Outputs

Final outputs of the notebook and module include:

- `ZooSpecPhotoDR19_filtered.csv.gz`: Cleaned galaxy catalog.  
- TAR archives in `/Images/`: Compressed image sets.  
- `/Images/Images_downloaded.csv.gz`: Metadata of downloaded images.  

These outputs can be reused for further analysis or machine learning training.
