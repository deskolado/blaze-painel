import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
import os

def treinar_modelo():
    if not os.path.exists("model/dataset.csv"):
        return

    df = pd.read_csv("model/dataset.csv")
    if len(df) < 30:
        return

    df = df.dropna()
    le_cor = LabelEncoder()
    df['cor'] = le_cor.fit_transform(df['cor'])

    X = df[['numero']]  # você pode incluir horário e padrões futuros aqui
    y = df['cor']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    modelo = RandomForestClassifier()
    modelo.fit(X_train, y_train)
    joblib.dump((modelo, le_cor), 'model/modelo.pkl')
