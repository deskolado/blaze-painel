import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import LabelEncoder

def extrair_recursos(df):
    df = df.copy()
    df['cor_cod'] = LabelEncoder().fit_transform(df['cor'])

    # Hora em minutos
    df['minuto'] = pd.to_datetime(df['horario'], format='%H:%M').dt.minute
df['hora'] = pd.to_datetime(df['horario'], format='%H:%M').dt.hour
df['momento'] = df['hora'].apply(lambda h: 'madrugada' if h < 6 else 'manha' if h < 12 else 'tarde' if h < 18 else 'noite')
df['momento_cod'] = LabelEncoder().fit_transform(df['momento'])
