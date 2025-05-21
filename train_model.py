import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import joblib

# Load data dari Excel
df = pd.read_excel("data_smart_feeder_udang_stepwise.xlsx")

# Ekstraksi fitur
df['Jam'] = pd.to_datetime(df['Waktu']).dt.hour
X = df[['Jam', 'SuhuAir (°C)', 'SisaPakan (g)']]
y = df['PerluDiberiPakan'].map({'Ya': 1, 'Tidak': 0})

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Latih model
model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train)

# Simpan model
joblib.dump(model, "decision_tree_model.pkl")
print("Model telah disimpan.")
