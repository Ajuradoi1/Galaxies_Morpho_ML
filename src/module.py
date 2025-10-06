# Data Retrieval

import pandas as pd
import requests
import time
import tarfile
import io
from urllib.parse import urlencode

pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)


def safe_to_numeric(col):
    try:
        return pd.to_numeric(col, errors="raise")
    except Exception:
        return col  # leave unchanged if it can't be fully parsed


# Image download


HIPS_URL = "https://alasky.cds.unistra.fr/hips-image-services/hips2fits"


def Hips2Fits_access(
    ra, dec, petroR90_r, width=64, height=64, hips="CDS/P/SDSS9/color"
):
    # As we could see, one of the compulsory input parameters was the FOV. We need to optimize it with the following equation:
    # FOV = 2*petroR90_r_deg*(1+margin_base)

    # We are using margin_base = 0.25 (25%) as default.
    # We also have to be careful. Hips2Fits works with degreen when it comes to FOV. As we are using petroR90_r in
    # the equation and the csv works with arcsecs for it, we need to change units!

    petroR90_r_deg = float(petroR90_r) / 3600.0  # from arcsecs to deg
    FOV = 2 * petroR90_r_deg * (1 + 0.25)

    # Request for an especific galaxy using everything we have mentioned
    params = {
        "hips": hips,
        "ra": ra,
        "dec": dec,
        "width": width,  # pixels
        "height": height,  # pixels
        "fov": FOV,
        "projection": "TAN",  # Minimal distortions for tangential projection
        "format": "jpg",  # Format of the images we are getting. It can be jpg, png or fits.
    }

    return f"{HIPS_URL}?{urlencode(params)}"


def save_images_to_TAR(TAR_path, contents):
    with (
        tarfile.open(TAR_path, "w") as tar
    ):  # The "w" is from "write". It creates a new TAR (eliminates if it already exists)
        # The "with" command is called context manager. Its main purpouse is to open a resource (in our case a TAR file),
        # run the block and close the file properly even if there is an error.
        for filename, bits, extra in contents:
            # Be careful because TAR files don't accept bytes directly but something that behaves as a "file-like object".
            # That is why we use io.BytesIO. It creates temporal files in RAM memory from these bytes.
            File_obj = io.BytesIO(bits)

            # We move the "cursor" to the beginning. When opening or creating a file, Python has an inner "cursor"
            # that indicates where in the file you are. Every time you read or write, the "cursor" moves forward.
            # That is why we need to use the .seek(0) command, so we guarantee that the "cursor" is in the beginning
            # before doing anything.
            File_obj.seek(0)

            TAR_info = tarfile.TarInfo(name=f"{filename}.jpg")
            TAR_info.size = len(bits)  # Add the size info to TAR_info
            tar.addfile(TAR_info, File_obj)
    print("TAR saved in:", TAR_path)


session = requests.Session()


def download_with_retries(ra, dec, petroR90_r, max_retries=5, delay=2):
    URL = Hips2Fits_access(ra, dec, petroR90_r)  # URL of the desired image to download.
    for attempt in range(1, max_retries + 1):
        try:
            response = session.get(
                URL, timeout=30
            )  # We get into our session (defined with the request.Session())
            if response.status_code == 200:  # This code means the download has succeded
                return response.content  # Return the bytes
            else:
                print(
                    f"[{attempt}/{max_retries}] Error {response.status_code} in {URL}"
                )
        except requests.RequestException as e:  # These are type of error that aren't given in the form of ERROR #NUMBER. These
            # most of the times are associated with connection errors.
            print(f"[{attempt}/{max_retries}] Connection error: {e}")
        if attempt < max_retries:
            time.sleep(delay)  # Wait before the following attempt
    print(f"Permanent error after {max_retries} retries: {URL}")
    return None
