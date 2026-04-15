import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
import pickle

df = pd.read_csv('dataset.csv', sep=r'\s+')

df = df.fillna(df.mean(numeric_only=True))

df['temp'] = np.random.uniform(20, 35, size=len(df))

df['dosage'] = (
    0.4 * df['Turbidity'] +
    0.3 * abs(df['ph'] - 7) * 10 +
    0.2 * df['Chloramines'] +
    0.1 * (df['temp'] / 10)
)

X = df[['ph', 'Turbidity', 'temp']]
y = df['dosage']

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# 🔥 Accuracy
y_pred = model.predict(X)
accuracy = r2_score(y, y_pred)

print("Model Accuracy:", round(accuracy * 100, 2), "%")

pickle.dump(model, open('model.pkl', 'wb'))

print("✅ Model trained successfully")