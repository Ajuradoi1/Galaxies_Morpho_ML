from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import pandas as pd
import matplotlib.pyplot as plt



#MORPHOLOGY CLASSIFIER

#Load the dataset
df = pd.read_parquet("/Users/elisacamilleri/Desktop/Dataset_combinado.parquet")

#Define classifier as 1 for spiral, 0 for elliptical
df["morphology"] = df["spiral"].apply(lambda x: "Spiral" if x == 1 else "Elliptical")

#Choose whichever has higher probability
df["morphology"] = df.apply(
    lambda row: "Spiral" if row["spiral"] > row["elliptical"] else "Elliptical", axis=1)



#EXTRACTING PCA COLUMNS AND MORPHOLOGY LABELS

# Keep only PCA features as predictors
X = df[[col for col in df.columns if col.startswith("PC")]]

# Target label
Y = df["morphology"]



#ENCODE AND SPLIT THE DATA

#convert string labels into numeric binary form (0-elliptical, 1-spiral)
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(Y)

#splitting data into 80% training, 20% test
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded)



#TRAIN THE RANDOM FOREST CLASSIFIER

rf = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced")

rf.fit(X_train, y_train)



#EVALUATE PERFORMANCE

y_pred = rf.predict(X_test)

#prediction accuracy
print("Accuracy:", accuracy_score(y_test, y_pred))

#percentage of correct predictions
print(classification_report(y_test, y_pred, target_names=encoder.classes_))



