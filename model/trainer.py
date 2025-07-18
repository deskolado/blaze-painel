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
    df['momento'] = df['hora]()
