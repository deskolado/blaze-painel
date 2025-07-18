import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import LabelEncoder

def extrair_recursos(df):
    df = df.copy()
    df['cor_cod'] = LabelEncoder().fit_transform(df['cor'])
    df['minuto'] = pd.to_datetime(df['horario'], format='%H:%M').dt.minute
    df['hora'] = pd.to_datetime(df['horario'], format='%H:%M').dt.hour
    df['momento'] = df['hora'].apply(lambda h: 'madrugada' if h < 6 else 'manha' if h < 12 else 'tarde' if h < 18 else 'noite')
    df['momento_cod'] = LabelEncoder().fit_transform(df['momento'])
    return df[['minuto', 'hora', 'momento_cod']], df['cor_cod']

def treinar_modelo():
    if not os.path.exists("model/dataset.csv"):
        return
    df = pd.read_csv("model/dataset.csv")
    if len(df) < 10:
        return
    X, y = extrair_recursos(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    modelo = GradientBoostingClassifier()
    modelo.fit(X_train, y_train)
    joblib.dump(modelo, "model/modelo.pkl")
