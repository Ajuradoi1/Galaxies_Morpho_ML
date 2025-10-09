# Galaxy Morphology Classification using Machine Learning

## Overview
This project applies machine learning techniques to classify galaxy morphologies (between spiral and elliptical) based on astronomical data retrieved from online databases. 
It aims to help automate the morphological classification of galaxies — a key task in understanding galaxy evolution and large-scale structure in the universe.

The workflow includes:
- Querying astronomical data from the TAP (Table Access Protocol) service  
- Cleaning and preparing data using pandas  
- Training and evaluating machine learning models  
- Visualizing results and model performance  

## Objectives
- Retrieve and preprocess galaxy data using astroquery and ADQL queries  
- Extract photometric and spectroscopic features relevant to morphology  
- Train and evaluate supervised ML models (e.g., Random Forest, SVM, Neural Networks)  
- Visualize key insights and classification results  

## Project Structure
```
├── docs/
│   └──  Galaxies_Morpho_ML_doc.pdf # Documentation of the module.py functions and the code.ipynb
├── src/
│   └── module.py              # Custom helper functions (data cleaning, modeling, etc.)
├── tests/
│   └── tests.md               # Brief summary of test code
│   └── test_file.py           # Test code using pytest
├── .gitignore                 # Avoid commiting large files, config files
├── ZooSpecPhotoDR19.csv.gz    # (optional) Local cached dataset
├── README.md                  # Project documentation (this file)
├── code.ipynb                 # Main Jupyter Notebook (data retrieval, analysis, ML)
└── pyproject.toml             # Python dependencies
```

## Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/Ajuradoi1/Galaxies_Morpho_ML.git
cd Galaxies_Morpho_ML
pip install pip-tools
pip install .
```

Alternatively, open the notebook directly in JupyterLab or VS Code and install missing libraries as needed.

## Usage
Run the Jupyter notebook step by step:
1. **Data Retrieval** — Downloads data from the TAP service or loads local cache.  
2. **Preprocessing** — Cleans, filters, and merges relevant features.  
3. **Model Training** — Trains ML classifiers on the prepared dataset.  
4. **Evaluation** — Computes metrics like accuracy, precision, recall, and confusion matrix.  
5. **Visualization** — Generates plots for feature importance and classification performance.

To launch:
```bash
jupyter notebook code.ipynb
```

## Dependencies
The project mainly uses:
- pandas
- numpy
- scikit-learn
- astroquery
- matplotlib
- seaborn
- tqdm

(See pyproject.toml for full list.)

## Results
The notebook outputs:
- Data summary statistics and visualizations  
- Trained model accuracy and evaluation metrics  
- Galaxy morphology classification plots and confusion matrices  

These results demonstrate the potential of ML to replicate or assist human morphological classification efforts.

## Acknowledgments
- Galaxy Zoo for labeled morphological data  
- SDSS / TAP Service for public access to galaxy spectra and photometry  
- Astroquery developers for providing convenient astronomical data access tools  

## Authors
- Alex Jurado
- Elisa Camilleri
- Noah Alberca
