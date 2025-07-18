import pandas as pd
import joblib
import os
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

def extrair_recursos(df):
    df['minuto'] = pd.to_datetime(df['horario'], format='%H:%M').dt.minute
    df['hora'] = pd.to_datetime(df['horario'], format='%H:%M').dt.hour
    df['momento'] = df['hora'].apply(lambda h: 'madrugada' if h < 6 else 'manha' if h < 12 else 'tarde' if h < 18 else 'noite')
    df['momento_cod'] = LabelEncoder().fit_transform(df['momento'])
    df['cor_cod'] = LabelEncoder().fit(['V', 'P', 'B']).transform(df['cor'])
    return df[['minuto', 'hora', 'momento_cod']], df['cor_cod']

def treinar_modelo():
    if not os.path.exists("model/dataset.csv"):
        return
    df = pd.read_csv("model/dataset.csv")
    if len(df) < 20:
        return
    X, y = extrair_recursos(df)
    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2)
    modelo = MLPClassifier(hidden_layer_sizes=(50, 20), max_iter=500)
    modelo.fit(X_train, y_train)
    joblib.dump(modelo, "model/modelo.pkl")
