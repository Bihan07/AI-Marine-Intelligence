import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


# ==========================================
# 1. LOAD DATA
# ==========================================

print("Loading OBIS data...")

df = pd.read_csv("data/raw/obis_fish.csv")

print("Total observations:", len(df))


# ==========================================
# 2. CREATE FEATURES
# ==========================================

df["eventDate"] = pd.to_datetime(df["eventDate"], errors="coerce")

df["month"] = df["eventDate"].dt.month

df["year"] = df["eventDate"].dt.year


features = ["decimalLatitude", "decimalLongitude", "depth", "month"]

target = "scientificName"


# ==========================================
# 3. SELECT COLUMNS
# ==========================================

df = df[features + [target]].copy()


# ==========================================
# 4. CLEAN NUMERIC DATA
# ==========================================

for column in ["decimalLatitude", "decimalLongitude", "depth", "month"]:
    df[column] = pd.to_numeric(df[column], errors="coerce")


# ==========================================
# 5. REMOVE MISSING COORDINATES
# ==========================================

df = df.dropna(subset=["decimalLatitude", "decimalLongitude"])


# ==========================================
# 6. FILL MISSING DEPTH
# ==========================================

df["depth"] = df["depth"].fillna(df["depth"].median())


# ==========================================
# 7. FILL MISSING MONTH
# ==========================================

df["month"] = df["month"].fillna(df["month"].median())


# ==========================================
# 8. REMOVE NON-SPECIES RECORDS
# ==========================================

invalid_names = ["Actinopteri", "Ariidae", "Nemapteryx", "Auxis"]

df = df[~df[target].isin(invalid_names)]


# ==========================================
# 9. SELECT TOP SPECIES
# ==========================================

species_counts = df[target].value_counts()

TOP_N = 8

top_species = species_counts.head(TOP_N).index

df = df[df[target].isin(top_species)]


print("\n==============================")
print("SPECIES DISTRIBUTION")
print("==============================")

print(df[target].value_counts())


print("\nRows:", len(df))

print("Species:", df[target].nunique())


# ==========================================
# 10. PREPARE DATA
# ==========================================

X = df[features]

y = df[target]


# ==========================================
# 11. TRAIN TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)


# ==========================================
# 12. RANDOM FOREST
# ==========================================

print("\nTraining model...")

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=10,
    min_samples_leaf=2,
    class_weight="balanced",
    random_state=42,
)

model.fit(X_train, y_train)


# ==========================================
# 13. PREDICTION
# ==========================================

predictions = model.predict(X_test)


# ==========================================
# 14. ACCURACY
# ==========================================

accuracy = accuracy_score(y_test, predictions)


print("\n==============================")
print("MODEL RESULTS")
print("==============================")

print(f"Accuracy: {accuracy * 100:.2f}%")


print("\nClassification Report:")

print(classification_report(y_test, predictions, zero_division=0))


# ==========================================
# 15. FEATURE IMPORTANCE
# ==========================================

importance = pd.DataFrame(
    {"Feature": features, "Importance": model.feature_importances_}
)

importance = importance.sort_values("Importance", ascending=False)


print("\n==============================")
print("FEATURE IMPORTANCE")
print("==============================")

print(importance.to_string(index=False))


# ==========================================
# 16. SAMPLE PREDICTION
# ==========================================

sample = pd.DataFrame(
    {"decimalLatitude": [10], "decimalLongitude": [75], "depth": [50], "month": [6]}
)


prediction = model.predict(sample)[0]


probabilities = model.predict_proba(sample)[0]


results = pd.DataFrame({"Species": model.classes_, "Probability": probabilities})


results = results.sort_values("Probability", ascending=False)


print("\n==============================")
print("PREDICTION")
print("==============================")

print("Location: 10°N, 75°E")

print("Depth: 50 m")

print("Month: June")

print("\nMost likely species:", prediction)


print("\nTop 5 predictions:")

print(results.head(5).to_string(index=False))
import joblib

joblib.dump(model, "src/ml/species_model.pkl")

print("\nModel saved successfully!")
